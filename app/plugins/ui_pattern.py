"""Pattern view. One job: show the method notes of the selected pattern(s), the marks it carries in real papers, and
the patterns it is most often examined with (bars, with buttons to combine them or see those past questions)."""
import subjects
import re
import tkinter as tk
from tkinter import ttk


def plain(md):
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    return re.sub(r"`([^`]+)`", r"\1", md)


def marks_line(by_section, subject=None):
    """'分值（真题中此题型在一道题里占）：计算器禁用 一般 2–4 分，最多 6 分（9 道）· …' from the printed marks."""
    out = []
    for sec, name in subjects.section_labels(subject).items():
        v = by_section.get(sec)
        if v:
            r = [round(x) for x in v]
            lo, hi = r[len(r) // 4], r[(3 * len(r)) // 4]
            out.append(f"{name} 一般 {lo}{f'–{hi}' if hi != lo else ''} 分，最多 {max(r)} 分（{len(r)} 道）")
    return "分值（此题型在一道真题里占）：" + (" · ".join(out) if out else "暂无数据")


def setup(k):
    store = k.get("store")
    C = k.get("ui.colors")

    def related_panel(t, code):
        """常一起考的题型: the patterns sharing this one's past questions, one row each — bar = share of its
        questions, then 「组合出题」 (select both in the tree) and 「看这几道真题」 (真题搜索 for both)."""
        w = k.get("ui.write")
        total, pairs = store.related(code)
        if not pairs:
            w(t, "常一起考的题型：没有和它在同一道真题里出现 2 次以上的题型（多为单独出题）\n\n", "muted")
            return
        w(t, f"常一起考的题型（在 {total} 道考它的真题里）\n", "sub")
        box = tk.Frame(t, bg=C["panel"])
        width = 200
        for i, (p, n) in enumerate(pairs):
            tk.Label(box, text=store.pattern_name(p), bg=C["panel"], fg=C["ink"], anchor="w", width=34).grid(
                row=i, column=0, sticky="w", pady=2)
            bar = tk.Canvas(box, width=width, height=12, bg=C["panel"], highlightthickness=0)
            bar.grid(row=i, column=1, padx=6)
            bar.create_rectangle(0, 2, width, 10, fill=C["line"], width=0)
            bar.create_rectangle(0, 2, max(4, width * n / total), 10, fill=C["accent"], width=0)
            tk.Label(box, text=f"{n}/{total} 道 · {n / total:.0%}", bg=C["panel"], fg=C["muted"]).grid(
                row=i, column=2, sticky="w")
            ttk.Button(box, text="组合出题", command=lambda p=p: combine([code, p])).grid(row=i, column=3, padx=(10, 2))
            ttk.Button(box, text="看这几道真题", command=lambda p=p: (combine([code, p]), k.get("search.show")())).grid(
                row=i, column=4)
        t.window_create("end", window=box)
        w(t, "\n\n")

    def combine(pattern_codes):
        k.get("tree.combine", lambda c: None)(pattern_codes)
        k.get("ui.status")("已在左侧选中：" + " + ".join(store.pattern_name(c) for c in pattern_codes)
                           + " —— 点「AI 生成相似题」组合出题")

    def show(codes):
        page = k.get("ui.tab")("pattern", "题型讲解")
        t = k.get("ui.text")(page)
        t.frame.pack(fill="both", expand=True)
        w = k.get("ui.write")
        for code in codes:
            p = store.pattern(code)
            n = len(store.questions_for(code))
            w(t, f"{p['topic_zh']} · 题型 {p['n']}：{p['title']}\n", "h")
            w(t, f"{code} · 真题 {n} 道 · 展开左侧节点查看；多选题型后点「AI 生成相似题」可组合出题\n", "muted")
            w(t, marks_line(store.pattern_marks(code), code.split('.')[0]) + "\n\n", "muted")
            if len(codes) == 1:
                related_panel(t, code)
            for line in plain(p["method"]).splitlines():
                w(t, line.lstrip("# ") + "\n", *(("sub",) if line.startswith("#") else ()))
            w(t, "\n")

    k.on("select.pattern", show)

    def show_unit(code):
        """What unit questions are built from: the unit's real questions, per section — cross-topic rate and
        partners, and each pattern's share of the unit's marks, usual marks and how often it comes with a figure /
        a drawing part."""
        import blueprint  # tools/: real-paper statistics
        subj = code.split(".")[0]
        page = k.get("ui.tab")("pattern", "题型讲解")
        t = k.get("ui.text")(page)
        t.frame.pack(fill="both", expand=True)
        w = k.get("ui.write")
        w(t, f"单元：{store.topic_name(code)}\n", "h")
        w(t, "选中单元后点「AI 生成相似题」= 单元出题：每道题沿用一道以本单元为主的真题的题型组合与每个题型的分值，"
             "再随机换成同单元、分值相近的题型并微调 ±1 分；所以题型频率、分值区间和跨单元搭配都跟真题一致。"
             "卷型选「任意」时按本单元真题在各部分的题数比例抽。下面是这些统计。\n\n", "muted")
        for name, sec in list(subjects.section_options(subj).items())[1:]:
            with store.lock:
                bp = blueprint.blueprint(store.db, subj, sec)
                draw = blueprint.pattern_drawing(store.db, subj, sec)
            shapes = [sk for sk in bp["skeletons"] if blueprint.lead(sk) == code]
            if not shapes:
                continue
            cross = [sk for sk in shapes if len({blueprint.topic(p) for p in sk}) > 1]
            partners = {}
            for sk in cross:
                for tp in {blueprint.topic(p) for p in sk} - {code}:
                    partners[tp] = partners.get(tp, 0) + 1
            w(t, f"{name}：以本单元为主的真题 {len(shapes)} 道，{len(cross) / len(shapes):.0%} 跨单元", "sub")
            w(t, ("（常搭配：" + "、".join(f"{store.topic_name(tp).split(' ', 1)[-1]} {n / len(cross):.0%}" for tp, n in
                                         sorted(partners.items(), key=lambda x: -x[1])) + "）") if cross else "")
            w(t, "\n")
            marks = {}
            for sk in shapes:
                for p, m in sk.items():
                    if blueprint.topic(p) == code:
                        marks.setdefault(p, []).append(m)
            total = sum(sum(v) for v in marks.values())
            for p, v in sorted(marks.items(), key=lambda x: -sum(x[1])):
                v = sorted(v)
                lo, hi = v[len(v) // 4], v[(3 * len(v)) // 4]
                f, d, _ = draw.get(p, (0, 0, 0))
                w(t, f"  {store.pattern_name(p)} · 占本单元分值 {sum(v) / total:.0%} · 一般 {lo}"
                     f"{f'–{hi}' if hi != lo else ''} 分 · 配图 {f:.0%} · 作图 {d:.0%}\n")
            w(t, "\n")

    k.on("select.topic", show_unit)
