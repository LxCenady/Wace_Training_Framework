"""Formula sheet / data booklet. One job: keep the official reference sheet beside everything else.

A right-hand pane (drag its edge to resize; re-rendered sharp at every width) showing <subj>/papers/<year>_<subj>_<sheet>.pdf
for the sheets the subject's pack names. Two drop-downs: the installed subjects, and the years on this computer. It follows
whatever is selected — a past question gets the sheet of its own year (else the latest one before it); F2 hides it.
"""
import base64, glob, os, re
import tkinter as tk
from tkinter import ttk
import pymupdf
import subjects

SHARE = 0.26  # initial share of the window width
SHEET_NAME = {"FormulaSheet": "公式表", "DataBooklet": "数据手册"}


def setup(k):
    pane, C = k.get("ui.pane"), k.get("ui.colors")
    frame = ttk.Frame(pane)
    pane.add(frame, weight=0)
    english = k.get("config").get("language") == "en"
    names = subjects.names(k.root, "en" if english else "zh")  # installed subject packs, in pack order
    have = list(names)
    state = {"subj": None, "year": None, "doc": None, "width": 0, "job": None, "shown": True, "images": []}

    head = ttk.Frame(frame)
    head.pack(fill="x", padx=8, pady=(8, 4))
    heading = ttk.Label(head, text="公式表", style="H.TLabel")
    heading.pack(side="left")
    labels = {f"{s} · {names[s].removesuffix(' ATAR') if english else names[s].split()[-1]}": s
              for s in have}  # "MAM · 数学方法" / "MAM · Mathematics Methods"
    subj = tk.StringVar()
    pick_subj = ttk.Combobox(head, textvariable=subj, values=list(labels), state="readonly",
                             width=max(sum(2 if ord(c) > 0x2E80 else 1 for c in x) for x in labels) + 2 if labels else 12)  # CJK = 2 columns
    pick_subj.pack(side="left", padx=(10, 0))
    pick_subj.bind("<<ComboboxSelected>>", lambda e: switch(labels[subj.get()]))
    year = tk.StringVar()
    pick_year = ttk.Combobox(head, textvariable=year, state="readonly", width=6)
    pick_year.pack(side="left", padx=(6, 0))
    pick_year.bind("<<ComboboxSelected>>", lambda e: show(state["subj"], int(year.get())))
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

    def sheets(s):
        """{year: path} of the subject's reference sheets on this computer."""
        out = {}
        for sheet in subjects.info(s, k.root)["sheets"]:
            for path in glob.glob(os.path.join(k.root, s, "papers", f"*_{sheet}.pdf")):
                m = re.match(r"(\d{4})_", os.path.basename(path))
                if m:
                    out[int(m.group(1))] = path
        return out

    def sheet_name(s):
        kinds = subjects.info(s, k.root)["sheets"]
        return SHEET_NAME.get(kinds[0], kinds[0]) if kinds else "公式表"

    def render():
        state["job"] = None
        canvas.delete("all")
        state["images"].clear()
        doc = state["doc"]
        if doc is None:
            canvas.create_text(12, 12, anchor="nw", fill=C["muted"], width=max(200, state["width"] - 24),
                               text=f"本机还没有 {state['subj']} 的{sheet_name(state['subj'])}（导入真题后自动出现）。")
            return
        y, width = 6, max(200, state["width"] - 12)
        pages = [p for p in doc if len(p.get_text().split()) >= 40          # skip cover pages
                 and "table of contents" not in p.get_text().lower()] or list(doc)  # and a data booklet's contents
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

    def show(s, wanted=None):
        """Subject `s`, the sheet of year `wanted` (else the latest one before it, else the newest)."""
        if s not in names:
            return
        found = sheets(s)
        years = sorted(found, reverse=True)
        pick = next((y for y in years if wanted is None or y <= wanted), years[-1] if years else None)
        if (s, pick) == (state["subj"], state["year"]) and state["doc"] is not None:
            return
        state["subj"], state["year"] = s, pick
        subj.set(next(label for label, code in labels.items() if code == s))
        pick_year.configure(values=[str(y) for y in years])
        year.set(str(pick) if pick else "")
        heading.configure(text=sheet_name(s))
        state["doc"] = pymupdf.open(found[pick]) if pick else None
        title.configure(text=f"官方{sheet_name(s)} · 拖动左边缘调宽度" if pick else "")
        canvas.yview_moveto(0)
        schedule()

    def switch(s):  # kept for other plugins (formula.switch): the subject's newest sheet
        show(s)

    def follow(ref):
        """select.* events: a pattern list, a question id like 'MAS-2024A-Q9', or a generated item id."""
        if isinstance(ref, list) and ref:
            show(ref[0].split(".")[0], state["year"] if ref[0].split(".")[0] == state["subj"] else None)
        elif isinstance(ref, str):
            m = re.match(r"([A-Z]+)-(\d{4})", ref)
            show(ref.split("-")[0], int(m.group(2)) if m else None)
        elif isinstance(ref, int):
            item = k.get("store").generated(ref)
            if item["patterns"]:
                show(item["patterns"][0].split(".")[0])

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
    shown_first = k.get("config").get("tree.subject")  # the subject the knowledge tree opens on
    first = shown_first if shown_first in have else (k.get("store").subjects() or have or [None])[0]
    k.on("ui.ready", lambda: show(first) if first else None)
    k.provide("formula.switch", switch)
