"""我的 AI 题库. One job: an index of every generated question — grouped, searchable, sortable, openable.

Questions with exactly the same pattern tags fold into one group row (collapsed; expanded while searching).
Opening a question emits select.generated(gid); the AI view shows it with answers still hidden.
"""
import tkinter as tk
from tkinter import ttk

COLS = (("id", "#", 50), ("created", "时间", 130), ("difficulty", "难度", 120), ("section", "卷型", 50),
        ("marks", "分", 40), ("model", "模型", 130), ("stem", "题目开头", 460))
SECTION = {"CalcFree": "CF", "CalcAssumed": "CA"}
LEVEL_ORDER = {"基础": 0, "标准": 1, "拔高": 2}


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

    def load():
        """-> list of (group key, row values, searchable text)."""
        out = []
        for gid, created, pats, section, marks, provider, model, question, diff in store.generated_all():
            key = tuple(sorted(pats))
            stem = " ".join(question.split())
            row = (gid, created, diff or "标准", SECTION.get(section, section or ""), marks, model or provider,
                   stem[:160])
            out.append((key, row, " ".join(map(str, row)) + " " + " ".join(title(c) for c in key) + " " + stem))
        return out

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
        ttk.Label(bar, text="同标签折叠为一组 · 双击打开 · 点表头排序", style="Muted.TLabel").pack(side="right")

        body = ttk.Frame(page)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        table = ttk.Treeview(body, columns=[c for c, _, _ in COLS], show="tree headings", selectmode="browse")
        sb = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        table.heading("#0", text="知识点 / 题型标签")
        table.column("#0", width=380, stretch=False)
        data = load()
        order = {"col": "id", "desc": True}
        opened = set()

        def sort_key(row):
            i = [c for c, _, _ in COLS].index(order["col"])
            v = row[i]
            return LEVEL_ORDER.get(v, v) if order["col"] == "difficulty" else (v is None, v)

        def fill():
            q = query.get().strip().lower()
            groups = {}
            for key, row, text in data:
                if not q or q in text.lower():
                    groups.setdefault(key, []).append(row)
            for rows in groups.values():
                rows.sort(key=sort_key, reverse=order["desc"])
            table.delete(*table.get_children())
            # groups follow the order of their best row under the current sort
            for key in sorted(groups, key=lambda g: sort_key(groups[g][0]), reverse=order["desc"]):
                rows = groups[key]
                levels = {}
                for r in rows:
                    levels[r[2]] = levels.get(r[2], 0) + 1
                mix = " ".join(f"{lv}×{n}" for lv, n in sorted(levels.items(), key=lambda x: LEVEL_ORDER.get(x[0], 9)))
                gid = "grp:" + "|".join(key)
                table.insert("", "end", iid=gid, text="；".join(title(c) for c in key),
                             values=("", rows[0][1], mix, "", "", "", f"{len(rows)} 道"),
                             open=bool(q) or gid in opened)
                for r in rows:
                    table.insert(gid, "end", iid=str(r[0]), text=f"  AI #{r[0]}", values=r)
            hits = sum(len(r) for r in groups.values())
            count.configure(text=f"{hits} / {len(data)} 道 · {len(groups)} 组" if data else
                            "还没有 AI 题：在知识图谱选题型后点「AI 生成相似题」")

        def sort_by(col):
            order["desc"] = not order["desc"] if order["col"] == col else col in ("id", "created", "marks")
            order["col"] = col
            fill()

        for col, head, width in COLS:
            table.heading(col, text=head, command=lambda c=col: sort_by(c))
            table.column(col, width=width, stretch=col == "stem", anchor="w")

        def open_row(event):
            sel = table.selection()
            if sel and sel[0].isdigit():
                k.emit("select.generated", int(sel[0]))
            elif sel and event.keysym == "Return":  # group row (double-click already toggles it natively)
                table.item(sel[0], open=not table.item(sel[0], "open"))

        table.bind("<<TreeviewOpen>>", lambda e: opened.add(table.focus()))
        table.bind("<<TreeviewClose>>", lambda e: opened.discard(table.focus()))
        table.bind("<Double-1>", open_row)
        table.bind("<Return>", open_row)
        query.trace_add("write", lambda *_: fill())
        fill()
        entry.focus_set()

    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="我的 AI 题库", command=show, accelerator="Ctrl+B")
    k.get("ui.menu").add_cascade(label="题库", menu=menu)
    k.get("ui.root").bind_all("<Control-b>", lambda e: show())
    ttk.Button(k.get("ui.left"), text="我的 AI 题库", command=show).pack(side="bottom", fill="x", padx=10, pady=(0, 8))
    k.provide("mybank.show", show)
