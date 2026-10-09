"""Figures. One job: a declarative figure spec (written by the model) -> an exam-style SVG drawing.

The model never writes plotting code. It writes data:
  {"x": [-3, 3], "y": [-4, 5], "axes": true, "equal": false, "grid": true,
   "items": [{"curve": "x**3 - 3*x + 1", "domain": [-2, 2], "label": "$y=f(x)$"},
             {"fill": "x**3 - 3*x + 1", "to": "0", "from_x": 0, "to_x": 1},
             {"implicit": "(x-1)**2 + (y-1)**2 - 1/4"},
             {"param": ["2*cos(t)", "sin(t)"], "t": [0, "2*pi"]},
             {"point": [1, -1], "label": "$B(1,-1)$"},
             {"segment": [[0, 0], [1, 2]], "dashed": true}, {"polygon": [[0, 0], [10, 0], [5, 8]]},
             {"circle": [0, 2], "r": 1}, {"vline": 2, "dashed": true}, {"hline": 0},
             {"vector": [[0, 0], [3, 2]], "label": "$\\mathbf{a}$"},
             {"text": [5, -1], "s": "$10$ cm"}, {"bars": [[1, 0.2], [2, 0.5]], "width": 1}]}
Expressions go through the same whitelist as the SymPy check (plugins/symcheck.safe) and become plain
math-module functions. Items that cannot be drawn are skipped and reported; the rest is still drawn.
"""
import math

CSS = """
Graph { color: none; edge_width: 1.5; }
Graph.GridX { color: #dddddd; stroke: solid; stroke_width: 0.6; }
Graph.GridY { color: #dddddd; stroke: solid; stroke_width: 0.6; }
Element { colorcycle: black; }
Point { color: black; }
Text { color: black; }
"""
NO_GRID = "Graph.GridX { color: none; } Graph.GridY { color: none; }"
FILL = "#9fb4d8"


