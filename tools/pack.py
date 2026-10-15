"""Data-only subject archives: export, validate, install. No paper download or database writes."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
from urllib.parse import urlsplit
import zipfile
import subjects

ROOT = Path(__file__).resolve().parent.parent
MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
APP_VERSION = (ROOT / 'app' / 'version.txt').read_text(encoding='utf-8').strip() if (ROOT / 'app' / 'version.txt').exists() else '0.0.0'


def destination(name, subject):
    path = PurePosixPath(name)
    if (not name or path.is_absolute() or str(path) != name or '\\' in name
            or any(p in ('.', '..') or re.search(r'[\x00-\x1f<>:"|?*]', p) or p.endswith((' ', '.'))
                   or re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', p, re.I) for p in path.parts)):
        raise ValueError(f'Unsafe archive path: {name}')
    fixed = {'pack.json': f'{subject}/pack.json', 'sources.tsv': f'{subject}/sources.tsv',
             'tags.txt': f'tools/tags_{subject}.txt', 'parttags.txt': f'tools/parttags_{subject}.txt',
             'catalogue.json': f'tools/catalogue_{subject}.json', 'marktags.json': f'tools/marktags_{subject}.json',
             'splits.json': f'tools/splits_{subject}.json'}
    if name in fixed:
        return fixed[name]
    if path.parts[0] in ('methods', 'methods_en') and path.suffix in ('.md', '.pdf'):
        return f'{subject}/{name}'
    if path.parts[0] == 'skill' and path.suffix == '.md':
        return str(PurePosixPath('skills', f'wace-{subject.lower()}-questions', *path.parts[1:]))
    if len(path.parts) == 2 and path.parts[0] == 'cheatsheet' and path.name.startswith(subject + '_') and path.suffix in ('.md', '.pdf'):
        return name
    raise ValueError(f'File not allowed in a subject pack: {name}')


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d+\.\d+\.\d+', value):
        raise ValueError('Version must be major.minor.patch')
    return tuple(map(int, value.split('.')))


def validate_sources(data, subject):
    """The columns are described in fetch.py; a pack's manifest must carry the full metadata."""
    import fetch
    seen = set()
    for line in data.decode('utf-8').splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        fields = line.split('\t')
        if len(fields) != len(fetch.COLUMNS):
            raise ValueError('Invalid sources.tsv line (needs ' + ', '.join(fetch.COLUMNS) + ')')
        path, url, method, capture, sha256, size, pages, need = fields
        if (method not in ('wayback', 'browser', 'direct') or need not in ('required', 'optional')
                or (method == 'wayback') != bool(re.fullmatch(r'\d{14}', capture)) or (capture and method != 'wayback')
                or not re.fullmatch(r'[0-9a-f]{64}', sha256) or not size.isdigit() or not pages.isdigit()):
            raise ValueError(f'Invalid source metadata: {path}')
        archived = method == 'wayback'
        parts = PurePosixPath(path).parts
        if (len(parts) != 3 or parts[:2] != (subject, 'papers') or not parts[2].endswith('.pdf')
                or str(PurePosixPath(path)) != path or '\\' in path or ':' in path or path.casefold() in seen):
            raise ValueError(f'Invalid source path: {path}')
        destination('methods/' + parts[2], subject)  # same safe filename rules as archive payloads
        seen.add(path.casefold())
        parsed = urlsplit(url)
        if parsed.scheme not in (('https', 'http') if archived else ('https',)) or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Paper sources must use HTTPS without credentials')
    if not seen:
        raise ValueError('Empty paper sources')


