"""Self-marking + 错题本. One job: record lost marks per sub-question and turn them into targeted practice.

Views call k.get("mistakes.popup")(event, ctx) on right-click, where ctx describes one sub-question:
  {"source": "gen"|"past", "ref": generated id or question id, "label": "b", "part_marks": 4,
   "patterns": ["MAM.D.6"], "points": ["differentiates …", …], "title": "AI #4 (b)"}
The 错题本 groups records by pattern (weakest first) and can generate 错题加强题: the generator is told the
exact mark points the student missed, so the new question requires those steps.
"""
import tkinter as tk
from tkinter import ttk

LEVELS = ["基础", "标准", "拔高"]


def setup(k):
    store, C = k.get("store"), k.get("ui.colors")
    root = k.get("ui.root")

    # ---------- marking a sub-question
    def popup(event, ctx):
        m = tk.Menu(root, tearoff=False)
        had = store.mistake(ctx["source"], ctx["ref"], ctx["label"])
        m.add_command(label=f"{ctx['title']}：此题扣分…" + ("（修改）" if had else ""), command=lambda: dialog(ctx))
        if had:
            m.add_command(label="此题满分（从错题本移除）", command=lambda: remove(ctx))
        m.add_separator()
        m.add_command(label="打开我的错题本", command=show)
        m.tk_popup(event.x_root, event.y_root)

    def remove(ctx):
        store.delete_mistake(ctx["source"], ctx["ref"], ctx["label"])
        k.emit("mistakes.changed")
        k.get("ui.status")(f"{ctx['title']} 已移出错题本")

    def dialog(ctx):
        had = store.mistake(ctx["source"], ctx["ref"], ctx["label"]) or {}
        top = tk.Toplevel(root)
        top.title(f"自批卷 — {ctx['title']}")
        top.transient(root)
        f = ttk.Frame(top, padding=14)
        f.pack(fill="both", expand=True)
        full = ctx.get("part_marks") or max(1, len(ctx.get("points") or []))
        ttk.Label(f, text=f"{ctx['title']} · 满分 {full} 分", style="H.TLabel").pack(anchor="w")
        ttk.Label(f, text="题型：" + "；".join(store.pattern_name(c) for c in ctx["patterns"]),
                  style="Muted.TLabel", wraplength=560).pack(anchor="w", pady=(0, 8))
        checks = []
        if ctx.get("points"):
            ttk.Label(f, text="勾出你没拿到的得分点：").pack(anchor="w")
            for text in ctx["points"]:
                v = tk.BooleanVar(value=text in had.get("missed", []))
                checks.append((v, text))
                ttk.Checkbutton(f, text=text, variable=v, command=lambda: lost.set(sum(c.get() for c, _ in checks))
                                ).pack(anchor="w", padx=8)
        row = ttk.Frame(f)
        row.pack(fill="x", pady=(10, 4))
        lost = tk.IntVar(value=had.get("lost", 1 if not checks else 0))
        ttk.Label(row, text="扣分").pack(side="left")
        ttk.Spinbox(row, from_=0, to=full, textvariable=lost, width=4).pack(side="left", padx=6)
        ttk.Label(row, text=f"/ {full}").pack(side="left")
        note = tk.StringVar(value=had.get("note", ""))
        ttk.Label(f, text="备注（错因，可选）").pack(anchor="w", pady=(6, 0))
        ttk.Entry(f, textvariable=note, width=70).pack(fill="x")
        msg = ttk.Label(f, foreground=C["warn"])
        msg.pack(anchor="w")

        def save():
            n = lost.get()
            if not 0 < n <= full:
                msg.configure(text=f"扣分应在 1–{full} 之间；满分请用右键「此题满分」。")
                return
            store.save_mistake(ctx["source"], ctx["ref"], ctx["label"], full, n, ctx["patterns"],
                               [t for v, t in checks if v.get()], note.get().strip())
            k.emit("mistakes.changed")
            k.get("ui.status")(f"{ctx['title']} 扣 {n} 分，已记入错题本")
            top.destroy()

        btns = ttk.Frame(f)
        btns.pack(fill="x", pady=(10, 0))
        ttk.Button(btns, text="记入错题本", style="Accent.TButton", command=save).pack(side="right")
        ttk.Button(btns, text="取消", command=top.destroy).pack(side="right", padx=6)

    # ---------- 错题本
    def weak():
        """{pattern: {"lost", "marks", "count", "rows"}} from all records."""
        out = {}
        for m in store.mistakes():
            for c in m["patterns"]:
                g = out.setdefault(c, {"lost": 0, "marks": 0, "count": 0, "rows": []})
                g["lost"] += m["lost"]
                g["marks"] += m["part_marks"] or 0
                g["count"] += 1
                g["rows"].append(m)
        return out

    def source_title(m):
        if m["source"] == "gen":
            return f"AI #{m['ref']} ({m['label']})"
        subj, ys, q = m["ref"].split("-")
        sec = "CF" if ys.endswith("F") else "CA"
        return f"{ys[:4]} {subj} {sec} {q} ({m['label'] or '整题'})"

    def show():
        page = k.get("ui.tab")("mistakes", "我的错题本")
        groups = weak()
        records = store.mistakes()
        head = ttk.Frame(page)
        head.pack(fill="x", padx=10, pady=8)
        ttk.Label(head, text=f"错题 {len(records)} 小题 · 共扣 {sum(m['lost'] for m in records)} 分 · "
                             f"涉及 {len(groups)} 个题型", style="H.TLabel").pack(side="left")
        ttk.Label(head, text="按扣分从多到少 · 双击打开原题 · 右键移除", style="Muted.TLabel").pack(side="right")

        body = ttk.Frame(page)
        body.pack(fill="both", expand=True, padx=10)
        cols = (("count", "次数", 50), ("lost", "扣分", 70), ("date", "时间", 130), ("missed", "没拿到的得分点 / 备注", 520))
        table = ttk.Treeview(body, columns=[c for c, _, _ in cols], show="tree headings")
        sb = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        table.heading("#0", text="题型 / 小题")
        table.column("#0", width=330, stretch=False)
        for c, h, w in cols:
            table.heading(c, text=h)
            table.column(c, width=w, stretch=c == "missed", anchor="w")
        rows = {}
        for code, g in sorted(groups.items(), key=lambda x: (-x[1]["lost"], -x[1]["count"])):
            gid = f"p:{code}"
            table.insert("", "end", iid=gid, text=store.pattern_name(code),
                         values=(g["count"], f"{g['lost']} / {g['marks']}", "", ""), open=False)
            for m in g["rows"]:
                iid = f"{gid}|{m['id']}"
                rows[iid] = m
                detail = ("📖 已讲解 · " if m.get("explain") else "") + "；".join(m["missed"]) + (
                    f"  〔{m['note']}〕" if m["note"] else "")
                table.insert(gid, "end", iid=iid, text=source_title(m),
                             values=("", f"{m['lost']} / {m['part_marks']}", m["created"], detail or "—"))
        if not records:
            ttk.Label(body, text="还没有错题：在 AI 题「显示得分点」后或真题「显示评分标准」后，右键某个小问选择「此题扣分」。",
                      style="Muted.TLabel").place(x=20, y=60)

        def open_row(_=None):
            m = rows.get(table.focus())
            if m:
                k.emit("select.generated", int(m["ref"])) if m["source"] == "gen" else k.emit("select.question",
                                                                                               m["ref"])

        def context(e):
            iid = table.identify_row(e.y)
            m = rows.get(iid)
            if m:
                table.selection_set(iid)
                menu = tk.Menu(root, tearoff=False)
                if k.get("mistakes.explain", None):
                    menu.add_command(label="一键讲解" + ("（已讲解，直接查看）" if m.get("explain") else ""),
                                     command=lambda: k.get("mistakes.explain")(m))
                menu.add_command(label="打开原题", command=open_row)
                menu.add_command(label="移出错题本（这题已掌握）",
                                 command=lambda: (store.delete_mistake(m["source"], m["ref"], m["label"]),
                                                  k.emit("mistakes.changed")))
                menu.tk_popup(e.x_root, e.y_root)

        table.bind("<Double-1>", open_row)
        table.bind("<Button-3>", context)

        foot = ttk.Frame(page)
        foot.pack(fill="x", padx=10, pady=8)
        level, count = tk.StringVar(value="标准"), tk.IntVar(value=3)
        ttk.Label(foot, text="难度").pack(side="left")
        ttk.Combobox(foot, textvariable=level, values=LEVELS, state="readonly", width=6).pack(side="left", padx=4)
        ttk.Label(foot, text="数量").pack(side="left", padx=(10, 0))
        ttk.Spinbox(foot, from_=1, to=20, textvariable=count, width=4).pack(side="left", padx=4)
        hint = ttk.Label(foot, style="Muted.TLabel")
        hint.pack(side="left", padx=10)

        def chosen():
            codes = []
            for iid in table.selection():
                code = iid.split("|")[0][2:]
                if code not in codes:
                    codes.append(code)
            if not codes and groups:  # nothing selected: the weakest pattern
                codes = [max(groups, key=lambda c: (groups[c]["lost"], groups[c]["count"]))]
            subj = codes[0].split(".")[0] if codes else ""
            return [c for c in codes if c.startswith(subj + ".")]

        def drill():
            codes = chosen()
            if not codes:
                hint.configure(text="错题本还是空的")
                return
            missed, notes = [], []
            for c in codes:
                for m in groups[c]["rows"]:
                    missed += [t for t in m["missed"] if t not in missed]
                    if m["note"] and m["note"] not in notes:
                        notes.append(m["note"])
                    if not m["missed"]:
                        line = f"lost {m['lost']} of {m['part_marks']} marks on part ({m['label']}) of a question on {c}"
                        if line not in missed:
                            missed.append(line)
            focus = "\n".join(f"- {t}" for t in missed[:12]) + (
                "\nStudent's own notes on the errors: " + "; ".join(notes[:6]) if notes else "")
            hint.configure(text="针对：" + "；".join(store.pattern_name(c) for c in codes))
            k.get("generator.start")(codes, "any", 0, level.get(), max(1, min(20, count.get())), focus)

        ttk.Button(foot, text="生成错题加强题（未选中时针对最弱题型）", style="Accent.TButton",
                   command=drill).pack(side="right")

        def explain_selected():
            m = rows.get(table.focus())
            if m and k.get("mistakes.explain", None):
                k.get("mistakes.explain")(m)
            else:
                hint.configure(text="先展开题型，选中一道错题")

        ttk.Button(foot, text="一键讲解所选错题", command=explain_selected).pack(side="right", padx=6)
        k.provide("mistakes.table", table)

    def refresh():
        if k.get("ui.tab.frame")("mistakes") is not None:
            current = k.get("ui.tabs").select() if k.get("ui.tabs", None) else None
            show()
            if current:
                k.get("ui.tabs").select(current)

    k.on("mistakes.changed", refresh)
    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="我的错题本", command=show, accelerator="Ctrl+E")
    k.get("ui.menu").add_cascade(label="错题", menu=menu)
    root.bind_all("<Control-e>", lambda e: show())
    ttk.Button(k.get("ui.left"), text="我的错题本", command=show).pack(side="bottom", fill="x", padx=10, pady=(0, 4))
    k.provide("mistakes.popup", popup)
    k.provide("mistakes.dialog", dialog)
    k.provide("mistakes.show", show)
