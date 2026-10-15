"""Export subject packs for WTF Hub and prove each one. One job: subjects -> verified .wtfpack files + a report.

For every subject: copy this repository's pack inputs into an isolated export root (with a reference bank, so the
pack checks run against it), export the .wtfpack (tools/pack.py), install it into an empty data root, rebuild the
bank there from the local original PDFs, and compare every table of that subject with the reference bank. A pack is
only written to --out when the rebuild matches row for row. Never touches the owner's data root.

  python tools/export_packs.py --reference <bank.db built from this repo> --out packs MAM MAS MAA CHE PHY ACF
"""
import argparse, json, os, shutil, sqlite3, subprocess, sys, tempfile
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import pack  # noqa: E402

TABLES = {  # table -> how its rows belong to a subject
    "topics": "code LIKE :s || '.%'", "patterns": "code LIKE :s || '.%'", "knowledge": "code LIKE :s || '.%'",
    "pattern_flags": "code LIKE :s || '.%'", "axis_codes": "code LIKE :s || '.%'",
    "questions": "id LIKE :s || '-%'", "parts": "qid LIKE :s || '-%'", "part_patterns": "qid LIKE :s || '-%'",
    "points": "qid LIKE :s || '-%'", "award_tags": "qid LIKE :s || '-%'", "rubrics": "qid LIKE :s || '-%'",
}


def compare(subject, a, b):
    out = {}
    for table, where in TABLES.items():
        rows = [Counter(db.execute(f"SELECT * FROM {table} WHERE {where}", {"s": subject}).fetchall()) for db in (a, b)]
        out[table] = dict(rows=sum(rows[0].values()), differ=sum((rows[0] - rows[1]).values()) + sum((rows[1] - rows[0]).values()))
    return out


def export_one(subject, reference, work):
    lower = subject.lower()
    export = work / "export"
    for folder in ("tools", "app", "skills/wtf-subject-pack", f"skills/wace-{lower}-questions", subject, "cheatsheet"):
        if (ROOT / folder).exists():
            shutil.copytree(ROOT / folder, export / folder,
                            ignore=shutil.ignore_patterns("__pycache__", "*.bak", "*.log", "topics", "题库"))
    shutil.copy2(ROOT / ".gitignore", export / ".gitignore")
    shutil.copy2(reference, export / "bank.db")
    subprocess.run(["git", "init", "-q"], cwd=export, check=True)
    subprocess.run(["git", "add", "-A"], cwd=export, check=True, capture_output=True)
    artifact = pack.export(subject, export, work / "dist")
    profile, contents = pack.inspect(artifact)
    assert profile["quality"] == "ready", profile.get("quality")
    assert all(not any(p in ("papers", "evidence", "题库", "topics") for p in Path(n).parts[:1]) for n in contents), \
        "source material in the pack"
    installed = work / "installed"
    pack.install(artifact, installed)
    subprocess.run(["cmd", "/c", "mklink", "/J", str(installed / subject / "papers"), str(ROOT / subject / "papers")],
                   check=True, capture_output=True)
    env = {**os.environ, "WACE_MATHS_ROOT": str(installed), "PYTHONIOENCODING": "utf-8"}
    subprocess.run([sys.executable, str(ROOT / "tools/build_all.py"), subject], env=env, check=True, capture_output=True)
    a = sqlite3.connect(Path(reference).as_uri() + "?mode=ro", uri=True)
    b = sqlite3.connect((installed / "bank.db").as_uri() + "?mode=ro", uri=True)
    try:
        tables = compare(subject, a, b)
    finally:
        a.close()
        b.close()
    return artifact, profile, tables


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("subjects", nargs="+")
    p.add_argument("--reference", required=True, help="a bank.db built from this repository (tools/build_db.py)")
    p.add_argument("--out", default="packs")
    args = p.parse_args(argv)
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    report = {}
    for subject in args.subjects:
        with tempfile.TemporaryDirectory(prefix=f"wtf-export-{subject}-", dir=ROOT / "evidence" / "runtime") as tmp:
            artifact, profile, tables = export_one(subject, Path(args.reference).resolve(), Path(tmp))
            bad = {t: c for t, c in tables.items() if c["differ"]}
            if not bad:
                shutil.copy2(artifact, out / artifact.name)
            report[subject] = dict(pack=artifact.name, version=profile["version"], requires_wtf=profile.get("requires_wtf"),
                                   ok=not bad, tables=tables)
            print(subject, "READY" if not bad else f"DIFFERENT {bad}", artifact.name, flush=True)
    (out / "export_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0 if all(r["ok"] for r in report.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
