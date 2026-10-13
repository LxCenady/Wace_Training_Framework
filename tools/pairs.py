"""Stage 1 of the pack flow: resource judgement. One job: is every exam paired with the marking key that belongs to it?

  python tools/pairs.py CHE            -> table on stdout, evidence/<s>/flow/pairs.json; exit 1 if any pair fails

For every exam the manifest lists, its key must be listed and on disk, both must be recognised from their own
covers as that subject / year / section (paperid), and the key must mark the same questions with the same marks:
every "Question N (n marks)" heading of the exam appears in the key with the same n, and nothing extra.
Every year the pack promises (pack.json papers.years) needs a passing pair; a year left out must be written down
in papers.excluded with the reason. A real discrepancy in the official documents (the exam and its key print
different marks) is found here, checked by a person against the PDFs and written down in papers.acknowledged
{"<year>": "what differs and which side the bank uses"}: the pair then passes with the note. Read-only apart
from the report file.
"""
import json, os, sys

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import fetch, paperid, segment, subjects  # noqa: E402


def heads(path, shared, first_question=None):
    """{question number: printed marks or None} from the "Question N" headings of one PDF."""
    doc, found, _, _ = segment.scan(path, shared=shared, first_question=first_question)
    doc.close()
    return {q: marks for q, _, _, marks in found}


def judge(subj, rel_exam, listed, shared):
    """One exam -> dict(exam, key, year, ok, problems, questions)."""
    rel_key = rel_exam.replace("_Exam", "_MarkingKey")
    year = os.path.basename(rel_exam).split("_")[0]
    out = dict(exam=rel_exam, key=rel_key, year=year, ok=False, problems=[], questions=0)
    bad = out["problems"]
    if rel_key not in listed:
        bad.append("marking key not in the manifest")
    for rel in (rel_exam, rel_key):
        path = os.path.join(ROOT, rel)
        if not os.path.isfile(path):
            bad.append(f"not on disk: {rel}")
        elif paperid.identify(path) != rel:
            bad.append(f"cover says {paperid.identify(path)}, manifest says {rel}")
    if bad:
        return out
    exam = heads(os.path.join(ROOT, rel_exam), shared)
    key = heads(os.path.join(ROOT, rel_key), shared, min(exam) if shared and exam else None)
    out["questions"] = len(exam)
    if not exam:
        bad.append("no 'Question N' headings found in the exam")
    if missing := sorted(set(exam) - set(key)):
        bad.append(f"questions with no key: {missing}")
    if extra := sorted(set(key) - set(exam)):
        bad.append(f"key questions not in the exam: {extra}")
    if differ := [f"Q{q} exam {exam[q]} key {key[q]}" for q in sorted(set(exam) & set(key))
                  if exam[q] and key[q] and exam[q] != key[q]]:
        bad.append("marks differ: " + ", ".join(differ))
    if unmarked := sorted(q for q in exam if not exam[q]):
        bad.append(f"no printed marks in the exam for: {unmarked}")
    out["ok"] = not bad
    return out


def run(subj):
    profile = subjects.info(subj)
    shared = profile.get("paper_layout") == "shared"
    listed = {e["path"] for e in fetch.entries(ROOT, [subj])}
    exams = sorted(p for p in listed if os.path.basename(p).split("_")[2].startswith("Exam")
                   and "ExamReport" not in p)
    papers = profile.get("papers", {})
    pairs = []
    for rel in exams:
        year = os.path.basename(rel).split("_")[0]
        if year in papers.get("excluded", {}):
            pairs.append(dict(exam=rel, year=year, ok=True, excluded=papers["excluded"][year], problems=[], questions=0))
            continue
        p = judge(subj, rel, listed, shared)
        if p["problems"] and year in papers.get("acknowledged", {}):
            p.update(ok=True, acknowledged=papers["acknowledged"][year])
        pairs.append(p)
    passed = {p["year"] for p in pairs if p["ok"] and not p.get("excluded")}
    years = [str(y) for y in papers.get("years", [])]
    gaps = [y for y in years if y not in passed and y not in papers.get("excluded", {})]
    report = dict(subject=subj, pairs=pairs, years_without_pair=gaps,
                  ok=all(p["ok"] for p in pairs) and not gaps and bool(pairs))
    out_dir = os.path.join(ROOT, "evidence", subj.lower(), "flow")
    os.makedirs(out_dir, exist_ok=True)
    json.dump(report, open(os.path.join(out_dir, "pairs.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return report


if __name__ == "__main__":
    code = 0
    for s in sys.argv[1:]:
        r = run(s.upper())
        for p in r["pairs"]:
            state = "skip" if p.get("excluded") else "ack " if p.get("acknowledged") else "ok  " if p["ok"] else "FAIL"
            note = p.get("excluded") or "; ".join(p["problems"]) + (f"  [acknowledged: {p['acknowledged']}]"
                                                                   if p.get("acknowledged") else "")
            print(f"{state} {os.path.basename(p['exam']):38} {p['questions']:3} questions  {note}")
        if r["years_without_pair"]:
            print("years promised by pack.json with no passing pair and no exclusion:", r["years_without_pair"])
        print(s, "PASS" if r["ok"] else "FAIL")
        code |= not r["ok"]
    sys.exit(code)
