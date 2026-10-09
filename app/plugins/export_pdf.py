"""Worksheet export. One job: AI questions -> two A4 PDFs, a question paper with working space and an answer
paper whose mark points carry tick boxes for marking on paper.

Fonts come from the Windows font folder: Microsoft YaHei for text, Segoe UI Symbol for the glyphs YaHei
lacks (⇒ ☐ ✓ …), chosen per character.
"""
import html, io, os, time
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
.space {color: #ffffff; margin: 0;}
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


def render(body, path, assets):
    story = pymupdf.Story(html=body, user_css=CSS, archive=assets.archive)
    buf = io.BytesIO()
    writer = pymupdf.DocumentWriter(buf)
    page = pymupdf.paper_rect("a4")
    more, n = True, 0
    while more:
        n += 1
        dev = writer.begin_page(page)
        more, _ = story.place(page + (48, 48, -48, -56))
        story.draw(dev)
        writer.end_page()
    writer.close()
    doc = pymupdf.open("pdf", buf.getvalue())  # page numbers + subset fonts (a full YaHei is ~20 MB)
    for i, pg in enumerate(doc):
        pg.insert_text((page.width / 2 - 12, page.height - 28), f"{i + 1} / {doc.page_count}", fontsize=8,
                       color=(.5, .5, .5))
    doc.subset_fonts()
    doc.save(path, garbage=4, deflate=True)
    doc.close()
    return n


def worksheet(items, path, title, name, maths=None, figures=None):
    """items: generated items (store.generated). Writes <path> (questions) and <path>_答案.pdf; returns both."""
    font = pymupdf.Font(fontfile=os.path.join(FONTS, "msyh.ttc"))
    qa, aa = Assets(maths, figures), Assets(maths, figures)
    marks = sum(i["marks"] for i in items)
    meta = (f"{len(items)} 题 · 共 {marks} 分 · 建议用时约 {marks} 分钟（WACE 约每分钟 1 分）· "
            f"{time.strftime('%Y-%m-%d')} · WTF — WACE Training Framework")
    q, a = [f"<h1>{text(title, font)}</h1><p class='meta'>{text(meta, font)}</p>"], \
        [f"<h1>{text(title + ' — 答案与评分标准', font)}</h1><p class='meta'>{text(meta, font)}</p>"]
    for n, it in enumerate(items, 1):
        head = f"Question {n}（{it['marks']} 分 · {SECTION.get(it.get('section'), '')} · AI #{it['id']}）"
        q.append(f"<h2>{text(head, font)}</h2><p>{text(it['question'], font, qa)}</p>")
        q.append(qa.figure(it.get("figure")))
        q.append("<p class='space'>.</p>" * (3 * it["marks"] + 2))  # working space ~ 3 lines per mark
        a.append(f"<h2>{text(head, font)}</h2>")
        by = {}
        for label, t in it["points"]:
            by.setdefault(label, []).append(t)
        for p in it["parts"]:
            tags = "；".join(name(c) for c in p.get("patterns") or it["patterns"])
            line = "({}) {} 分　答案：{}".format(p["label"], p["marks"], p["answer"])
            a.append(f"<p class='part'>{text(line, font, aa)} <span class='tag'>{text(tags, font)}</span></p>")
            a.append(aa.figure(p.get("figure"), 240))
            for t in by.get(p["label"], []):
                a.append(f"<p class='pt'>{text('☐ ' + t, font, aa)}</p>")
        a.append(f"<p class='sol'>{text('解答：' + chr(10) + it['solution'], font, aa)}</p>")
    answers = path[:-4] + "_答案.pdf"
    render("".join(q), path, qa)
    render("".join(a), answers, aa)
    return path, answers


def setup(k):
    store = k.get("store")
    k.provide("export.worksheet", lambda gids, path, title: worksheet(
        [store.generated(g) for g in gids], path, title, store.pattern_name,
        k.get("math.svg", None), k.get("figure.svg", None)))
