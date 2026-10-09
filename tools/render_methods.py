"""Render <subj>/methods/*.md to PDF (A4, CJK font). One job: markdown -> PDF."""
import glob, os, sys
import markdown
import pymupdf

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = r"C:\Windows\Fonts"
CSS = """
@font-face {font-family: yahei; src: url(msyh.ttc);}
@font-face {font-family: mono; src: url(consola.ttf);}
* {font-family: yahei; font-size: 9.5pt; line-height: 1.45;}
h1 {font-size: 16pt; color: #1f3a73; margin: 0 0 6pt 0;}
h2 {font-size: 12pt; color: #1f3a73; margin: 12pt 0 4pt 0; border-bottom: 0.5pt solid #1f3a73;}
h3 {font-size: 10.5pt; margin: 8pt 0 3pt 0;}
p, li {margin: 2pt 0;}
blockquote {color: #555; margin: 0 0 6pt 8pt; font-size: 8.5pt;}
blockquote p {font-size: 8.5pt;}
code {font-family: mono; font-size: 8.5pt; color: #8c2626;}
table {border-collapse: collapse; margin: 4pt 0;}
td, th {border: 0.5pt solid #999; padding: 2pt 4pt; font-size: 8.5pt;}
th {background-color: #e8ecf5;}
strong {color: #8c2626;}
"""


LIST = __import__("re").compile(r"^\s*([-*]|\d+\.)\s")


def loosen(md):
    """Python-Markdown needs a blank line before a list or table that follows a paragraph."""
    out, prev = [], ""
    for line in md.splitlines():
        if line.startswith("   ") and not line.startswith("    ") and LIST.match(line):
            line = " " + line  # nested items need 4-space indent
        elif line.startswith("   ") and not line.startswith("    ") and prev.strip():
            line = " " + line  # continuation text under a numbered item
        starts_block = LIST.match(line) or line.startswith("|")
        prev_is_block = LIST.match(prev) or prev.startswith("|") or not prev.strip()
        if starts_block and not prev_is_block:
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


def render(md_path, pdf_path):
    html = markdown.markdown(loosen(open(md_path, encoding="utf-8").read()), extensions=["tables"])
    story = pymupdf.Story(html=html, user_css=CSS, archive=pymupdf.Archive(FONTS))
    writer = pymupdf.DocumentWriter(pdf_path)
    rect = pymupdf.paper_rect("a4")
    where = rect + (40, 40, -40, -40)
    more = True
    while more:
        dev = writer.begin_page(rect)
        more, _ = story.place(where)
        story.draw(dev)
        writer.end_page()
    writer.close()


def shrink(pdf_path):
    """Subset embedded fonts (a full YaHei is ~24 MB per file)."""
    d = pymupdf.open(pdf_path)
    d.subset_fonts()
    tmp = pdf_path + ".tmp"
    d.save(tmp, garbage=4, deflate=True, clean=True)
    d.close()
    os.replace(tmp, pdf_path)


if __name__ == "__main__":
    for s in sys.argv[1:]:
        for md in sorted(glob.glob(f"{ROOT}/{s}/methods/*.md")):
            out = md[:-3] + ".pdf"
            render(md, out)
            shrink(out)
            print(os.path.basename(out), pymupdf.open(out).page_count, "pages")

