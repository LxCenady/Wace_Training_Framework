"""Audit questions.json: marks per paper, key coverage, empty regions."""
import json, sys, os, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for s in sys.argv[1:]:
    qs = json.load(open(f"{ROOT}/{s}/questions.json", encoding="utf-8"))
    by = collections.defaultdict(list)
    for q in qs: by[(q["year"], q["section"])].append(q)
    for k, v in sorted(by.items()):
        tot = sum(q["marks"] or 0 for q in v)
        miss = [q["q"] for q in v if q["marks"] is None]
        nokey = [q["q"] for q in v if not q["key_regions"]]
        pages = sum(len(q["exam_regions"]) for q in v)
        print(s, *k, f"Q{v[0]['q']}-{v[-1]['q']}", "marks", tot, "noMarks", miss or "", "noKey", nokey or "", "examRegions", pages)
