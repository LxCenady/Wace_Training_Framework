"""External PDF geometry: inspect, suggest question crops, validate and render arbitrary page rectangles."""
import math
import re
import pymupdf

HEAD = re.compile(r"^(?:Question\s+|Q\s*)(\d+)\b(.*)$", re.I)
MARKS = re.compile(r"\((\d+)\s*marks?\)", re.I)
STOP = re.compile(r"^(?:End of questions|Additional working space|Acknowledgements)\b", re.I)


def inspect(path):
    with pymupdf.open(path) as doc:
        if doc.needs_pass or not doc.page_count:
            raise ValueError("PDF 必须有页面且未加密")
        return [list(page.rect) for page in doc]


def validate(path, regions):
    pages = inspect(path)
    clean = []
    for region in regions:
        if len(region) != 5:
            raise ValueError("切块范围无效")
        p, *coords = region
        if type(p) is not int or not 0 <= p < len(pages):
            raise ValueError("页码超出原件范围")
        if not all(isinstance(x, (float, int)) and math.isfinite(x) for x in coords):
            raise ValueError("切块范围无效")
        x0, y0, x1, y1 = coords
        px0, py0, px1, py1 = pages[p]
        if not (px0 <= x0 < x1 <= px1 and py0 <= y0 < y1 <= py1):
            raise ValueError("切块范围超出页面")
        clean.append([p, *coords])
    return clean


def text(path, regions):
    regions = validate(path, regions)
    with pymupdf.open(path) as doc:
        return "\n".join(doc[p].get_text("text", clip=pymupdf.Rect(*coords) * doc[p].derotation_matrix)
                         for p, *coords in regions).strip()


def render(path, page, rectangle=None, zoom=1.0):
    with pymupdf.open(path) as doc:
        pg = doc[page]
        clip = pymupdf.Rect(*rectangle) if rectangle else pg.rect
        return pg.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=clip).tobytes("png")


def suggest(path):
    """Only explicit Question/Q headings; uncertain/scanned layouts are left for manual cropping."""
    with pymupdf.open(path) as doc:
        if doc.needs_pass or not doc.page_count:
            raise ValueError("PDF 必须有页面且未加密")
        if any(page.rotation for page in doc):
            return []  # rotated heading order is ambiguous; the manual picker uses displayed coordinates
        heads, seen = [], set()
        end = (doc.page_count - 1, doc[-1].rect.y1)
        stopped = False
        for p, page in enumerate(doc):
            lines = []
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    words = "".join(span["text"] for span in line["spans"]).strip()
                    lines.append((line["bbox"], words))
            for box, words in sorted(lines, key=lambda row: (row[0][1], row[0][0])):
                match = HEAD.match(words)
                if heads and STOP.match(words):
                    end, stopped = (p, box[1]), True
                    break
                if not match or "continued" in match[2].lower():
                    continue
                n = int(match[1])
                if n in seen:
                    continue
                marks = MARKS.search(words)
                heads.append((n, p, max(page.rect.y0, box[1] - 2), int(marks[1]) if marks else None))
                seen.add(n)
            if stopped:
                break
        result = []
        for i, (n, p, y, marks) in enumerate(heads):
            ep, ey = (heads[i + 1][1], heads[i + 1][2]) if i + 1 < len(heads) else end
            regions = []
            for pg in range(p, ep + 1):
                r = doc[pg].rect
                y0 = y if pg == p else r.y0
                y1 = ey if pg == ep else r.y1
                if y1 > y0:
                    regions.append([pg, r.x0, y0, r.x1, y1])
            if regions:
                result.append(dict(label=f"Q{n}", marks=marks, regions=regions))
        return result


def setup(k):
    for name, fn in (("inspect", inspect), ("validate", validate), ("text", text), ("render", render), ("suggest", suggest)):
        k.provide("external.pdf." + name, fn)
