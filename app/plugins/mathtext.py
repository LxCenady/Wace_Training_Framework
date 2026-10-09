"""LaTeX in text. One job: turn '... $\\frac{dy}{dx}$ ...' into rendered maths wherever text is shown.

Rendering: ziamath (pure Python, no TeX install) -> SVG -> PyMuPDF raster (Tk) or vector (PDF export).
$...$ is inline, $$...$$ is a display line. Anything that fails to render is shown as its source text.

repair(): models often write \\frac inside JSON with a single backslash; JSON then silently turns
\\f \\b \\t \\r \\n into control characters ('\\frac' -> formfeed + 'rac'). Inside maths those are put back.
"""
import base64, re
import tkinter as tk

# $$display$$ or $inline$ (may contain a newline left by JSON damage); \$ is a literal dollar (money)
SPLIT = re.compile(r"(\$\$.+?\$\$|(?<!\\)\$(?:[^$\\]|\\.)+?(?<!\\)\$)", re.S)
# a real newline inside display maths is legitimate; only "\n" + an n-command was meant as a command
N_COMMAND = re.compile(r"\n(?=(abla|eq|eg|ot|otin|mid|ewline|exists|leq|geq|parallel|subseteq|e|u|i)(?![a-z]))")


def repair(text):
    """Undo JSON escape damage inside $…$; formfeed/backspace are never meant anywhere."""
    if not isinstance(text, str):
        return text
    text = text.replace("\f", "\\f").replace("\b", "\\b")

    def fix(m):
        s = re.sub(r"\t(?=[A-Za-z])", r"\\t", m.group(0))  # \theta \times \text \tan …
        s = re.sub(r"\r(?=[A-Za-z])", r"\\r", s)           # \rho \right \rangle …
        return N_COMMAND.sub(r"\\n", s)

    return SPLIT.sub(fix, text)


def segments(text):
    """-> [(kind, s)] with kind 'text' | 'inline' | 'display'."""
    out = []
    for piece in SPLIT.split(text or ""):
        if not piece:
            continue
        if piece.startswith("$$") and piece.endswith("$$") and len(piece) > 4:
            out.append(("display", piece[2:-2].strip()))
        elif piece.startswith("$") and piece.endswith("$") and len(piece) > 2:
            out.append(("inline", piece[1:-1].strip()))
        else:
            out.append(("text", piece.replace("\\$", "$")))
    return out


def plain(text):
    """Maths shown as its source without dollars (for one-line previews)."""
    return "".join(s if kind == "text" else s for kind, s in segments(text))


def svg(tex, size=20):
    import ziamath as zm
    zm.config.svg2 = False  # inline glyph paths: MuPDF's SVG reader ignores <use>
    return zm.Latex(tex, size=size).svg()


def setup(k):
    import pymupdf
    cache = {}

    def image(tex, size, colour):
        key = (tex, size, colour)
        if key not in cache:
            src = svg(tex, size).replace('fill="black"', f'fill="{colour}"').replace("currentColor", colour)
            doc = pymupdf.open("svg", src.encode())
            cache[key] = tk.PhotoImage(data=base64.b64encode(doc[0].get_pixmap(dpi=96, alpha=True).tobytes("png")))
        return cache[key]

    def write(t, text, *tags, size=17):
        """Insert text with rendered maths into a read-only Text widget made by ui.text."""
        t.configure(state="normal")
        for kind, s in segments(repair(text)):
            if kind == "text":
                t.insert("end", s, tags)
                continue
            try:
                img = image(s, size + (3 if kind == "display" else 0), "#1f1d1a")
                if kind == "display":
                    t.insert("end", "\n", tags)
                t.image_create("end", image=img, align="center", padx=1)
                for tag in tags:  # keep part tags (right-click marking) on images too
                    t.tag_add(tag, "end-2c", "end-1c")
                if kind == "display":
                    t.insert("end", "\n", tags)
            except Exception:  # unsupported LaTeX: show the source rather than nothing
                t.insert("end", f"${s}$", tags)
        t.configure(state="disabled")

    k.provide("math.write", write)
    k.provide("math.repair", repair)
    k.provide("math.plain", plain)
    k.provide("math.svg", svg)
    k.provide("math.segments", segments)
