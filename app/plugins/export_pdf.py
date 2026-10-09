"""Worksheet export. One job: AI questions -> two A4 PDFs, a question paper (one question per page, the rest of
the page is working space) and an answer paper whose mark points carry tick boxes for marking on paper (a
question never split across pages unless it is longer than one).

Fonts come from the Windows font folder: Microsoft YaHei for text, Segoe UI Symbol for the glyphs YaHei
lacks (⇒ ☐ ✓ …), chosen per character.
"""
import html, io, os, re, time
import pymupdf

FONTS = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")
CSS = """
@font-face {font-family: yahei; src: url(msyh.ttc);}
@font-face {font-family: sym; src: url(seguisym.ttf);}
* {font-family: yahei; font-size: 10.5pt; line-height: 1.5;}
h1 {font-size: 16pt; color: #1f3a73; margin: 0 0 2pt 0;}
.meta {color: #666; font-size: 9pt; margin-bottom: 10pt;}
h2 {font-size: 12pt; margin: 14pt 0 4pt 0; border-bottom: 0.6pt solid #1f3a73; color: #1f3a73;}
p {margin: 2pt 0;}
.part {font-weight: bold; margin-top: 6pt;}
.tag {color: #1f3a73; font-size: 8.5pt;}
.pt {margin: 1pt 0 1pt 14pt;}
.sol {color: #333; font-size: 9.5pt;}
.s {font-family: sym;}
"""
SECTION = {"CalcFree": "计算器禁用 (Calculator-free)", "CalcAssumed": "计算器允许 (Calculator-assumed)"}


class Assets:
    """Fonts + every formula / figure of one document, as an in-memory archive the Story reads images from."""

    def __init__(self, maths=None, figures=None):
        self.archive = pymupdf.Archive(FONTS)
        self.maths, self.figures, self.n = maths, figures, 0

    def add_svg(self, svg):
        self.n += 1
        name = f"a{self.n}.svg"
        self.archive.add((svg.encode(), name))
        w, h = pymupdf.open("svg", svg.encode())[0].rect[2:]
        return name, w, h

    def formula(self, tex, display):
        name, w, h = self.add_svg(self.maths(tex, 20))
        k = 0.56  # 20 px maths -> 10.5 pt text
        img = f"<img src='{name}' width='{w * k:.1f}' height='{h * k:.1f}'/>"
        return f"<br/>{img}<br/>" if display else img

    def figure(self, spec, width=300):
        if not spec or not self.figures:
            return ""
        try:
            svg, _ = self.figures(spec)
        except Exception:
            return ""
        name, w, h = self.add_svg(svg)
        return f"<p><img src='{name}' width='{width}' height='{width * h / w:.1f}'/></p>"


def text(s, font, assets=None):
    """HTML-escape, keep line breaks, render $maths$ (when assets are given), and route glyphs YaHei lacks
    to the symbol font."""
    from plugins.mathtext import segments, repair
    out = []
    for kind, piece in segments(repair(s)) if assets and assets.maths else [("text", s)]:
        if kind != "text":
            try:
                out.append(assets.formula(piece, kind == "display"))
                continue
            except Exception:  # unsupported LaTeX: print its source
                piece = f"${piece}$"
        for ch in piece:
            e = html.escape(ch)
            if ch == "\n":
                out.append("<br/>")
            elif ord(ch) > 127 and not font.has_glyph(ord(ch)):
                out.append(f'<span class="s">{e}</span>')
            else:
                out.append(e)
    return "".join(out)


