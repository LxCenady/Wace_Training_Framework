"""Locate every question in each exam + marking key; write questions.json.

One job: PDFs -> question regions (page, y0, y1), marks, and plain stem text.
"""
import json, re, sys, glob, os
import pymupdf

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = re.compile(r"^Question\s+(\d+)\s*(\(?continued\)?)?", re.I)
MARKS = re.compile(r"\((\d+)\s*marks?\)", re.I)
STOP = re.compile(r"End of questions|Supplementary page|Spare grid|Additional working space|"
                  r"ACKNOWLEDGEMENTS|This document\s*[–-]\s*apart from", re.I)
FOOT = re.compile(r"See next page|End of questions", re.I)


def lines(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t:
                out.append((l["bbox"], t))
    return out


def band(page, ls):
    """Content band (top, bottom) excluding running header and footer."""
    h = page.rect.height
    top = max([b[3] for b, t in ls if b[3] < 56] + [30]) + 2
    foot = [b[1] for b, t in ls if b[1] > h - 70 and (FOOT.search(t) or re.fullmatch(r"\d+", t))]
    bot = min(foot + [h - 30]) - 2
    return top, bot


def scan(path):
    """Return ordered list of (q, page, y, marks) heads and the stop point (page, y)."""
    doc = pymupdf.open(path)
    heads, seen, stop = [], set(), (doc.page_count - 1, None)
    bands = []
    for i, pg in enumerate(doc):
        ls = lines(pg)
        bands.append(band(pg, ls))
        for b, t in sorted(ls, key=lambda x: x[0][1]):
            if heads and STOP.match(t) and b[1] > bands[i][0] + 5 and not HEAD.match(t):
                stop = (i, b[1]) if b[1] > bands[i][0] + 20 else (i - 1, None)
                return doc, heads, stop, bands
            if heads and STOP.match(t):
                stop = (i - 1, None)
                return doc, heads, stop, bands
            m = HEAD.match(t)
            if m and not m.group(2):
                q = int(m.group(1))
                if q in seen or (heads and q != heads[-1][0] + 1):
                    continue
                mk = MARKS.search(t)
                if not mk:
                    near = [tt for bb, tt in ls if abs(bb[1] - b[1]) < 6 and MARKS.search(tt)]
                    mk = MARKS.search(near[0]) if near else None
                heads.append((q, i, b[1], int(mk.group(1)) if mk else None))
                seen.add(q)
    return doc, heads, stop, bands


def regions(heads, stop, bands, npages):
    out = {}
    for k, (q, p, y, _) in enumerate(heads):
        if k + 1 < len(heads):
            ep, ey = heads[k + 1][1], heads[k + 1][2]
        else:
            ep, ey = stop
        regs = []
        for pg in range(p, min(ep, npages - 1) + 1):
            top, bot = bands[pg]
            y0 = y - 3 if pg == p else top
            y1 = (ey - 3) if (pg == ep and ey is not None) else bot
            if y1 - y0 > 12:
                regs.append([pg, round(y0, 1), round(y1, 1)])
        out[q] = regs
    return out


def text_of(doc, regs):
    parts = []
    for pg, y0, y1 in regs:
        r = pymupdf.Rect(0, y0, 560, y1)
        parts.append(doc[pg].get_text("text", clip=r))
    t = "\n".join(parts)
    t = re.sub(r"DO NOT WRITE IN THIS AREA AS IT WILL BE CUT OFF", "", t)
    return re.sub(r"[ \t  ]+", " ", re.sub(r"\n\s*\n+", "\n", t)).strip()


def main(subj):
    res = []
    for ex in sorted(glob.glob(f"{ROOT}/{subj}/papers/*_Exam_*.pdf")):
        name = os.path.basename(ex)
        year, sec = name.split("_")[0], name.split("_")[-1][:-4]
        key = ex.replace("_Exam_", "_MarkingKey_")
        if not os.path.exists(key):  # partial import: questions without their key are left out until it arrives
            print("skip (marking key not imported yet):", name)
            continue
        edoc, eh, es, eb = scan(ex)
        er = regions(eh, es, eb, edoc.page_count)
        kdoc, kh, ks, kb = scan(key)
        kr = regions(kh, ks, kb, kdoc.page_count)
        for q, p, y, mk in eh:
            res.append(dict(subject=subj, year=year, section=sec, q=q, marks=mk,
                            exam=os.path.relpath(ex, ROOT).replace("\\", "/"), exam_regions=er[q],
                            key=os.path.relpath(key, ROOT).replace("\\", "/"), key_regions=kr.get(q, []),
                            text=text_of(edoc, er[q])))
    json.dump(res, open(f"{ROOT}/{subj}/questions.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(subj, len(res), "questions")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        main(s)
