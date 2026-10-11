"""Installed subject profiles. One job: validate and read <subject>/pack.json."""
import json
import os
from pathlib import Path
import re
import scoring
import handlers


def profiles(root=None):
    root = Path(root or os.environ.get('WACE_MATHS_ROOT') or Path(__file__).resolve().parent.parent)
    out = {}
    for path in root.glob('*/pack.json'):
        data = json.loads(path.read_text(encoding='utf-8'))
        validate_profile(data, path)
        subject = data["subject"]
        out[subject] = data
    return dict(sorted(out.items(), key=lambda item: (item[1].get('order', 100), item[0])))


def info(subject, root=None):
    return profiles(root)[subject]


def names(root=None, language='zh'):
    return {s: p['name'][language] for s, p in profiles(root).items()}


def topics(subject, root=None):
    return {t['code']: (t['file'], t['zh'], t['en']) for t in info(subject, root)['topics']}


def sections(subject, root=None):
    return info(subject, root)['sections']


def section_letter(subject, code, root=None):
    for section in sections(subject, root):
        if section['code'] == code:
            return section['letter']
    raise ValueError(f'Unknown section {subject}: {code}')


def section_codes(subject=None, root=None):
    """Stable section order; a union is useful for filters spanning subjects."""
    return list(section_labels(subject, 'code', root))


def section_labels(subject=None, field='zh', root=None):
    packs = {subject: info(subject, root)} if subject else profiles(root)
    out = {}
    for pack in packs.values():
        for section in pack['sections']:
            value = section.get(field, section['code'])
            if section['code'] in out and out[section['code']] != value:
                raise ValueError(f'Ambiguous section label: {section["code"]}; specify subject')
            out[section['code']] = value
    return out


def section_name(subject, code, field='zh', root=None):
    return section_labels(subject, field, root).get(code, code or '')


def section_minutes(subject, code, root=None):
    pack = info(subject, root)
    for section in pack['sections']:
        if section['code'] == code:
            return section['minutes'] or pack['paper_minutes']
    raise ValueError(f'Unknown section {subject}: {code}')


def section_options(subject=None, any_value='any', root=None):
    labels = section_labels(subject, root=root)
    shorts = section_labels(subject, 'short', root)
    return {'任意': any_value, **{f'{name} ({shorts[code]})': code for code, name in labels.items()}}


def validate_profile(data, path):
    path = Path(path)
    if not isinstance(data, dict):
        raise ValueError(f'Invalid profile: {path}')
    subject = data.get('subject', '')
    if not isinstance(subject, str) or not re.fullmatch('[A-Z]{2,4}', subject) or path.parent.name != subject:
        raise ValueError(f'Invalid subject identity: {path}')
    if data.get('wtf_pack') != 1:
        raise ValueError(f'Unsupported pack protocol: {path}')
    for field in ('name', 'course', 'topics', 'sections', 'recognise'):
        if not data.get(field):
            raise ValueError(f'Missing {field}: {path}')
    if (not isinstance(data['name'], dict) or not isinstance(data['course'], str)
            or not isinstance(data['recognise'], dict)
            or type(data.get('order', 100)) is not int):
        raise ValueError(f'Invalid profile metadata: {path}')
    titles = data['recognise'].get('title')
    if not isinstance(titles, list) or not titles or any(not isinstance(t, str) or not t.strip() for t in titles):
        raise ValueError(f'Invalid recognition titles: {path}')
    for field in ('sections', 'topics'):
        if not isinstance(data[field], list) or any(not isinstance(item, dict) for item in data[field]):
            raise ValueError(f'Invalid {field}: {path}')
    for language in ('zh', 'en'):
        if not isinstance(data['name'].get(language), str) or not data['name'][language].strip():
            raise ValueError(f'Invalid name: {path}')
    for field in ('code', 'letter'):
        values = [s.get(field) for s in data['sections']]
        if any(not isinstance(v, str) or not v for v in values) or len(set(values)) != len(values):
            raise ValueError(f'Invalid section {field}: {path}')
    codes = [t.get('code') for t in data['topics']]
    if any(not isinstance(c, str) or not c for c in codes) or len(set(codes)) != len(codes):
        raise ValueError(f'Invalid topics: {path}')
    for topic in data['topics']:
        if any(not isinstance(topic.get(f), str) or not topic[f].strip() for f in ('file', 'zh', 'en')):
            raise ValueError(f'Invalid topic metadata: {path}')
        if not re.fullmatch(r'[A-Za-z0-9_-]+', topic['file']) or not re.fullmatch(r'[A-Za-z0-9_]+', topic['code']):
            raise ValueError(f'Unsafe topic identifier: {path}')
    for section in data['sections']:
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', section['code']) or not re.fullmatch(r'[A-Z0-9]{1,4}', section['letter']):
            raise ValueError(f'Unsafe section identifier: {path}')
        minutes = section.get('minutes')
        if (any(not isinstance(section.get(f), str) or not section[f].strip() for f in ('zh', 'en'))
                or (minutes is not None and (not isinstance(minutes, list) or len(minutes) != 2
                    or any(type(m) is not int or m < 0 for m in minutes)))):
            raise ValueError(f'Invalid section metadata: {path}')
        if minutes is None and (not isinstance(data.get('paper_minutes'), list)
                or len(data['paper_minutes']) != 2
                or any(type(m) is not int or m < 0 for m in data['paper_minutes'])):
            raise ValueError(f'Shared sections need paper_minutes: {path}')
    for field in ('sketch_words', 'sheets'):
        if not isinstance(data.get(field), list) or any(not isinstance(word, str) or not word for word in data[field]):
            raise ValueError(f'Invalid {field}: {path}')
    if data.get('sketch_mode', 'words') not in ('words', 'legacy-maths'):
        raise ValueError(f'Invalid sketch mode: {path}')
    if any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', sheet) for sheet in data['sheets']):
        raise ValueError(f'Unsafe sheet identifier: {path}')
    scoring.validate(data)
    handlers.validate(data)
    return data
