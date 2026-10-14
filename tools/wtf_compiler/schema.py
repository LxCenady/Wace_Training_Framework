"""Validate portable recipes and their source geometry; never execute pack content."""
import json
import math
import re
import uuid
from urllib.parse import urlsplit
import rubric

CAPABILITIES = {'read', 'export', 'generate', 'mark'}
ROLES = {'exam', 'key', 'syllabus', 'report', 'reference'}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def fields(value, allowed, required=()):
    require(isinstance(value,dict),'Expected a JSON object')
    extra=set(value)-set(allowed);missing=set(required)-set(value)
    require(not extra,'Unknown fields: '+', '.join(sorted(extra)))
    require(not missing,'Missing required fields: '+', '.join(sorted(missing)))


def identifier(value):
    require(isinstance(value, str) and bool(re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.:-]{0,119}', value)), 'Invalid ID')
    return value


def number(value):
    return type(value) in (int, float) and math.isfinite(value) and value >= 0


def url(value):
    p = urlsplit(value)
    require(p.scheme == 'https' and p.hostname and not p.username and not p.password and not p.fragment,
            'Source URL must be credential-free HTTPS')


def region(value, sources):
    fields(value, ('document', 'page', 'bbox', 'rotate'), ('document', 'page', 'bbox'))
    require(value['document'] in sources, 'Unknown source document')
    require(type(value['page']) is int and 0 <= value['page'] < sources[value['document']]['pages'], 'Invalid source page')
    box = value['bbox']
    require(isinstance(box, list) and len(box) == 4 and all(number(v) for v in box)
            and 0 <= box[0] < box[2] <= 1 and 0 <= box[1] < box[3] <= 1, 'Invalid normalized source rectangle')
    require(type(value.get('rotate', 0)) is int and value.get('rotate', 0) in (0, 90, 180, 270), 'Invalid rotation')


def regions(values, sources, required=False):
    require(isinstance(values, list) and len(values) <= 64 and (values or not required), 'Missing source evidence')
    for value in values:
        region(value, sources)


def validate_tree(tree, printed, sources, known_nodes=None):
    nodes, maxima = rubric.validate(tree, printed)
    allowed = {'id', 'kind', 'max_marks', 'positive_band', 'children', 'take', 'cap', 'requires', 'conditions',
               'conditional_caps', 'knowledge', 'patterns', 'source', 'levels', 'ecf', 'credit_step'}
    for node in nodes.values():
        fields(node, allowed, ('id', 'kind'))
        identifier(node['id'])
        if node['kind']!='award':
            require(not {'positive_band','levels','ecf','credit_step'}&set(node),'Award-only fields on scoring group')
            if 'max_marks' in node:require(number(node['max_marks']) and math.isclose(node['max_marks'],maxima[node['id']],abs_tol=1e-9),'Group max_marks differs from computed maximum')
            if 'source' in node:regions(node['source'],sources,True)
        if node['kind']!='select':require('take' not in node,'take belongs only to select groups')
        if node['kind'] == 'award':
            regions(node.get('source', []), sources, True)
            step=node.get('credit_step',1)
            if 'credit_step' in node or not node.get('levels'):require(number(step) and step>0 and step<=node['max_marks'],'Invalid credit step')
            if not node.get('levels'):require(math.isclose(node['max_marks']/step,round(node['max_marks']/step),abs_tol=1e-9),'Maximum must be reachable using credit_step; declare fractional steps explicitly')
            levels = node.get('levels')
            if levels is not None:
                require(isinstance(levels, list) and levels and len(levels) <= 100, 'Invalid scoring levels')
                scores = []
                for level in levels:
                    fields(level, ('score', 'source'), ('score', 'source'))
                    require(number(level['score']) and level['score'] <= node['max_marks'], 'Invalid level score')
                    regions(level['source'], sources, True)
                    scores.append(level['score'])
                require(len(set(scores)) == len(scores) and max(scores) == node['max_marks'], 'Levels must reach the maximum')
            ecf = node.get('ecf')
            if ecf is not None:
                fields(ecf, ('policy', 'from', 'source'), ('policy', 'from', 'source'))
                require(ecf['policy'] in ('explicit', 'reviewed', 'unspecified') and isinstance(ecf['from'], list)
                        and ecf['from'] and len(set(ecf['from'])) == len(ecf['from'])
                        and all(v in (known_nodes or nodes) and v != node['id'] for v in ecf['from']), 'Invalid ECF references')
                regions(ecf['source'], sources, True)
    visiting, done = set(), set()
    def walk(ident):
        require(ident not in visiting, 'Cyclic ECF links')
        if ident in done:
            return
        visiting.add(ident)
        for ref in nodes[ident].get('ecf', {}).get('from', []):
            if ref in nodes:walk(ref)
        visiting.remove(ident); done.add(ident)
    for ident in nodes:
        walk(ident)
    return nodes


def validate(recipe,complete=True):
    fields(recipe, ('wtf_pack', 'pack_id', 'version', 'course', 'capabilities', 'sources', 'questions', 'taxonomy',
                    'notes', 'skill','coverage'), ('wtf_pack', 'pack_id', 'version', 'course', 'capabilities', 'sources', 'questions', 'taxonomy','coverage'))
    require(recipe['wtf_pack'] == 2, 'Unsupported recipe protocol')
    require(isinstance(recipe['pack_id'], str) and uuid.UUID(recipe['pack_id']).hex == recipe['pack_id'], 'Invalid pack ID')
    require(isinstance(recipe['version'], str) and re.fullmatch(r'\d+\.\d+\.\d+', recipe['version']), 'Invalid version')
    course = recipe['course']
    fields(course, ('id', 'name', 'sections'), ('id', 'name', 'sections'))
    identifier(course['id']); require(isinstance(course['name'], dict) and course['name']
                                    and all(k in ('zh', 'en') and isinstance(v, str) and v.strip() for k, v in course['name'].items()), 'Invalid course names')
    sections = {}
    require(isinstance(course['sections'], list) and course['sections'], 'Missing sections')
    for section in course['sections']:
        fields(section, ('id', 'name', 'weight', 'minutes'), ('id', 'name'))
        identifier(section['id']); require(section['id'] not in sections and isinstance(section['name'], str) and section['name'], 'Invalid section')
        require(number(section.get('weight', 0)) and number(section.get('minutes', 0)), 'Invalid section weight/time')
        sections[section['id']] = section
    require(isinstance(recipe['capabilities'], list) and set(recipe['capabilities']) <= CAPABILITIES
            and len(set(recipe['capabilities'])) == len(recipe['capabilities']) and 'read' in recipe['capabilities'], 'Invalid capabilities')
    sources = {}
    require(isinstance(recipe['sources'], list) and recipe['sources'], 'Missing documents')
    for doc in recipe['sources']:
        fields(doc, ('id', 'sha256', 'pages', 'roles', 'url'), ('id', 'sha256', 'pages', 'roles'))
        identifier(doc['id']); require(doc['id'] not in sources, 'Duplicate document ID')
        require(isinstance(doc['sha256'], str) and re.fullmatch('[0-9a-f]{64}', doc['sha256'])
                and type(doc['pages']) is int and 0 < doc['pages'] <= 2000, 'Invalid document fingerprint')
        require(isinstance(doc['roles'], list) and doc['roles'] and set(doc['roles']) <= ROLES, 'Invalid document roles')
        if doc.get('url'):
            url(doc['url'])
        sources[doc['id']] = doc
    require({'exam', 'key', 'syllabus'} <= {v for d in sources.values() for v in d['roles']}, 'Exam, key and syllabus are required')
    coverage=recipe['coverage'];require(isinstance(coverage,dict) and set(coverage)=={i for i,d in sources.items() if 'exam' in d['roles']},'Every exam needs printed coverage metadata')
    for ident,row in coverage.items():
        fields(row,('questions','marks','source'),('questions','marks','source'))
        require(type(row['questions'])is int and 0<row['questions']<=10000 and number(row['marks']) and row['marks']>0,'Invalid printed coverage')
        regions(row['source'],sources,True)
        require(all(r['document']==ident for r in row['source']),'Coverage evidence must reference its original exam')
    taxonomy = recipe['taxonomy']
    fields(taxonomy, ('topics', 'knowledge', 'patterns', 'axes'), ('topics', 'knowledge', 'patterns'))
    codes = {}
    for group in ('topics', 'knowledge', 'patterns', 'axes'):
        require(isinstance(taxonomy.get(group, []), list), 'Invalid taxonomy')
        codes[group] = set()
        for item in taxonomy.get(group, []):
            fields(item, ('id', 'name', 'definition', 'topic', 'members', 'source'), ('id', 'name'))
            identifier(item['id']); require(item['id'] not in codes[group] and isinstance(item['name'], str) and item['name'], 'Invalid taxonomy entry')
            codes[group].add(item['id'])
            if 'source' in item:
                regions(item['source'], sources, True)
    require(codes['topics'] and codes['knowledge'] and codes['patterns'], 'Incomplete taxonomy')
    for group in ('knowledge', 'patterns'):
        for item in taxonomy[group]:
            require(item.get('topic') in codes['topics'], 'Unknown taxonomy topic')
    for axis in taxonomy.get('axes', []):
        require(isinstance(axis.get('members'), list) and set(axis['members']) <= codes['knowledge'], 'Invalid axis members')
    require(isinstance(recipe['questions'], list) and 0 < len(recipe['questions']) <= 10000, 'Missing questions')
    ids = set(); all_parts = set(); all_nodes = set()
    known_nodes={}
    question_nodes={}
    for q in recipe['questions']:
        for p in q.get('parts',[]):
            nodes,_=rubric.validate(p['rubric'],p['marks'])
            require(not set(nodes)&set(known_nodes),'Rubric IDs must be globally unique')
            known_nodes.update(nodes)
            for ident in nodes:question_nodes[ident]=q['id']
    for question in recipe['questions']:
        fields(question, ('id', 'label', 'section', 'marks', 'source', 'key_source', 'shared_source', 'parts'),
               ('id', 'label', 'section', 'marks', 'source', 'key_source', 'parts'))
        identifier(question['id']); require(question['id'] not in ids and isinstance(question['label'], str), 'Duplicate question ID')
        ids.add(question['id']); require(question['section'] in sections and number(question['marks']), 'Invalid question marks/section')
        regions(question['source'], sources, True); regions(question['key_source'], sources, True)
        require(all('exam' in sources[r['document']]['roles'] for r in question['source']), 'Question evidence must reference exams')
        require(len({r['document'] for r in question['source']})==1,'Question body belongs to one exam; separate stimuli belong in shared_source')
        require(all('key' in sources[r['document']]['roles'] for r in question['key_source']), 'Answer evidence must reference keys')
        regions(question.get('shared_source', []), sources)
        require(isinstance(question['parts'], list) and question['parts'], 'Missing parts')
        part_ids = set(); total = 0
        for part in question['parts']:
            fields(part, ('id', 'label', 'marks', 'rubric'), ('id', 'label', 'marks', 'rubric'))
            identifier(part['id']); require(part['id'] not in part_ids and isinstance(part['label'], str) and number(part['marks']), 'Invalid part')
            require(part['id'] not in all_parts, 'Part IDs must be globally unique')
            all_parts.add(part['id']); part_ids.add(part['id']); total += part['marks']
            for node in validate_tree(part['rubric'], part['marks'], sources, known_nodes).values():
                require(node['id'] not in all_nodes, 'Rubric IDs must be globally unique')
                all_nodes.add(node['id'])
                for group in ('knowledge', 'patterns'):
                    require(set(node.get(group, [])) <= codes[group], 'Unknown award association')
        require(math.isclose(total, question['marks'], abs_tol=1e-9), 'Part marks differ from question')
    active,done=set(),set()
    def ecf_walk(ident):
        require(ident not in active,'Cyclic cross-part ECF links')
        if ident in done:return
        active.add(ident)
        for ref in known_nodes[ident].get('ecf',{}).get('from',[]):ecf_walk(ref)
        active.remove(ident);done.add(ident)
    for ident in known_nodes:ecf_walk(ident)
    for ident,node in known_nodes.items():
        require(all(question_nodes[ref]==question_nodes[ident] for ref in node.get('ecf',{}).get('from',[])), 'ECF may cross parts of the same question, not separate questions')
    for ident,expected in coverage.items():
        questions=[q for q in recipe['questions'] if q['source'][0]['document']==ident]
        count=len(questions);marks=sum(q['marks'] for q in questions)
        valid=(count==expected['questions'] and math.isclose(marks,expected['marks'],abs_tol=1e-9)) if complete else count<=expected['questions'] and marks<=expected['marks']
        require(valid,f"Exam {ident}: expected {expected['questions']} questions / {expected['marks']} marks; got {count} questions / {marks} marks")
    notes = recipe.get('notes', {})
    require(isinstance(notes, dict) and not set(notes)-{'zh','en'} and all(isinstance(v,str) for v in notes.values()), 'Invalid notes')
    require(isinstance(recipe.get('skill', ''), str), 'Invalid skill')
    if 'generate' in recipe['capabilities']:
        require(recipe.get('skill') and notes.get('zh') and notes.get('en'), 'Generation requires bilingual notes and a skill')
    require(len(json.dumps(recipe).encode()) <= 16*1024*1024, 'Recipe too large')
    return recipe
