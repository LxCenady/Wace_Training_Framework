"""模拟考试. One job: sit a timed paper (a real past paper or an AI-assembled one), then mark it.

Timing follows WACE: calculator-free 5 min reading + 50 min working; calculator-assumed 10 + 100.
AI papers follow the blueprint of the real ones: patterns drawn in proportion to the marks they carried in
past papers of that subject and section, the median total and question count, difficulty rising through the
paper. Marking reuses self-marking (right-click a part in the opened question); the score is the paper total
minus the marks recorded as lost since the exam started.
"""
import base64, random, threading, time
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk

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
        ttk.Radiobutton(f, text="AI 组卷（按历年题型分值比例，难度前易后难；每题都经完整验证，约 2–4 分钟）",
                        value="ai", variable=src).grid(row=3, column=0, columnspan=6, sticky="w")
        msg = ttk.Label(f, style="Muted.TLabel")
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
        msg.configure(text=f"正在组卷：{count} 题、{total} 分……")
        post, done = k.get("ui.post"), []

        def one(spec):
            codes, marks, level = spec
            try:
                item = k.get("generator.run")(codes, sec, marks, difficulty=level)
                done.append(item)
                post(lambda: msg.configure(text=f"正在组卷：已完成 {len(done)} / {count} 题"))
                return item
            except Exception as e:  # a failed question is dropped; the paper is assembled from the rest
                post(lambda e=e: msg.configure(text=f"一题未通过验证（{str(e)[:60]}），继续组卷…"))
                return None

        def work():
            with ThreadPoolExecutor(int(k.get("config").get("parallel", 4))) as pool:
                got = [it for it in pool.map(one, items) if it]
            if not got:
                post(lambda: msg.configure(text="组卷失败：所有题都没有通过验证"))
                return
            eid = store.save_exam(subj, sec, "ai", [["gen", it["id"]] for it in got], sum(it["marks"] for it in got))
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
    k.provide("exam.submit", lambda: state["exam"] and submit(state["exam"]))