def setup(k):
    from plugins.symcheck import safe, namespace

    def fn(expr, args=("x",)):
        """Whitelisted expression -> float function of the given variables."""
        import sympy
        tree = safe(str(expr))
        ns = namespace(tree)
        value = eval(compile(tree, "<figure>", "eval"), ns)
        syms = [ns.get(a) if isinstance(ns.get(a), sympy.Symbol) else sympy.Symbol(a, real=True) for a in args]
        f = sympy.lambdify(syms, value, modules="math")

        def safe_call(*v):
            try:
                out = complex(f(*v))
                return out.real if abs(out.imag) < 1e-9 and math.isfinite(out.real) else math.nan
            except (ValueError, ZeroDivisionError, OverflowError, TypeError):
                return math.nan
        return safe_call

    def num(v):
        return float(v) if isinstance(v, (int, float)) else fn(v, ())()

    def pt(p):
        return (num(p[0]), num(p[1]))

    def draw(spec):
        """-> (svg text, [problems])."""
        import ziaplot as zp
        import ziamath as zm
        zp.config.svg2 = zm.config.svg2 = False  # MuPDF renders inline paths, not <use>/<marker>
        problems = []
        x0, x1 = (num(v) for v in spec.get("x", [-5, 5]))
        y0, y1 = (num(v) for v in spec.get("y", [-5, 5]))
        axes = spec.get("axes", True)
        H = 340
        W = int(H * min(1.7, max(0.6, (x1 - x0) / max(1e-9, y1 - y0)))) if spec.get("equal") or not axes else 460
        g = (zp.GraphQuad() if axes is True or axes == "origin" else zp.Graph() if axes == "box" else zp.Diagram())
        g.size(W, H).xrange(x0, x1).yrange(y0, y1)
        if spec.get("equal"):
            g.equal_aspect()
        g.css(CSS + ("" if spec.get("grid", bool(axes)) else NO_GRID))
        sx, sy = W * 0.86 / (x1 - x0), H * 0.86 / (y1 - y0)  # data -> pixel scale (approx. plot area)
        if spec.get("equal"):
            sx = sy = min(sx, sy)
        lo, hi = y0 - 0.05 * (y1 - y0), y1 + 0.05 * (y1 - y0)

        def runs(xs, ys):
            """Split a sampled curve where it is undefined or leaves the window (asymptotes)."""
            run = []
            for x, y in zip(xs, ys):
                if math.isfinite(y) and lo <= y <= hi:
                    run.append((x, y))
                elif run:
                    yield run
                    run = []
            if run:
                yield run

        def polyline(points, dashed=False):
            if len(points) > 1:
                line = zp.PolyLine([p[0] for p in points], [p[1] for p in points]).color("black")
                if dashed:
                    line.stroke("--")

        def dot(x, y, r=3.5):
            zp.Polygon([(x + r / sx * math.cos(a), y + r / sy * math.sin(a))
                        for a in (j * math.pi / 8 for j in range(16))]).color("black").fill("black")

        def label(x, y, text, pos="NE"):
            dx, dy = 6 / sx, 6 / sy
            zp.Text(x + (dx if "E" in pos else -dx), y + (dy if "N" in pos else -dy), text,
                    halign="left" if "E" in pos else "right", valign="bottom" if "N" in pos else "top")

        def arrow(a, b):
            (ax, ay), (bx, by) = a, b
            ux, uy = (bx - ax) * sx, (by - ay) * sy
            n = math.hypot(ux, uy) or 1
            ux, uy = ux / n, uy / n
            back = (bx - 10 * ux / sx, by - 10 * uy / sy)
            zp.Segment((ax, ay), back).color("black")
            zp.Polygon([(bx, by), (back[0] - 4 * uy / sx, back[1] + 4 * ux / sy),
                        (back[0] + 4 * uy / sx, back[1] - 4 * ux / sy)]).color("black").fill("black")

        with g:
            for i, it in enumerate(spec.get("items", [])):
                try:
                    if "curve" in it:
                        a, b = (num(v) for v in it.get("domain", [x0, x1]))
                        f = fn(it["curve"])
                        xs = [a + (b - a) * j / 600 for j in range(601)]
                        ys = [f(x) for x in xs]
                        for run in runs(xs, ys):
                            polyline(run, it.get("dashed"))
                        if it.get("label"):
                            # right-hand part of the visible curve, away from the x-axis and the window edge
                            ok = [(x, y) for x, y in zip(xs, ys) if math.isfinite(y)
                                  and y0 + 0.08 * (y1 - y0) < y < y1 - 0.12 * (y1 - y0)
                                  and abs(y) > 0.12 * (y1 - y0) and x < x1 - 0.2 * (x1 - x0)]
                            if ok:
                                x, y = ok[int(len(ok) * 0.8)]
                                label(x, y, it["label"], it.get("pos", "NW" if y > 0 else "SE"))
                    elif "fill" in it:
                        a, b = num(it.get("from_x", x0)), num(it.get("to_x", x1))
                        f1, f2 = fn(it["fill"]), fn(it.get("to", "0"))
                        xs = [a + (b - a) * j / 200 for j in range(201)]
                        top = [(x, f1(x)) for x in xs]
                        bottom = [(x, f2(x)) for x in reversed(xs)]
                        zp.Polygon([p for p in top + bottom if math.isfinite(p[1])]).color("none").fill(FILL)
                    elif "implicit" in it:
                        zp.Implicit(fn(it["implicit"], ("x", "y")), xlim=(x0, x1), ylim=(y0, y1), n=160).color(
                            "black")
                    elif "param" in it:
                        fx, fy = fn(it["param"][0], ("t",)), fn(it["param"][1], ("t",))
                        t0, t1 = (num(v) for v in it.get("t", [0, 2 * math.pi]))
                        ts = [t0 + (t1 - t0) * j / 400 for j in range(401)]
                        polyline([(fx(t), fy(t)) for t in ts if math.isfinite(fx(t)) and math.isfinite(fy(t))],
                                 it.get("dashed"))
                    elif "point" in it:
                        x, y = pt(it["point"])
                        if it.get("open"):
                            zp.Polygon([(x + 3.5 / sx * math.cos(a), y + 3.5 / sy * math.sin(a))
                                        for a in (j * math.pi / 8 for j in range(16))]).color("black").fill("white")
                        else:
                            dot(x, y)
                        if it.get("label"):
                            label(x, y, it["label"], it.get("pos", "NE"))
                    elif "segment" in it:
                        s = zp.Segment(pt(it["segment"][0]), pt(it["segment"][1])).color("black")
                        if it.get("dashed"):
                            s.stroke("--")
                    elif "polygon" in it:
                        p = zp.Polygon([pt(q) for q in it["polygon"]]).color("black")
                        if it.get("shade"):
                            p.fill(FILL)
                    elif "circle" in it:
                        zp.Circle(pt(it["circle"]), num(it.get("r", 1))).color("black")
                    elif "vline" in it or "hline" in it:
                        line = zp.VLine(num(it["vline"])) if "vline" in it else zp.HLine(num(it["hline"]))
                        line.color("black").stroke("--" if it.get("dashed", True) else "-")
                    elif "vector" in it:
                        a, b = pt(it["vector"][0]), pt(it["vector"][1])
                        arrow(a, b)
                        if it.get("label"):
                            label((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, it["label"], it.get("pos", "NW"))
                    elif "text" in it:
                        x, y = pt(it["text"])
                        zp.Text(x, y, it.get("s", ""), halign=it.get("halign", "center"),
                                valign=it.get("valign", "center"))
                    elif "bars" in it:
                        w = num(it.get("width", 1))
                        for x, h in it["bars"]:
                            x, h = num(x), num(h)
                            zp.Polygon([(x - w / 2, 0), (x + w / 2, 0), (x + w / 2, h), (x - w / 2, h)]).color(
                                "black").fill(FILL)
                    else:
                        problems.append(f"item {i}: unknown kind {sorted(it)}")
                except Exception as e:  # one bad item never loses the whole figure
                    problems.append(f"item {i}: {type(e).__name__}: {str(e)[:80]}")
        return g.imagebytes("svg").decode(), problems

    def png(spec, width=520):
        """-> (png bytes, problems) at the given pixel width."""
        import pymupdf
        svg, problems = draw(spec)
        doc = pymupdf.open("svg", svg.encode())
        zoom = width / doc[0].rect.width
        return doc[0].get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("png"), problems

    def pdf_page(spec):
        """-> single-page PDF bytes (vector) for embedding in exported worksheets."""
        import pymupdf
        svg, _ = draw(spec)
        return pymupdf.open("svg", svg.encode()).convert_to_pdf()

    k.provide("figure.svg", draw)
    k.provide("figure.png", png)
    k.provide("figure.pdf", pdf_page)
