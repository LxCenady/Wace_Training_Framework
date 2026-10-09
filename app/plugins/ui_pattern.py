"""Pattern view. One job: show the method notes of the selected pattern(s)."""
import re


def plain(md):
    md = re.sub(r"\*\*(.+?)\*\*", r"\1", md)
    return re.sub(r"`([^`]+)`", r"\1", md)


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
            w(t, f"{code} · 真题 {n} 道 · 展开左侧节点查看；多选题型后点「AI 生成相似题」可组合出题\n\n", "muted")
            for line in plain(p["method"]).splitlines():
                w(t, line.lstrip("# ") + "\n", *(("sub",) if line.startswith("#") else ()))
            w(t, "\n")

    k.on("select.pattern", show)
