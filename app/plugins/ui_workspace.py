"""工作区. One job: a basket of past and AI questions, filled by dragging, exported as one paper.

The lower half of the middle column. Questions are dragged in from the knowledge tree, 真题搜索 and 我的 AI 题库,
the way Windows Explorer works: dragging from an unselected row sweeps a selection, Ctrl / Shift select
precisely, dragging from a selected row carries the whole selection. In the 工作区: drag to reorder, Delete /
right-click to remove, Ctrl+A to select all, double-click to open, 全部清空 to start again; the list survives a
restart (generated.db). 合并导出 writes one question paper + one answers-and-keys PDF in this order.
出卷模式 counts CF and CA marks against a real paper of the subject (store.paper_totals) and lights the export
button once both are within TOL marks; the export is then one CF paper and one CA paper, with WACE timing.

Provides workspace.source(treeview, refs_of, sweep=True): make another list a drag source, refs_of(selection)
-> [("past", qid) | ("gen", gid)].
"""
import time
import tkinter as tk
from tkinter import ttk
import plat

COLS = (("n", "#", 40), ("kind", "来源", 56), ("label", "题目", 120), ("section", "卷型", 48), ("marks", "分", 40),
        ("patterns", "题型", 520))
SEC = {"CalcFree": "CF", "CalcAssumed": "CA"}
SEC_NAME = {"CalcFree": "计算器禁用 (Calculator-free)", "CalcAssumed": "计算器允许 (Calculator-assumed)"}
TIMES = {"CalcFree": (5, 50), "CalcAssumed": (10, 100)}  # WACE reading + working minutes
TOL = 3  # 出卷模式: a section is ready within this many marks of a real paper
MOVE = 6  # pixels the pointer must travel before a press becomes a drag


def visible_rows(tree, parent=""):
    """Rows in display order (children of open rows only)."""
    out = []
    for iid in tree.get_children(parent):
        out.append(iid)
        if tree.item(iid, "open"):
            out += visible_rows(tree, iid)
    return out


