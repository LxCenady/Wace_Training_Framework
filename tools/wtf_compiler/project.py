"""Durable project/task state, result validation and explicit human review."""
import copy
import hashlib
import json
from pathlib import Path
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from . import schema
from .jobs import STAGES, REQUIRED, contract
from .sources import Assets


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


class Projects:
    def __init__(self, root):
        self.root=Path(root).resolve();self.root.mkdir(parents=True,exist_ok=True)
        self.assets=Assets(self.root);self.lock=threading.RLock()
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY,state TEXT NOT NULL)')

    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.root/'projects.db',timeout=15)
        try:
            with db:yield db
        finally:db.close()

    @contextmanager
    def transaction(self, pid):
        schema.require(isinstance(pid,str) and uuid.UUID(pid).hex==pid,'Invalid project ID')
        with self.lock,self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT state FROM projects WHERE id=?',(pid,)).fetchone()
            schema.require(row is not None,'Unknown project')
            state=json.loads(row[0]);yield state
            db.execute('UPDATE projects SET state=? WHERE id=?',(json.dumps(state,ensure_ascii=False),pid))

    def list(self):
        with self.connect() as db:
            return [self.summary(json.loads(row[0])) for row in db.execute('SELECT state FROM projects ORDER BY rowid DESC')]

    def get(self,pid):
        with self.transaction(pid) as state:
            return copy.deepcopy(state)

    def summary(self,state):
        return {key:state[key] for key in ('id','course','state','stage','revision','issues','attempts')} | dict(
            external_agent_only=True,subscription_supported=False,sources=state['sources'],artifacts=list(state['outputs']))

    def create(self,course,documents,capabilities=None):
        schema.fields(course,('id','name'),('id','name'));schema.identifier(course['id'])
        schema.require(isinstance(course['name'],dict) and course['name'],'Missing course name')
        schema.require(all(key in ('zh','en') and isinstance(value,str) and value.strip() for key,value in course['name'].items()),'Invalid course names')
        schema.require(isinstance(documents,list) and 0<len(documents)<=100,'Choose 1 to 100 source PDFs')
        sources=[]
        for n,doc in enumerate(documents):
            schema.fields(doc,('path','roles','url'),('path','roles'))
            schema.require(isinstance(doc['roles'],list) and doc['roles'] and set(doc['roles'])<=schema.ROLES,'Invalid document roles')
            if doc.get('url'):schema.url(doc['url'])
            asset=self.assets.register(doc['path']);sources.append(dict(id=f'd{n+1}',roles=doc['roles'],**asset,**({'url':doc['url']} if doc.get('url') else {})))
        schema.require({'exam','key','syllabus'}<={r for d in sources for r in d['roles']},'Exam, key and syllabus required')
        caps=capabilities or ['read','export','mark','generate']
        schema.require(isinstance(caps,list) and 'read' in caps and set(caps)<=schema.CAPABILITIES,'Invalid capabilities')
        pid=uuid.uuid4().hex
        state=dict(id=pid,pack_id=uuid.uuid4().hex,version='1.0.0',course=course,sources=sources,capabilities=caps,
                   stage='pair',state='waiting_agent',revision=1,attempts=0,issues=[],outputs={},audit=[],task_id=uuid.uuid4().hex)
        with self.connect() as db:
            db.execute('INSERT INTO projects VALUES (?,?)',(pid,json.dumps(state,ensure_ascii=False)))
        return self.summary(state)

    def task(self,pid):
        state=self.get(pid)
        if state['state']!='waiting_agent':return None
        return dict(project_id=pid,task_id=state['task_id'],revision=state['revision'],**contract(state['stage']),
                    input=dict(course=state['course'],sources=state['sources'],capabilities=state['capabilities'],
                               artifacts=copy.deepcopy(state['outputs']),recipe=state.get('recipe'),
                               parsed_documents=list(state.get('chunks',{}))),
                    schema=self.example_schema())

    @staticmethod
    def example_schema():
        return dict(region={'document':'d1','page':0,'bbox':[0,0,1,1],'rotate':0},
                    pair_example={'sections':[{'id':'CF','name':'Calculator-free','weight':.35,'minutes':50},
                                               {'id':'CA','name':'Calculator-assumed','weight':.65,'minutes':100}],
                                  'pairs':[{'exam':'exam-doc-id','key':'key-doc-id'}],
                                  'coverage':{'exam-doc-id':{'questions':1,'marks':1,'source':[{'document':'exam-doc-id','page':0,'bbox':[0,0,1,1]}]}},
                                  'confidence':1,'issues':[],'explanation':'Verified pairing evidence'},
                    question_fields=['id','label','section','marks','source','key_source','shared_source','parts'],
                    part_fields=['id','label','marks','rubric'],
                    rubric_kinds=['award','sum','best','select'],
                    award_fields=['id','kind','max_marks','credit_step','source','knowledge','patterns','levels','ecf'],
                    credit_step='Default 1 (whole marks). Declare e.g. 0.5 explicitly when the standard permits fractional credits; levels are discrete allowed scores.',
                    level={'score':2,'source':[]},ecf={'policy':'explicit|reviewed|unspecified','from':['award-id'],'source':[]},
                    group_fields=['id','kind','children','take','cap','requires','conditions','conditional_caps'],
                    group_rules={'sum':'sum children','best':'best complete route','select':'sum best take children; take is an integer'},
                    condition_cap={'condition':'id','cap':2},positive_band=[1,3],
                    taxonomy_entry={'id':'K1','name':'Own wording','definition':'Own definition','topic':'T1','source':[{'document':'d3','page':0,'bbox':[0,0,1,1]}]},
                    parse_example={'questions':[{'id':'Q1','label':'Question A','section':'section-id-from-pair','marks':1,
                        'source':[{'document':'exam-doc-id','page':0,'bbox':[0,0,1,1]}],
                        'key_source':[{'document':'key-doc-id','page':0,'bbox':[0,0,1,1]}],
                        'parts':[{'id':'Q1.a','label':'a','marks':1,'rubric':{'id':'Q1.a.aw1','kind':'award','max_marks':1,
                            'source':[{'document':'key-doc-id','page':0,'bbox':[0,0,1,1]}]}}]}],
                        'content':{'Q1':{'stem':'Private transcription','solution':'Private answer','criteria':{'Q1.a.aw1':'Private criterion description'}}},'confidence':1,'issues':[]},
                    note='No question/answer/criterion text in the portable recipe. Submit those only in private content. All rubric/part IDs are globally unique. ECF may reference an award in another part; requires stays inside its own scoring tree.')

    def provisional(self,state,output,partial=False):
        recipe=self.recipe(state,parse=output)
        knowledge=set();patterns=set()
        for q in recipe['questions']:
            for p in q['parts']:
                import rubric
                nodes,_=rubric.validate(p['rubric'],p['marks'])
                for node in nodes.values():
                    knowledge.update(node.get('knowledge',[]));patterns.update(node.get('patterns',[]))
        recipe['taxonomy']=dict(topics=[dict(id='pending',name='Pending')],
            knowledge=[dict(id=v,name=v,topic='pending') for v in knowledge or {'pending'}],
            patterns=[dict(id=v,name=v,topic='pending') for v in patterns or {'pending'}])
        recipe['capabilities']=['read','export']
        schema.validate(recipe,complete=not partial)

    def recipe(self,state,parse=None,taxonomy=None,notes=None):
        if state.get('recipe'):return copy.deepcopy(state['recipe'])
        parse=parse or state['outputs'].get('parse',{})
        tax=taxonomy or state['outputs'].get('taxonomy',{})
        notes=notes or state['outputs'].get('notes',{})
        questions=copy.deepcopy(parse.get('questions',[]))
        assignments=tax.get('assignments',{})
        def apply(node):
            if node['id'] in assignments:node.update(assignments[node['id']])
            for child in node.get('children',[]):apply(child)
        for q in questions:
            for p in q['parts']:apply(p['rubric'])
        return dict(wtf_pack=2,pack_id=state['pack_id'],version=state['version'],
                    course={**state['course'],'sections':state['outputs'].get('pair',{}).get('sections',[])},
                    capabilities=state['capabilities'],sources=state['sources'],questions=questions,
                    coverage=state['outputs'].get('pair',{}).get('coverage',{}),
                    taxonomy=tax.get('taxonomy',dict(topics=[],knowledge=[],patterns=[])),
                    notes=notes.get('notes',{}),skill=notes.get('skill',''))

    def validate_output(self,state,output,partial=False):
        stage=state['stage']
        required=REQUIRED[stage]
        schema.fields(output,(*required,'confidence','issues','explanation'),(*required,'confidence','issues'))
        schema.require(isinstance(output.get('explanation',''),str) and len(output.get('explanation',''))<=20000,'Invalid explanation')
        schema.require(type(output['confidence']) in (int,float) and 0<=output['confidence']<=1
                       and isinstance(output['issues'],list) and all(isinstance(v,str) and len(v)<=1000 for v in output['issues']), 'Invalid confidence/issues')
        sources={d['id']:d for d in state['sources']}
        if stage=='pair':
            schema.require(isinstance(output['sections'],list) and output['sections'] and isinstance(output['pairs'],list) and output['pairs'],'Missing pairs/sections')
            for pair in output['pairs']:
                schema.fields(pair,('exam','key'),('exam','key'))
                schema.require(pair['exam'] in sources and 'exam' in sources[pair['exam']]['roles']
                               and pair['key'] in sources and 'key' in sources[pair['key']]['roles'],'Wrong document pairing')
            schema.require({p['exam'] for p in output['pairs']}=={d['id'] for d in sources.values() if 'exam' in d['roles']}, 'Unpaired exam')
            for section in output['sections']:
                schema.fields(section,('id','name','weight','minutes'),('id','name'));schema.identifier(section['id'])
                schema.require(isinstance(section['name'],str) and section['name'],'Invalid section name')
            schema.require(isinstance(output['coverage'],dict) and set(output['coverage'])=={d['id'] for d in sources.values() if 'exam' in d['roles']},'Every exam needs printed coverage')
            for ident,row in output['coverage'].items():
                schema.fields(row,('questions','marks','source'),('questions','marks','source'))
                schema.require(type(row['questions'])is int and row['questions']>0 and schema.number(row['marks']) and row['marks']>0,'Invalid printed counts')
                schema.regions(row['source'],sources,True)
                schema.require(all(r['document']==ident for r in row['source']),'Wrong cover evidence')
        elif stage=='parse':
            self.provisional(state,output,partial);self.validate_content(self.recipe(state,parse=output),output['content'])
        elif stage=='taxonomy':
            schema.require(isinstance(output['assignments'],dict),'Invalid associations')
            for assignment in output['assignments'].values():
                schema.fields(assignment,('knowledge','patterns'),('knowledge','patterns'))
                schema.require(all(isinstance(assignment[k],list) and assignment[k] for k in ('knowledge','patterns')), 'Awards need knowledge and pattern associations')
            recipe=self.recipe(state,taxonomy=output);recipe['capabilities']=['read','export'];schema.validate(recipe)
            import rubric
            award_ids={i for q in recipe['questions'] for p in q['parts'] for i,n in rubric.validate(p['rubric'])[0].items() if n['kind']=='award'}
            schema.require(set(output['assignments'])==award_ids,'Every award needs one association record')
        elif stage=='notes':
            schema.regions(output['evidence'],sources,True);schema.validate(self.recipe(state,notes=output))
        elif stage=='review':
            schema.require(output['verdict'] in ('pass','revise'),'Invalid review verdict')
            schema.validate(self.recipe(state))
        elif stage=='hydrate':
            self.validate_content(state['recipe'],output['content'])

    def validate_content(self,recipe,content):
        import rubric
        schema.require(isinstance(content,dict) and set(content)=={q['id'] for q in recipe['questions']},'Incomplete private content')
        for q in recipe['questions']:
            row=content[q['id']];schema.fields(row,('stem','solution','criteria'),('stem','solution','criteria'))
            schema.require(all(isinstance(row[k],str) and row[k].strip() for k in ('stem','solution')) and isinstance(row['criteria'],dict),'Unreadable question or answer')
            ids={i for p in q['parts'] for i,n in rubric.validate(p['rubric'])[0].items() if n['kind']=='award'}
            schema.require(set(row['criteria'])==ids and all(isinstance(v,str) and v.strip() for v in row['criteria'].values()),'Incomplete criterion descriptions')

    def submit(self,pid,task_id,revision,output):
        schema.require(len(json.dumps(output).encode())<=16*1024*1024,'Result too large')
        with self.transaction(pid) as state:
            schema.require(state['state']=='waiting_agent','No active agent task; local review or retry is required')
            schema.require(task_id==state['task_id'] and revision==state['revision'],'Stale task ID or revision; fetch the current task')
            try:self.validate_output(state,output)
            except (ValueError,KeyError,TypeError) as exc:
                state['attempts']+=1;state['revision']+=1;state['task_id']=uuid.uuid4().hex
                state['issues']=[str(exc)[:1000]]
                if state['attempts']>=2:state['state']='needs_review'
                return self.summary(state)
            state['outputs'][state['stage']]=copy.deepcopy(output)
            state['audit'].append(dict(stage=state['stage'],task_id=task_id,result_hash=digest(output),action='agent_submit'))
            state['issues']=output['issues'][:]
            if output['confidence']<.9:state['issues'].append('Low confidence')
            if state['stage']=='review' and output['verdict']!='pass':state['issues'].append('Independent review requests revision')
            if state['issues']:
                state['state']='needs_review';state['revision']+=1
            else:self.advance(state)
            return self.summary(state)

    def parse_chunk(self,pid,task_id,revision,exam_id,output):
        """One original exam per chunk; all chunks must pass the normal final parse gate."""
        schema.require(len(json.dumps(output).encode())<=16*1024*1024,'Result too large')
        complete=None
        with self.transaction(pid) as state:
            schema.require(state['state']=='waiting_agent' and state['stage']=='parse' and task_id==state['task_id'] and revision==state['revision'],'Stale or inactive parse task')
            exams={d['id'] for d in state['sources'] if 'exam' in d['roles']}
            schema.require(exam_id in exams,'Unknown exam document')
            try:
                self.validate_output(state,output,partial=True)
                schema.require(all(q['source'] and all(r['document']==exam_id for r in q['source']) for q in output['questions']), 'Chunk must contain only its selected exam')
                key=next(p['key'] for p in state['outputs']['pair']['pairs'] if p['exam']==exam_id)
                schema.require(all(all(r['document']==key for r in q['key_source']) for q in output['questions']),'Chunk must use the paired marking key')
                expected=state['outputs']['pair']['coverage'][exam_id]
                schema.require(len(output['questions'])==expected['questions'] and abs(sum(q['marks'] for q in output['questions'])-expected['marks'])<1e-9,
                               f"Exam {exam_id} chunk does not match printed coverage: {expected['questions']} questions / {expected['marks']} marks")
            except (ValueError,KeyError,TypeError) as exc:
                state['attempts']+=1;state['revision']+=1;state['task_id']=uuid.uuid4().hex
                state['issues']=[str(exc)[:1000]]
                if state['attempts']>=2:state['state']='needs_review'
                return self.summary(state)
            state.setdefault('chunks',{})[exam_id]=copy.deepcopy(output)
            schema.require(len(json.dumps(state['chunks']).encode())<=16*1024*1024,'Combined parse chunks too large')
            state['audit'].append(dict(action='agent_parse_chunk',exam=exam_id,result_hash=digest(output)))
            state.update(revision=state['revision']+1,task_id=uuid.uuid4().hex,attempts=0,issues=[])
            if set(state['chunks'])==exams:
                values=[state['chunks'][doc] for doc in sorted(exams)]
                complete=dict(questions=[q for v in values for q in v['questions']],
                    content={q:row for v in values for q,row in v['content'].items()},confidence=min(v['confidence'] for v in values),
                    issues=[issue for v in values for issue in v['issues']])
                next_id,next_revision=state['task_id'],state['revision']
            result=self.summary(state)
        return self.submit(pid,next_id,next_revision,complete) if complete else result

    def advance(self,state):
        if state['stage'] in ('review','hydrate'):
            schema.validate(self.recipe(state));state['state']='ready';state['stage']='complete'
        else:
            state['stage']=STAGES[STAGES.index(state['stage'])+1];state['state']='waiting_agent'
        state['revision']+=1;state['task_id']=uuid.uuid4().hex;state['attempts']=0;state['issues']=[]

    def resolve(self,pid,decision,note):
        schema.require(decision in ('accept','retry') and isinstance(note,str) and note.strip(),'Review decision and explanation required')
        with self.transaction(pid) as state:
            schema.require(state['state']=='needs_review','Project is not awaiting human review')
            if decision=='accept':
                schema.require(state['stage'] in state['outputs'],'Invalid results cannot be approved')
                self.validate_output(state,state['outputs'][state['stage']]);self.advance(state)
            else:
                state['outputs'].pop(state['stage'],None);state.update(state='waiting_agent',issues=[],attempts=0,revision=state['revision']+1,task_id=uuid.uuid4().hex)
                if state['stage']=='parse':state.pop('chunks',None)
            state['audit'].append(dict(action='human_'+decision,note=note[:2000]))
            return self.summary(state)

    def resource(self,pid,ref,image=False):
        state=self.get(pid);sources={d['id']:d for d in state['sources']};schema.region(ref,sources)
        return self.assets.render(sources[ref['document']],ref) if image else self.assets.extract(sources[ref['document']],ref)

    def finalized(self,pid):
        state=self.get(pid);schema.require(state['state']=='ready','Compiler project is not ready')
        recipe=self.recipe(state);schema.validate(recipe)
        schema.require(all(self.assets.bound(d) for d in recipe['sources']), 'Bind every original PDF before building')
        content=state['outputs'].get('hydrate',state['outputs'].get('parse',{})).get('content',{})
        self.validate_content(recipe,content)
        return recipe,content

    def import_task(self,recipe):
        schema.validate(recipe);pid=uuid.uuid4().hex
        state=dict(id=pid,pack_id=recipe['pack_id'],version=recipe['version'],course={k:recipe['course'][k] for k in ('id','name')},
            recipe=recipe,sources=recipe['sources'],capabilities=recipe['capabilities'],stage='hydrate',state='waiting_agent',
            revision=1,attempts=0,issues=[],outputs={},audit=[],task_id=uuid.uuid4().hex)
        with self.connect() as db:db.execute('INSERT INTO projects VALUES (?,?)',(pid,json.dumps(state,ensure_ascii=False)))
        return self.summary(state)
