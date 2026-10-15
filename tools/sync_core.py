"""The shared core. One job: copy WTF's core files to a product built on it (WTF Studio) and verify the copy.

WTF is the only source of the core: every tools/ module, the Compiler core, the kernel, main.py, plat.py, the English
dictionary, every plugin that is not a Tk view, the Tk views the setup wizard needs, the shared tests and the Compiler
documentation. A product keeps its own plugins.txt, setup.txt, edition.json, web front end and its own plugins; it never
edits a core file (improve it here, then sync). Files are compared with LF line endings, as Git stores them.

  python tools/sync_core.py E:\\WTF_Studio            copy, write tools/core_manifest.json there, report removals
  python tools/sync_core.py E:\\WTF_Studio --check    verify only (exit 1 on any difference)
"""
import argparse, fnmatch, hashlib, json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ["app/kernel.py", "app/main.py", "app/plat.py", "app/i18n/en.json", "app/plugins/__init__.py",
        "tools/*.py", "tools/wtf_compiler/*.py", "app/plugins/*.py",
        "app/tests/__init__.py", "app/tests/safe_runtime.py", "app/tests/test_*.py", "app/tests/smoke_setup.py",
        "app/tests/smoke_compiler.py", "docs/compiler.md", "skills/wtf-compiler/SKILL.md"]
TK_SHARED = {"ui_shell", "ui_subjects", "ui_setup", "ui_compiler", "ui_hub"}  # the Tk wizard, Compiler and Hub windows Studio opens
NOT_CORE = ["app/plugins/ui_*.py", "app/tests/smoke_gui.py", "app/tests/smoke_en.py", "app/tests/smoke_che.py",
            "app/tests/smoke_external.py", "tools/sync_core.py", "tools/sync_compiler.py"]


def core_files():
    tracked = subprocess.run(["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True,
                             encoding="utf-8").stdout.splitlines()
    keep = []
    for f in tracked:
        if not any(fnmatch.fnmatchcase(f, g) and f.count("/") == g.count("/") for g in CORE):
            continue
        tk = Path(f).stem in TK_SHARED and f.startswith("app/plugins/")
        if not tk and any(fnmatch.fnmatchcase(f, g) for g in NOT_CORE):
            continue
        keep.append(f)
    return sorted(keep)


def lf(path):
    return path.read_bytes().replace(b"\r\n", b"\n")


def sync(dest, check=False):
    dest = Path(dest).resolve()
    files = core_files()
    manifest = {f: hashlib.sha256(lf(ROOT / f)).hexdigest() for f in files}
    bad = []
    for f in files:
        target = dest / f
        if check:
            if not target.exists() or hashlib.sha256(lf(target)).hexdigest() != manifest[f]:
                bad.append(f)
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(lf(ROOT / f))
    path = dest / "tools" / "core_manifest.json"
    if check:
        if not path.exists() or json.loads(path.read_text(encoding="utf-8")) != manifest:
            bad.append("tools/core_manifest.json")
    else:
        path.write_text(json.dumps(manifest, indent=1) + "\n", encoding="utf-8", newline="\n")
    # Tk views and Tk smoke tests in the product that are not core: WTF's interface, never loaded there
    stale = sorted(str(p.relative_to(dest)).replace("\\", "/") for g in NOT_CORE[:5] for p in dest.glob(g)
                   if str(p.relative_to(dest)).replace("\\", "/") not in manifest)
    return files, bad, stale


if __name__ == "__main__":
    a = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    a.add_argument("product")
    a.add_argument("--check", action="store_true")
    args = a.parse_args()
    files, bad, stale = sync(args.product, args.check)
    for f in bad:
        print("DIFFERS", f)
    for f in stale:
        print("NOT CORE (WTF's Tk interface; remove from the product)", f)
    print(("Verified" if args.check else "Synced"), len(files), "core files;", len(bad), "differ;", len(stale), "stale")
    sys.exit(1 if bad else 0)
