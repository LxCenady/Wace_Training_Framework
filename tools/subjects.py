"""Installed subject packs. One job: validate and read every installed pack's profile.

WTF is the runtime of its packs: everything about a course (names, topics, sections, timing, recognition, scoring
handlers, notes, skill) comes from its pack. A profile says how its bank is made (`engine`):
  "flow"      <S>/pack.json — a data pack built locally from the original papers (tools/build_all.py)
  "compiler"  compiler/profiles/<S>.json — generated when a Compiler recipe pack is activated (wtf_compiler/bank.py)
"""
import json
import os
from pathlib import Path
import re
import scoring
import handlers
import paper_selection

BANK = "bank.db"            # the local question bank every view reads
LEGACY_BANK = "wace.db"     # its name before WTF 2.1 (read when no bank.db exists yet)
CODE = re.compile(r"[A-Z][A-Z0-9]{1,11}")  # MAM, ACF, CAIE9709


def data_root(root=None):
    return Path(root or os.environ.get('WACE_MATHS_ROOT') or Path(__file__).resolve().parent.parent)


def bank_path(root=None):
    """The bank file of a data root: bank.db, or a bank built before 2.1 under its old name."""
    root = data_root(root)
    return str(root / LEGACY_BANK) if not (root / BANK).exists() and (root / LEGACY_BANK).exists() else str(root / BANK)


def profiles(root=None, engine=None):
    """{subject: profile} of every installed pack (or only those of one `engine`), in display order."""
    root = data_root(root)
    out = {}
    for path, kind in [(p, "flow") for p in root.glob('*/pack.json')] +                       [(p, "compiler") for p in (root / 'compiler' / 'profiles').glob('*.json')]:
        data = json.loads(path.read_text(encoding='utf-8'))
        validate_profile(data, path, kind)
        if engine in (None, kind):
            out[data["subject"]] = dict(data, engine=kind)
    return dict(sorted(out.items(), key=lambda item: (item[1].get('order', 100), item[0])))


def info(subject, root=None):
    return profiles(root)[subject]


def names(root=None, language='zh', engine=None):
    return {s: p['name'][language] for s, p in profiles(root, engine).items()}


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
        if section['code'] == code:  # one section of a shared paper: its suggested working time, no reading time
            return section['minutes'] or ([0, section['suggested_minutes']] if section.get('suggested_minutes')
                                          else pack['paper_minutes'])
    raise ValueError(f'Unknown section {subject}: {code}')


def section_options(subject=None, any_value='any', root=None):
    labels = section_labels(subject, root=root)
    shorts = section_labels(subject, 'short', root)
    return {'任意': any_value, **{f'{name} ({shorts[code]})': code for code, name in labels.items()}}


def validate_profile(data, path, engine='flow'):
    path = Path(path)
    if not isinstance(data, dict):
        raise ValueError(f'Invalid profile: {path}')
    subject = data.get('subject', '')
    home = path.parent.name if engine == 'flow' else path.stem  # <S>/pack.json or compiler/profiles/<S>.json
    if not isinstance(subject, str) or not CODE.fullmatch(subject) or home != subject:
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
    # optional: another exam board's wording for its covers (tools/paperid.py DEFAULTS are SCSA's)
    for field in ('exam', 'report', 'key', 'year', 'sample'):
        words = data['recognise'].get(field)
        if words is not None and (not isinstance(words, list) or not words
                                  or any(not isinstance(w, str) or not w.strip() for w in words)):
            raise ValueError(f'Invalid recognise.{field}: {path}')
    for pattern in data['recognise'].get('year', []) + data['recognise'].get('sample', []):
        try:
            groups = re.compile(pattern).groups
        except re.error:
            raise ValueError(f'Invalid recognition pattern {pattern!r}: {path}')
        if pattern in data['recognise'].get('year', []) and groups != 1:
            raise ValueError(f'A year pattern needs exactly one group (the year): {path}')
    if not isinstance(data['recognise'].get('sample_year', ''), str):
        raise ValueError(f'Invalid recognise.sample_year: {path}')
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
        paper_selection.validate(section)
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
    if type(data.get('nested_part_totals', False)) is not bool:
        raise ValueError(f'Invalid nested_part_totals: {path}')
    if any(not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*', sheet) for sheet in data['sheets']):
        raise ValueError(f'Unsafe sheet identifier: {path}')
    papers = data.get('papers', {'years': [], 'excluded': {}})  # coverage, and why a year is left out
    if (not isinstance(papers, dict) or not isinstance(papers.get('years', []), list)
            or any(type(y) is not int for y in papers.get('years', []))
            or any(not isinstance(papers.get(field, {}), dict)  # acknowledged: source discrepancies checked by hand
                   or any(not isinstance(v, str) or not v.strip() for v in papers.get(field, {}).values())
                   for field in ('excluded', 'acknowledged'))):
        raise ValueError(f'Invalid papers: {path}')
    scoring.validate(data)
    handlers.validate(data)
    return data
