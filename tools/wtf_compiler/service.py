"""Application-neutral local orchestration; deliberately has no model provider."""
import base64
from pathlib import Path
from .project import Projects
from .library import Library
from . import archive, documents, scoring, schema


class Compiler:
    def __init__(self,root):
        self.projects=Projects(root);self.library=Library(self.projects)

    def status(self,pid):
        state=self.projects.get(pid)
        return self.projects.summary(state) | {'bindings':{d['id']:self.projects.assets.bound(d) for d in state['sources']}}

    def bind(self,pid,path):
        state=self.projects.get(pid);asset=self.projects.assets.register(path)
        schema.require(any(d['sha256']==asset['sha256'] and d['pages']==asset['pages'] for d in state['sources']),
                       'PDF does not match any project source hash')
        return self.status(pid)

    def download(self,pid,document):
        from .download import bind
        state=self.projects.get(pid);doc=next((d for d in state['sources'] if d['id']==document),None)
        schema.require(doc is not None,'Unknown document')
        bind(self.projects.assets,doc)
        return self.status(pid)

    def export(self,pid,path=None):
        recipe,_=self.projects.finalized(pid)
        if path is None:
            folder=self.projects.root/'exports';folder.mkdir(exist_ok=True)
            path=folder/(recipe['pack_id']+'-'+recipe['version']+'.wtfpack')
        return archive.export(recipe,path)

    def preview(self,pid,ref):
        return 'data:image/png;base64,'+base64.b64encode(self.projects.resource(pid,ref,True)).decode()

    def question(self,pack,qid,version=None):
        snapshot=self.library.snapshot(pack,qid,version)
        snapshot['images']=['data:image/png;base64,'+base64.b64encode(b).decode() for b in documents.images(self.projects.assets,snapshot)]
        return snapshot

    def grade(self,pack,qid,proposals,evidence_count,version=None):
        snapshot=self.library.snapshot(pack,qid,version)
        schema.require(isinstance(proposals,dict) and set(proposals)=={p['id'] for p in snapshot['question']['parts']}, 'Every part needs a proposal')
        result={p['id']:scoring.score(p['rubric'],proposals[p['id']],evidence_count) for p in snapshot['question']['parts']}
        schema.require(not any(r['needs_review'] for r in result.values()),'Resolve uncertain rubric/ECF judgments before saving')
        return {'attempt_id':self.library.record(snapshot,result),'parts':result}

    def practice(self,pack,qid,credits,conditions=None):
        import rubric
        snapshot=self.library.snapshot(pack,qid);results={};all_ids=set()
        for part in snapshot['question']['parts']:
            awards={i:n for i,n in rubric.validate(part['rubric'])[0].items() if n['kind']=='award'}
            all_ids.update(awards)
            proposal=dict(schema_version=2,conditions=(conditions or {}).get(part['id'],{}),awards=[dict(
                award_id=ident,got=credits.get(ident),reason='Self assessment',evidence=[]) for ident in awards])
            results[part['id']]=scoring.score(part['rubric'],proposal,0,manual=True)
        schema.require(set(credits)==all_ids and not any(r['needs_review'] for r in results.values()),'Complete every criterion and condition')
        saved=dict(origin='self',parts=results)
        return dict(attempt_id=self.library.record(snapshot,saved),earned=sum(r['score']['earned'] for r in results.values()),possible=snapshot['question']['marks'])

    def export_questions(self,pack,qids,path,answers=False):
        schema.require(len(qids)<=200,'Too many questions')
        snapshots=[self.library.snapshot(pack,q) for q in qids]
        return documents.export(self.projects.assets,snapshots,path,answers)

    def restart(self,pid,stage,note):
        import uuid
        from .jobs import STAGES
        schema.require(stage in STAGES and isinstance(note,str) and note.strip(),'Stage and revision note required')
        with self.projects.transaction(pid) as state:
            schema.require(not state.get('recipe'),'Imported recipes are immutable; create a new version')
            index=STAGES.index(stage)
            schema.require(all(s in state['outputs'] for s in STAGES[:index]),'Previous stages are incomplete')
            if state['state']=='ready':
                major,minor,patch=map(int,state['version'].split('.'))
                state['version']=f'{major}.{minor}.{patch+1}'
            for old in STAGES[index:]:state['outputs'].pop(old,None)
            if index<=STAGES.index('parse'):state.pop('chunks',None)
            state.update(stage=stage,state='waiting_agent',revision=state['revision']+1,task_id=uuid.uuid4().hex,issues=[],attempts=0)
            state['audit'].append({'action':'local_restart','stage':stage,'note':note[:2000]})
            return self.projects.summary(state)
