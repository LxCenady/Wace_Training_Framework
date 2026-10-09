"""Formula sheet. One job: keep the official formula sheet beside everything else.

A right-hand pane (drag its edge to resize; re-rendered sharp at every width) showing the newest
<subj>/papers/*_FormulaSheet.pdf. Follows the subject of whatever is selected; switch by hand too; F2 hides it.
"""
import base64, glob, os, re
import tkinter as tk
from tkinter import ttk
import pymupdf

SHARE = 0.26  # initial share of the window width


def setup(k):
    pane, C = k.get("ui.pane"), k.get("ui.colors")
    frame = ttk.Frame(pane)
    pane.add(frame, weight=0)
    state = {"subj": "MAM", "doc": None, "path": None, "width": 0, "job": None, "shown": True, "images": []}

    head = ttk.Frame(frame)
    head.pack(fill="x", padx=8, pady=(8, 4))
    ttk.Label(head, text="公式表", style="H.TLabel").pack(side="left")
    subj = tk.StringVar(value="MAM")
    for s in ("MAM", "MAS"):
        ttk.Radiobutton(head, text=s, value=s, variable=subj, command=lambda: switch(subj.get())).pack(side="left",
                                                                                                    padx=(8, 0))
    title = ttk.Label(frame, style="Muted.TLabel")
    title.pack(anchor="w", padx=10)

    body = ttk.Frame(frame)
    body.pack(fill="both", expand=True, pady=(4, 0))
    canvas = tk.Canvas(body, bg=C["panel"], highlightthickness=0)
    bar = ttk.Scrollbar(body, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=bar.set)
    bar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    wheel = lambda e: canvas.yview_scroll(int(-e.delta / 120), "units")  # noqa: E731
    canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", wheel))
    canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

    def newest(s):
        files = glob.glob(os.path.join(k.root, s, "papers", "*_FormulaSheet.pdf"))
        year = lambda f: int(re.match(r"(\d{4})", os.path.basename(f)).group(1))  # noqa: E731
        return max(files, key=year) if files else None

    def render():
        state["job"] = None
        canvas.delete("all")
        state["images"].clear()
        doc = state["doc"]
        if doc is None:
            canvas.create_text(12, 12, anchor="nw", fill=C["muted"], width=max(200, state["width"] - 24),
                               text=f"本机还没有 {state['subj']} 的公式表（导入真题后自动出现）。")
            return
        y, width = 6, max(200, state["width"] - 12)
        pages = [p for p in doc if len(p.get_text().split()) >= 40] or list(doc)  # skip cover / index pages
        for page in pages:
            zoom = width / page.rect.width
            png = page.get_pixmap(matrix=pymupdf.Matrix(zoom, zoom)).tobytes("png")
            img = tk.PhotoImage(data=base64.b64encode(png))
            state["images"].append(img)
            canvas.create_image(6, y, anchor="nw", image=img)
            y += img.height() + 8
        canvas.configure(scrollregion=(0, 0, width, y))

    def schedule():
        if state["job"]:
            canvas.after_cancel(state["job"])
        state["job"] = canvas.after(120, render)  # re-render once dragging pauses

    def on_resize(e):
        if abs(e.width - state["width"]) > 4:
            state["width"] = e.width
            schedule()

    def switch(s):
        if s == state["subj"] and state["doc"] is not None:
            return
        state["subj"] = s
        subj.set(s)
        path = newest(s)
        state["doc"] = pymupdf.open(path) if path else None
        title.configure(text=f"{os.path.basename(path)[:4]} {s} 官方公式表 · 拖动左边缘调宽度" if path else "")
        canvas.yview_moveto(0)
        schedule()

    def follow(ref):
        """select.* events: a pattern list, a question id like 'MAS-2024A-Q9', or a generated item id."""
        if isinstance(ref, list) and ref:
            switch(ref[0].split(".")[0])
        elif isinstance(ref, str):
            switch(ref.split("-")[0])
        elif isinstance(ref, int):
            item = k.get("store").generated(ref)
            if item["patterns"]:
                switch(item["patterns"][0].split(".")[0])

    def toggle(_=None):
        if state["shown"]:
            pane.forget(frame)
        else:
            pane.add(frame, weight=0)
            k.get("ui.root").after(50, lambda: pane.sashpos(len(pane.panes()) - 2, int(pane.winfo_width() * (1 - SHARE))))
        state["shown"] = not state["shown"]
        shown.set(state["shown"])

    canvas.bind("<Configure>", on_resize)
    k.on("ui.layout", lambda p, width: p.sashpos(len(p.panes()) - 2, int(width * (1 - SHARE))))
    for event in ("select.pattern", "select.question", "select.generated"):
        k.on(event, follow)
    shown = tk.BooleanVar(value=True)
    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_checkbutton(label="公式表", variable=shown, command=lambda: (shown.set(state["shown"]), toggle()),
                         accelerator="F2")
    k.get("ui.menu").add_cascade(label="视图", menu=menu)
    k.get("ui.root").bind_all("<F2>", toggle)
    k.on("ui.ready", lambda: switch("MAM"))
    k.provide("formula.switch", switch)
