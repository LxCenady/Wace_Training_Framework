"""Independent external-paper library: paired import, draft review and source-separated search."""
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def setup(k):
    state = {"paper": "", "busy": False}

    def import_dialog():
        dlg = tk.Toplevel(k.get("ui.root"))
        dlg.title("导入外源试卷与答案")
        dlg.transient(k.get("ui.root"))
        form = ttk.Frame(dlg, padding=12)
        form.pack(fill="both", expand=True)
        title, source = tk.StringVar(), tk.StringVar()
        subject, section = tk.StringVar(value="MAM"), tk.StringVar(value="CalcFree")
        paths = {name: tk.StringVar() for name in ("exam", "answer")}
        for row, (caption, variable) in enumerate((("试卷名称（可含年份）", title), ("来源（学校或机构）", source))):
            ttk.Label(form, text=caption).grid(row=row, column=0, sticky="w")
            ttk.Entry(form, textvariable=variable, width=48).grid(row=row, column=1, padx=6, pady=4)
        for row, (caption, variable, values) in enumerate((("科目", subject, ["MAM", "MAS"]),
                                                           ("卷型", section, ["CalcFree", "CalcAssumed"])), 2):
            ttk.Label(form, text=caption).grid(row=row, column=0, sticky="w")
            ttk.Combobox(form, textvariable=variable, values=values, state="readonly").grid(row=row, column=1, sticky="w", padx=6, pady=4)

        def choose(name):
            path = filedialog.askopenfilename(parent=dlg, title="选择 PDF 原件", filetypes=[("PDF", "*.pdf")])
            if path:
                paths[name].set(path)

        for row, (name, caption) in enumerate((("exam", "选择试卷 PDF"), ("answer", "选择答案 PDF")), 4):
            ttk.Button(form, text=caption, command=lambda n=name: choose(n)).grid(row=row, column=0, sticky="w")
            ttk.Entry(form, textvariable=paths[name], width=48, state="readonly").grid(row=row, column=1, padx=6, pady=4)
        ttk.Label(form, text="原件会复制到独立外源目录。自动切块只是草稿；扫描件与不规则版式请手动切块。",
                  wraplength=520).grid(row=6, column=0, columnspan=2, sticky="w", pady=8)
        msg = ttk.Label(form, wraplength=520)
        msg.grid(row=7, column=0, columnspan=2, sticky="w")

        def start():
            if not all(v.get().strip() for v in (title, source, *paths.values())):
                msg.configure(text="请填写名称、来源，并选择试卷与答案")
                return
            args = (paths["exam"].get(), paths["answer"].get(), title.get(), source.get(), subject.get(), section.get())
            button.state(["disabled"])
            msg.configure(text="正在导入并生成切块草稿…")

            def worker():
                try:
                    paper_id = k.get("external.store")().import_pair(*args)
                except Exception as exc:
                    error = str(exc)

                    def failed():
                        if dlg.winfo_exists():
                            button.state(["!disabled"])
                            msg.configure(text=error)
                    k.get("ui.post")(failed)
                    return

                def done():
                    state["paper"] = paper_id
                    if dlg.winfo_exists():
                        dlg.destroy()
                    show()
                k.get("ui.post")(done)
            threading.Thread(target=worker, daemon=True).start()

        button = ttk.Button(form, text="导入并自动切块", style="Accent.TButton", command=start)
        button.grid(row=8, column=0, columnspan=2, sticky="w", pady=8)
        return dlg

    def show():
        store = k.get("external.store")()
        page = k.get("ui.tab")("external", "外源卷库")
        bar = ttk.Frame(page, padding=10)
        bar.pack(fill="x")
        ttk.Label(bar, text="外源卷库", style="H.TLabel").pack(side="left")
        ttk.Button(bar, text="导入试卷与答案", command=import_dialog, style="Accent.TButton").pack(side="right")
        description = ttk.Label(page, text="学校或其他来源的卷子单独保存、单独检索；不计入 SCSA 真卷统计。", style="Muted.TLabel", wraplength=600)
        description.pack(anchor="w", padx=10)
        page.bind("<Configure>", lambda e: description.configure(wraplength=max(200, e.width - 24)))
        papers = ttk.Treeview(page, columns=("title", "source", "subject", "section", "count"), show="headings", height=2, selectmode="browse")
        for name, caption, width in (("title", "试卷", 210), ("source", "来源", 140), ("subject", "科目", 75), ("section", "卷型", 100), ("count", "切块数量", 65)):
            papers.heading(name, text=caption)
            papers.column(name, width=width, stretch=name in ("title", "source"))
        papers.pack(fill="x", padx=10, pady=6)
        for paper in store.papers():
            papers.insert("", "end", iid=paper["id"], values=(paper["title"], paper["source"], paper["subject"], "CF" if paper["section"] == "CalcFree" else "CA", paper["count"]))
        bar = ttk.Frame(page, padding=(10, 2))
        bar.pack(fill="x")

        def all_papers():
            state["paper"] = ""
            if papers.selection():
                papers.selection_remove(*papers.selection())
            fill()

        def new_question():
            if not state["paper"]:
                status.configure(text="请先在上方选中一份外源试卷")
                return
            k.get("external.edit")(state["paper"], saved=show)

        ttk.Button(bar, text="检索全部外源卷", command=all_papers).pack(side="left")
        ttk.Button(bar, text="新增题目或小问切块", command=new_question).pack(side="left", padx=5)
        chosen = []
        condition = ttk.Label(bar, style="Muted.TLabel")
        condition.pack(side="right")
        filters = ttk.Frame(page, padding=(10, 3))
        filters.pack(fill="x")
        subject, section, words = tk.StringVar(value=""), tk.StringVar(value=""), tk.StringVar()
        confirmed = tk.BooleanVar()
        for caption, variable, values, width in (("科目", subject, ["", "MAM", "MAS"], 6), ("卷型", section, ["", "CalcFree", "CalcAssumed"], 14)):
            ttk.Label(filters, text=caption).pack(side="left")
            ttk.Combobox(filters, textvariable=variable, values=values, width=width, state="readonly").pack(side="left", padx=4)
        word_row = ttk.Frame(page, padding=(10, 3))
        word_row.pack(fill="x")
        ttk.Label(word_row, text="关键词").pack(side="left")
        ttk.Checkbutton(word_row, text="只看已确认", variable=confirmed, command=lambda: fill()).pack(side="right", padx=4)
        ttk.Entry(word_row, textvariable=words, width=18).pack(side="left", fill="x", expand=True, padx=4)

        def tree_tags():
            unit, codes = k.get("tree.selection", lambda: (None, []))()
            chosen[:] = [unit] if unit else list(codes)
            fill()

        def clear_tags():
            chosen.clear()
            fill()

        actions = ttk.Frame(page, padding=(10, 3))
        actions.pack(fill="x")
        ttk.Button(actions, text="用左侧选中的单元/题型", command=tree_tags).pack(side="left")
        ttk.Button(actions, text="清除题型条件", command=clear_tags).pack(side="left", padx=4)
        body = ttk.Frame(page)
        table = ttk.Treeview(body, columns=("paper", "label", "marks", "state", "tags"), show="headings", selectmode="extended", height=5)
        for name, caption, width in (("paper", "试卷及来源", 155), ("label", "题号或小问", 120), ("marks", "分", 60), ("state", "状态", 100), ("tags", "题型", 150)):
            table.heading(name, text=caption)
            table.column(name, width=width, stretch=name in ("paper", "tags"))
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        table.pack(side="left", fill="both", expand=True)
        footer = ttk.Frame(page, padding=10)
        footer.pack(side="bottom", fill="x")
        status = ttk.Label(page, wraplength=900, style="Muted.TLabel")
        status.pack(side="bottom", anchor="w", padx=10, pady=(0, 6))
        body.pack(fill="both", expand=True, padx=10)

        def fill(*_):
            found = store.search(subject.get(), section.get(), words.get(), chosen, state["paper"], confirmed.get())
            table.delete(*table.get_children())
            for q in found:
                table.insert("", "end", iid=str(q["id"]), values=(f"{q['title']} · {q['source']}", q["label"], q["marks"] or "?",
                    "已确认" if q["confirmed"] else "待确认", "; ".join(k.get("store").pattern_name(t) for t in q["tags"])))
            condition.configure(text="；".join(chosen))
            status.configure(text=f"{len(found)} 个外源切块 · 双击打开题目与答案")

        def take_paper(_):
            if papers.selection():
                state["paper"] = papers.selection()[0]
                fill()

        def edit_selected():
            if table.selection():
                qid = int(table.selection()[0])
                k.get("external.edit")(store.question(qid)["paper"], qid, show)

        def delete_selected():
            ids = list(table.selection())
            if ids and messagebox.askyesno("删除外源切块", "删除选中的切块与标注？原始试卷和答案不会删除。", parent=k.get("ui.root")):
                for qid in ids:
                    store.delete_question(int(qid))
                show()

        def tag_selected():
            if state["busy"]:
                return
            ids = table.selection()
            if not ids:
                status.configure(text="请先选中需要 AI 标注的外源切块")
                return
            expected = [store.question(int(qid)) for qid in ids]
            if any(q["confirmed"] for q in expected):
                status.configure(text="已确认的标注受保护，请仅选择待确认切块")
                return
            state["busy"] = True
            status.configure(text="正在用你设置的 API 标注，结果仅保存为待确认草稿…")

            def worker():
                done, error = 0, ""
                try:
                    for q in expected:
                        proposal = k.get("external.tag.propose")(q["id"])
                        store.save_proposal(q["id"], proposal, q)
                        done += 1
                except Exception as exc:
                    error = str(exc)

                def finished():
                    state["busy"] = False
                    if status.winfo_exists():
                        fill()
                        status.configure(text=f"AI 标注草稿已保存 {done} 个" + (f" · {error}" if error else ""))
                    k.get("ui.status")(f"AI 标注草稿已保存 {done} 个" + (f" · {error}" if error else ""))
                k.get("ui.post")(finished)
            threading.Thread(target=worker, daemon=True).start()

        ttk.Button(footer, text="编辑切块与标注", command=edit_selected).pack(side="left")
        ttk.Button(footer, text="AI 标注选中项", command=tag_selected, style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(footer, text="删除选中切块", command=delete_selected).pack(side="right")
        table.bind("<Double-1>", lambda e: table.selection() and k.emit("select.external", int(table.selection()[0])))
        table.bind("<Return>", lambda e: table.selection() and k.emit("select.external", int(table.selection()[0])))
        papers.bind("<<TreeviewSelect>>", take_paper)
        if state["paper"] and papers.exists(state["paper"]):
            papers.selection_set(state["paper"])
        for variable in (subject, section, words):
            variable.trace_add("write", fill)
        fill()
        k.provide("external.table", table)

    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="外源卷库", command=show)
    menu.add_command(label="导入试卷与答案", command=import_dialog)
    k.get("ui.menu").add_cascade(label="外源卷库", menu=menu)
    k.provide("external.show", show)
    k.provide("external.import_dialog", import_dialog)
