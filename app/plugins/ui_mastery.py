"""掌握度地图. One job: one tile per pattern — colour = how well you do on it, number = how much it is worth.

Mastery = 1 − marks lost / marks attempted (a part counts as attempted once its answer was revealed).
Grey = not attempted yet. The number on a tile is the marks that pattern carried across all past papers,
so weak-and-important patterns stand out. Click: method notes; right-click: practise it.
"""
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk

TILE_W, TILE_H, GAP = 168, 54, 6


def colour(rate):
    """0 -> red, 0.5 -> amber, 1 -> green (muted, readable with dark text)."""
    stops = ((0.0, (222, 120, 110)), (0.5, (236, 196, 110)), (1.0, (130, 190, 130)))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if rate <= b:
            t = (rate - a) / (b - a)
            return "#%02x%02x%02x" % tuple(int(x + (y - x) * t) for x, y in zip(ca, cb))
    return "#%02x%02x%02x" % stops[-1][1]


def setup(k):
    store, root, C = k.get("store"), k.get("ui.root"), k.get("ui.colors")

    tile_font = tkfont.Font(family="Microsoft YaHei UI", size=9)

    def fit(text, width):
        """Cut to one line of `width` pixels, with an ellipsis."""
        if tile_font.measure(text) <= width:
            return text
        while text and tile_font.measure(text + "…") > width:
            text = text[:-1]
        return text + "…"

    def show():
        page = k.get("ui.tab")("mastery", "掌握度")
        head = ttk.Frame(page, padding=(12, 8))
        head.pack(fill="x")
        subj = tk.StringVar(value=k.get("mastery.subject", "MAM"))
        ttk.Label(head, text="掌握度地图", style="H.TLabel").pack(side="left")
        for s in ("MAM", "MAS"):
            ttk.Radiobutton(head, text=s, value=s, variable=subj,
                            command=lambda: (k.provide("mastery.subject", subj.get()), show())).pack(side="left",
                                                                                                padx=(10, 0))
        ttk.Label(head, text="颜色 = 你的得分率（灰 = 还没做过）· 数字 = 历年真卷中该题型的总分 · 单击看讲解 · 右键出题",
                  style="Muted.TLabel").pack(side="right")
        stats = store.mastery()
        weights = store.exam_weights(subj.get())
        canvas = tk.Canvas(page, bg=C["panel"], highlightthickness=0)
        bar = ttk.Scrollbar(page, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=bar.set)
        bar.pack(side="right", fill="y")
        canvas.pack(fill="both", expand=True)
        tiles = {}

        def draw(_=None):
            canvas.delete("all")
            tiles.clear()
            per_row = max(1, (canvas.winfo_width() - 24) // (TILE_W + GAP))
            y = 10
            for tcode, zh, en, n in store.topics(subj.get()):
                canvas.create_text(12, y, anchor="nw", text=f"{zh}", font=("Microsoft YaHei UI", 11, "bold"),
                                   fill=C["accent"])
                y += 24
                pats = sorted(store.patterns(tcode), key=lambda p: -weights.get(p[0], 0))
                for i, (code, num, title, cnt) in enumerate(pats):
                    x0 = 12 + (i % per_row) * (TILE_W + GAP)
                    y0 = y + (i // per_row) * (TILE_H + GAP)
                    s = stats.get(code)
                    tried = s and s["attempted"] > 0
                    rate = max(0.0, 1 - s["lost"] / s["attempted"]) if tried else None
                    fill = colour(rate) if tried else "#e4ded2"
                    tag = f"t:{code}"
                    canvas.create_rectangle(x0, y0, x0 + TILE_W, y0 + TILE_H, fill=fill, outline=C["line"], tags=tag)
                    label = fit(f"{num}. {title.split('★')[0].split('（')[0].strip()}", TILE_W - 12)
                    canvas.create_text(x0 + 6, y0 + 5, anchor="nw", tags=tag, text=label,
                                       font=("Microsoft YaHei UI", 9), fill=C["ink"])
                    note = f"{rate:.0%} · 做过 {s['parts']} 问" if tried else "未做"
                    canvas.create_text(x0 + 6, y0 + TILE_H - 6, anchor="sw", tags=tag, text=note,
                                       font=("Microsoft YaHei UI", 8), fill=C["ink"])
                    canvas.create_text(x0 + TILE_W - 6, y0 + TILE_H - 6, anchor="se", tags=tag,
                                       text=f"{weights.get(code, 0)} 分", font=("Microsoft YaHei UI", 8, "bold"),
                                       fill=C["accent"])
                    tiles[tag] = code
                y += ((len(pats) + per_row - 1) // per_row) * (TILE_H + GAP) + 10
            canvas.configure(scrollregion=(0, 0, canvas.winfo_width(), y + 10))

        def hit(e):
            for t in canvas.gettags(canvas.find_closest(canvas.canvasx(e.x), canvas.canvasy(e.y))):
                if t in tiles:
                    return tiles[t]

        def click(e):
            code = hit(e)
            if code:
                k.emit("select.pattern", [code])

        def menu(e):
            code = hit(e)
            if not code:
                return
            m = tk.Menu(root, tearoff=False)
            for level in ("基础", "标准", "拔高"):
                m.add_command(label=f"针对 {store.pattern_name(code)} 出 3 道{level}题",
                              command=lambda lv=level: k.get("generator.start")([code], "any", 0, lv, 3))
            m.tk_popup(e.x_root, e.y_root)

        canvas.bind("<Configure>", draw)
        canvas.bind("<Button-1>", click)
        canvas.bind("<Button-3>", menu)
        wheel = lambda e: canvas.yview_scroll(int(-e.delta / 120), "units")  # noqa: E731
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))
        k.provide("mastery.canvas", canvas)

    def refresh():
        tab = k.get("ui.tab.frame")("mastery")
        if tab is not None and k.get("ui.tabs").select() == str(tab):
            show()

    k.on("mistakes.changed", refresh)
    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="掌握度地图", command=show, accelerator="Ctrl+G")
    k.get("ui.menu").add_cascade(label="掌握度", menu=menu)
    root.bind_all("<Control-g>", lambda e: show())
    k.provide("mastery.show", show)
