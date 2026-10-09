"""Past-question view. One job: show the exam crop; reveal the marking key and its one-mark points on click."""
import base64
import tkinter as tk
from tkinter import ttk


def setup(k):
    store, C = k.get("store"), k.get("ui.colors")
    keep = []  # Tk drops PhotoImages without a Python reference

    def images(parent, pdf, regs):
        for png in k.get("render.regions")(pdf, regs):
            img = tk.PhotoImage(data=base64.b64encode(png))
            keep.append(img)
            tk.Label(parent, image=img, bg="#ffffff", bd=1, relief="solid").pack(anchor="w", padx=12, pady=4)

    def show(qid):
        keep.clear()
        d = store.question(qid)
        page = k.get("ui.tab")("question", "真题")
        inner = k.get("ui.scroll")(page)
        sec = "计算器禁用" if d["section"] == "CalcFree" else "计算器允许"
        ttk.Label(inner, text=f"{d['year']} {d['subject']} {sec}  Question {d['q']}  ·  {d['marks']} 分",
                  style="H.TLabel", background=C["panel"]).pack(anchor="w", padx=12, pady=(12, 2))
        for label, m, pats in d["parts"]:
            names = "；".join(f"{c} {store.pattern(c)['title'].split('★')[0].split('（')[0].strip()}" for c in pats)
            ttk.Label(inner, text=f"({label if label else '整题'})  {m or '?'} 分  ·  {names}", style="Muted.TLabel",
                      background=C["panel"]).pack(anchor="w", padx=16)
        images(inner, d["exam"], d["exam_regions"])
        box = ttk.Frame(inner, style="Panel.TFrame")
        btn = ttk.Button(inner, text="显示评分标准（拆分到每一分）", style="Accent.TButton")
        btn.pack(anchor="w", padx=12, pady=10)
        box.pack(fill="x")

        def reveal():
            btn.destroy()
            ttk.Label(box, text="评分标准（官方 marking key）", style="H.TLabel", background=C["panel"]).pack(
                anchor="w", padx=12, pady=(6, 2))
            if d["points_ok"]:
                for i, (label, text) in enumerate(d["points"], 1):
                    ttk.Label(box, text=f"{i:>2}. ({label or '整题'}) ✓ {text}", background=C["panel"],
                              wraplength=760).pack(anchor="w", padx=18)
            else:
                ttk.Label(box, text="此题评分点自动拆分与总分不符，请以下方原始评分标准图为准。", foreground=C["warn"],
                          background=C["panel"]).pack(anchor="w", padx=18)
            images(box, d["key"], d["key_regions"])

        btn.configure(command=reveal)

    k.on("select.question", show)
