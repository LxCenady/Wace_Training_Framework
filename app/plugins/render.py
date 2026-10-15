"""PDF crops. One job: (pdf, regions) -> list of PNG bytes.

A region is [page, y0, y1] (a full-width band in PDF points, packs built from papers) or
{"page", "bbox": [x0, y0, x1, y1] as fractions of the page, "rotate": 0|90|180|270} (Compiler packs).
"""
import os
import pymupdf

X0, X1 = 28, 572


def crop(page, region, zoom):
    if isinstance(region, dict):
        a, b, c, d = region["bbox"]
        w, h = page.rect.width, page.rect.height
        png = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=pymupdf.Rect(a * w, b * h, c * w, d * h)).tobytes("png")
        if region.get("rotate"):
            with pymupdf.open("png", png) as image:
                png = image[0].get_pixmap(matrix=pymupdf.Matrix(1, 1).prerotate(region["rotate"])).tobytes("png")
        return png
    _, y0, y1 = region
    return page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=pymupdf.Rect(X0, y0, X1, y1)).tobytes("png")


def setup(k):
    docs = {}

    def regions(pdf, regs, zoom=1.35):
        if pdf not in docs:
            docs[pdf] = pymupdf.open(os.path.join(k.root, pdf))
        doc = docs[pdf]
        return [crop(doc[r["page"] if isinstance(r, dict) else r[0]], r, zoom) for r in regs]

    k.provide("render.regions", regions)
