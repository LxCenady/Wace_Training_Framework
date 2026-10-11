"""Locate every question in each exam + marking key; write questions.json.

One job: PDFs -> question regions (page, y0, y1), marks, and plain stem text.
"""
import json, re, sys, glob, os
import pymupdf
import fetch
import subjects

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


def scan(path, shared=False):
    """Return ordered list of (q, page, y, marks) heads and the stop point (page, y)."""
    doc = pymupdf.open(path)
    heads, seen, stop = [], set(), (doc.page_count - 1, None)
    bands = []
    for i, pg in enumerate(doc):
        ls = lines(pg)
        bands.append(band(pg, ls))
        if shared and heads and any(t.startswith('Published by the School Curriculum') for _, t in ls) \
                and any(t == 'Copyright' for _, t in ls) and not any(HEAD.match(t) for _, t in ls):
            return doc, heads, (i - 1, None), bands
        for b, t in sorted(ls, key=lambda x: x[0][1]):
            # Shared papers repeat supplementary-page instructions at each
            # section entrance. Only the actual spare-page heading ends a paper.
            if shared and re.match(r"Supplementary pages?\b", t, re.I) and not re.fullmatch(
                    r"Supplementary page", t, re.I):
                continue
            if heads and STOP.match(t) and b[1] > bands[i][0] + 5 and not HEAD.match(t):
                stop = (i, b[1]) if b[1] > bands[i][0] + 20 else (i - 1, None)
                return doc, heads, stop, bands
            if heads and STOP.match(t):
                stop = (i - 1, None)
                return doc, heads, stop, bands
            m = HEAD.match(t)
            if m and not m.group(2):
                if shared and not re.fullmatch(r"Question\s+\d+\s*(?:\(\d+\s*marks?\))?", t, re.I):
                    continue  # e.g. MC stimulus: 'Question 24 refers to ...'
                q = int(m.group(1))
                if q in seen or (heads and q != heads[-1][0] + 1):
                    continue
                mk = MARKS.search(t)
                if not mk:
                    # Mixed fonts can give the heading a taller bounding box. Match
                    # the same visual row, rather than requiring identical top edges.
                    near = [tt for bb, tt in ls if bb[0] >= b[2]
                            and min(bb[3], b[3]) > max(bb[1], b[1]) and MARKS.search(tt)]
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
    profile = subjects.info(subj)
    shared = profile.get('paper_layout') == 'shared'
    section_blocks = []
    listed = {s[0] for s in fetch.sources(ROOT, [subj])}  # the bank holds only papers sources.tsv lists
    pattern = '*_Exam.pdf' if shared else '*_Exam_*.pdf'
    for ex in sorted(glob.glob(f"{ROOT}/{subj}/papers/{pattern}")):
        name = os.path.basename(ex)
        year, sec = name.split("_")[0], None if shared else name.split("_")[-1][:-4]
        key = ex.replace("_Exam", "_MarkingKey")
        if f"{subj}/papers/{name}" not in listed:  # e.g. MAA 2019: no usable marking key exists, so not listed
            continue
        if not os.path.exists(key):  # partial import: questions without their key are left out until it arrives
            print("skip (marking key not imported yet):", name)
            continue
        edoc, eh, es, eb = scan(ex, shared=shared)
        sections = []
        if shared:
            seen = set()
            for page, pg in enumerate(edoc):
                for box, text in sorted(lines(pg), key=lambda item: item[0][1]):
                    for section in profile['sections']:
                        if section['code'] not in seen and any(text.lower().startswith(h.lower())
                                for h in section.get('headings', [])):
                            sections.append((section['code'], page, box[1], None))
                            seen.add(section['code'])
            if seen != set(subjects.section_codes(subj)):
                raise ValueError(f'Section headings missing: {name}: {seen}')
            blocks = regions(sections, es, eb, edoc.page_count)
            section_blocks.append(dict(exam=os.path.relpath(ex, ROOT).replace(os.sep, '/'),
                                       sections=blocks))
        er = regions(eh, es, eb, edoc.page_count)
        kdoc, kh, ks, kb = scan(key, shared=shared)
        kr = regions(kh, ks, kb, kdoc.page_count)
        for q, p, y, mk in eh:
            if shared:
                found = [code for code, page, top, _ in sections if (page, top) <= (p, y)]
                if not found:
                    raise ValueError(f'Question outside sections: {name} Q{q}')
                sec = found[-1]
                section = next(s for s in profile['sections'] if s['code'] == sec)
                if section.get('question_mode') == 'section-only':
                    continue
                # Do not append the next section's header/instructions to the
                # final question of this section.
                later = [(page, top) for code, page, top, _ in sections if (page, top) > (p, y)]
                if later:
                    end_page, end_top = later[0]
                    er[q] = [[page, top, min(bottom, round(end_top - 3, 1)) if page == end_page else bottom]
                             for page, top, bottom in er[q] if page <= end_page]
                    er[q] = [r for r in er[q] if r[2] - r[1] > 12]
            res.append(dict(subject=subj, year=year, section=sec, q=q, marks=mk,
                            exam=os.path.relpath(ex, ROOT).replace("\\", "/"), exam_regions=er[q],
                            key=os.path.relpath(key, ROOT).replace("\\", "/"), key_regions=kr.get(q, []),
                            text=text_of(edoc, er[q])))
    with open(f"{ROOT}/{subj}/questions.json", 'w', encoding='utf-8') as file:
        json.dump(res, file, ensure_ascii=False, indent=1)
    if shared:
        with open(f"{ROOT}/{subj}/sections.json", 'w', encoding='utf-8') as file:
            json.dump(section_blocks, file, ensure_ascii=False, indent=1)
    print(subj, len(res), "questions")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        main(s)
