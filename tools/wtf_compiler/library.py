"""Independent immutable versions, private content cache and rubric snapshots."""
import copy
import json
import sqlite3
import uuid
from contextlib import contextmanager
from . import archive, schema
from .project import digest


class Library:
    def __init__(self, projects):
        self.projects = projects; self.path = projects.root/'library.db'
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS versions(pack TEXT,version TEXT,hash TEXT,recipe TEXT,content TEXT,PRIMARY KEY(pack,version))')
            db.execute('CREATE TABLE IF NOT EXISTS active(pack TEXT PRIMARY KEY,version TEXT)')
            db.execute('CREATE TABLE IF NOT EXISTS attempts(id TEXT PRIMARY KEY,snapshot TEXT,result TEXT)')
            db.execute('CREATE TABLE IF NOT EXISTS content_cache(hash TEXT PRIMARY KEY,content TEXT)')

    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.path,timeout=15)
        try:
            with db:yield db
        finally:db.close()

    def build(self,pid):
        recipe,content=self.projects.finalized(pid); fingerprint=digest(recipe)
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            old=db.execute('SELECT hash FROM versions WHERE pack=? AND version=?',(recipe['pack_id'],recipe['version'])).fetchone()
            schema.require(old is None or old[0]==fingerprint,'Version already exists with different recipe; increase version')
            db.execute('INSERT OR IGNORE INTO versions VALUES (?,?,?,?,?)',(recipe['pack_id'],recipe['version'],fingerprint,
                        json.dumps(recipe,ensure_ascii=False),json.dumps(content,ensure_ascii=False)))
            db.execute('INSERT OR REPLACE INTO active VALUES (?,?)',(recipe['pack_id'],recipe['version']))
            db.execute('INSERT OR REPLACE INTO content_cache VALUES (?,?)',(digest([recipe['sources'],recipe['questions']]),json.dumps(content,ensure_ascii=False)))
        return dict(pack_id=recipe['pack_id'],version=recipe['version'],hash=fingerprint)

    def list(self):
        with self.connect() as db:
            return [dict(pack_id=p,version=v,hash=h,course=json.loads(r)['course']) for p,v,h,r in db.execute(
                'SELECT v.pack,v.version,v.hash,v.recipe FROM versions v JOIN active a ON a.pack=v.pack AND a.version=v.version')]

    def load(self,pack,version=None):
        with self.connect() as db:
            row=db.execute('SELECT recipe,content,hash FROM versions WHERE pack=? AND version=COALESCE(?,(SELECT version FROM active WHERE pack=?))',(pack,version,pack)).fetchone()
        schema.require(row is not None,'Unknown installed version')
        recipe=json.loads(row[0]); schema.validate(recipe)
        schema.require(all(self.projects.assets.bound(d) for d in recipe['sources']),'Original PDFs missing or changed; rebind before use')
        return recipe,json.loads(row[1]),row[2]

    def activate(self,pack,version):
        self.load(pack,version)
        with self.connect() as db:db.execute('INSERT OR REPLACE INTO active VALUES (?,?)',(pack,version))
        return dict(pack_id=pack,version=version)

    def import_pack(self,path):
        recipe=archive.inspect(path)
        with self.connect() as db:
            row=db.execute('SELECT content FROM content_cache WHERE hash=?',(digest([recipe['sources'],recipe['questions']]),)).fetchone()
        result=self.projects.import_task(recipe)
        if row and all(self.projects.assets.bound(d) for d in recipe['sources']):
            task=self.projects.task(result['id'])
            result=self.projects.submit(result['id'],task['task_id'],task['revision'],dict(content=json.loads(row[0]),confidence=1,issues=[]))
        return result

    def profile(self,pack,version=None):
        recipe,_,fingerprint=self.load(pack,version)
        return {key:recipe.get(key) for key in ('course','taxonomy','notes','skill','capabilities','version')} | {'pack_id':pack,'recipe_hash':fingerprint}

    def versions(self,pack):
        with self.connect() as db:
            return [dict(version=v,hash=h) for v,h in db.execute('SELECT version,hash FROM versions WHERE pack=? ORDER BY rowid DESC',(pack,))]

    def questions(self,pack,text='',version=None,codes=None):
        recipe,content,_=self.load(pack,version)
        import rubric
        codes=set(codes or [])
        known={v['id'] for g in ('knowledge','patterns') for v in recipe['taxonomy'][g]}
        schema.require(codes<=known,'Unknown catalogue filter')
        text=text.casefold()
        return [dict(id=q['id'],label=q['label'],marks=q['marks'],section=q['section']) for q in recipe['questions']
                if text in (q['label']+' '+content[q['id']]['stem']).casefold() and (not codes or codes & {
                    code for p in q['parts'] for n in rubric.validate(p['rubric'])[0].values() for g in ('knowledge','patterns') for code in n.get(g,[])})]

    def snapshot(self,pack,qid,version=None):
        recipe,content,fingerprint=self.load(pack,version)
        q=next((q for q in recipe['questions'] if q['id']==qid),None);schema.require(q is not None,'Unknown question')
        return copy.deepcopy(dict(kind='compiler',pack_id=pack,version=recipe['version'],recipe_hash=fingerprint,
            question=q,content=content[qid],sources=recipe['sources'],taxonomy=recipe['taxonomy']))

    def record(self,snapshot,result):
        schema.require(snapshot.get('kind')=='compiler','Invalid snapshot')
        ident=uuid.uuid4().hex
        with self.connect() as db:db.execute('INSERT INTO attempts VALUES (?,?,?)',(ident,json.dumps(snapshot),json.dumps(result)))
        return ident
