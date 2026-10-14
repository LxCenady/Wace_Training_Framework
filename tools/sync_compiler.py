"""Copy the canonical Compiler core to Studio and verify the complete hash manifest."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil


def sync(destination,check=False):
    root=Path(__file__).resolve().parents[1];dest=Path(destination).resolve()
    files=[*sorted((root/'tools/wtf_compiler').glob('*.py')),root/'tools/compiler.py',root/'tools/rubric.py',root/'app/plugins/compiler.py',root/'app/plugins/ui_compiler.py',root/'app/tests/test_compiler.py',root/'docs/compiler.md',root/'skills/wtf-compiler/SKILL.md']
    manifest={str(p.relative_to(root)).replace('\\','/'):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    for source in files:
        target=dest/source.relative_to(root)
        if check:
            if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest()!=manifest[str(source.relative_to(root)).replace('\\','/')]:
                raise ValueError('Compiler mirror differs: '+str(target))
        else:
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    target=dest/'tools/compiler_manifest.json'
    if check:
        if json.loads(target.read_text())!=manifest:raise ValueError('Compiler manifest differs')
    else:target.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    return len(files)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('studio');p.add_argument('--check',action='store_true');a=p.parse_args()
    print('Verified' if a.check else 'Synced',sync(a.studio,a.check),'files')
