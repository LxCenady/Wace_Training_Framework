"""Render a cheat-sheet markdown to a dense 2-column A4 PDF. One job: md -> compact PDF."""
import sys
import markdown
import pymupdf
from render_methods import loosen, FONTS, shrink

CSS = """
@font-face {font-family: yahei; src: url(msyh.ttc);}
* {font-family: yahei; font-size: 9pt; line-height: 1.38;}
h1 {font-size: 13pt; color: #1f3a73; margin: 0 0 2pt 0;}
h2 {font-size: 10.5pt; color: #ffffff; background-color: #1f3a73; margin: 5pt 0 2pt 0; padding: 1pt 3pt;}
p {margin: 1pt 0;}
ul {margin: 0 0 0 9pt; padding: 0;}
li {margin: 0.6pt 0;}
strong {color: #8c2626;}
"""


def render(md_path, pdf_path):
    html = markdown.markdown(loosen(open(md_path, encoding="utf-8").read()))
    story = pymupdf.Story(html=html, user_css=CSS, archive=pymupdf.Archive(FONTS))
    page = pymupdf.paper_rect("a4")
    m, gap = 22, 12
    w = (page.width - 2 * m - gap) / 2
    cols = [pymupdf.Rect(m, m, m + w, page.height - m), pymupdf.Rect(m + w + gap, m, page.width - m, page.height - m)]
    writer = pymupdf.DocumentWriter(pdf_path)
    more, n = True, 0
    while more:
        dev = writer.begin_page(page)
        for c in cols:
            if not more:
                break
            more, _ = story.place(c)
            story.draw(dev)
        writer.end_page()
        n += 1
    writer.close()
    return n


if __name__ == "__main__":
    for md in sys.argv[1:]:
        n = render(md, md[:-3] + ".pdf")
        shrink(md[:-3] + ".pdf")
        print(md, n, "pages")
