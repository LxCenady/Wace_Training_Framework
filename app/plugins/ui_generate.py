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

    def started(codes, count=1):
        page = k.get("ui.tab")("gen", "AI 出题")
        state.update(page=page, count=count, ids=[])
        t = ui_text(page)
        t.frame.pack(fill="both", expand=True)
        state["log"] = t
        w(t, f"正在生成并验证{'' if count == 1 else f' {count} 道题'}…\n", "h")
        w(t, "题型：" + "，".join(f"{c} {store.pattern(c)['title'].split('★')[0].strip()}" for c in codes) + "\n", "muted")
        w(t, "流程：出题 → 独立解题（只看题目）→ 独立核对 → 拆分得分点；全部通过前不显示答案。\n\n", "muted")
        k.get("ui.status")("AI 出题中…")

    def progress(msg):
        if "log" in state:
            w(state["log"], msg + "\n", "warn" if "未通过" in msg else "mono")

    def error(msg):
        progress("✗ " + msg)
        k.get("ui.status")("生成失败：" + msg[:120])

    def done(item):
        """Single question: show it. Batch: log it and keep the progress view until gen.finished."""
        if state.get("count", 1) == 1:
            show(item)
        else:
            state["ids"].append(item["id"])
            progress(f"✓ 完成：AI 题 #{item['id']}（{item['marks']} 分 · {item.get('difficulty', '标准')}）")
            k.get("ui.status")(f"已完成 {len(state['ids'])} / {state['count']} 道")

    def finished(ok, count):
        if count == 1 or "log" not in state:
            return
        t = state["log"]
        w(t, f"\n批量完成：{ok} / {count} 道通过验证" + ("" if ok == count else f"，{count - ok} 道未通过（未保存、不显示答案）")
          + "\n", "h")
        bar = ttk.Frame(state["page"])
        bar.pack(fill="x", padx=8, pady=6, before=t.frame)
        ttk.Button(bar, text="在「我的 AI 题库」中查看", style="Accent.TButton",
                   command=lambda: k.get("mybank.show", lambda: None)()).pack(side="left")
        k.get("ui.status")(f"批量完成：{ok} / {count} 道通过验证")

    def show(item):
        page = k.get("ui.tab")("gen", "AI 出题")
        state.pop("log", None)
        bar = ttk.Frame(page)
        bar.pack(fill="x", padx=8, pady=6)
        t = ui_text(page)
        t.frame.pack(fill="both", expand=True)
        sec = {"CalcFree": "计算器禁用", "CalcAssumed": "计算器允许"}.get(item.get("section"), item.get("section", ""))
        w(t, f"AI 题 #{item['id']} · {item['marks']} 分 · {sec} · {item.get('difficulty') or '标准'}\n", "h")
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
    k.on("gen.done", done)
    k.on("gen.finished", finished)
    k.on("select.generated", lambda gid: show(store.generated(gid)))