def render(blocks, path, assets, own_page=False):
    """blocks: [(html, working space in pt)], one per question. A question never starts where it would not fit:
    with own_page each one opens a new page (the rest of the page is its working space, plus a blank page
    when less than its space is left); otherwise questions share pages but one that does not fit in what is
    left moves whole to the next page. Only a question longer than a page runs over."""
    buf = io.BytesIO()
    writer = pymupdf.DocumentWriter(buf)
    page = pymupdf.paper_rect("a4")
    area = page + (48, 48, -48, -56)
    state = {"dev": None, "y": area.y0, "n": 0}

    def new_page():
        if state["dev"] is not None:
            writer.end_page()
        state.update(dev=writer.begin_page(page), y=area.y0, n=state["n"] + 1)

    def height(html_):
        _, filled = pymupdf.Story(html=html_, user_css=CSS, archive=assets.archive).place(
            pymupdf.Rect(0, 0, area.width, 1e5))
        return filled[3]

    for html_, space in blocks:
        if state["dev"] is None or own_page or height(html_) > area.y1 - state["y"]:
            new_page()
        story = pymupdf.Story(html=html_, user_css=CSS, archive=assets.archive)
        while True:
            more, filled = story.place(pymupdf.Rect(area.x0, state["y"], area.x1, area.y1))
            story.draw(state["dev"])
            if not more:
                state["y"] = filled[3] + 12
                break
            new_page()
        if own_page and area.y1 - state["y"] < space:
            new_page()  # a blank page of working space
    if state["dev"] is not None:
        writer.end_page()
    writer.close()
    doc = pymupdf.open("pdf", buf.getvalue())  # page numbers + subset fonts (a full YaHei is ~20 MB)
    for i, pg in enumerate(doc):
        pg.insert_text((page.width / 2 - 12, page.height - 28), f"{i + 1} / {doc.page_count}", fontsize=8,
                       color=(.5, .5, .5))
    doc.subset_fonts()
    doc.save(path, garbage=4, deflate=True)
    doc.close()
    return state["n"]


def worksheet(items, path, title, name, maths=None, figures=None, meta=None):
    """items: generated items (store.generated). Writes <path> (questions) and <path>_答案.pdf; returns both."""
    font = pymupdf.Font(fontfile=os.path.join(FONTS, "msyh.ttc"))
    qa, aa = Assets(maths, figures), Assets(maths, figures)
    marks = sum(i["marks"] for i in items)
    meta = meta or (f"{len(items)} 题 · 共 {marks} 分 · 建议用时约 {marks} 分钟（WACE 约每分钟 1 分）· "
                    f"{time.strftime('%Y-%m-%d')} · WTF — WACE Training Framework")
    q, a = [], []
    for n, it in enumerate(items, 1):
        head = f"Question {n}（{it['marks']} 分 · {SECTION.get(it.get('section'), '')} · AI #{it['id']}）"
        stem = re.sub(r"^\s*Question\s*\d*\s*\(\s*\d+\s*marks?\s*\)\s*", "", it["question"])  # models repeat it
        q.append((f"<h2>{text(head, font)}</h2><p>{text(stem, font, qa)}</p>" + qa.figure(it.get("figure")),
                  3 * 16 * it["marks"]))  # working space ~ 3 lines per mark
        ans = [f"<h2>{text(head, font)}</h2>"]
        by = {}
        for label, t in it["points"]:
            by.setdefault(label, []).append(t)
        for p in it["parts"]:
            tags = "；".join(name(c) for c in p.get("patterns") or it["patterns"])
            line = "({}) {} 分　答案：{}".format(p["label"], p["marks"], p["answer"])
            ans.append(f"<p class='part'>{text(line, font, aa)} <span class='tag'>{text(tags, font)}</span></p>")
            ans.append(aa.figure(p.get("figure"), 240))
            for t in by.get(p["label"], []):
                ans.append(f"<p class='pt'>{text('☐ ' + t, font, aa)}</p>")
        ans.append(f"<p class='sol'>{text('解答：' + chr(10) + it['solution'], font, aa)}</p>")
        a.append(("".join(ans), 0))
    q[0] = (f"<h1>{text(title, font)}</h1><p class='meta'>{text(meta, font)}</p>" + q[0][0], q[0][1])
    a[0] = (f"<h1>{text(title + ' — 答案与评分标准', font)}</h1><p class='meta'>{text(meta, font)}</p>" + a[0][0], 0)
    answers = path[:-4] + "_答案.pdf"
    render(q, path, qa, own_page=True)
    render(a, answers, aa)
    return path, answers


def setup(k):
    store = k.get("store")
    k.provide("export.worksheet", lambda gids, path, title, meta=None: worksheet(
        [store.generated(g) for g in gids], path, title, store.pattern_name,
        k.get("math.svg", None), k.get("figure.svg", None), meta))