def setup(k):
    store, C, root = k.get("store"), k.get("ui.colors"), k.get("ui.root")
    middle = k.get("ui.middle")
    items = [tuple(r) for r in store.workspace() if store.item_info(*r)]
    info_cache = {}

    def info(ref):
        if ref not in info_cache:
            info_cache[ref] = store.item_info(*ref)
        return info_cache[ref]

    st = ttk.Style()
    st.configure("Ready.TButton", foreground="#ffffff", background=C["ok"])
    st.map("Ready.TButton", background=[("active", C["ok"])])
    for name, colour in (("Ws", C["accent"]), ("WsOk", C["ok"])):  # meters: blue while filling, green when ready
        st.configure(f"{name}.Horizontal.TProgressbar", background=colour, troughcolor=C["line"], borderwidth=0,
                     lightcolor=colour, darkcolor=colour)

    frame = ttk.Frame(middle)
    middle.add(frame, weight=1)
    head = ttk.Frame(frame)
    head.pack(fill="x", padx=8, pady=(6, 2))
    ttk.Label(head, text="工作区", style="H.TLabel").pack(side="left")
    count = ttk.Label(head, style="Muted.TLabel")
    count.pack(side="left", padx=8)
    paper = tk.BooleanVar(value=False)
    ttk.Checkbutton(head, text="出卷模式", variable=paper).pack(side="left", padx=8)
    paper.trace_add("write", lambda *_: refresh())
    bars = ttk.Frame(frame)  # 出卷模式: one row of CF / CA meters under the header
    meters = {}
    for sec in ("CalcFree", "CalcAssumed"):
        ttk.Label(bars, text=SEC_NAME[sec].split(" ")[0]).pack(side="left", padx=(0, 4))
        bar = ttk.Progressbar(bars, length=200, style="Ws.Horizontal.TProgressbar")
        bar.pack(side="left")
        lbl = tk.Label(bars, width=16, anchor="w", bg=C["bg"], fg=C["muted"])
        lbl.pack(side="left", padx=(6, 18))
        meters[sec] = (bar, lbl)
    clear_btn = ttk.Button(head, text="全部清空", command=lambda: clear_all())
    clear_btn.pack(side="right")
    export_btn = ttk.Button(head, text="合并导出", command=lambda: export())
    export_btn.pack(side="right", padx=6)
    note = ttk.Label(frame, style="Muted.TLabel", text=(
        "把知识图谱、真题搜索、我的 AI 题库里选中的题拖到这里 · 从未选中的行拖 = 滑动多选，Ctrl / Shift = 精确多选 · "
        "拖动调整顺序 · 右键或 Delete 删除 · Ctrl+A 全选 · 双击打开"))
    note.pack(anchor="w", padx=8)
    body = ttk.Frame(frame)
    body.pack(fill="both", expand=True, padx=8, pady=(2, 6))
    table = ttk.Treeview(body, columns=[c for c, _, _ in COLS], show="headings", selectmode="extended", height=6)
    sb = ttk.Scrollbar(body, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    table.pack(side="left", fill="both", expand=True)
    for col, text, width in COLS:
        table.heading(col, text=text)
        table.column(col, width=width, stretch=col == "patterns", anchor="w")
    table.tag_configure("drop", background="#e3ebf8")

    def subject():
        subs = [info(r)["subject"] for r in items]
        return max(set(subs), key=subs.count) if subs else ""

    def refresh(select=()):
        table.delete(*table.get_children())
        sums = {"CalcFree": 0, "CalcAssumed": 0}
        unknown = 0
        for n, ref in enumerate(items, 1):
            d = info(ref)
            if d["section"] in sums:
                sums[d["section"]] += d["marks"] or 0
            else:
                unknown += 1
            table.insert("", "end", iid=f"{ref[0]}|{ref[1]}", values=(
                n, "真题" if ref[0] == "past" else "AI", d["label"], SEC.get(d["section"], "?"), d["marks"],
                "；".join(store.pattern_name(p) for p in d["patterns"])))
        for iid in select:
            if table.exists(iid):
                table.selection_add(iid)
        total = sum(info(r)["marks"] or 0 for r in items)
        count.configure(text=f"{len(items)} 题 · {total} 分" if items else "空：把题拖进来")
        subj = subject()
        ready = False
        if paper.get():
            bars.pack(fill="x", padx=8, pady=(0, 2), after=head)
            target = store.paper_totals(subj) if subj else {}
            ready = bool(items) and not unknown and all(
                abs(sums[s] - target.get(s, 0)) <= TOL for s in sums)
            for sec, (bar, lbl) in meters.items():
                goal = target.get(sec, 0) or 1
                bar.configure(maximum=goal, value=min(sums[sec], goal))
                gap = sums[sec] - target.get(sec, 0)
                fine = target.get(sec) and abs(gap) <= TOL
                bar.configure(style="WsOk.Horizontal.TProgressbar" if fine else "Ws.Horizontal.TProgressbar")
                lbl.configure(text=f"{sums[sec]} / {target.get(sec, '?')} 分  " + (
                    "✓ 已凑齐" if fine else f"还差 {-gap}" if gap < 0 else f"多了 {gap}"),
                    fg=C["ok"] if fine else C["muted"])
            mixed = len({info(r)["subject"] for r in items}) > 1
            warn = ("  混了 MAM 和 MAS" if mixed else "") + (f"  {unknown} 题没有卷型" if unknown else "")
            count.configure(text=count.cget("text") + f" · {subj}{warn}")
            export_btn.configure(text="导出试卷（CF 卷 + CA 卷）", style="Ready.TButton" if ready else "TButton")
        else:
            bars.pack_forget()
            export_btn.configure(text="合并导出", style="TButton")

    def save(select=()):
        store.save_workspace(items)
        refresh(select)

    def add(refs, at=None):
        new = [tuple(r) for r in refs if tuple(r) not in items and info(tuple(r))]
        if not new:
            k.get("ui.status")("这些题已经在工作区里了")
            return
        at = len(items) if at is None else at
        items[at:at] = new
        save([f"{a}|{b}" for a, b in new])
        k.get("ui.status")(f"已加入工作区：{len(new)} 道题")

    def move(refs, at):
        refs = [r for r in refs if r in items]
        before = sum(1 for r in items[:at] if r in refs)
        rest = [r for r in items if r not in refs]
        at -= before
        rest[at:at] = refs
        items[:] = rest
        save([f"{a}|{b}" for a, b in refs])

    def remove(iids):
        drop = {tuple(i.split("|", 1)) for i in iids}
        items[:] = [r for r in items if r not in drop]
        save()

    def clear_all():
        if items:
            items.clear()
            save()

    def refs_of_table(sel):
        return [tuple(i.split("|", 1)) for i in sel]

    def drop_index(y_root):
        """Insert position for a drop at screen y: before the row under the pointer, else at the end."""
        row = table.identify_row(y_root - table.winfo_rooty())
        return table.index(row) if row else len(items)

    def over_workspace(x, y):
        """Is the screen point inside the 工作区 (by geometry: no dependence on which window the OS puts on top)?"""
        fx, fy = frame.winfo_rootx(), frame.winfo_rooty()
        return frame.winfo_ismapped() and fx <= x < fx + frame.winfo_width() and fy <= y < fy + frame.winfo_height()

    # ---- drag and drop (inside the app; Explorer-like)
    ghost = {"win": None, "mark": None}

    def ghost_show(text, x, y):
        if ghost["win"] is None:
            g = tk.Toplevel(root)
            g.overrideredirect(True)
            g.attributes("-topmost", True)
            tk.Label(g, text=text, bg=C["accent"], fg="#ffffff", padx=8, pady=3).pack()
            ghost["win"] = g
        ghost["win"].geometry(f"+{x + 14}+{y + 10}")
        if ghost["mark"] and table.exists(ghost["mark"]):
            table.item(ghost["mark"], tags=())
        ghost["mark"] = None
        if over_workspace(x, y):
            row = table.identify_row(y - table.winfo_rooty())
            if row:
                table.item(row, tags=("drop",))
                ghost["mark"] = row

    def ghost_hide():
        if ghost["win"] is not None:
            ghost["win"].destroy()
        if ghost["mark"] and table.exists(ghost["mark"]):
            table.item(ghost["mark"], tags=())
        ghost.update(win=None, mark=None)

    def source(tree, refs_of, sweep=True):
        """Make `tree` a drag source (see the module docstring)."""
        s = {}

        def press(e):
            s.clear()
            row = tree.identify_row(e.y)
            if not row or e.state & 0x0005:  # empty space, or Shift / Ctrl held: the normal selection rules
                return None
            s.update(row=row, x=e.x_root, y=e.y_root, dragging=False)
            if row in tree.selection():
                s["mode"] = "drag"
                tree.focus_set()  # what the skipped class binding would do (Delete, Ctrl+A need the focus)
                return "break"  # keep a multi-selection for dragging (a plain click is settled on release)
            s["mode"] = "sweep" if sweep else "drag-one"
            return None  # the class binding selects the row

        def motion(e):
            if not s:
                return None
            far = abs(e.x_root - s["x"]) + abs(e.y_root - s["y"]) > MOVE
            if s["mode"] == "sweep":
                if far:  # select every visible row between the pressed one and the pointer
                    row = tree.identify_row(e.y)
                    order = visible_rows(tree)
                    if row in order and s["row"] in order:
                        i, j = sorted((order.index(s["row"]), order.index(row)))
                        tree.selection_set(order[i:j + 1])
                return "break"
            if s["mode"] in ("drag", "drag-one") and (far or s["dragging"]):
                refs = refs_of(tree.selection())
                if not refs:
                    return None
                s["dragging"] = True
                ghost_show(f"＋ {len(refs)} 道题", e.x_root, e.y_root)
                return "break"
            return None

        def release(e):
            if not s:
                return None
            mode, dragging, row = s.get("mode"), s.get("dragging"), s.get("row")
            s.clear()
            if dragging:
                ghost_hide()
                refs = refs_of(tree.selection())
                if over_workspace(e.x_root, e.y_root) and refs:
                    at = drop_index(e.y_root)
                    move(refs, at) if tree is table else add(refs, at)
                return "break"
            if mode == "drag":  # a click on a selected row without moving: select just that row (Explorer)
                tree.selection_set(row)
                tree.focus(row)
            return None

        tree.bind("<ButtonPress-1>", press, add="+")
        tree.bind("<B1-Motion>", motion, add="+")
        tree.bind("<ButtonRelease-1>", release, add="+")

    source(table, refs_of_table)

    def tree_refs(sel):  # knowledge tree: question rows only (Q: past, G: AI)
        out = []
        for iid in sel:
            kind, rest = iid.split(":", 1)
            if kind in "QG" and "|" in rest:
                out.append(("past" if kind == "Q" else "gen", rest.split("|", 1)[1]))
        return out

    tree = k.get("tree.widget", None)
    if tree is not None:
        source(tree, tree_refs, sweep=False)

    # ---- Explorer keys and menu
    def open_row(_=None):
        sel = table.selection()
        if sel:
            kind, ref = sel[0].split("|", 1)
            k.emit("select.question" if kind == "past" else "select.generated", ref if kind == "past" else int(ref))

    menu = tk.Menu(root, tearoff=False)

    def context(e):
        row = table.identify_row(e.y)
        if row and row not in table.selection():
            table.selection_set(row)
        menu.delete(0, "end")
        if table.selection():
            menu.add_command(label="打开", command=open_row)
            menu.add_command(label=f"删除所选（{len(table.selection())}）",
                             command=lambda: remove(table.selection()))
            menu.add_separator()
        menu.add_command(label="全部清空", command=clear_all)
        menu.tk_popup(e.x_root, e.y_root)

    plat.on_right_click(table, context)
    table.bind("<Delete>", lambda e: remove(table.selection()))
    table.bind("<BackSpace>", lambda e: remove(table.selection()))
    table.bind(f"<{plat.MOD}-a>", lambda e: (table.selection_set(table.get_children()), "break")[1])
    table.bind("<Double-1>", open_row)
    table.bind("<Return>", open_row)

    def export():
        if not items:
            k.get("ui.status")("工作区是空的：先把题拖进来")
            return
        stamp = time.strftime("%Y%m%d_%H%M")
        done = []
        if paper.get():
            subj = subject()
            for sec in ("CalcFree", "CalcAssumed"):
                refs = [r for r in items if info(r)["section"] == sec]
                if not refs:
                    continue
                path = k.get("export.target")(f"WTF_{subj}_{SEC[sec]}卷_{stamp}.pdf", f"导出 {SEC[sec]} 卷")
                if not path:
                    return
                marks = sum(info(r)["marks"] or 0 for r in refs)
                reading, working = TIMES[sec]
                meta = (f"{len(refs)} 题 · 共 {marks} 分 · 阅读时间 {reading} 分钟 + 作答时间 {working} 分钟 · "
                        f"{time.strftime('%Y-%m-%d')} · WTF — WACE Training Framework")
                done.append(k.get("export.combined")(refs, path, f"WACE {subj} 模拟卷 · {SEC_NAME[sec]}", meta))
        else:
            path = k.get("export.target")(f"WTF组卷_{stamp}.pdf", "合并导出")
            if not path:
                return
            done.append(k.get("export.combined")(list(items), path, f"WTF 组卷 · {len(items)} 题"))
        k.get("ui.status")("已导出：" + "；".join(f"{q.split('/')[-1].split(chr(92))[-1]} + 答案" for q, _ in done))
        plat.open_file(done[0][0])

    def first_layout(e):
        if e.height > 300:
            middle.sashpos(0, int(e.height * 0.66))
            middle.unbind("<Configure>")

    middle.bind("<Configure>", first_layout)
    k.provide("workspace.source", source)
    k.provide("workspace.add", add)
    k.provide("workspace.items", lambda: list(items))
    k.provide("workspace.export", export)
    k.provide("workspace.paper_mode", paper)
    refresh()