def inspect(file, app_version=APP_VERSION):
    with zipfile.ZipFile(file) as archive:
        entries = archive.infolist()
        names = [entry.filename for entry in entries]
        if (len(names) != len(set(names)) or len(names) > 2000 or 'pack.json' not in names
                or sum(e.file_size for e in entries) > MAX_TOTAL):
            raise ValueError('Invalid archive inventory or size')
        for entry in entries:
            if entry.is_dir() or entry.file_size > MAX_FILE or stat.S_ISLNK(entry.external_attr >> 16):
                raise ValueError('Directories, links or oversized files are not allowed')
        if archive.getinfo('pack.json').file_size > 1024 * 1024:
            raise ValueError('Manifest too large')
        profile = json.loads(archive.read('pack.json').decode('utf-8'))
        if isinstance(profile,dict) and profile.get('wtf_pack')==2:
            from wtf_compiler.archive import inspect as inspect_recipe
            return inspect_recipe(file), {}
        if not isinstance(profile, dict):
            raise ValueError('Invalid manifest')
        subject = profile.get('subject', '')
        if not isinstance(subject, str):
            raise ValueError('Invalid subject')
        subjects.validate_profile(profile, Path(subject) / 'pack.json')
        version(profile.get('version'))
        requirement = profile.get('requires_wtf', '')
        if not isinstance(requirement, str) or not requirement.startswith('>=') or version(requirement[2:]) > version(app_version):
            raise ValueError('Pack requires a newer WTF version')
        hashes = profile.get('files')
        if not isinstance(hashes, dict) or set(hashes) != set(names) - {'pack.json'}:
            raise ValueError('Manifest must hash every payload file')
        payload = {}
        targets = set()
        for name in names:
            target = destination(name, subject)
            if target.casefold() in targets:
                raise ValueError('Archive paths collide on Windows')
            targets.add(target.casefold())
            data = archive.read(name)
            if name != 'pack.json' and hashes[name] != 'sha256:' + hashlib.sha256(data).hexdigest():
                raise ValueError(f'Hash mismatch: {name}')
            payload[name] = data
        for required in ('sources.tsv', 'tags.txt', 'parttags.txt', 'skill/SKILL.md'):
            if required not in payload:
                raise ValueError(f'Missing required payload: {required}')
        validate_sources(payload['sources.tsv'], subject)
        validate_tags(payload, subject, version(requirement[2:]))
    return profile, payload


def validate_tags(payload, subject, required):
    """Catalogue, award tags and split shapes are data checked by marktags.py; award-level files need WTF 2.0.1+."""
    import marktags
    data = {name: json.loads(payload[name].decode('utf-8')) for name in ('catalogue.json', 'marktags.json', 'splits.json')
            if name in payload}
    if ('marktags.json' in data or 'splits.json' in data) and required < marktags.FIRST_FLOW_WTF:
        raise ValueError('Award-level tags need requires_wtf >= ' + '.'.join(map(str, marktags.FIRST_FLOW_WTF)))
    if 'catalogue.json' in data:
        marktags.validate_catalogue(data['catalogue.json'])
    if 'marktags.json' in data:
        if 'catalogue.json' not in data:
            raise ValueError('marktags.json needs catalogue.json')
        marktags.validate_marktags(data['marktags.json'], data['catalogue.json'], subject)
    if 'splits.json' in data:
        marktags.validate_splits(data['splits.json'])


def install(file, root, overwrite=False, app_version=APP_VERSION):
    profile, payload = inspect(file, app_version)
    root = Path(root).resolve()
    if profile.get('wtf_pack')==2:
        from wtf_compiler.service import Compiler
        return Compiler(root/'compiler').library.import_pack(file)
    subject = profile['subject']
    if (root / subject / 'pack.json').exists() and not overwrite:
        raise ValueError('Subject already installed; replacement needs confirmation')
    targets = {name: root / destination(name, subject) for name in payload}
    for target in targets.values():
        if not target.resolve().is_relative_to(root):
            raise ValueError('Install target escapes data root')
    root.mkdir(parents=True, exist_ok=True)
    before, written = {}, []
    with tempfile.TemporaryDirectory(prefix='.pack-', dir=root) as temporary:
        try:
            # Registration comes last. Failed installs restore every overwritten payload.
            for index, name in enumerate([n for n in payload if n != 'pack.json'] + ['pack.json']):
                target = targets[name]
                before[target] = target.read_bytes() if target.exists() else None
                target.parent.mkdir(parents=True, exist_ok=True)
                stage = Path(temporary) / str(index)
                stage.write_bytes(payload[name])
                os.replace(stage, target)
                written.append(target)
        except BaseException:
            for target in reversed(written):
                if before[target] is None:
                    target.unlink()
                else:
                    target.write_bytes(before[target])
            raise
    return profile


