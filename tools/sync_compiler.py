"""Superseded by tools/sync_core.py: the Compiler is part of the shared core. Kept so older instructions still work.

  python tools/sync_compiler.py E:\\WTF_Studio [--check]   ==   python tools/sync_core.py E:\\WTF_Studio [--check]
"""
import runpy, sys
from pathlib import Path

if __name__ == "__main__":
    sys.argv[0] = str(Path(__file__).with_name("sync_core.py"))
    runpy.run_path(sys.argv[0], run_name="__main__")
