"""The pack flow. One job: say where a subject stands and run its next scripted step — the glue, nothing else.

  python tools/packflow.py <S>               status: every stage, its gate, the next command
  python tools/packflow.py <S> run <stage>   run a scripted stage: pair | cut | build
  python tools/packflow.py <S> approve       the proposed catalogue becomes the catalogue (after a person read it)
  python tools/packflow.py <S> export        award codes -> tools/marktags_<S>.json, parttags_<S>.txt, tags_<S>.txt

Stages (each is its own tool; AI steps are fixed jobs in skills/wtf-subject-pack/jobs, run by flowjobs.py):
  1 pair     resource judgement: every exam with its own key, same questions, same marks      tools/pairs.py
  2 cut      PDF segmentation + section totals + mark points (awards)        segment.py, audit_totals.py, awards.py
             └ job split: parts whose key the parser could not divide
  3 label    job label: what every award assesses (skill, operation, knowledge), bottom-up
  4 atomise  job atomise → proposed catalogue (patterns + knowledge atoms) → approve → job assign → job review
             → export: award codes; part and question tags are derived from them
  5 build    the subject's rows in a scratch database + statistics (frequency, marks, co-occurrence)
  6 notes    job notes (English first) → job translate (Chinese) → render PDFs
Nothing here writes wace.db, generated.db or the user's config.
"""
import json, os, re, shutil, subprocess, sys
from datetime import datetime

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import flowjobs as fj  # noqa: E402

PY = sys.executable


def sh(*args):
    print("$", " ".join(args), flush=True)
    return subprocess.run([PY, *args], cwd=ROOT).returncode == 0


def covered(subj, name):
    """Share of awards that have an entry in flow/<name>.json."""
    done, ids = fj.load(fj.flow(subj, name + ".json"), {}), [a["id"] for _, _, a in fj.awards(subj)]
    return sum(i in done for i in ids), len(ids)


def stages(subj):
    """[(number, name, passed, detail, next command)] — read from the files each stage leaves; no state of its own."""
    f, out = lambda *p: fj.flow(subj, *p), []
    pairs = fj.load(f("pairs.json"))
    out.append(("1", "pair", bool(pairs and pairs["ok"]),
                f"{sum(p['ok'] for p in pairs['pairs'])}/{len(pairs['pairs'])} exams paired" if pairs else "not run",
                f"packflow.py {subj} run pair"))
    aw = fj.load(f("awards.json"))
    parts = [p for q in aw or [] for p in q["parts"]]
    split = [p for p in parts if p["status"] == "split"]
    out.append(("2", "cut", bool(aw) and not split,
                f"{len(aw)} questions, {len(parts)} parts, {len(split)} parts need the split job" if aw else "not run",
                f"packflow.py {subj} run cut" if not aw else f"flowjobs.py tasks {subj} split"))
    n, total = covered(subj, "labels")
    out.append(("3", "label", bool(total) and n == total, f"{n}/{total} awards labelled", f"flowjobs.py tasks {subj} label"))
    cat, proposed = fj.catalogue(subj) or {}, fj.catalogue(subj, proposed=True)
    approved = cat.get("catalogue_status") == "approved" and cat.get("schema_version") == 2
    n, total = covered(subj, "assign")
    review = fj.load(f("review.json"))
    rate = review["agree"] / max(1, review["sample"]) if review else 0
    exported = os.path.isfile(os.path.join(ROOT, "tools", f"marktags_{subj}.json"))
    if not approved:
        detail, nxt = ("proposed catalogue waiting for approval", f"packflow.py {subj} approve") if proposed else \
            ("no catalogue from the awards yet", f"flowjobs.py tasks {subj} atomise")
    elif n < total:
        detail, nxt = f"catalogue approved; {n}/{total} awards assigned", f"flowjobs.py tasks {subj} assign"
    elif rate < 0.9:
        detail = f"assigned; review agreement {rate:.0%} (needs ≥90%)" if review else "assigned; not reviewed"
        nxt = f"flowjobs.py tasks {subj} review"
    else:
        detail, nxt = f"reviewed {rate:.0%}; " + ("exported" if exported else "not exported"), f"packflow.py {subj} export"
    out.append(("4", "atomise", approved and n == total and rate >= 0.9 and exported, detail, nxt))
    stats = fj.load(f("stats.json"))
    out.append(("5", "build", bool(stats) and not stats.get("problems"),
                f"{len(stats.get('problems', []))} build problems, {len(stats.get('patterns', {}))} patterns with statistics"
                if stats else "not run", f"packflow.py {subj} run build"))
    files = list(fj.topics(subj).values())
    en = sum(os.path.isfile(os.path.join(ROOT, subj, "methods_en", fn + "_Methods.md")) for fn, _, _ in files)
    zh = sum(os.path.isfile(os.path.join(ROOT, subj, "methods", fn + "_解题思路.md")) for fn, _, _ in files)
    out.append(("6", "notes", en == zh == len(files), f"English {en}/{len(files)}, Chinese {zh}/{len(files)}",
                f"flowjobs.py tasks {subj} notes" if en < len(files) else f"flowjobs.py tasks {subj} translate"))
    return out