def export(subject, root=ROOT, out=None, draft=False):
    root = Path(root)
    profile = {k: v for k, v in subjects.info(subject, root).items() if k != 'engine'}  # runtime field, not pack data
    checker = ROOT / 'skills/wtf-subject-pack/scripts/pack_status.py'
    result = subprocess.run([os.sys.executable, str(checker), subject, '--root', str(root)],
                            capture_output=True, text=True, encoding='utf-8', env={**os.environ, 'PYTHONUTF8': '1'})
    if result.returncode and not draft:
        raise ValueError('Subject is incomplete; export refused:\n' + result.stdout + result.stderr)
    profile['quality'] = 'draft' if result.returncode else 'ready'
    # Export only Git-tracked original inputs; never recursively package arbitrary data folders.
    tracked = subprocess.run(['git', 'ls-files', '-z'], cwd=root, check=True, capture_output=True,
                             text=True, encoding='utf-8').stdout.split('\0')
    payload = {}
    for name in tracked:
        if not name or name == f'{subject}/pack.json':
            continue
        archive_name = None
        if name.startswith(f'{subject}/methods/') or name.startswith(f'{subject}/methods_en/'):
            archive_name = name[len(subject) + 1:]
        elif name.startswith(f'skills/wace-{subject.lower()}-questions/'):
            archive_name = 'skill/' + name.split('/', 2)[2]
        elif name.startswith(f'cheatsheet/{subject}_'):
            archive_name = name
        else:
            archive_name = {f'tools/tags_{subject}.txt': 'tags.txt', f'tools/parttags_{subject}.txt': 'parttags.txt',
                            f'tools/catalogue_{subject}.json': 'catalogue.json', f'tools/marktags_{subject}.json': 'marktags.json',
                            f'tools/splits_{subject}.json': 'splits.json'}.get(name)
        if archive_name:
            destination(archive_name, subject)
            payload[archive_name] = (root / name).read_bytes()
    if 'marktags.json' not in payload:  # split shapes only number awards for marktags: without them, WTF 2.0 can install
        payload.pop('splits.json', None)
    payload['sources.tsv'] = (root / subject / 'sources.tsv').read_bytes()
    profile['files'] = {name: 'sha256:' + hashlib.sha256(data).hexdigest() for name, data in payload.items()}
    target = Path(out or root / 'dist') / f'{subject}-{profile["version"]}.wtfpack'
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.export-', dir=target.parent) as temporary:
        stage = Path(temporary) / target.name
        with zipfile.ZipFile(stage, 'w', zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('pack.json', json.dumps(profile, ensure_ascii=False, indent=2).encode('utf-8'))
            for name, data in sorted(payload.items()):
                archive.writestr(name, data)
        inspect(stage)
        os.replace(stage, target)
    return target


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    ex = sub.add_parser('export')
    ex.add_argument('subject')
    ex.add_argument('--root', type=Path, default=ROOT)
    ex.add_argument('--out', type=Path)
    ex.add_argument('--draft', action='store_true', help='local regression only; mark incomplete packs as drafts')
    im = sub.add_parser('import')
    im.add_argument('file', type=Path)
    im.add_argument('--root', type=Path, default=ROOT)
    im.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    print(export(args.subject, args.root, args.out, args.draft) if args.command == 'export'
          else install(args.file, args.root, args.replace))
