"""Compare summed question marks with the section total printed in each paper."""
import json, re, sys, os, collections, pymupdf
ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = re.compile(r"Section (One|Two)\s*:?\s*Calculator[\s-]*(free|assumed).{0,40}?\((\d+)\s*Marks\)", re.I | re.S)
bad = 0
for s in sys.argv[1:]:
    qs = json.load(open(f"{ROOT}/{s}/questions.json", encoding="utf-8"))
    by = collections.defaultdict(list)
    for q in qs: by[q["exam"]].append(q)
    for ex, v in sorted(by.items()):
        doc = pymupdf.open(f"{ROOT}/{ex}")
        txt = " ".join(doc[i].get_text() for i in range(min(6, doc.page_count)))
        sec = v[0]["section"].replace("Calc", "").lower()
        tots = [int(m.group(3)) for m in PAT.finditer(txt) if m.group(2).lower() == sec]
        got = sum(q["marks"] for q in v)
        ok = got in tots
        bad += not ok
        print("OK " if ok else "BAD", ex.split("/")[-1], "sum", got, "printed", sorted(set(tots)))
print("mismatches:", bad)
