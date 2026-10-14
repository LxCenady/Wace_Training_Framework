"""Run required isolated regression checks and write a local, reproducible result manifest."""
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid
from verify_compiler_regression import protected

ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'evidence/runtime/compiler-regression'/('final-'+uuid.uuid4().hex[:8]);folder.mkdir(parents=True,exist_ok=True)
temp=folder/'temp';temp.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONUTF8='1',TEMP=str(temp),TMP=str(temp))
before=protected();results=[]
tests=[('providers',['tests/test_providers.py']),('gui',['tests/smoke_gui.py',str(folder/'gui')]),
       ('en',['tests/smoke_en.py',str(folder/'en')]),('setup',['tests/smoke_setup.py',str(folder/'setup'),str(ROOT)]),
       ('external',['tests/test_external.py']),('external_en',['tests/smoke_external.py',str(folder/'external'),'en']),
       ('compiler',['tests/test_compiler.py']),('compiler_ui',['tests/smoke_compiler.py'])]
for name,args in tests:
    (folder/name).mkdir(exist_ok=True)
    with (folder/(name+'.log')).open('w',encoding='utf-8') as log:
        completed=subprocess.run([sys.executable,*args],cwd=ROOT/'app',env=env,stdout=log,stderr=subprocess.STDOUT)
    results.append(dict(test=name,exit_code=completed.returncode));print(name,completed.returncode,flush=True)
after=protected();changed=[p for p in before if before[p]!=after.get(p)]
report=dict(tests=results,protected_changed=changed)
(folder/'results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print('Protected files changed:',len(changed),flush=True)
if changed or any(r['exit_code'] for r in results):raise SystemExit(1)
