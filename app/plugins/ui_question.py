"""Past-question view. One job: show the exam crop; reveal the marking key and its one-mark points on click."""
import base64
import tkinter as tk
from tkinter import ttk


def setup(k):
    store, C = k.get("store"), k.get("ui.colors")
    keep = []  # Tk drops PhotoImages without a Python reference

    def images(parent, pdf, regs):
        tab = k.get("ui.tab.frame", lambda key: None)("question")
        width = tab.winfo_width() if tab is not None and tab.winfo_width() > 100 else 800
        zoom = max(0.8, min(1.35, (width - 60) / 544))  # fit the centre pane; crops are 544 pt wide
        for png in k.get("render.regions")(pdf, regs, zoom):
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
        parts = {label: (m, pats) for label, m, pats in d["parts"]}

        def ctx(label):
            m, pats = parts.get(label, (None, []))
            pts = [t for l, t in d["points"] if l == label] if d["points_ok"] else []
            return {"source": "past", "ref": qid, "label": label, "part_marks": m or len(pts) or max(1, round(d["marks"] / max(1, len(parts)))),
                    "patterns": pats, "points": pts,
                    "title": f"{d['year']} {d['subject']} {'CF' if d['section'] == 'CalcFree' else 'CA'} "
                             f"Q{d['q']} ({label or '整题'})"}

        def markable(widget, label):
            if label in parts and k.get("mistakes.popup", None):
                widget.bind("<Button-3>", lambda e: k.get("mistakes.popup")(e, ctx(label)))

        for label, m, pats in d["parts"]:
            had = store.mistake("past", qid, label)
            row = ttk.Label(inner, text=f"({label if label else '整题'})  {m or '?'} 分  ·  "
                                        + "；".join(store.pattern_name(c) for c in pats)
                                        + (f"   ✗ 已扣 {had['lost']} 分" if had else ""),
                            style="Muted.TLabel", background=C["panel"])
            row.pack(anchor="w", padx=16)
            markable(row, label)
        images(inner, d["exam"], d["exam_regions"])
        box = ttk.Frame(inner, style="Panel.TFrame")
        btn = ttk.Button(inner, text="显示评分标准（拆分到每一分）", style="Accent.TButton")
        btn.pack(anchor="w", padx=12, pady=10)
        box.pack(fill="x")

        def reveal():
            btn.destroy()
            store.record_attempt("past", qid, [(label, ctx(label)["part_marks"], pats) for label, m, pats in d["parts"]])
            ttk.Label(box, text="评分标准（官方 marking key）· 右键小问或得分点可「此题扣分」", style="H.TLabel",
                      background=C["panel"]).pack(anchor="w", padx=12, pady=(6, 2))
            if d["points_ok"]:
                for i, (label, text) in enumerate(d["points"], 1):
                    pt = ttk.Label(box, text=f"{i:>2}. ({label or '整题'}) ✓ {text}", background=C["panel"],
                                   wraplength=760)
                    pt.pack(anchor="w", padx=18)
                    markable(pt, label)
            else:
                ttk.Label(box, text="此题评分点自动拆分与总分不符，请以下方原始评分标准图为准。", foreground=C["warn"],
                          background=C["panel"]).pack(anchor="w", padx=18)
            images(box, d["key"], d["key_regions"])

        btn.configure(command=reveal)

    k.on("select.question", show)
