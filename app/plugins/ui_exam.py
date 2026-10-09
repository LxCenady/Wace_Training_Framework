"""模拟考试. One job: sit a timed paper (a real past paper or an AI-assembled one), then mark it.

Timing follows WACE: calculator-free 5 min reading + 50 min working; calculator-assumed 10 + 100.
AI papers follow the blueprint of the real ones: patterns drawn in proportion to the marks they carried in
past papers of that subject and section, the median total and question count, difficulty rising through the
paper. Marking reuses self-marking (right-click a part in the opened question); the score is the paper total
minus the marks recorded as lost since the exam started.
"""
import base64, os, random, shutil, threading, time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog, ttk

TIMES = {"CalcFree": (5, 50), "CalcAssumed": (10, 100)}
BLUEPRINT = {("MAM", "CalcFree"): (52, 7), ("MAM", "CalcAssumed"): (98, 10),  # median total marks, questions
             ("MAS", "CalcFree"): (48, 8), ("MAS", "CalcAssumed"): (89, 11)}
SEC_NAME = {"CalcFree": "计算器禁用", "CalcAssumed": "计算器允许"}


def plan(weights, total, count, rng):
    """-> [(patterns, marks, difficulty)] for an AI paper; patterns sampled by historical weight, no repeats."""
    pool = dict(weights)
    marks = [total // count + (1 if i < total % count else 0) for i in range(count)]
    out = []
    for i, m in enumerate(marks):
        codes = []
        for _ in range(2 if rng.random() < 0.35 and len(pool) > 1 else 1):  # a third of questions combine two
            pick = rng.choices(list(pool), weights=list(pool.values()))[0]
            if codes and pick.split(".")[1] != codes[0].split(".")[1]:  # combine within one topic only
                continue
            codes.append(pick)
            pool.pop(pick)
        level = "基础" if i < count * 0.3 else "拔高" if i >= count * 0.75 else "标准"
        out.append((codes, m, level))
    return out


def setup(k):
    store, root, C = k.get("store"), k.get("ui.root"), k.get("ui.colors")
    state = {"exam": None, "job": None, "score": None}

    # ---------- start page
    def show():
        stop_timer()
        page = k.get("ui.tab")("exam", "模拟考试")
        f = ttk.Frame(page, padding=14)
        f.pack(fill="x")
        ttk.Label(f, text="模拟考试", style="H.TLabel").grid(row=0, column=0, columnspan=6, sticky="w")
        subj, sec, src = tk.StringVar(value="MAM"), tk.StringVar(value="CalcAssumed"), tk.StringVar(value="past")
        years = sorted({r[0] for r in store.q("SELECT DISTINCT year FROM questions")}, reverse=True)
        year = tk.StringVar(value=str(years[0]))
        ttk.Label(f, text="科目").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Combobox(f, textvariable=subj, values=["MAM", "MAS"], state="readonly", width=6).grid(row=1, column=1)
        ttk.Label(f, text="卷型").grid(row=1, column=2, sticky="w", padx=(12, 0))
        ttk.Combobox(f, textvariable=sec, values=["CalcFree", "CalcAssumed"], state="readonly", width=12).grid(
            row=1, column=3)
        ttk.Radiobutton(f, text="历年真卷", value="past", variable=src).grid(row=2, column=0, sticky="w")
        ttk.Combobox(f, textvariable=year, values=[str(y) for y in years], state="readonly", width=6).grid(
            row=2, column=1)
        ttk.Radiobutton(f, text="AI 组卷（按历年题型分值比例，难度前易后难；每题都经完整验证，约 5–10 分钟）",
                        value="ai", variable=src).grid(row=3, column=0, columnspan=6, sticky="w")
        msg = ttk.Label(f, style="Muted.TLabel", wraplength=820, justify="left")
        msg.grid(row=5, column=0, columnspan=6, sticky="w", pady=(6, 0))
        ttk.Button(f, text="开始考试", style="Accent.TButton",
                   command=lambda: start(subj.get(), sec.get(), src.get(), year.get(), msg)).grid(
            row=4, column=0, columnspan=2, sticky="w", pady=(10, 0))

        hist = ttk.Frame(page, padding=(14, 0))
        hist.pack(fill="both", expand=True)
        ttk.Label(hist, text="历次模拟考试（双击继续或查看）", style="H.TLabel").pack(anchor="w", pady=(8, 4))
        table = ttk.Treeview(hist, columns=("when", "paper", "score", "state"), show="headings", height=12)
        for c, h, w in (("when", "时间", 140), ("paper", "试卷", 300), ("score", "得分", 120), ("state", "状态", 120)):
            table.heading(c, text=h)
            table.column(c, width=w, anchor="w")
        table.pack(fill="both", expand=True)
        for e in store.exams():
            got = e["total"] - e["lost"]
            table.insert("", "end", iid=str(e["id"]), values=(
                e["created"], f"{e['subject']} {SEC_NAME[e['section']]} · {paper_name(e)}",
                f"{got} / {e['total']}" if e["submitted"] else "—", "已交卷" if e["submitted"] else "未交卷"))
        table.bind("<Double-1>", lambda ev: table.focus() and open_exam(store.exam(int(table.focus()))))

    def progress_page(subj, sec, total, items):
        """The exam tab while an AI paper is assembled: one row per question, live stage, overall bar."""
        page = k.get("ui.tab")("exam", "模拟考试")
        head = ttk.Frame(page, padding=(14, 12, 14, 4))
        head.pack(fill="x")
        ttk.Label(head, text=f"正在组卷：{subj} {SEC_NAME[sec]} · {len(items)} 题 · {total} 分",
                  style="H.TLabel").pack(side="left")
        ttk.Button(head, text="返回", command=show).pack(side="right")
        clock = ttk.Label(head, style="Muted.TLabel")
        clock.pack(side="right", padx=12)
        bar = ttk.Progressbar(page, maximum=len(items))
        bar.pack(fill="x", padx=14, pady=4)
        msg = ttk.Label(page, style="Muted.TLabel", wraplength=900, justify="left",
                        text="每道题依次：出题 → 独立解题 → 核对 → SymPy 验算 → 拆得分点；同时进行 "
                             f"{int(k.get('config').get('parallel', 4))} 道。可以切到别的页面，完成后自动打开试卷。")
        msg.pack(anchor="w", padx=14, pady=(0, 6))
        rows = ttk.Treeview(page, columns=("n", "patterns", "level", "marks", "status", "time"), show="headings",
                            height=len(items))
        for c, h, w in (("n", "#", 40), ("patterns", "题型", 330), ("level", "难度", 60), ("marks", "分", 40),
                        ("status", "状态", 380), ("time", "用时", 60)):
            rows.heading(c, text=h)
            rows.column(c, width=w, anchor="w", stretch=c == "status")
        rows.pack(fill="x", padx=14)
        for i, (codes, marks, level) in enumerate(items):
            rows.insert("", "end", iid=str(i), values=(f"Q{i + 1}", "；".join(store.pattern_name(c) for c in codes),
                                                         level, marks, "排队中", ""))
        return msg, rows, bar, clock

    def stage_text(event):
        """Generator progress line ('[2] VERIFY …', '[1] 未通过：…', 'SYMPY 验算 3 个小问 …') -> short status."""
        names = {"GENERATE": "出题", "SOLVE": "独立解题", "VERIFY": "核对", "MARKS": "拆得分点"}
        for key, zh in names.items():
            if key in event:
                attempt = event[1:event.index("]")] if event.startswith("[") else "1"
                return f"第 {attempt} 次 · {zh}中…"
        if "SYMPY" in event:
            return "SymPy 验算中…"
        if "未通过" in event:
            return "未通过，重新出题：" + event.split("：", 1)[-1][:70]
        return event[:80]

    def export_exam(e):
        """AI paper -> exam-style question paper + answer paper; past paper -> copies of the official exam + key."""
        reading, working = TIMES[e["section"]]
        name = f"WTF_{e['subject']}_{e['section']}_{paper_name(e).replace(' ', '')}_{e['created'][:10]}"
        if e["source"] == "ai":
            if not k.get("export.worksheet", None):
                return
            path = filedialog.asksaveasfilename(title="导出模拟卷", defaultextension=".pdf", initialfile=name + ".pdf",
                                                filetypes=[("PDF", "*.pdf")])
            if not path:
                return
            title = f"WACE {e['subject']} 模拟卷 · {SEC_NAME[e['section']]}"
            meta = (f"{len(e['refs'])} 题 · 共 {e['total']} 分 · 阅读时间 {reading} 分钟 + 作答时间 {working} 分钟 · "
                    f"{e['created'][:10]} · WTF — WACE Training Framework")
            q, a = k.get("export.worksheet")([int(r) for _, r in e["refs"]], path, title, meta)
            k.get("ui.status")(f"已导出：{os.path.basename(q)} + {os.path.basename(a)}")
            if hasattr(os, "startfile"):
                os.startfile(q)
            return
        folder = filedialog.askdirectory(title="导出真卷：选择保存的文件夹")
        if not folder:
            return
        d = store.question(e["refs"][0][1])
        out = []
        for rel, suffix in ((d["exam"], ""), (d["key"], "_评分标准")):
            dest = os.path.join(folder, name + suffix + ".pdf")
            shutil.copyfile(os.path.join(k.root, rel), dest)
            out.append(dest)
        k.get("ui.status")(f"已导出官方原卷与评分标准到 {folder}")
        if hasattr(os, "startfile"):
            os.startfile(out[0])

    def paper_name(e):
        return f"{e['source'][5:]} 真卷" if e["source"].startswith("past:") else "AI 组卷"

    def start(subj, sec, src, year, msg):
        if src == "past":
            qs = store.paper(subj, year, sec)
            if not qs:
                msg.configure(text="本机没有这份试卷（导入真题后再试）")
                return
            eid = store.save_exam(subj, sec, f"past:{year}", [["past", q] for q, _ in qs], sum(m for _, m in qs))
            open_exam(store.exam(eid))
            return
        total, count = BLUEPRINT[(subj, sec)]
        items = plan(store.pattern_weights(subj, sec), total, count, random.Random())
        post, done, failed = k.get("ui.post"), [], []
        msg, rows, bar, clock = progress_page(subj, sec, total, items)
        t0 = time.time()

        def tick():
            if len(done) + len(failed) < count and clock.winfo_exists():
                clock.configure(text=f"已用 {int(time.time() - t0) // 60}:{int(time.time() - t0) % 60:02d}")
                root.after(1000, tick)

        tick()

        def progress():
            if bar.winfo_exists():
                bar.configure(value=len(done) + len(failed))
                msg.configure(text=f"已完成 {len(done)} / {count} 题" + (f"，{len(failed)} 题未通过" if failed else ""))
            k.get("ui.status")(f"AI 组卷：已完成 {len(done)} / {count} 题" + (f"，{len(failed)} 题未通过" if failed else ""))

        def row(i, status, started=None):
            took = f"{time.time() - started:.0f}s" if started else ""

            def apply():  # the page may have been left ("返回") while questions are still being made
                if rows.winfo_exists() and rows.exists(str(i)):
                    rows.set(str(i), "status", status)
                    rows.set(str(i), "time", took)
            post(apply)

        fatal = k.get("llm.ProviderError", ())
        stop = {}  # the first error retrying cannot fix (no balance, bad key) skips the rest of the paper

        def one(i_spec):
            i, (codes, marks, level) = i_spec
            if stop:
                failed.append(f"Q{i + 1} 已跳过：{stop['why']}")
                row(i, "已跳过（API 错误，见上方）")
                post(progress)
                return None
            started = time.time()
            row(i, "出题中…", started)

            def event(kind, data):
                if kind == "progress":
                    row(i, stage_text(data), started)

            try:
                item = k.get("generator.run")(codes, sec, marks, event, difficulty=level)
                done.append(item)
                row(i, f"✓ 通过（{item['marks']} 分）", started)
                post(progress)
                return item
            except Exception as e:  # a failed question is dropped; the paper is assembled from the rest
                if isinstance(e, fatal):
                    stop.setdefault("why", str(e))
                    row(i, f"✗ API 错误：{str(e)[:90]}", started)
                else:
                    row(i, f"✗ 未通过验证：{str(e)[:90]}", started)
                failed.append(f"Q{i + 1} {'+'.join(codes)}（{level}）：{type(e).__name__}: {e}")
                post(progress)
                return None

        def work():
            with ThreadPoolExecutor(int(k.get("config").get("parallel", 4))) as pool:
                got = [it for it in pool.map(one, enumerate(items)) if it]
            if failed:  # every reason, for the student and for a bug report
                try:
                    with open(os.path.join(k.root, "WTF.log"), "a", encoding="utf-8") as f:
                        f.write("\n--- AI 组卷：未通过的题 ---\n" + "\n".join(failed) + "\n")
                except OSError:
                    pass
            if not got:
                reasons = "\n".join("· " + r[:160] for r in failed[:5])
                text = (f"组卷失败：{stop['why']}" if stop else
                        f"组卷失败：{count} 题都没有通过验证。原因（详见 WTF.log）：\n{reasons}")
                post(lambda: (msg.winfo_exists() and msg.configure(text=text), k.get("ui.status")(text.split("\n")[0])))
                return
            got_marks = sum(it["marks"] for it in got)
            eid = store.save_exam(subj, sec, "ai", [["gen", it["id"]] for it in got], got_marks)
            post(lambda: k.get("ui.status")(f"AI 组卷完成：{len(got)} 题、{got_marks} 分" + (
                f"（{len(failed)} 题未通过，已略去，原因见 WTF.log）" if failed else "")))
            post(lambda: open_exam(store.exam(eid)))

        threading.Thread(target=work, daemon=True).start()

    # ---------- sitting the paper
    def stop_timer():
        if state["job"]:
            root.after_cancel(state["job"])
            state["job"] = None

    def open_exam(e):
        stop_timer()
        state["exam"] = e
        page = k.get("ui.tab")("exam", "模拟考试")
        bar = ttk.Frame(page, padding=(12, 8))
        bar.pack(fill="x")
        ttk.Label(bar, text=f"{e['subject']} {SEC_NAME[e['section']]} · {paper_name(e)} · {e['total']} 分",
                  style="H.TLabel").pack(side="left")
        ttk.Button(bar, text="返回", command=show).pack(side="right")
        ttk.Button(bar, text="导出 PDF", command=lambda: export_exam(e)).pack(side="right", padx=6)
        if e["submitted"]:
            return marking(page, e)
        row2 = ttk.Frame(page, padding=(12, 0, 12, 6))
        row2.pack(fill="x")
        clock = ttk.Label(row2, style="H.TLabel", foreground=C["warn"])
        clock.pack(side="left")
        ttk.Button(row2, text="交卷", style="Accent.TButton", command=lambda: submit(e)).pack(side="left", padx=12)
        ttk.Label(row2, text="公式表在右侧（F2 收起）", style="Muted.TLabel").pack(side="left")
        if not e["started"]:
            e["started"] = time.strftime("%Y-%m-%d %H:%M")
            store.update_exam(e["id"], started=e["started"])
            state["t0"] = time.time()
        else:
            state["t0"] = time.mktime(time.strptime(e["started"], "%Y-%m-%d %H:%M"))
        reading, working = (m * 60 for m in TIMES[e["section"]])

        def tick():
            left = reading + working - (time.time() - state["t0"])
            if left <= 0:
                state["job"] = None
                return submit(e, auto=True)
            phase, rest = ("阅读时间", left - working) if left > working else ("作答时间", left)
            clock.configure(text=f"{phase} {int(rest // 60):02d}:{int(rest % 60):02d}")
            state["job"] = root.after(1000, tick)

        tick()
        inner = k.get("ui.scroll")(page)
        for n, (src, ref) in enumerate(e["refs"], 1):
            question_block(inner, n, src, ref)

    keep = []

    def question_block(parent, n, src, ref):
        if src == "past":
            d = store.question(ref)
            ttk.Label(parent, text=f"Question {n}  ({d['marks']} 分)", style="H.TLabel",
                      background=C["panel"]).pack(anchor="w", padx=12, pady=(12, 2))
            for png in k.get("render.regions")(d["exam"], d["exam_regions"], 1.1):
                img = tk.PhotoImage(data=base64.b64encode(png))
                keep.append(img)
                tk.Label(parent, image=img, bg="#ffffff", bd=1, relief="solid").pack(anchor="w", padx=12, pady=2)
        else:
            it = store.generated(int(ref))
            ttk.Label(parent, text=f"Question {n}  ({it['marks']} 分)", style="H.TLabel",
                      background=C["panel"]).pack(anchor="w", padx=12, pady=(12, 2))
            text = tk.Text(parent, wrap="word", width=86, relief="flat", bg=C["panel"], fg=C["ink"],
                           font=("Microsoft YaHei UI", 11), padx=4, pady=4, insertwidth=0,
                           height=min(40, it["question"].count("\n") + len(it["question"]) // 80 + 3))
            text.pack(anchor="w", padx=12)
            math = k.get("math.write", None)
            if math:
                math(text, it["question"])
            else:
                text.insert("end", it["question"])
            text.configure(state="disabled")
            draw = k.get("figure.png", None)
            if it.get("figure") and draw:
                try:
                    img = tk.PhotoImage(data=base64.b64encode(draw(it["figure"], 480)[0]))
                    keep.append(img)
                    tk.Label(parent, image=img, bg="#ffffff").pack(anchor="w", padx=16, pady=4)
                except Exception:
                    pass  # the question text is still there; the figure is shown in the AI view too

    def submit(e, auto=False):
        stop_timer()
        e["submitted"] = time.strftime("%Y-%m-%d %H:%M")
        store.update_exam(e["id"], submitted=e["submitted"])
        k.get("ui.status")("时间到，已自动交卷" if auto else "已交卷：逐题打开批改")
        open_exam(store.exam(e["id"]))

    # ---------- marking
    def marking(page, e):
        top = ttk.Frame(page, padding=(12, 0))
        top.pack(fill="x")
        score = ttk.Label(top, style="H.TLabel", foreground=C["accent"])
        score.pack(anchor="w")
        state["score"] = score
        ttk.Label(top, text="逐题点「批改」：打开原题与评分标准，右键没拿满分的小问选「此题扣分」，这里的得分自动更新。",
                  style="Muted.TLabel").pack(anchor="w", pady=(2, 8))
        refresh_score()
        inner = k.get("ui.scroll")(page)
        for n, (src, ref) in enumerate(e["refs"], 1):
            row = ttk.Frame(inner, style="Panel.TFrame")
            row.pack(fill="x", padx=12, pady=3)
            marks = store.question(ref)["marks"] if src == "past" else store.generated(int(ref))["marks"]
            lost = sum(m["lost"] for m in store.mistakes() if (m["source"], m["ref"]) == (src, str(ref))
                       and m["created"] >= (e["started"] or e["created"]))
            ttk.Label(row, text=f"Question {n}　{marks - lost} / {marks} 分", background=C["panel"],
                      width=24).pack(side="left")
            ttk.Button(row, text="批改", command=lambda s=src, r=ref: k.emit(
                "select.question" if s == "past" else "select.generated", r if s == "past" else int(r))).pack(
                side="left")

    def refresh_score():
        e = state["exam"]
        if e and state["score"] is not None and state["score"].winfo_exists():
            e = store.exam(e["id"])
            state["score"].configure(text=f"得分 {e['total'] - e['lost']} / {e['total']}"
                                          f"（{100 * (e['total'] - e['lost']) / max(1, e['total']):.0f}%）")

    def changed():
        refresh_score()
        e = state["exam"]
        tab = k.get("ui.tab.frame")("exam")
        if e and e["submitted"] and tab is not None and k.get("ui.tabs").select() == str(tab):
            open_exam(store.exam(e["id"]))  # per-question scores too

    k.on("mistakes.changed", changed)
    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="模拟考试…", command=show, accelerator="Ctrl+M")
    k.get("ui.menu").add_cascade(label="考试", menu=menu)
    root.bind_all("<Control-m>", lambda ev: show())
    k.provide("exam.show", show)
    k.provide("exam.start", start)
    k.provide("exam.open", open_exam)
    k.provide("exam.export", export_exam)
    k.provide("exam.submit", lambda: state["exam"] and submit(state["exam"]))