def status(subj):
    print(f"{subj} pack flow")
    rows = stages(subj)
    for num, name, ok, detail, _ in rows:
        print(f"  {'✓' if ok else '·'} {num} {name:8} {detail}")
    todo = next((r for r in rows if not r[2]), None)
    print("next:", f"python tools/{todo[4]}" if todo else "done — pack it: python tools/pack.py export " + subj)


def run(subj, stage):
    if stage == "pair":
        return sh("tools/pairs.py", subj)
    if stage == "cut":
        return sh("tools/segment.py", subj) and sh("tools/audit_totals.py", subj) and sh("tools/awards.py", subj)
    if stage == "build":
        return build(subj)
    raise SystemExit(f"{stage} is not a scripted stage: its work is an AI job (flowjobs.py)")


def approve(subj):
    src = os.path.join(ROOT, "tools", f"catalogue_{subj}.proposed.json")
    dst = os.path.join(ROOT, "tools", f"catalogue_{subj}.json")
    cat = fj.load(src)
    if not cat:
        raise SystemExit("no proposed catalogue: run the atomise job first")
    if os.path.isfile(dst):
        shutil.copy(dst, dst + f".{datetime.now():%Y%m%d_%H%M%S}.bak")
    cat["catalogue_status"] = "approved"
    cat["approved"] = datetime.now().strftime("%Y-%m-%d")
    fj.save(dst, cat)
    os.remove(src)
    print("approved:", os.path.relpath(dst, ROOT), len(cat["patterns"]), "patterns", len(cat["knowledge"]), "atoms")


