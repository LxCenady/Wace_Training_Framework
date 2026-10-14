"""Runtime adapters preserve criterion maxima and non-additive scoring trees."""
import copy
import json
import rubric
from .schema import require
from .scoring import score


def snapshot(library,pack,qid,version=None):
    snap=library.snapshot(pack,qid,version);q=snap['question']
    return snap | dict(ref=pack+':'+snap['version']+':'+qid,label=q['label'],marks=q['marks'],
        subject='compiler:'+pack,parts=q['parts'],points=[],schema_version=2)


def points(item):
    snap=item['snapshot'];out=[]
    for part in snap['parts']:
        nodes,_=rubric.validate(part['rubric'],part['marks']);unit=0
        for node in nodes.values():
            if node['kind']!='award':continue
            out.append(dict(point_id=node['id'],number=len(out)+1,label=part['label'],unit=unit,
                text=snap['content']['criteria'][node['id']],max_marks=node['max_marks'],levels=node.get('levels'),credit_step=node.get('credit_step',1),
                ecf_policy=node.get('ecf'),manual_only=node.get('manual_only',False),part_id=part['id'],schema_version=2,**({'rubric':copy.deepcopy(part['rubric'])} if unit==0 else {})))
            unit+=1
    require(bool(out),'Missing rubric criteria')
    return out


def proposal(value,canonical,evidence_count,manual=False):
    require(isinstance(value,dict) and value.get('schema_version')==2 and isinstance(value.get('points'),list),'Expected rubric schema_version 2')
    rows={}
    for row in value['points']:
        require(isinstance(row,dict) and row.get('point_id') not in rows,'Duplicate criterion')
        rows[row.get('point_id')]=row
    require(set(rows)=={p['point_id'] for p in canonical},'Incomplete rubric proposal')
    results={};out=[];conditions=value.get('conditions',{})
    require(isinstance(conditions,dict),'Invalid condition judgments')
    groups={}
    for p in canonical:groups.setdefault(p['part_id'],[]).append(p)
    for part,ps in groups.items():
        awards=[]
        for p in ps:
            row=rows[p['point_id']]
            awards.append(dict(award_id=p['point_id'],**{key:row[key] for key in ('got','reason','evidence')},
                               **({'ecf':row['ecf']} if row.get('ecf') else {})))
        checked=score(ps[0]['rubric'],dict(schema_version=2,awards=awards,conditions=conditions.get(part,{})),evidence_count,manual=manual)
        results[part]=checked
        for p,row in zip(ps,checked['awards']):
            out.append({**p,**{k:v for k,v in row.items() if k!='award_id'},
                        'got':None if checked['needs_review'] else row['got']})
    return dict(schema_version=2,points=out,conditions=conditions,rubric_scores=results,origin='teacher' if manual else 'model')


def score_rows(item,value):
    canonical=points(item)
    require(isinstance(value,dict),'Compiler scores require rubric proposals')
    evidence_count=value.get('evidence_count',1)
    manual=value.get('origin')=='teacher'
    checked=proposal(value,canonical,0 if manual else evidence_count,manual=manual)
    require(all(r['score']['resolved'] and not r['needs_review'] for r in checked['rubric_scores'].values()),'Unresolved rubric judgments')
    total=item['snapshot']['marks'];got=sum(r['score']['earned'] for r in checked['rubric_scores'].values())
    # Store complete tree decisions on an aggregate row; overlapping tags/alternative routes do not add credit.
    return [('rubric',0,got,json.dumps(checked,ensure_ascii=False))],total,got
