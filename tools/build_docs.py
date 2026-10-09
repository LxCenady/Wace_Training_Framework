"""questions.json + tags_<S>.txt -> per-topic PDF (exam + marking key, vector crops) and Markdown index.

One job: assemble topic documents. No classification logic lives here.
"""
import json, os, re, sys
import pymupdf

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOPICS = {
    "MAM": {
        "D": ("01_Differentiation", "微分及其应用", "Differentiation & applications"),
        "I": ("02_Integration", "积分及其应用", "Integration & applications"),
        "M": ("03_Rectilinear_Motion", "直线运动", "Rectilinear motion (kinematics)"),
        "L": ("04_Exp_Log", "指数与对数函数", "Exponential & logarithmic functions"),
        "DRV": ("05_Discrete_RV", "离散随机变量与二项分布", "Discrete random variables & binomial"),
        "CRV": ("06_Continuous_RV_Normal", "连续随机变量与正态分布", "Continuous random variables & normal"),
        "CI": ("07_Sample_Proportions_CI", "样本比例与置信区间", "Sample proportions & confidence intervals"),
    },
    "MAS": {
        "C": ("01_Complex_Numbers", "复数", "Complex numbers"),
        "F": ("02_Functions_Graphs", "函数与图像", "Functions & sketching graphs"),
        "V": ("03_Vectors_3D", "三维向量与线性方程组", "Vectors in 3D, lines, planes, spheres, linear systems"),
        "VC": ("04_Vector_Calculus", "向量微积分与运动", "Vector calculus & motion"),
        "I": ("05_Integration", "积分技巧与应用", "Integration techniques & applications"),
        "DE": ("06_Rates_DiffEq", "变化率与微分方程", "Rates of change & differential equations"),
        "S": ("07_Statistical_Inference", "统计推断（样本均值）", "Statistical inference (sample means)"),
    },
}
A4 = pymupdf.paper_rect("a4")
MARGIN, GAP = 28, 8
FONT = pymupdf.Font("helv")
CJK = "china-s"


def read_tags(subj):
    tags = {}
    for line in open(f"{ROOT}/tools/tags_{subj}.txt", encoding="utf-8"):
        if line.startswith("#") or not line.strip():
            continue
        p, *items = line.split()
        sec = "CalcFree" if p[4] == "F" else "CalcAssumed"
        for it in items:
            q, t = it.split(":")
            tags[(p[:4], sec, int(q))] = t.split(",")
    return tags


class Layout:
    """Stack page regions top-to-bottom onto A4 output pages."""

    def __init__(self, out):
        self.out, self.page, self.y = out, None, A4.height

    def new_page(self):
        self.page = self.out.new_page(width=A4.width, height=A4.height)
        self.y = MARGIN

    def need(self, h):
        if self.page is None or self.y + h > A4.height - MARGIN:
            self.new_page()

    def bar(self, text, color, h=20):
        self.need(h + 60)
        r = pymupdf.Rect(MARGIN, self.y, A4.width - MARGIN, self.y + h)
        self.page.draw_rect(r, color=None, fill=color)
        self.page.insert_text((r.x0 + 6, r.y0 + h - 6), text.replace("★", "[primary]").replace("☆", "[secondary]"),
                              fontsize=10, fontname="helv", color=(1, 1, 1))
        self.y += h + GAP

    def region(self, src, pno, y0, y1):
        for a, b in segments(src[pno], y0, y1):
            self._piece(src, pno, a, b)

    def _piece(self, src, pno, y0, y1):
        clip = pymupdf.Rect(X0, y0, X1, y1)
        w = A4.width - 2 * MARGIN
        s = min(1.0, w / clip.width)
        h = clip.height * s
        if h > A4.height - 2 * MARGIN:  # never happens for A4 sources, but be safe
            s = (A4.height - 2 * MARGIN) / clip.height
            h = clip.height * s
        self.need(h)
        r = pymupdf.Rect(MARGIN, self.y, MARGIN + clip.width * s, self.y + h)
        self.page.show_pdf_page(r, src, pno, clip=clip)
        self.page.draw_rect(r, color=(0.8, 0.8, 0.8), width=0.4)
        self.y += h + GAP


X0, X1, BLANK = 40, 562, 40


