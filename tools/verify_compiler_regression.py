"""Rebuild official data to a scratch DB and compare rows without writing owner files."""
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))


def protected():
    paths=[Path(os.environ['APPDATA'])/name/'config.json' for name in ('wace-maths','wtf-studio')]
    paths += [root/name for root in (ROOT,ROOT.parent/'WTF_Studio') for name in ('wace.db','generated.db','external.db')]
    return {str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.exists()}


def main():
    folder=ROOT/'evidence/runtime/compiler-regression';folder.mkdir(parents=True,exist_ok=True)
    before=protected()
    import build_db
    target=folder/'comparison.db';build_db.build(str(target),subjects=['MAM','MAS','MAA'])
    old=sqlite3.connect('file:'+str(ROOT/'wace.db')+'?mode=ro',uri=True);new=sqlite3.connect('file:'+str(target)+'?mode=ro',uri=True)
    results=[]
    try:
        for subject in ('MAM','MAS','MAA'):
            for table in ('questions','parts','part_patterns','points','patterns'):
                cols={r[1] for r in old.execute('PRAGMA table_info('+table+')')}
                if 'subject' in cols:where='subject=?'
                elif 'topic' in cols:where='topic IN (SELECT code FROM topics WHERE subject=?)'
                elif 'question_id' in cols:where='question_id IN (SELECT id FROM questions WHERE subject=?)'
                elif 'qid' in cols:where='qid IN (SELECT id FROM questions WHERE subject=?)'
                else:raise ValueError('Unknown subject join: '+table)
                sql='SELECT * FROM '+table+' WHERE '+where
                a=set(old.execute(sql,(subject,)));b=set(new.execute(sql,(subject,)))
                results.append(dict(subject=subject,table=table,rows=len(a),differing_rows=len(a^b)))
    finally:old.close();new.close()
    after=protected();changed=[p for p in before if before[p]!=after.get(p)]
    report=dict(comparisons=results,total_rows=sum(r['rows'] for r in results),protected_changed=changed)
    (folder/'comparison.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2))
    if changed or any(r['differing_rows'] for r in results):raise SystemExit(1)


if __name__=='__main__':main()
