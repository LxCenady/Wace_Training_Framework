"""我的 AI 题库. One job: an index of every generated question — grouped, searchable, sortable, openable.

The index follows the knowledge tree: subject -> unit -> pattern -> questions, in the tree's order, showing only
nodes that hold questions (collapsed; expanded while searching). A question sits once, under its lead pattern
(the first of its tags: the one the setter was given first, or the one carrying most marks in a unit question);
its other patterns are listed in their own column. Opening a question emits select.generated(gid); the AI view
shows it with answers still hidden.
"""
import os, time
import tkinter as tk
from tkinter import filedialog, ttk
import plat

COLS = (("id", "#", 50), ("created", "时间", 130), ("difficulty", "难度", 120), ("section", "卷型", 50),
        ("marks", "分", 40), ("also", "其他题型", 150), ("model", "模型", 120), ("stem", "题目开头", 420))
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
        for gid, created, pats, section, marks, provider, model, question, diff, focus in store.generated_all():
            stem = " ".join(k.get("math.plain", lambda s: s)(question).split())
            row = (gid, created, (diff or "标准") + ("·错题加强" if focus else ""), SECTION.get(section, section or ""),
                   marks, " ".join(pats[1:]), model or provider, stem[:160])
            out.append((pats[0] if pats else "?", row, " ".join(map(str, row)) + " " + " ".join(title(c) for c in pats)
                        + " " + stem))
        return out

    def layout():
        """[(subject, name, [(unit code, unit name, [pattern codes])])] in the knowledge tree's order."""
        names = {"MAM": "Mathematics Methods 数学方法", "MAS": "Mathematics Specialist 专业数学"}
        return [(subj, names.get(subj, subj), [(code, zh, [p for p, *_ in store.patterns(code)])
                                               for code, zh, *_ in store.topics(subj)])
                for subj in store.subjects()]

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
        ttk.Button(bar, text="导出练习卷 PDF", command=lambda: export()).pack(side="right")
        ttk.Label(bar, text="按知识图谱归类 · 双击打开 · 点表头排序 · 选中单元/题型可整组导出", style="Muted.TLabel").pack(
            side="right", padx=8)

        body = ttk.Frame(page)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        table = ttk.Treeview(body, columns=[c for c, _, _ in COLS], show="tree headings", selectmode="extended")
        sb = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        table.heading("#0", text="科目 / 单元 / 题型")
        table.column("#0", width=380, stretch=False)
        data, shape = load(), layout()
        order = {"col": "id", "desc": True}
        opened = set()

        def sort_key(row):
            i = [c for c, _, _ in COLS].index(order["col"])
            v = row[i]
            return (LEVEL_ORDER.get(str(v)[:2], 9), str(v)) if order["col"] == "difficulty" else (v is None, v)

        def fill():
            q = query.get().strip().lower()
            by_pattern = {}
            for lead, row, text in data:
                if not q or q in text.lower():
                    by_pattern.setdefault(lead, []).append(row)
            for rows in by_pattern.values():
                rows.sort(key=sort_key, reverse=order["desc"])
            table.delete(*table.get_children())
            placed = set()

            def node(parent, iid, text, rows):
                table.insert(parent, "end", iid=iid, text=text, values=("", "", "", "", "", "", "", f"{len(rows)} 道"),
                             open=bool(q) or iid in opened)

            def pattern_node(parent, code, rows):
                levels = {}
                for r in rows:
                    levels[r[2]] = levels.get(r[2], 0) + 1
                mix = " ".join(f"{lv}×{n}" for lv, n in sorted(levels.items(),
                                                              key=lambda x: (LEVEL_ORDER.get(x[0][:2], 9), x[0])))
                iid = "pat:" + code
                table.insert(parent, "end", iid=iid, text=title(code), values=("", "", mix, "", "", "", "", f"{len(rows)} 道"),
                             open=bool(q) or iid in opened)
                for r in rows:
                    table.insert(iid, "end", iid=str(r[0]), text=f"  AI #{r[0]}", values=r)

            for subj, sname, units in shape:
                in_subj = [(u, n, [p for p in ps if p in by_pattern]) for u, n, ps in units]
                in_subj = [(u, n, ps) for u, n, ps in in_subj if ps]
                if not in_subj:
                    continue
                node("", "subj:" + subj, sname, [r for _, _, ps in in_subj for p in ps for r in by_pattern[p]])
                for u, uname, ps in in_subj:
                    node("subj:" + subj, "unit:" + u, f"{uname}", [r for p in ps for r in by_pattern[p]])
                    for p in ps:
                        pattern_node("unit:" + u, p, by_pattern[p])
                        placed.add(p)
            rest = [p for p in by_pattern if p not in placed]  # tags no longer in wace.db
            if rest:
                node("", "subj:?", "其他", [r for p in rest for r in by_pattern[p]])
                for p in rest:
                    pattern_node("subj:?", p, by_pattern[p])
            hits = sum(len(r) for r in by_pattern.values())
            count.configure(text=f"{hits} / {len(data)} 道 · {len(by_pattern)} 个题型" if data else
                            "还没有 AI 题：在知识图谱选单元或题型后点「AI 生成相似题」")

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

        def export():
            """Selected questions (a selected subject / unit / pattern = everything under it); nothing selected =
            everything currently listed."""
            def leaves(iid):
                return [iid] if iid.isdigit() else [x for c in table.get_children(iid) for x in leaves(c)]

            picked = []
            for iid in table.selection() or table.get_children():
                for one in leaves(iid):
                    if int(one) not in picked:
                        picked.append(int(one))
            if not picked or not k.get("export.worksheet", None):
                count.configure(text="没有可导出的题")
                return
            path = filedialog.asksaveasfilename(
                title="导出练习卷", defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
                initialfile=f"WTF练习卷_{time.strftime('%Y%m%d_%H%M')}.pdf")
            if not path:
                return
            q, a = k.get("export.worksheet")(picked, path, f"WTF 练习卷 · {len(picked)} 题")
            count.configure(text=f"已导出 {len(picked)} 题：{os.path.basename(q)} + {os.path.basename(a)}")
            plat.open_file(q)

        k.provide("mybank.export", export)
        query.trace_add("write", lambda *_: fill())
        fill()
        entry.focus_set()

    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="我的 AI 题库", command=show, accelerator="Ctrl+B")
    k.get("ui.menu").add_cascade(label="题库", menu=menu)
    plat.shortcut(k.get("ui.root"), "b", lambda e: show())
    ttk.Button(k.get("ui.left"), text="我的 AI 题库", command=show).pack(side="bottom", fill="x", padx=10, pady=(0, 8))
    k.provide("mybank.show", show)
