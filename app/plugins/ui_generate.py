"""AI question view. One job: show pipeline progress, then the verified question; mark points on click.

Answers only exist in a finished item, which the generator emits after the independent solve,
verification and mark-point split have all passed.
"""
import tkinter as tk
from tkinter import ttk


def setup(k):
    store = k.get("store")
    w, ui_text = k.get("ui.write"), k.get("ui.text")
    state = {}

    def started(codes):
        page = k.get("ui.tab")("gen", "AI 出题")
        t = ui_text(page)
        t.frame.pack(fill="both", expand=True)
        state["log"] = t
        w(t, "正在生成并验证…\n", "h")
        w(t, "题型：" + "，".join(f"{c} {store.pattern(c)['title'].split('★')[0].strip()}" for c in codes) + "\n", "muted")
        w(t, "流程：出题 → 独立解题（只看题目）→ 独立核对 → 拆分得分点；全部通过前不显示答案。\n\n", "muted")
        k.get("ui.status")("AI 出题中…")

    def progress(msg):
        if "log" in state:
            w(state["log"], msg + "\n", "warn" if "未通过" in msg else "mono")

    def error(msg):
        progress("\n✗ " + msg)
        k.get("ui.status")("生成失败：" + msg[:120])

    def show(item):
        page = k.get("ui.tab")("gen", "AI 出题")
        state.pop("log", None)
        bar = ttk.Frame(page)
        bar.pack(fill="x", padx=8, pady=6)
        t = ui_text(page)
        t.frame.pack(fill="both", expand=True)
        sec = {"CalcFree": "计算器禁用", "CalcAssumed": "计算器允许"}.get(item.get("section"), item.get("section", ""))
        w(t, f"AI 题 #{item['id']} · {item['marks']} 分 · {sec}\n", "h")
        w(t, "题型：" + "，".join(item["patterns"]) + f"   ·   {item.get('provider')} {item.get('model', '')}"
             "   ·   ✓ 已通过独立解题与核对\n\n", "muted")
        w(t, item["question"] + "\n")

        def reveal():
            btn.destroy()
            w(t, "\n\n评分标准（每条 1 分）\n", "h")
            by = {}
            for label, text in item["points"]:
                by.setdefault(label, []).append(text)
            for p in item["parts"]:
                w(t, f"({p['label']})  {p['marks']} 分   答案：{p['answer']}\n", "sub")
                for text in by.get(p["label"], []):
                    w(t, f"    ✓ {text}\n")
            w(t, "\n解答过程\n", "h")
            w(t, item["solution"] + "\n")

        btn = ttk.Button(bar, text="显示得分点与解答", style="Accent.TButton", command=reveal)
        btn.pack(side="left")
        ttk.Button(bar, text="查看验证记录", command=lambda: audit(item)).pack(side="left", padx=8)
        k.get("ui.status")(f"AI 题 #{item['id']} 已生成并通过验证")

    def audit(item):
        top = tk.Toplevel(k.get("ui.root"))
        top.title(f"AI 题 #{item['id']} — 各阶段原始回复")
        top.geometry("900x700")
        t = ui_text(top)
        t.frame.pack(fill="both", expand=True)
        for e in item["log"]:
            w(t, f"── 第 {e['attempt']} 次 · {e['stage']} ──\n", "sub")
            w(t, e["reply"] + "\n\n", "mono")

    k.on("gen.started", started)
    k.on("gen.progress", progress)
    k.on("gen.error", error)
    k.on("gen.done", show)
    k.on("select.generated", lambda gid: show(store.generated(gid)))
