"""Question-only topic banks (no marking keys), newest year first.

One job: questions.json + tags -> <subj>/题库/NN_Topic_题库.pdf
"""
import json, os, sys
import pymupdf
from build_docs import TOPICS, read_tags, Layout, ROOT, A4, MARGIN, CJK


def build(subj):
    qs = [q for q in json.load(open(f"{ROOT}/{subj}/questions.json", encoding="utf-8")) if q["year"] != "2016Sample"]
    tags = read_tags(subj)
    outdir = f"{ROOT}/{subj}/题库"
    os.makedirs(outdir, exist_ok=True)
    cache = {}
    src = lambda p: cache.setdefault(p, pymupdf.open(f"{ROOT}/{p}"))
    for code, (fname, zh, en) in TOPICS[subj].items():
        sel = [q for q in qs if code in tags[(q["year"], q["section"], q["q"])]]
        sel.sort(key=lambda q: (-int(q["year"]), q["section"] != "CalcFree", q["q"]))
        out = pymupdf.open()
        lay = Layout(out)
        lay.new_page()
        lay.page.insert_text((MARGIN, 80), f"WACE {subj} ATAR", fontsize=20, fontname="hebo")
        lay.page.insert_text((MARGIN, 108), f"{zh} · 题库", fontsize=18, fontname=CJK)
        lay.page.insert_text((MARGIN, 130), f"{en} - questions only, newest first", fontsize=12, fontname="helv")
        lay.page.insert_text((MARGIN, 150), f"{len(sel)} questions - {sum(q['marks'] for q in sel)} marks - 2025 to 2016 - source: SCSA",
                             fontsize=10, fontname="helv")
        toc = []
        for q in sel:
            sec = "Calculator-free" if q["section"] == "CalcFree" else "Calculator-assumed"
            head = f"{q['year']} {sec} - Question {q['q']} - {q['marks']} marks"
            lay.new_page()
            lay.bar(head, (0.12, 0.22, 0.45))
            toc.append((head, out.page_count))
            for pno, y0, y1 in q["exam_regions"]:
                lay.region(src(q["exam"]), pno, y0, y1)
        y = 170
        for head, p in toc:
            if y > A4.height - 40:
                out[0].insert_text((MARGIN, y), "... see bookmarks for the full list", fontsize=7.5, fontname="cour")
                break
            out[0].insert_text((MARGIN, y), f"p.{p:<4} {head}", fontsize=7.5, fontname="cour")
            y += 10.5
        out.set_toc([[1, h, p] for h, p in toc])
        path = f"{outdir}/{fname}_题库.pdf"
        out.subset_fonts()
        out.save(path, garbage=4, deflate=True, deflate_images=True, deflate_fonts=True, clean=True)
        print(subj, fname, len(sel), "questions", out.page_count, "pages", round(os.path.getsize(path) / 1e6, 1), "MB")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        build(s)
