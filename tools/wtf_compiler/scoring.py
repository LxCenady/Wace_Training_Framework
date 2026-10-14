"""Versioned criterion proposals, level restrictions and explicit ECF evidence."""
import rubric
import math
from .schema import number, require, fields


def score(tree, proposal, evidence_count,manual=False):
    nodes, _ = rubric.validate(tree)
    fields(proposal, ('schema_version','awards','conditions'), ('schema_version','awards'))
    require(proposal['schema_version'] == 2 and isinstance(proposal['awards'],list), 'Invalid rubric proposal')
    conditions=proposal.get('conditions',{})
    require(isinstance(conditions,dict) and all(isinstance(k,str) and (v is None or type(v)is bool) for k,v in conditions.items()), 'Invalid condition judgments')
    require(type(evidence_count)is int and (evidence_count==0 if manual else 0<evidence_count<=64),'Invalid evidence count')
    awards={key:value for key,value in nodes.items() if value['kind']=='award'}
    by={};credits={};pending=[]
    for row in proposal['awards']:
        fields(row, ('award_id','got','reason','evidence','ecf'), ('award_id','got','reason','evidence'))
        key=row['award_id'];require(key in awards and key not in by, 'Unknown or duplicate award')
        require(isinstance(row['reason'],str) and 0<len(row['reason'])<=1000, 'Missing criterion explanation')
        refs=row['evidence'];require(isinstance(refs,list) and (not refs if manual else refs and all(type(v)is int and 0<=v<evidence_count for v in refs)), 'Invalid student evidence')
        value=row['got'];node=awards[key]
        if not manual and node.get('ecf',{}).get('policy') in ('unspecified','reviewed') and value is not None and number(value) and value>0:
            pending.append(key);value=None
        require(value is None or number(value) and value<=node['max_marks'], 'Credit out of range')
        if value is not None and node.get('levels'):
            require(value==0 or value in [v['score'] for v in node['levels']], 'Credit not in a permitted level')
        elif value is not None:
            step=node.get('credit_step',1)
            require(number(step) and step>0 and math.isclose(value/step,round(value/step),abs_tol=1e-9),'Credit not on the declared credit_step')
        ecf=row.get('ecf')
        if ecf:
            fields(ecf, ('from','used_value','reason','evidence'), ('from','used_value','reason','evidence'))
            policy=node.get('ecf',{})
            require(isinstance(ecf['from'],list) and ecf['from'] and set(ecf['from'])<=set(policy.get('from',[])), 'ECF outside permitted links')
            require(all(isinstance(ecf[v],str) and 0<len(ecf[v])<=1000 for v in ('used_value','reason')), 'Missing ECF working')
            require(isinstance(ecf['evidence'],list) and ecf['evidence'] and all(type(v)is int and 0<=v<evidence_count for v in ecf['evidence']), 'Missing ECF evidence')
            if policy.get('policy') not in ('explicit','reviewed'):
                pending.append(key);value=None
        by[key]={**row,'got':value}
        if value is None:
            pending.append(key)
        else:
            credits[key]=value
    require(set(by)==set(awards), 'Incomplete criterion proposal')
    result=rubric.score(tree,credits,conditions)
    pending.extend(result.get('unresolved_conditions',[]))
    if not result['resolved']:pending.append('rubric_conditions')
    if pending:
        result.update(earned=None,resolved=False,lower=0,upper=result['possible'])
    return dict(schema_version=2,awards=list(by.values()),score=result,needs_review=sorted(set(pending)))
