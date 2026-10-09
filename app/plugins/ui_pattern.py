"""Pattern view. One job: show the method notes of the selected pattern(s) and the marks it carries in real papers."""
import re


def plain(md):
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    return re.sub(r"`([^`]+)`", r"\1", md)


def marks_line(by_section):
    """'分值（真题中此题型在一道题里占）：计算器禁用 一般 2–4 分，最多 6 分（9 道）· …' from the printed marks."""
    out = []
    for sec, name in (("CalcFree", "计算器禁用"), ("CalcAssumed", "计算器允许")):
        v = by_section.get(sec)
        if v:
            r = [round(x) for x in v]
            lo, hi = r[len(r) // 4], r[(3 * len(r)) // 4]
            out.append(f"{name} 一般 {lo}{f'–{hi}' if hi != lo else ''} 分，最多 {max(r)} 分（{len(r)} 道）")
    return "分值（此题型在一道真题里占）：" + (" · ".join(out) if out else "暂无数据")


def setup(k):
    store = k.get("store")

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
            w(t, marks_line(store.pattern_marks(code)) + "\n\n", "muted")
            for line in plain(p["method"]).splitlines():
                w(t, line.lstrip("# ") + "\n", *(("sub",) if line.startswith("#") else ()))
            w(t, "\n")

    k.on("select.pattern", show)
