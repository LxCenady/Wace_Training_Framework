"""Per-topic evidence pack: stem + marking-key 'Specific behaviours' for every question,
plus all examination-report text. Feeds the hand-written solving-method notes.

One job: questions.json + tags + PDFs -> evidence/<subj>_<topic>.txt and <subj>_reports.txt
"""
import json, os, re, sys, glob
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build_docs import TOPICS, read_tags  # noqa: E402

TICK = re.compile(r"^[-✓✔•\-•]\s*")


def key_text(doc, regs):
    return "\n".join(doc[p].get_text("text", clip=pymupdf.Rect(20, y0, 575, y1)) for p, y0, y1 in regs)


def behaviours(text):
    """Return list of (part, behaviour) from a marking-key text block."""
    out, part, on = [], "", False
    for raw in text.splitlines():
        t = raw.strip()
        if not t:
            continue
        m = re.match(r"^\(([a-z]|i{1,3}|iv|v)\)$", t)
        if m:
            part = m.group(1) if len(m.group(1)) == 1 and m.group(1) not in "iv" or not part else part + m.group(1)
            on = False
            continue
        if re.match(r"Specific behaviou?rs", t, re.I):
            on = True
            continue
        if re.match(r"^Solution", t) or re.match(r"^Question \d+", t):
            on = False
            continue
        if on and (TICK.match(t) or len(t) > 12):
            b = TICK.sub("", t)
            if out and on and not TICK.match(t) and out[-1][0] == part and b[:1].islower():
                out[-1] = (part, out[-1][1] + " " + b)  # wrapped line
            else:
                out.append((part, b))
    return out


def main(subj):
    tags = read_tags(subj)
    qs = [q for q in json.load(open(f"{ROOT}/{subj}/questions.json", encoding="utf-8")) if q["year"] != "2016Sample"]
    os.makedirs(f"{ROOT}/evidence", exist_ok=True)
    cache = {}
    doc = lambda p: cache.setdefault(p, pymupdf.open(f"{ROOT}/{p}"))
    for code, (fname, zh, en) in TOPICS[subj].items():
        lines = [f"# {subj} {fname} {zh}"]
        for q in sorted(qs, key=lambda q: (q["year"], q["section"], q["q"])):
            t = tags[(q["year"], q["section"], q["q"])]
            if code not in t:
                continue
            sec = "F" if q["section"] == "CalcFree" else "A"
            stem = re.sub(r"\s+", " ", re.sub(r"DO NOT WRITE IN THIS AREA AS IT WILL BE CUT OFF", "", q["text"]))
            lines.append(f"\n## {q['year']}{sec}-Q{q['q']} [{q['marks']}m] tags={','.join(t)}")
            lines.append("STEM: " + stem[:900])
            for part, b in behaviours(key_text(doc(q["key"]), q["key_regions"])):
                lines.append(f"  ({part}) {b}")
        open(f"{ROOT}/evidence/{subj}_{fname}.txt", "w", encoding="utf-8").write("\n".join(lines))
    rep = []
    for p in sorted(glob.glob(f"{ROOT}/{subj}/papers/*ExamReport.pdf")):
        t = "\n".join(pg.get_text() for pg in pymupdf.open(p))
        t = re.sub(r"[ \t]+", " ", t)
        t = t[t.find("General comments"):] if "General comments" in t else t
        rep.append(f"\n===== {os.path.basename(p)}\n{t}")
    open(f"{ROOT}/evidence/{subj}_reports.txt", "w", encoding="utf-8").write("\n".join(rep))


if __name__ == "__main__":
    for s in sys.argv[1:]:
        main(s)