def export(subj):
    """Award codes are the source; part tags = the patterns of a part's awards (most marks first), question topics =
    the topics of its patterns. Writes the three files the build and the pack read; the old ones are kept as .bak."""
    assigned = fj.load(fj.flow(subj, "assign.json"), {})
    marktags = dict(schema=1, subject=subj, awards={})
    parts, papers = {}, {}
    for q, p, a in fj.awards(subj):
        got = assigned.get(a["id"])
        if not got:
            raise SystemExit(f"{a['id']} has no assignment: finish the assign job first")
        marktags["awards"][a["id"]] = dict(marks=a["marks"], patterns=got["patterns"], knowledge=got["knowledge"],
                                           confidence=got["confidence"])
        weight = parts.setdefault((q["id"], p["label"]), {})
        for code in got["patterns"]:
            weight[code] = weight.get(code, 0) + a["marks"]
    tools = os.path.join(ROOT, "tools")
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    for name in (f"marktags_{subj}.json", f"parttags_{subj}.txt", f"tags_{subj}.txt"):
        if os.path.isfile(os.path.join(tools, name)):
            shutil.copy(os.path.join(tools, name), os.path.join(tools, f"{name}.{stamp}.bak"))
    fj.save(os.path.join(tools, f"marktags_{subj}.json"), marktags)
    lines, by_q = [f"# {subj} part tags, derived from award codes (tools/packflow.py export); edit the awards, not this"], {}
    for (qid, label), weight in parts.items():
        by_q.setdefault(qid, []).append((label, sorted(weight, key=lambda c: (-weight[c], c))))
    for qid, plist in by_q.items():
        ys, q = qid.split("-")
        lines.append(f"{ys} {q} " + " ".join(f"{label or '-'}={'+'.join(codes)}" for label, codes in plist))
        topics = []
        for _, codes in plist:
            topics += [re.match(r"[A-Z]+", c).group(0) for c in codes]
        papers.setdefault(ys, []).append(f"{q}:{','.join(dict.fromkeys(topics))}")
    fj.write(os.path.join(tools, f"parttags_{subj}.txt"), "\n".join(lines) + "\n")
    letters = "/".join(s["letter"] for s in fj.subjects.sections(subj))
    tags = [f"# year section({letters}) Q: topics (first = primary), derived from award codes",
            "# " + " ".join(f"{c}={en}" for c, (_, _, en) in fj.topics(subj).items())]
    tags += [f"{ys} " + " ".join(items) for ys, items in papers.items()]
    fj.write(os.path.join(tools, f"tags_{subj}.txt"), "\n".join(tags) + "\n")
    print(f"exported {len(marktags['awards'])} awards, {len(parts)} parts, {len(by_q)} questions (old files: *.{stamp}.bak)")


def build(subj):
    """The subject alone into evidence/<s>/flow/check.db (never the user's wace.db), then its statistics."""
    import sqlite3
    from build_db import build as build_db
    path = fj.flow(subj, "check.db")
    db, problems = build_db(path, [subj])
    db.close()
    db = sqlite3.connect(path)
    co = {}
    for qid, pats in db.execute("SELECT qid, GROUP_CONCAT(DISTINCT pattern) FROM part_patterns GROUP BY qid"):
        pats = sorted(set(pats.split(",")))
        for i, a in enumerate(pats):
            for b in pats[i + 1:]:
                co[f"{a}+{b}"] = co.get(f"{a}+{b}", 0) + 1
    stats = dict(subject=subj, problems=problems, patterns=fj.pattern_stats(subj),
                 knowledge=knowledge_stats(subj), together=dict(sorted(co.items(), key=lambda x: -x[1])[:60]),
                 points_ok=db.execute("SELECT SUM(points_ok), COUNT(*) FROM questions").fetchone())
    db.close()
    fj.save(fj.flow(subj, "stats.json"), stats)
    print(f"{subj}: {len(problems)} build problems; points_ok {stats['points_ok'][0]}/{stats['points_ok'][1]}; "
          f"statistics for {len(stats['patterns'])} patterns, {len(stats['knowledge'])} knowledge atoms")
    print("\n".join(problems[:30]))
    return not problems


def knowledge_stats(subj):
    """Per knowledge atom: awards and the marks that depend on it (overlapping: one award can need two atoms)."""
    out, assigned = {}, fj.load(fj.flow(subj, "assign.json"), {})
    for _, _, a in fj.awards(subj):
        for k in assigned.get(a["id"], {}).get("knowledge", []):
            s = out.setdefault(k, dict(awards=0, marks=0))
            s["awards"] += 1
            s["marks"] += a["marks"]
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        raise SystemExit(__doc__)
    S = args[0].upper()
    if len(args) == 1:
        status(S)
    elif args[1] == "run":
        sys.exit(0 if run(S, args[2]) else 1)
    elif args[1] == "approve":
        approve(S)
    elif args[1] == "export":
        export(S)
    else:
        raise SystemExit(__doc__)
