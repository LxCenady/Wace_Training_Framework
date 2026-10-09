"""PDF crops. One job: (pdf, [[page, y0, y1], ...]) -> list of PNG bytes."""
import os
import pymupdf

X0, X1 = 28, 572


def setup(k):
    docs = {}

    def regions(pdf, regs, zoom=1.35):
        if pdf not in docs:
            docs[pdf] = pymupdf.open(os.path.join(k.root, pdf))
        doc = docs[pdf]
        return [doc[p].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom), clip=pymupdf.Rect(X0, y0, X1, y1)).tobytes("png")
                for p, y0, y1 in regs]

    k.provide("render.regions", regions)
