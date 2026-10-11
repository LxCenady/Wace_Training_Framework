"""External question view and manual review: paired crops, marks, searchable text and taxonomy tags."""
import base64
import tkinter as tk
from tkinter import ttk


def setup(k):
    keep = []

    def edit(paper_id, qid=None, saved=lambda: None):
        store = k.get("external.store")()
        paper = store.paper(paper_id)
        q = store.question(qid) if qid is not None else dict(label="", marks=None, exam_regions=[], answer_regions=[],
                    tags=[], stem="", answer_text="", confirmed=False, tag_note="")
        dlg = tk.Toplevel(k.get("ui.root"))
        dlg.title("外源题目：切块与标注")
        dlg.transient(k.get("ui.root"))
        form = ttk.Frame(dlg, padding=10)
        form.pack(fill="both", expand=True)
        label, marks = tk.StringVar(value=q["label"]), tk.StringVar(value=str(q["marks"] or ""))
        confirmed = tk.BooleanVar(value=bool(q["confirmed"]))
        row = ttk.Frame(form)
        row.pack(fill="x")
        ttk.Label(row, text="题号或小问（如 Q1、Q1(a)）").pack(side="left")
        ttk.Entry(row, textvariable=label, width=18).pack(side="left", padx=5)
        ttk.Label(row, text="分值").pack(side="left")
        ttk.Entry(row, textvariable=marks, width=6).pack(side="left", padx=5)
        ttk.Label(form, text="先核对题目与答案区域，再选择题型；新切块需要重新确认。", wraplength=700).pack(anchor="w", pady=5)
        crops = {name: [list(r) for r in q[name + "_regions"]] for name in ("exam", "answer")}
        row = ttk.Frame(form)
        row.pack(fill="x")
        crop_count = ttk.Label(row)
        crop_count.pack(side="right")

        def update_count():
            crop_count.configure(text=f"题目区域 {len(crops['exam'])} · 答案区域 {len(crops['answer'])}")

        def crop(name):
            def apply(regions):
                crops[name] = regions
                confirmed.set(False)
                update_count()
            k.get("external.crop.open")(store.asset(paper[name]), crops[name], apply)

        ttk.Button(row, text="题目切块", command=lambda: crop("exam")).pack(side="left")
        ttk.Button(row, text="答案切块", command=lambda: crop("answer")).pack(side="left", padx=5)
        update_count()
        ttk.Label(form, text="题型：可多选；只选此题实际考查的内容").pack(anchor="w", pady=(8, 2))
        tag_frame = ttk.Frame(form)
        tag_frame.pack(fill="x")
        tags = ttk.Treeview(tag_frame, columns=("name",), show="headings", height=7, selectmode="extended")
        tags.heading("name", text="题型")
        tags.column("name", width=680)
        tag_scroll = ttk.Scrollbar(tag_frame, orient="vertical", command=tags.yview)
        tags.configure(yscrollcommand=tag_scroll.set)
        tag_scroll.pack(side="right", fill="y")
        tags.pack(side="left", fill="x", expand=True)
        for (code,) in k.get("store").q("SELECT code FROM patterns WHERE code LIKE ? ORDER BY topic,n", paper["subject"] + ".%"):
            tags.insert("", "end", iid=code, values=(k.get("store").pattern_name(code),))
        if q["tags"]:
            tags.selection_set([tag for tag in q["tags"] if tags.exists(tag)])
            if tags.selection():
                tags.see(tags.selection()[0])
        ttk.Label(form, text="题目文字（用于检索和 AI 标注；扫描件可手动补充）").pack(anchor="w", pady=(8, 2))
        stem = tk.Text(form, height=5, width=85, wrap="word")
        stem.pack(fill="both", expand=True)
        stem.insert("1.0", q["stem"])
        ttk.Label(form, text="答案文字（可选：扫描件可手动补充；空白时从答案切块读取）").pack(anchor="w", pady=(8, 2))
        answer = tk.Text(form, height=3, width=85, wrap="word")
        answer.pack(fill="x")
        answer.insert("1.0", q["answer_text"])
        ttk.Label(form, text=q["tag_note"], wraplength=700, style="Muted.TLabel").pack(anchor="w", pady=5)
        ttk.Checkbutton(form, text="我已核对切块、分值与题型，确认标注", variable=confirmed).pack(anchor="w")
        message = ttk.Label(form, wraplength=700, style="Muted.TLabel")
        message.pack(anchor="w")

        def read_text():
            try:
                text = k.get("external.pdf.text")(store.asset(paper["exam"]), crops["exam"])
                stem.delete("1.0", "end")
                stem.insert("1.0", text)
                confirmed.set(False)
            except Exception as exc:
                message.configure(text=str(exc))

        def save():
            try:
                mark = int(marks.get()) if marks.get().strip() else None
                store.save_question(paper_id, label.get(), mark, crops["exam"], crops["answer"], tags.selection(),
                                    confirmed.get(), qid, stem.get("1.0", "end"), answer.get("1.0", "end"), q["tag_note"])
            except Exception as exc:
                message.configure(text=str(exc))
                return
            dlg.destroy()
            saved()

        row = ttk.Frame(form)
        row.pack(fill="x", pady=6)
        ttk.Button(row, text="读取题目切块文字", command=read_text).pack(side="left")
        ttk.Button(row, text="保存标注", command=save, style="Accent.TButton").pack(side="right")
        return dlg

    def show(qid):
        keep.clear()
        store = k.get("external.store")()
        q = store.question(qid)
        page = k.get("ui.tab")("external.question", "外源题目")
        inner = k.get("ui.scroll")(page)
        ttk.Label(inner, text=f"{q['title']} · {q['source']} · {q['label']} · {q['marks'] or '?'} 分", style="H.TLabel").pack(anchor="w", padx=12, pady=8)
        ttk.Label(inner, text="已确认" if q["confirmed"] else "待确认", style="Muted.TLabel").pack(anchor="w", padx=12)
        ttk.Label(inner, text="；".join(k.get("store").pattern_name(t) for t in q["tags"]), wraplength=800).pack(anchor="w", padx=12)
        ttk.Button(inner, text="编辑切块与标注", command=lambda: edit(q["paper"], qid, lambda: show(qid))).pack(anchor="w", padx=12, pady=6)

        def images(name):
            for p, *rectangle in q[name + "_regions"]:
                zoom = min(1.2, 800 / (rectangle[2] - rectangle[0]))
                png = k.get("external.pdf.render")(store.asset(q[name]), p, rectangle, zoom)
                img = tk.PhotoImage(data=base64.b64encode(png))
                keep.append(img)
                tk.Label(inner, image=img, bg="#ffffff").pack(anchor="w", padx=12, pady=4)

        images("exam")

        def reveal():
            btn.destroy()
            ttk.Label(inner, text="外源答案（以原件为准）", style="H.TLabel").pack(anchor="w", padx=12, pady=8)
            images("answer")
            if not q["answer_regions"]:
                ttk.Label(inner, text="此题尚未配对答案切块").pack(anchor="w", padx=12)

        btn = ttk.Button(inner, text="显示外源答案", command=reveal)
        btn.pack(anchor="w", padx=12, pady=8)

    k.provide("external.edit", edit)
    k.provide("external.question.show", show)
    k.on("select.external", show)
