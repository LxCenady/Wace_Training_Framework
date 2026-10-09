"""Knowledge tree. One job: browse subject -> topic -> pattern -> questions, and start AI generation.

Selecting several patterns (Ctrl/Shift-click) asks the generator for one question combining them.
Emits select.pattern([codes]), select.question(qid), select.generated(gid).
"""
import tkinter as tk
from tkinter import ttk

NAMES = {"MAM": "Mathematics Methods 数学方法", "MAS": "Mathematics Specialist 专业数学"}
SECTIONS = {"任意": "any", "计算器禁用 (CF)": "CalcFree", "计算器允许 (CA)": "CalcAssumed"}
LEVELS = ["基础", "标准", "拔高"]


def short(title):
    return title.split("★")[0].split("（")[0].strip()


def setup(k):
    store, left = k.get("store"), k.get("ui.left")
    head = ttk.Frame(left)
    head.pack(fill="x", padx=10, pady=(10, 4))
    ttk.Label(head, text="知识图谱", style="H.TLabel").pack(side="left")
    ttk.Label(head, text="Ctrl+点击可多选题型组合出题", style="Muted.TLabel").pack(side="right")

    body = ttk.Frame(left)
    body.pack(fill="both", expand=True, padx=(10, 0))
    tree = ttk.Treeview(body, show="tree", selectmode="extended")
    bar = ttk.Scrollbar(body, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=bar.set)
    bar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    foot = ttk.Frame(left)
    foot.pack(fill="x", padx=10, pady=8)
    pick = k.get("i18n.choices", lambda v: (list(v), lambda s: s))
    sec_shown, sec_code = pick(list(SECTIONS))
    lvl_shown, lvl_code = pick(LEVELS)
    section, marks = tk.StringVar(value=sec_shown[0]), tk.IntVar(value=0)
    level, count = tk.StringVar(value=lvl_shown[1]), tk.IntVar(value=1)
    ttk.Label(foot, text="卷型").grid(row=0, column=0, sticky="w")
    ttk.Combobox(foot, textvariable=section, values=sec_shown, state="readonly", width=16).grid(row=0, column=1,
                                                                                                    padx=4)
    ttk.Label(foot, text="总分(0=自动)").grid(row=0, column=2, sticky="w", padx=(8, 0))
    ttk.Spinbox(foot, from_=0, to=20, textvariable=marks, width=4).grid(row=0, column=3, padx=4)
    ttk.Label(foot, text="难度").grid(row=1, column=0, sticky="w", pady=(6, 0))
    ttk.Combobox(foot, textvariable=level, values=lvl_shown, state="readonly", width=16).grid(row=1, column=1, padx=4,
                                                                                           pady=(6, 0))
    ttk.Label(foot, text="数量").grid(row=1, column=2, sticky="w", padx=(8, 0), pady=(6, 0))
    ttk.Spinbox(foot, from_=1, to=20, textvariable=count, width=4).grid(row=1, column=3, padx=4, pady=(6, 0))
    go = ttk.Button(foot, text="AI 生成相似题", style="Accent.TButton")
    go.grid(row=2, column=0, columnspan=4, sticky="ew", pady=(8, 0))
    foot.columnconfigure(1, weight=1)

    for subj in store.subjects():
        s = tree.insert("", "end", f"S:{subj}", text=NAMES.get(subj, subj), open=True)
        for code, zh, en, n in store.topics(subj):
            t = tree.insert(s, "end", f"T:{code}", text=f"{zh}  ·  {n} 题")
            for pcode, num, title, cnt in store.patterns(code):
                p = tree.insert(t, "end", f"P:{pcode}", text=f"题型 {num}  {short(title)}  ·  {cnt}")
                tree.insert(p, "end", f"X:{pcode}", text="…")  # lazy placeholder

    def fill(pcode):
        node = f"P:{pcode}"
        if not tree.exists(f"X:{pcode}"):
            return
        tree.delete(f"X:{pcode}")
        for gid, created, m, diff in store.generated_for(pcode):
            tree.insert(node, "end", f"G:{pcode}|{gid}", text=f"★ AI #{gid}  [{m}分 · {diff}]  {created}")
        for qid, year, sec, q, m, labels in store.questions_for(pcode):
            parts = "整题" if labels == "" else ",".join(f"({l})" for l in labels.split(","))
            tree.insert(node, "end", f"Q:{pcode}|{qid}",
                        text=f"{year} {'CF' if sec == 'CalcFree' else 'CA'} Q{q}  [{m}分]  {parts}")

    tree.bind("<<TreeviewOpen>>", lambda e: tree.focus().startswith("P:") and fill(tree.focus()[2:]))

    def codes():
        out = []
        for iid in tree.selection():
            kind, rest = iid.split(":", 1)
            code = rest.split("|")[0]
            if kind in "PQGX" and code not in out:
                out.append(code)
        return out

    def on_select(_):
        sel = tree.selection()
        if len(sel) == 1 and sel[0][0] in "QG":
            kind, rest = sel[0].split(":", 1)
            ref = rest.split("|")[1]
            k.emit("select.question" if kind == "Q" else "select.generated", ref if kind == "Q" else int(ref))
        elif codes():
            k.emit("select.pattern", codes())

    tree.bind("<<TreeviewSelect>>", on_select)

    def generate():
        c = codes()
        if not c:
            k.get("ui.status")("先在知识图谱里选中至少一个题型")
            return
        go.state(["disabled"])
        n = max(1, min(20, count.get()))
        k.get("generator.start")(c, SECTIONS[sec_code(section.get())], marks.get(), lvl_code(level.get()), n)

    go.configure(command=generate)

    def done(item):
        for code in item["patterns"]:
            node = f"P:{code}"
            if tree.exists(node) and not tree.exists(f"X:{code}"):
                tree.insert(node, 0, f"G:{code}|{item['id']}",
                            text=f"★ AI #{item['id']}  [{item['marks']}分 · {item.get('difficulty', '标准')}]  新")

    k.on("gen.done", done)
    k.on("gen.finished", lambda ok, n: go.state(["!disabled"]))