def segments(page, y0, y1):
    """Split [y0, y1] into ink-bearing bands, dropping blank gaps taller than BLANK."""
    clip = pymupdf.Rect(X0, y0, X1, y1)
    boxes = [pymupdf.Rect(b[:4]) for b in page.get_text("blocks", clip=clip)]
    boxes += [d["rect"] for d in page.get_drawings() if d["rect"].intersects(clip)]
    boxes += [pymupdf.Rect(i["bbox"]) for i in page.get_image_info() if pymupdf.Rect(i["bbox"]).intersects(clip)]
    iv = sorted((max(b.y0, y0), min(b.y1, y1)) for b in boxes if b.y1 > y0 and b.y0 < y1)
    out = []
    for a, b in iv:
        if out and a - out[-1][1] <= BLANK:
            out[-1][1] = max(out[-1][1], b)
        else:
            out.append([a, b])
    return [(max(y0, a - 6), min(y1, b + 6)) for a, b in out if b - a > 2]


def clean(t):
    t = re.sub(r"DO NOT WRITE IN THIS AREA AS IT WILL BE CUT OFF|See next page|\bD?O? ?N?O?T? ?WRITE IN TH\w*", "", t)
    return re.sub(r"\s+", " ", t).strip()


def build(subj):
    qs = [q for q in json.load(open(f"{ROOT}/{subj}/questions.json", encoding="utf-8")) if q["year"] != "2016Sample"]
    tags = read_tags(subj)
    outdir = f"{ROOT}/{subj}/topics"
    os.makedirs(outdir, exist_ok=True)
    cache = {}
    src = lambda p: cache.setdefault(p, pymupdf.open(f"{ROOT}/{p}"))
    summary = []
    for code, (fname, zh, en) in TOPICS[subj].items():
        sel = [q for q in qs if code in tags[(q["year"], q["section"], q["q"])]]
        sel.sort(key=lambda q: (q["year"], q["section"] != "CalcFree", q["q"]))
        out = pymupdf.open()
        lay = Layout(out)
        # cover
        lay.new_page()
        lay.page.insert_text((MARGIN, 80), f"WACE {subj} ATAR", fontsize=20, fontname="hebo")
        lay.page.insert_text((MARGIN, 108), zh, fontsize=18, fontname=CJK)
        lay.page.insert_text((MARGIN, 130), en, fontsize=13, fontname="helv")
        total = sum(q["marks"] for q in sel)
        lay.page.insert_textbox(pymupdf.Rect(MARGIN, 140, A4.width - MARGIN, 170),
                                f"{len(sel)} questions - {total} marks - 2016-2025 - source: SCSA past ATAR exams & ratified marking keys",
                                fontsize=10, fontname="helv")
        md = [f"# WACE {subj} · {zh} ({en})", "",
              f"{len(sel)} questions, {total} marks, 2016–2025. PDF: `{fname}.pdf` (each entry: exam crop then marking key crop).",
              "Tags: ★ = primary topic of the question; ☆ = secondary (question also appears in another topic file).", ""]
        toc = []
        for q in sel:
            t = tags[(q["year"], q["section"], q["q"])]
            star = "★" if t[0] == code else "☆"
            sec = "Calculator-free" if q["section"] == "CalcFree" else "Calculator-assumed"
            others = "+".join(x for x in t if x != code)
            head = f"{star} {q['year']} {sec} · Question {q['q']} · {q['marks']} marks" + (f" · also: {others}" if others else "")
            lay.new_page()
            lay.bar(head, (0.12, 0.22, 0.45))
            start = out.page_count
            for pno, y0, y1 in q["exam_regions"]:
                lay.region(src(q["exam"]), pno, y0, y1)
            lay.bar("Marking key - " + f"{q['year']} {sec} Q{q['q']}", (0.55, 0.15, 0.15))
            for pno, y0, y1 in q["key_regions"]:
                lay.region(src(q["key"]), pno, y0, y1)
            end = out.page_count
            toc.append((head, start))
            md += [f"## {head}", f"- PDF pages {start}–{end} · original: `{q['exam']}` / `{q['key']}`",
                   "", clean(q["text"]), ""]
        # table of contents on cover
        y = 185
        for head, p in toc:
            if y > A4.height - 40:
                break
            out[0].insert_text((MARGIN, y), f"p.{p:<4} " + head.replace("★", "*").replace("☆", "o").replace("·", "-"), fontsize=7.5, fontname="cour")
            y += 10.5
        if y > A4.height - 40:
            out[0].insert_text((MARGIN, y), "... full list in the .md index", fontsize=7.5, fontname="cour")
        out.set_toc([[1, h, p] for h, p in toc])
        out.save(f"{outdir}/{fname}.pdf", garbage=4, deflate=True)
        open(f"{outdir}/{fname}.md", "w", encoding="utf-8").write("\n".join(md))
        summary.append((fname, zh, len(sel), total, out.page_count))
    for s in summary:
        print(subj, *s)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        build(s)
