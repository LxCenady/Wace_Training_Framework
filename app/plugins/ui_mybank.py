"""我的 AI 题库. One job: an index of every generated question — search, sort, open.

Opening a row emits select.generated(gid); the AI view shows the question with answers still hidden.
"""
import tkinter as tk
from tkinter import ttk

COLS = (("id", "#", 50), ("created", "时间", 130), ("subject", "科目", 55), ("patterns", "题型", 330),
        ("section", "卷型", 70), ("marks", "分", 40), ("model", "模型", 140), ("stem", "题目开头", 420))
SECTION = {"CalcFree": "CF", "CalcAssumed": "CA"}


def setup(k):
    store = k.get("store")
    titles = {}

    def title(code):
        if code not in titles:
            try:
                titles[code] = f"{code} {store.pattern(code)['title'].split('★')[0].split('（')[0].strip()}"
            except IndexError:  # pattern no longer in wace.db
                titles[code] = code
        return titles[code]

    def rows():
        for gid, created, pats, section, marks, provider, model, question in store.generated_all():
            stem = " ".join(question.split())
            yield (gid, created, pats[0].split(".")[0] if pats else "", "；".join(title(c) for c in pats),
                   SECTION.get(section, section or ""), marks, model or provider, stem[:160])

    def show():
        page = k.get("ui.tab")("mybank", "我的 AI 题库")
        bar = ttk.Frame(page)
        bar.pack(fill="x", padx=10, pady=8)
        query = tk.StringVar()
        ttk.Label(bar, text="搜索").pack(side="left")
        entry = ttk.Entry(bar, textvariable=query, width=40)
        entry.pack(side="left", padx=6)
        count = ttk.Label(bar, style="Muted.TLabel")
        count.pack(side="left", padx=8)
        ttk.Label(bar, text="双击打开 · 点表头排序 · 搜索题型、科目、模型或题目文字",
                  style="Muted.TLabel").pack(side="right")

        body = ttk.Frame(page)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        table = ttk.Treeview(body, columns=[c for c, _, _ in COLS], show="headings", selectmode="browse")
        sb = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        data = list(rows())
        order = {"col": "id", "desc": True}

        def fill():
            q = query.get().strip().lower()
            hit = [r for r in data if not q or q in " ".join(map(str, r)).lower()]
            i = [c for c, _, _ in COLS].index(order["col"])
            hit.sort(key=lambda r: (r[i] is None, r[i]), reverse=order["desc"])
            table.delete(*table.get_children())
            for r in hit:
                table.insert("", "end", iid=str(r[0]), values=r)
            count.configure(text=f"{len(hit)} / {len(data)} 道")

        def sort_by(col):
            order["desc"] = not order["desc"] if order["col"] == col else col in ("id", "created", "marks")
            order["col"] = col
            fill()

        for col, head, width in COLS:
            table.heading(col, text=head, command=lambda c=col: sort_by(c))
            table.column(col, width=width, stretch=col == "stem", anchor="w")

        def open_row(_=None):
            sel = table.selection()
            if sel:
                k.emit("select.generated", int(sel[0]))

        table.bind("<Double-1>", open_row)
        table.bind("<Return>", open_row)
        query.trace_add("write", lambda *_: fill())
        fill()
        entry.focus_set()
        if not data:
            count.configure(text="还没有 AI 题：在知识图谱选题型后点「AI 生成相似题」")

    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="我的 AI 题库", command=show, accelerator="Ctrl+B")
    k.get("ui.menu").add_cascade(label="题库", menu=menu)
    k.get("ui.root").bind_all("<Control-b>", lambda e: show())
    ttk.Button(k.get("ui.left"), text="我的 AI 题库", command=show).pack(side="bottom", fill="x", padx=10, pady=(0, 8))
    k.provide("mybank.show", show)
