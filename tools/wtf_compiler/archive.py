"""Hash-checked recipe archives: never include PDFs or private OCR content."""
import hashlib
import json
from pathlib import Path
import zipfile
import uuid
from .schema import require, validate

LIMIT = 16 * 1024 * 1024


def encode(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2).encode('utf-8')


def export(recipe, target):
    validate(recipe)
    payload = {'sources.json': encode(recipe['sources']), 'layout.json': encode(recipe['questions']),
               'taxonomy.json': encode(recipe['taxonomy']), 'coverage.json':encode(recipe['coverage'])}
    for lang, text in recipe.get('notes', {}).items():
        payload[f'notes/{lang}.md'] = text.encode('utf-8')
    if recipe.get('skill'):
        payload['skill/SKILL.md'] = recipe['skill'].encode('utf-8')
    manifest = {key: recipe[key] for key in ('wtf_pack', 'pack_id', 'version', 'course', 'capabilities')}
    manifest['files'] = {name: hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    target = Path(target)
    require(target.suffix == '.wtfpack', 'Expected .wtfpack destination')
    require(sum(map(len, payload.values())) <= LIMIT, 'Recipe archive too large')
    temp = target.with_suffix('.'+uuid.uuid4().hex+'.tmp')
    try:
        with zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) as z:
            z.writestr('pack.json', encode(manifest))
            for name, data in payload.items():
                z.writestr(name, data)
        inspect(temp)
        temp.replace(target)
    finally:
        temp.unlink(missing_ok=True)
    return str(target)


def inspect(path):
    allowed = {'pack.json','sources.json','layout.json','taxonomy.json','coverage.json','notes/zh.md','notes/en.md','skill/SKILL.md'}
    with zipfile.ZipFile(path) as z:
        infos = z.infolist(); names = [v.filename for v in infos]
        require(len(names) == len(set(names)) and set(names) <= allowed, 'Unknown or duplicate archive paths')
        require({'pack.json','sources.json','layout.json','taxonomy.json','coverage.json'} <= set(names), 'Incomplete recipe archive')
        require(sum(v.file_size for v in infos) <= LIMIT and all(not v.is_dir() and
                (v.external_attr >> 16) & 0o170000 != 0o120000 for v in infos), 'Oversized or linked archive')
        manifest = json.loads(z.read('pack.json'))
        require(set(manifest) == {'wtf_pack','pack_id','version','course','capabilities','files'}, 'Invalid manifest')
        require(isinstance(manifest['files'],dict) and set(manifest['files']) == set(names)-{'pack.json'}, 'Incomplete file hashes')
        for name, expected in manifest['files'].items():
            require(hashlib.sha256(z.read(name)).hexdigest() == expected, 'Payload hash mismatch: '+name)
        recipe = {k:v for k,v in manifest.items() if k != 'files'}
        recipe.update(sources=json.loads(z.read('sources.json')), questions=json.loads(z.read('layout.json')),
                      taxonomy=json.loads(z.read('taxonomy.json')),coverage=json.loads(z.read('coverage.json')))
        recipe['notes'] = {lang:z.read(f'notes/{lang}.md').decode('utf-8') for lang in ('zh','en') if f'notes/{lang}.md' in names}
        recipe['skill'] = z.read('skill/SKILL.md').decode('utf-8') if 'skill/SKILL.md' in names else ''
    return validate(recipe)
