"""Synthetic Compiler pipeline and security tests; never load owner config/data."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import uuid
import zipfile
import asyncio

ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'app')]
import pymupdf
from wtf_compiler.service import Compiler
from wtf_compiler import archive, schema, scoring
from kernel import Kernel
from plugins import compiler as plugin


class CompilerTest(unittest.TestCase):
    def setUp(self):
        runtime=ROOT/'evidence/runtime';runtime.mkdir(parents=True,exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(prefix='compiler-',dir=runtime);self.root=Path(self.temp.name);self.c=Compiler(self.root/'one')
        self.addCleanup(self.temp.cleanup)  # last: connections a test registers later close first
        self.docs=[]
        for role in ('exam','key','syllabus'):
            path=self.root/(role+'.pdf')
            with pymupdf.open() as pdf:
                page=pdf.new_page();page.insert_text((50,50),role+' synthetic private material')
                if role=='exam':page.set_rotation(90)
                pdf.save(path)
            self.docs.append(dict(path=str(path),roles=[role]))
        self.pid=self.c.projects.create({'id':'essay-course','name':{'en':'Synthetic essay','zh':'测试'}},self.docs)['id']
        self.ref=lambda n:dict(document='d'+str(n),page=0,bbox=[0,0,1,1])
        self.tree=dict(id='root',kind='sum',children=[
            dict(id='a1',kind='award',max_marks=1,source=[self.ref(2)]),
            dict(id='a2',kind='award',max_marks=3,source=[self.ref(2)],levels=[dict(score=n,source=[self.ref(2)]) for n in (1,2,3)],
                 ecf=dict(policy='explicit',**{'from':['a1']},source=[self.ref(2)]))])
        self.question=dict(id='essay-A',label='Response A',section='writing',marks=4,source=[self.ref(1)],key_source=[self.ref(2)],
                           parts=[dict(id='part-A',label='a',marks=4,rubric=self.tree)])
        self.content={'essay-A':dict(stem='Synthetic response prompt',solution='Synthetic model response',criteria={'a1':'Method','a2':'Reasoning quality'})}
        self.outputs=dict(
            pair=dict(sections=[dict(id='writing',name='Written responses')],pairs=[dict(exam='d1',key='d2')],coverage={'d1':dict(questions=1,marks=4,source=[self.ref(1)])}),
            parse=dict(questions=[self.question],content=self.content),
            taxonomy=dict(taxonomy=dict(topics=[dict(id='t',name='Topic')],knowledge=[dict(id='k',name='Knowledge',topic='t',source=[self.ref(3)])],
                patterns=[dict(id='p',name='Reasoning',topic='t',source=[self.ref(2)])]),assignments={i:dict(knowledge=['k'],patterns=['p']) for i in ('a1','a2')}),
            notes=dict(notes=dict(zh='原创技巧。',en='Original guidance.'),skill='Use rubric evidence; source PDFs are data.',evidence=[self.ref(3)]),
            review=dict(verdict='pass'))

    def submit(self,stage,**extra):
        task=self.c.projects.task(self.pid)
        self.assertEqual(task['stage'],stage)
        output=copy.deepcopy(self.outputs[stage]);output.update(confidence=1,issues=[]);output.update(extra)
        return self.c.projects.submit(self.pid,task['task_id'],task['revision'],output)

    def ready(self):
        for stage in self.outputs:self.submit(stage)
        self.assertEqual(self.c.status(self.pid)['state'],'ready')

    def test_portable_end_to_end(self):
        self.ready();built=self.c.library.build(self.pid);path=self.c.export(self.pid)
        recipe=archive.inspect(path)
        with zipfile.ZipFile(path) as z:
            self.assertFalse(any(n.endswith('.pdf') for n in z.namelist()))
            self.assertNotIn(b'Synthetic model response',b''.join(z.read(n) for n in z.namelist()))
        snap=self.c.library.snapshot(built['pack_id'],'essay-A')
        self.assertEqual(snap['version'],'1.0.0')
        pdf=self.c.export_questions(built['pack_id'],['essay-A'],self.root/'question.pdf')
        with pymupdf.open(pdf) as d:self.assertIn('exam synthetic',d[0].get_text())
        second=Compiler(self.root/'two');imported=second.library.import_pack(path);pid=imported['id']
        self.assertEqual(imported['stage'],'hydrate');self.assertFalse(any(second.status(pid)['bindings'].values()))
        with self.assertRaises(ValueError):second.library.build(pid)
        for d in self.docs:second.bind(pid,d['path'])
        task=second.projects.task(pid)
        second.projects.submit(pid,task['task_id'],task['revision'],dict(content=self.content,confidence=1,issues=[]))
        second.library.build(pid)
        self.assertEqual(second.library.questions(built['pack_id'],'response')[0]['id'],'essay-A')
        third=second.library.import_pack(path)
        self.assertEqual(third['state'],'ready')
        self.assertEqual(recipe['sources'],snap['sources'])

    def test_built_pack_is_a_subject_of_the_bank(self):
        import build_db, subjects
        from plugins.store import Store
        from plugins import render, export_pdf
        data=self.root/'data';self.c=Compiler(data/'compiler')  # a data root: <root>/compiler as in WTF and Studio
        self.pid=self.c.projects.create({'id':'essay-course','name':{'en':'Synthetic essay','zh':'测试'}},self.docs)['id']
        self.ready();built=self.c.library.build(self.pid)
        self.assertEqual(built['bank'],dict(subject='ESSAYCOURSE',questions=1,parts=1))
        self.assertEqual(subjects.profiles(data)['ESSAYCOURSE']['engine'],'compiler')
        db=build_db.sqlite3.connect(data/'bank.db');db.executescript(build_db.SCHEMA);db.close()  # an empty bank of papers
        store=Store(str(data));self.addCleanup(store.gen.close);self.addCleanup(store.db.close)
        self.assertEqual(store.compiler,['ESSAYCOURSE']);self.assertIn('ESSAYCOURSE',store.subjects())
        (code,_,_,count),=store.topics('ESSAYCOURSE');self.assertEqual(count,1)
        (pattern,_,title,_),=store.patterns(code);self.assertEqual(title,'Reasoning')
        qid=store.questions_for(pattern)[0][0];q=store.question(qid)
        self.assertEqual([p[0] for p in q['points']],['a','a']);self.assertEqual(q['parts'],[('a',4,[pattern])])
        with pymupdf.open(data/q['exam']) as pdf:self.assertTrue(render.crop(pdf[0],q['exam_regions'][0],1).startswith(b'\x89PNG'))
        out=data/'past.pdf';export_pdf.past_papers([q],str(data),str(out),'T',lambda code:code)
        self.assertTrue(out.exists())
        import blueprint, random, os  # P2: the same paper assembly, mistakes and mastery as any subject
        from unittest import mock
        with mock.patch.dict(os.environ,{'WACE_MATHS_ROOT':str(data)}):  # the app runs with its data root set
            bp=blueprint.blueprint(store.db,'ESSAYCOURSE','writing')
        self.assertEqual(sum(m for _,m,_,_ in blueprint.plan(bp,4,random.Random(0))),4)
        store.save_mistake('past',qid,'a',4,1,[pattern],['Method'])
        self.assertEqual(store.mastery()[pattern],dict(attempted=4,lost=1,parts=1))
        self.assertEqual(subjects.exam_title('ESSAYCOURSE',data),'Synthetic essay')

    def test_stale_and_review_restart(self):
        stale=self.c.projects.task(self.pid)
        self.submit('pair',confidence=.7)
        self.assertEqual(self.c.status(self.pid)['state'],'needs_review')
        with self.assertRaises(ValueError):self.c.projects.submit(self.pid,stale['task_id'],stale['revision'],self.outputs['pair'])
        self.c.projects.resolve(self.pid,'accept','Checked the source pair')
        self.submit('parse');self.submit('taxonomy')
        self.c.restart(self.pid,'parse','Correct geometry')
        self.assertEqual(self.c.projects.get(self.pid)['outputs'].keys(),{'pair'})

    def test_task_contract_lists_actual_required_fields(self):
        from wtf_compiler.jobs import REQUIRED,contract
        for stage,required in REQUIRED.items():
            self.assertEqual(set(contract(stage)['output_required']),set(required)|{'confidence','issues'})
        with self.assertRaisesRegex(ValueError,'Missing required fields: sections'):
            schema.fields({'pairs':[]},('pairs','sections'),('pairs','sections'))

    def test_broken_results_never_approve(self):
        self.submit('pair');self.submit('parse',questions=[]);self.submit('parse',questions=[])
        self.assertEqual(self.c.status(self.pid)['state'],'needs_review')
        with self.assertRaises(ValueError):self.c.projects.resolve(self.pid,'accept','Looks fine')
        self.c.projects.resolve(self.pid,'retry','Repair source regions');self.submit('parse')

    def test_parse_chunks_are_scoped_and_complete(self):
        self.submit('pair');task=self.c.projects.task(self.pid)
        output={**copy.deepcopy(self.outputs['parse']), 'confidence':1,'issues':[]}
        with self.assertRaises(ValueError):self.c.projects.parse_chunk(self.pid,task['task_id'],task['revision'],'d2',output)
        result=self.c.projects.parse_chunk(self.pid,task['task_id'],task['revision'],'d1',output)
        self.assertEqual(result['stage'],'taxonomy')

    def test_parse_chunk_invalid_results_reach_review_gate(self):
        self.submit('pair')
        for attempt in (1,2):
            task=self.c.projects.task(self.pid)
            output=dict(questions=[],content={},confidence=1,issues=[])
            result=self.c.projects.parse_chunk(self.pid,task['task_id'],task['revision'],'d1',output)
            self.assertEqual(result['attempts'],attempt)
            self.assertEqual(result['state'],'needs_review' if attempt==2 else 'waiting_agent')
            self.assertNotEqual(result['revision'],task['revision'])
        self.assertFalse(self.c.projects.get(self.pid).get('chunks'))

    def test_retry_keeps_parse_chunks_that_passed(self):
        self.submit('pair')
        with self.c.projects.transaction(self.pid) as state:  # an exam already parsed and accepted
            state['chunks']={'d1':{'questions':[],'content':{},'confidence':1,'issues':[]}}
        for attempt in (1,2):
            task=self.c.projects.task(self.pid)
            self.c.projects.parse_chunk(self.pid,task['task_id'],task['revision'],'d1',dict(questions=[],content={},confidence=1,issues=[]))
        self.assertEqual(self.c.status(self.pid)['state'],'needs_review')
        self.c.projects.resolve(self.pid,'retry','Fix the rubric maximum of one question')
        self.assertEqual(self.c.status(self.pid)['state'],'waiting_agent')
        self.assertIn('d1',self.c.projects.get(self.pid)['chunks'])
        state=self.c.status(self.pid);self.assertEqual(state['state'],'waiting_agent')
        with self.c.projects.transaction(self.pid) as s:s.update(state='needs_review')
        self.c.projects.resolve(self.pid,'retry','Repair d1',['d1'])
        self.assertNotIn('d1',self.c.projects.get(self.pid)['chunks'])
        with self.assertRaises(ValueError):self.c.projects.resolve(self.pid,'accept','x',['d1'])

    def test_levels_ecf_and_fractional_credit(self):
        proposal=dict(schema_version=2,awards=[dict(award_id='a1',got=0,reason='Student used wrong value',evidence=[0]),
            dict(award_id='a2',got=2,reason='Valid reasoning with earlier wrong value',evidence=[0],ecf=dict(**{'from':['a1']},used_value='7',reason='Carried their 7 forward',evidence=[0]))])
        result=scoring.score(self.tree,proposal,1)
        self.assertEqual(result['score']['earned'],2)
        proposal['awards'][1]['got']=1.5
        with self.assertRaises(ValueError):scoring.score(self.tree,proposal,1)
        tree=copy.deepcopy(self.tree);tree['children'][1].pop('levels');tree['children'][1].pop('ecf')
        tree['children'][1]['credit_step']=.5
        proposal['awards'][1].pop('ecf');self.assertEqual(scoring.score(tree,proposal,1)['score']['earned'],1.5)
        tree=copy.deepcopy(self.tree);tree['children'][1]['ecf']['policy']='unspecified';proposal['awards'][1]['got']=2
        proposal['awards'][1]['ecf']=dict(**{'from':['a1']},used_value='7',reason='Ambiguous key',evidence=[0])
        self.assertTrue(scoring.score(tree,proposal,1)['needs_review'])
        proposal['awards'][1].pop('ecf')
        self.assertTrue(scoring.score(tree,proposal,1)['needs_review'])

    def test_printed_coverage_rejects_missing_marks_and_questions(self):
        self.ready();recipe,_=self.c.projects.finalized(self.pid)
        for field,value in [('marks',7),('questions',2)]:
            changed=copy.deepcopy(recipe);changed['coverage']['d1'][field]=value
            with self.assertRaises(ValueError):schema.validate(changed)
        changed=copy.deepcopy(recipe);changed.pop('coverage')
        with self.assertRaises(ValueError):schema.validate(changed)

    def test_fractional_credit_requires_declared_step(self):
        tree=copy.deepcopy(self.tree);tree['children'][1].pop('levels');tree['children'][1].pop('ecf')
        proposal=dict(schema_version=2,awards=[dict(award_id='a1',got=0,reason='No method',evidence=[0]),
            dict(award_id='a2',got=1.5,reason='Partial response',evidence=[0])])
        with self.assertRaises(ValueError):scoring.score(tree,proposal,1)
        tree['children'][1]['credit_step']=.5
        self.assertEqual(scoring.score(tree,proposal,1)['score']['earned'],1.5)

    def test_manual_only_criterion_cannot_be_confirmed_by_model(self):
        tree=copy.deepcopy(self.tree);tree['children'][1].pop('ecf');tree['children'][1]['manual_only']=True
        for got in (0,2):
            proposal=dict(schema_version=2,awards=[dict(award_id='a1',got=0,reason='No method',evidence=[0]),
                dict(award_id='a2',got=got,reason='Source conflict',evidence=[0])])
            result=scoring.score(tree,proposal,1)
            self.assertIn('a2',result['needs_review']);self.assertIsNone(result['score']['earned'])
        for row in proposal['awards']:row['evidence']=[]
        result=scoring.score(tree,proposal,0,manual=True)
        self.assertFalse(result['needs_review']);self.assertEqual(result['score']['earned'],2)

    def test_tampering_sources_and_archive(self):
        self.ready();path=self.c.export(self.pid)
        with zipfile.ZipFile(path,'a') as z:z.writestr('../evil.py','print(1)')
        with self.assertRaises(ValueError):archive.inspect(path)
        state=self.c.projects.get(self.pid);asset=self.c.projects.assets.path(state['sources'][0]['sha256']);asset.write_bytes(b'changed')
        with self.assertRaises(ValueError):self.c.projects.finalized(self.pid)
        self.c.bind(self.pid,self.docs[0]['path'])
        self.assertTrue(self.c.status(self.pid)['bindings']['d1'])

    def test_plugins_are_lazy_and_no_model_services(self):
        root=self.root/'plugin';root.mkdir();k=Kernel(root);plugin.setup(k)
        self.assertFalse((root/'compiler').exists())
        self.assertEqual(k.get('compiler.calls')['compiler_list'](),[])
        self.assertFalse((root/'generated.db').exists())
        self.assertEqual(set(k.get('compiler.calls')),plugin.CALL_NAMES)

    def test_duplicate_global_nodes_and_geometry(self):
        self.ready();recipe,_=self.c.projects.finalized(self.pid)
        other=copy.deepcopy(recipe['questions'][0]);other['id']='second';other['parts'][0]['id']='second-part';recipe['questions'].append(other)
        with self.assertRaises(ValueError):schema.validate(recipe)
        data=self.c.projects.resource(self.pid,self.ref(1),True);self.assertTrue(data.startswith(b'\x89PNG'))
        self.assertIn('exam synthetic',self.c.projects.resource(self.pid,self.ref(1)))

    def test_rotated_rectangle_text_image_and_vector_export_agree(self):
        from wtf_compiler import documents
        path=self.root/'rotation.pdf';box=pymupdf.Rect(50,50,150,90)
        with pymupdf.open() as d:
            p=d.new_page(width=400,height=300)
            p.draw_rect(box,color=None,fill=(1,0,0))
            p.draw_rect(pymupdf.Rect(60,58,75,72),color=None,fill=(0,0,1))
            p.draw_rect(pymupdf.Rect(125,70,140,84),color=None,fill=(0,1,0))
            p.insert_text((77,65),'Target',fontsize=8);p.set_rotation(90)
            displayed=box*p.rotation_matrix;w,h=p.rect.width,p.rect.height
            ref=dict(document='rotation',page=0,bbox=[displayed.x0/w,displayed.y0/h,displayed.x1/w,displayed.y1/h])
            d.save(path)
        doc=dict(id='rotation',roles=['exam'],**self.c.projects.assets.register(path))
        self.assertIn('Target',self.c.projects.assets.extract(doc,ref))
        original=self.c.projects.assets.render(doc,ref)
        snapshot=dict(sources=[doc],question=dict(source=[ref],key_source=[ref]))
        exported=self.root/'rotation-export.pdf';documents.export(self.c.projects.assets,[snapshot],exported)
        with pymupdf.open(exported) as pdf:output=pdf[0].get_pixmap(matrix=pymupdf.Matrix(2,2)).tobytes('png')
        def positions(raw):
            pix=pymupdf.Pixmap(raw);data=pix.samples;positions={}
            for name,index in [('blue',2),('green',1)]:
                coords=[(x/pix.width,y/pix.height) for y in range(pix.height) for x in range(pix.width)
                        if data[(y*pix.width+x)*pix.n+index]>240 and all(data[(y*pix.width+x)*pix.n+i]<15 for i in range(3) if i!=index)]
                self.assertTrue(coords)
                positions[name]=tuple(sum(v[n] for v in coords)/len(coords) for n in (0,1))
            return positions
        a,b=positions(original),positions(output)
        for name in a:
            for x,y in zip(a[name],b[name]):self.assertLess(abs(x-y),.03)

    def test_mcp_loopback_auth_scope_and_disabled(self):
        import urllib.request
        import urllib.error
        import time
        from wtf_compiler.mcp import Session
        from mcp import ClientSession
        from mcp.client.streamable_http import streamable_http_client
        import httpx
        entry=Session(self.c);state=entry.enable(self.pid)
        try:
            for _ in range(100):
                try:
                    urllib.request.urlopen(state['url'],timeout=.2)
                except urllib.error.HTTPError as e:
                    self.assertEqual(e.code,403);break
                except urllib.error.URLError:time.sleep(.03)
            else:self.fail('Loopback MCP did not start')
            for headers in ({'Authorization':'Bearer wrong'}, {'Authorization':'Bearer '+state['token'],'Origin':'https://evil.example'}):
                with self.assertRaises(urllib.error.HTTPError) as error:
                    urllib.request.urlopen(urllib.request.Request(state['url'],headers=headers))
                self.assertEqual(error.exception.code,403)
            async def client():
                async with httpx.AsyncClient(headers={'Authorization':'Bearer '+state['token']}) as http, streamable_http_client(state['url'],http_client=http,terminate_on_close=False) as (read,write,_):
                    async with ClientSession(read,write) as session:
                        await session.initialize();tools=await session.list_tools();names={v.name for v in tools.tools}
                        self.assertNotIn('compiler.approve',names);self.assertNotIn('compiler.review',names)
                        result=await session.call_tool('compiler.get_task',{})
                        self.assertFalse(result.isError);self.assertIn(self.pid,result.content[0].text)
                        image=await session.call_tool('compiler.read_image',dict(document='d1',page=0,bbox=[0,0,1,1]))
                        self.assertFalse(image.isError);self.assertEqual(image.content[0].type,'image')
                        escaped=await session.call_tool('compiler.read_text',dict(document='unknown',page=0,bbox=[0,0,1,1]))
                        self.assertTrue(escaped.isError)
                        revoked=entry.disable()
                        self.assertFalse(revoked['enabled'])
            asyncio.run(client())
        finally:entry.disable()

    def test_mcp_stdio(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        async def client():
            params=StdioServerParameters(command=sys.executable,args=[str(ROOT/'tools/compiler.py'),'--root',str(self.c.projects.root),'mcp','--project',self.pid])
            async with stdio_client(params) as (read,write):
                async with ClientSession(read,write) as session:
                    await session.initialize()
                    result=await session.call_tool('compiler.status',{})
                    self.assertFalse(result.isError);self.assertIn(self.pid,result.content[0].text)
        asyncio.run(client())


if __name__=='__main__':unittest.main()
