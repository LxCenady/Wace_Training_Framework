"""真题搜索. One job: find past questions by any mix of patterns and units — cross-topic and cross-pattern.

Filters: subject, section, years, marks, words in the stem; patterns / units taken from the knowledge-tree
selection, matched all-of or any-of; only cross-unit questions, only questions with a drawing part or a figure.
Results list each question's patterns with the marks they carried; double-click opens it (select.question).
Below the list, the patterns and units that most often appear together with the chosen ones in the results:
the cross-pattern index. 导出 PDF: the selected results (or all of them) cut from the papers, plus their keys.
"""
import os, re, time
import tkinter as tk
from tkinter import filedialog, ttk
import plat

COLS = (("year", "年份", 60), ("section", "卷型", 50), ("q", "题号", 50), ("marks", "分", 40),
        ("cross", "跨单元", 60), ("draw", "作图/配图", 80), ("patterns", "题型（分值）", 620))
MODES = ["同时包含全部", "包含任一"]
SECTIONS = {"任意": None, "计算器禁用 (CF)": "CalcFree", "计算器允许 (CA)": "CalcAssumed"}


def unit_of(code):
    return code.rsplit(".", 1)[0]


def setup(k):
    store = k.get("store")
    pick = k.get("i18n.choices", lambda v: (list(v), lambda s: s))

    def show():
        unit, codes = k.get("tree.selection", lambda: (None, []))()
        want = [unit] if unit else list(codes)
        index = store.past_index()
        page = k.get("ui.tab")("search", "真题搜索")
        C = k.get("ui.colors")

        bar = ttk.Frame(page)
        bar.pack(fill="x", padx=10, pady=(8, 2))
        subjects = sorted({r["subject"] for r in index})
        subj = tk.StringVar(value=(want[0].split(".")[0] if want else subjects[0]) if subjects else "")
        sec_shown, sec_code = pick(list(SECTIONS))
        section = tk.StringVar(value=sec_shown[0])
        years = sorted({r["year"] for r in index}) or [2016]
        y0, y1 = tk.IntVar(value=years[0]), tk.IntVar(value=years[-1])
        m0, m1 = tk.IntVar(value=0), tk.IntVar(value=30)
        words = tk.StringVar()
        ttk.Label(bar, text="科目").pack(side="left")
        ttk.Combobox(bar, textvariable=subj, values=subjects, state="readonly", width=6).pack(side="left", padx=4)
        ttk.Label(bar, text="卷型").pack(side="left", padx=(8, 0))
        ttk.Combobox(bar, textvariable=section, values=sec_shown, state="readonly", width=16).pack(side="left", padx=4)
        ttk.Label(bar, text="年份").pack(side="left", padx=(8, 0))
        ttk.Spinbox(bar, from_=years[0], to=years[-1], textvariable=y0, width=6).pack(side="left", padx=2)
        ttk.Label(bar, text="–").pack(side="left")
        ttk.Spinbox(bar, from_=years[0], to=years[-1], textvariable=y1, width=6).pack(side="left", padx=2)
        ttk.Label(bar, text="分值").pack(side="left", padx=(8, 0))
        ttk.Spinbox(bar, from_=0, to=30, textvariable=m0, width=4).pack(side="left", padx=2)
        ttk.Label(bar, text="–").pack(side="left")
        ttk.Spinbox(bar, from_=0, to=30, textvariable=m1, width=4).pack(side="left", padx=2)
        ttk.Label(bar, text="关键词").pack(side="left", padx=(8, 0))
        ttk.Entry(bar, textvariable=words, width=18).pack(side="left", padx=4)

        bar2 = ttk.Frame(page)
        bar2.pack(fill="x", padx=10, pady=2)
        mode_shown, mode_code = pick(MODES)
        mode = tk.StringVar(value=mode_shown[0])
        cross, draw, fig = tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()
        chosen = ttk.Label(bar2, style="Muted.TLabel")
        chosen.pack(side="left")
        ttk.Combobox(bar2, textvariable=mode, values=mode_shown, state="readonly", width=14).pack(side="left", padx=6)

        def take_tree():
            u, c = k.get("tree.selection", lambda: (None, []))()
            want[:] = [u] if u else list(c)
            if want:
                subj.set(want[0].split(".")[0])
            fill()

        def clear():
            want.clear()
            fill()

        ttk.Button(bar2, text="用左侧选中的单元/题型", command=take_tree).pack(side="left", padx=4)
        ttk.Button(bar2, text="清除题型条件", command=clear).pack(side="left", padx=4)
        ttk.Button(bar2, text="导出 PDF", style="Accent.TButton", command=lambda: export()).pack(side="right")
        for var, text in ((cross, "只看跨单元"), (draw, "含作图小问"), (fig, "有配图")):
            ttk.Checkbutton(bar2, text=text, variable=var, command=lambda: fill()).pack(side="left", padx=6)

        body = ttk.Frame(page)
        body.pack(fill="both", expand=True, padx=10, pady=(4, 2))
        table = ttk.Treeview(body, columns=[c for c, _, _ in COLS], show="headings", selectmode="extended")
        sb = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        for col, head, width in COLS:
            table.heading(col, text=head)
            table.column(col, width=width, stretch=col == "patterns", anchor="w")
        count = ttk.Label(page, style="Muted.TLabel")
        count.pack(anchor="w", padx=10)
        together = tk.Text(page, height=5, wrap="word", relief="flat", bg=C["panel"], font=(plat.UI_FONT, 9))
        together.pack(fill="x", padx=10, pady=(0, 8))

        def matches(r):
            if r["subject"] != subj.get() or not (y0.get() <= r["year"] <= y1.get()):
                return False
            if not (m0.get() <= r["marks"] <= max(m0.get(), m1.get())):
                return False
            sec = SECTIONS[sec_code(section.get())]
            if sec and r["section"] != sec:
                return False
            units = {unit_of(p) for p in r["split"]}
            if cross.get() and len(units) < 2:
                return False
            if draw.get() and not r["sketch"]:
                return False
            if fig.get() and not r["figure"]:
                return False
            if words.get().strip() and words.get().strip().lower() not in r["stem"].lower():
                return False
            if want:
                hit = [w in r["split"] or w in units for w in want]
                return all(hit) if mode_code(mode.get()) == MODES[0] else any(hit)
            return True

        def fill(*_):
            try:
                found = [r for r in index if matches(r)]
            except (tk.TclError, ValueError):  # a spinbox is being edited
                return
            names = "、".join(store.topic_name(w) if w.count(".") == 1 else store.pattern_name(w) for w in want)
            chosen.configure(text=f"题型/单元条件：{names}" if want else "题型/单元条件：无（在左侧选中后点右边按钮）")
            table.delete(*table.get_children())
            for r in found:
                split = r["split"]
                pats = "；".join(f"{store.pattern_name(p)}（{m}）" for p, m in sorted(split.items(), key=lambda x: -x[1]))
                units = {unit_of(p) for p in split}
                marks = ("作图" if r["sketch"] else "") + ("/" if r["sketch"] and r["figure"] else "") + \
                        ("配图" if r["figure"] else "")
                table.insert("", "end", iid=r["id"], values=(
                    r["year"], "CF" if r["section"] == "CalcFree" else "CA", f"Q{r['q']}", r["marks"],
                    "✓" if len(units) > 1 else "", marks, pats))
            total_marks = sum(r["marks"] for r in found)
            count.configure(text=f"{len(found)} 道真题 · 共 {total_marks} 分 · 双击打开原题（可看评分标准、右键扣分）· "
                                 "Ctrl/Shift 多选后「导出 PDF」只导出选中的")
            # cross-pattern index: what appears together with the chosen patterns / units in these questions
            pats, units = {}, {}
            for r in found:
                for p in r["split"]:
                    if p not in want and unit_of(p) not in want:
                        pats[p] = pats.get(p, 0) + 1
                for u in {unit_of(p) for p in r["split"]}:
                    if u not in want and u not in {unit_of(w) for w in want}:
                        units[u] = units.get(u, 0) + 1
            together.configure(state="normal")
            together.delete("1.0", "end")
            if found and want:
                together.insert("end", "常一起出现的题型：" + "，".join(
                    f"{store.pattern_name(p)} {n} 道" for p, n in sorted(pats.items(), key=lambda x: -x[1])[:10]) + "\n")
                together.insert("end", "常一起出现的单元：" + "，".join(
                    f"{store.topic_name(u)} {n} 道" for u, n in sorted(units.items(), key=lambda x: -x[1])[:6]))
            elif found:
                multi = sum(1 for r in found if len({unit_of(p) for p in r["split"]}) > 1)
                together.insert("end", f"其中跨单元 {multi} 道（{multi / len(found):.0%}）。在左侧选中题型或单元后点"
                                       "「用左侧选中的单元/题型」，可查看它们和哪些题型、单元一起出题。")
            together.configure(state="disabled")

        def paper_name(qids):
            """The paper's title: the searched patterns / units; without a pattern condition, the unit or pattern
            every exported question shares (else the subject)."""
            if want:
                return " + ".join(store.topic_name(w) if w.count(".") == 1 else store.pattern_name(w) for w in want)
            rows = [r for r in index if r["id"] in qids]
            common = set.intersection(*(set(r["split"]) for r in rows)) if rows else set()
            if common:
                return " + ".join(store.pattern_name(p) for p in sorted(common))
            units = set.intersection(*({unit_of(p) for p in r["split"]} for r in rows)) if rows else set()
            return " + ".join(store.topic_name(u) for u in sorted(units)) if units else f"{subj.get()} 真题"

        def export():
            """Selected results (Ctrl/Shift-click), else every result listed -> questions + marking keys (PDF)."""
            qids = list(table.selection() or table.get_children())
            if not qids or not k.get("export.past", None):
                count.configure(text="没有可导出的真题")
                return
            name = paper_name(qids)
            path = filedialog.asksaveasfilename(
                title="导出真题", defaultextension=".pdf", filetypes=[("PDF", "*.pdf")],
                initialfile=re.sub(r'[\\/:*?"<>|]+', "_", name)[:80] + f"_{time.strftime('%Y%m%d')}.pdf")
            if not path:
                return
            q, a = k.get("export.past")(qids, path, f"{name} · 真题 {len(qids)} 题")
            count.configure(text=f"已导出 {len(qids)} 道真题：{os.path.basename(q)} + {os.path.basename(a)}")
            plat.open_file(q)

        k.provide("search.export", export)
        for var in (subj, section, y0, y1, m0, m1, words, mode):
            var.trace_add("write", fill)
        table.bind("<Double-1>", lambda e: table.selection() and k.emit("select.question", table.selection()[0]))
        table.bind("<Return>", lambda e: table.selection() and k.emit("select.question", table.selection()[0]))
        fill()

    actions = k.get("ui.tree.actions", None)
    if actions is not None:
        ttk.Button(actions, text="真题搜索", command=show).pack(side="left", padx=(6, 0))
    plat.shortcut(k.get("ui.root"), "f", lambda e: show())
    k.provide("search.show", show)
