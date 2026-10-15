"""First-run wizard. One job: get the SCSA papers onto this computer, build the question bank, restart.

The papers are © SCSA and are not shipped with the app. Everything is fixed, nothing is watched:
2016-2019 come from the Wayback Machine straight into the bank's papers folders; 2020-2025 the student opens in
their own browser (the site refuses scripts) and saves with the browser's default — the Downloads folder — then
presses one button that checks that folder once (files are recognised by name or by content, tools/paperid.py).
Saved somewhere else, or on a Mac that keeps the app out of Downloads: "选择已下载的文件…" picks the files in the
system dialog (a file the user picks is always readable, macOS privacy included), wherever they are.
The bank is built only when every paper is in, and then by itself.

Subjects are chosen first (students take one or two of the maths courses, rarely all): only their papers are
downloaded and checked, and the bank holds only them. The choice is kept in the settings (`subjects`).
题库 → 管理科目 reopens this wizard over an existing bank (main.py --setup) to add or drop subjects; it rebuilds
when the newly needed papers are all in, or on request, and can return to the app without rebuilding.
"""
import ctypes, os, subprocess, sys, threading, time, uuid, webbrowser
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog, messagebox, ttk
import plat

BATCH = 6  # links opened per click
PARALLEL = 3  # archive downloads at the same time
FONT = plat.UI_FONT
SAVE = plat.MOD_NAME + "S"  # ⌘S on a Mac, Ctrl+S elsewhere
SAVE_HOW = ("⌘S（Safari 也可以用菜单「文件 → 存储为…」），保存位置选「下载」" if plat.MAC
            else "Ctrl+S（或点浏览器的下载按钮），直接点「保存」——不要改位置，存进「下载」文件夹")
NOT_PDF = "不是 PDF：存下来的是网页或官网的验证页面。请在浏览器里等 PDF 显示出来后再保存"
DOWNLOADS = "{374DE290-123F-4565-9164-39C4925E467B}"  # Windows known folder: the browser's default save place


def downloads_folder():
    """The user's real Downloads folder (it may have been moved off C: or into OneDrive)."""
    name = "Downloads"
    try:
        guid = uuid.UUID(DOWNLOADS)
        buf = ctypes.c_wchar_p()
        guid_buf = (ctypes.c_byte * 16).from_buffer_copy(guid.bytes_le)
        if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(guid_buf), 0, None, ctypes.byref(buf)) == 0:
            path = buf.value
            ctypes.windll.ole32.CoTaskMemFree(buf)
            return path
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), name)


import subjects
SUBJECTS = subjects.names(engine="flow")  # the wizard fetches papers: built-from-papers packs only


def restart(args=None):
    """Start the app again: with `args` (e.g. [] after building), else the same arguments (a language switch keeps
    --setup)."""
    main = [] if getattr(sys, "frozen", False) else [os.path.abspath(sys.modules["__main__"].__file__)]
    subprocess.Popen([sys.executable, *main, *(sys.argv[1:] if args is None else args)], close_fds=True)


def setup(k):
    import fetch, build_all  # tools/, on sys.path via main.py
    from build_docs import TOPICS  # subjects the bank can be built for
    root, post = k.root, k.get("ui.post")
    C = k.get("ui.colors")
    cfg = k.get("config")
    managing = os.path.isfile(os.path.join(root, "wace.db"))  # 题库 → 管理科目 (main.py --setup)
    page = k.get("ui.tab")("setup", "管理科目：添加或移除科目" if managing else "第一次使用：导入真题")
    k.get("ui.root").title(k.get("edition", {}).get("name", "WTF — Worldwide Teachers Friend") + " — 导入真题")
    left = k.get("ui.left")
    ttk.Label(left, text="欢迎", style="H.TLabel").pack(anchor="w", padx=12, pady=(12, 4))
    ttk.Label(left, wraplength=400, justify="left", text=(
        "SCSA的真题、评分标准和公式表受版权保护，不随程序分发；需要你自己从官方网站下载一次，"
        "导入后，题库、知识图谱和评分标准会保存在本机；AI 出题需要先在设置中配置模型服务，并保持联网。\n\n"
        "每门课约 37 MB，下载与建库只需做一次；之后可以在「题库 → 管理科目」随时添加或移除科目。")).pack(
        anchor="w", padx=12)

    lang = tk.StringVar(value="English" if k.get("config").get("language") == "en" else "中文")

    def switch_language(_=None):
        k.get("config")["language"] = "en" if lang.get() == "English" else "zh"
        k.get("config.save")()
        restart()
        k.get("ui.root").destroy()

    row = ttk.Frame(left)
    row.pack(anchor="w", padx=12, pady=(14, 0))
    ttk.Label(row, text="界面语言 / Language").pack(side="left")
    box = ttk.Combobox(row, textvariable=lang, values=["中文", "English"], state="readonly", width=9)
    box.pack(side="left", padx=6)
    box.bind("<<ComboboxSelected>>", switch_language)

    state = {"folder": downloads_folder(), "opened": set(), "busy": False}
    offered = [s for s in fetch.subjects(root) if s in TOPICS]  # can be fetched and built
    on_disk = [s for s in offered if any(fetch.is_pdf(os.path.join(root, x[0])) for x in fetch.sources(root, [s]))]
    chosen = [s for s in cfg.get("subjects", on_disk) if s in offered]  # old installs: what is already there

    def missing():
        return fetch.missing(root, chosen)  # required papers only: sample papers and reports are optional

    def all_sources():
        return fetch.sources(root, chosen, optional=False)

    head = ttk.Frame(page)
    head.pack(fill="x", padx=16, pady=(14, 4))
    ttk.Button(head, text='导入学科包…', command=lambda: k.get('subjects.import')()).pack(side='right')
    ttk.Button(head, text='WTF Hub：选择学科…', command=lambda: k.get('hub.open')()).pack(side='right', padx=6)
    count = ttk.Label(head, style="H.TLabel")
    count.pack(side="left")
    bar = ttk.Progressbar(head, length=320, maximum=1)  # set in refresh(): the chosen subjects
    bar.pack(side="left", padx=12)
    nxt = tk.Label(page, anchor="w", justify="left", wraplength=1000, bg=C["accent"], fg="#ffffff", padx=12, pady=8,
                   font=(FONT, 11, "bold"))  # what to do now, in one line
    nxt.pack(fill="x", padx=16, pady=(4, 2))

    # choose the subjects first
    s0 = ttk.LabelFrame(page, text="选择科目（只下载你选的科目；之后可以在「题库 → 管理科目」随时增减）", padding=10)
    s0.pack(fill="x", padx=16, pady=6)
    picks = {}
    if not SUBJECTS:  # WTF ships no subject: every course is a pack from WTF Hub (or a local .wtfpack)
        ttk.Label(s0, text="还没有安装学科。打开 WTF Hub 选择你要学的科目，装好后在这里提供原卷并建库。").pack(side="left")
        ttk.Button(s0, text="WTF Hub：选择学科…", style="Accent.TButton",
                   command=lambda: k.get('hub.open')()).pack(side="left", padx=12)
    for subj, name in SUBJECTS.items():
        var = tk.BooleanVar(value=subj in chosen)
        box = ttk.Checkbutton(s0, text=name, variable=var, command=lambda s=subj: toggle(s))
        box.pack(side="left", padx=(0, 18))
        if subj not in offered:
            box.state(["disabled"])
            box.configure(text=name + "（整理中，暂不可选）")
        picks[subj] = var

    # already have the papers (another computer, a USB stick, a colleague): one step, any folder or any files
    s_have = ttk.LabelFrame(page, text="我已有资源？一键导入（选一个文件夹，或框选文件；认出的真题复制到建库位置，原文件不动）", padding=10)
    s_have.pack(fill="x", padx=16, pady=6)
    b_have_dir = ttk.Button(s_have, text="选择文件夹…", style="Accent.TButton")
    b_have_dir.pack(side="left")
    b_have_files = ttk.Button(s_have, text="选择文件…（可框选多个）")
    b_have_files.pack(side="left", padx=8)
    ttk.Label(s_have, style="Muted.TLabel", text="包括子文件夹；不认识的文件会跳过并列出原因").pack(side="left", padx=6)

    # ① archived years
    s1 = ttk.LabelFrame(page, text="① 2016–2019：自动下载（Wayback Machine 存档）", padding=10)
    s1.pack(fill="x", padx=16, pady=6)
    b1 = ttk.Button(s1, text="开始下载", style="Accent.TButton")
    b1.pack(side="left")
    s1_msg = ttk.Label(s1, style="Muted.TLabel")
    s1_msg.pack(side="left", padx=10)

    # ② browser years
    s2 = ttk.LabelFrame(page, text="② 2020–2025：用你的浏览器下载（官网不允许程序直接下载）", padding=10)
    s2.pack(fill="x", padx=16, pady=6)
    ttk.Label(s2, wraplength=900, justify="left", text=(
        f"1. 点「打开下一批」，浏览器会打开 {BATCH} 个官方 PDF。\n"
        f"2. 在每个 PDF 页面按 {SAVE_HOW}；文件名随意。\n"
        "3. 这一批存好后，点「我存好了，检查下载文件夹」。全部到齐后自动建库并进入学习系统。\n"
        "存到了别的地方，或者检查不到？点「选择已下载的文件…」，在弹出的窗口里直接选中这些 PDF（可以一次全选）。")).pack(
        anchor="w")
    row = ttk.Frame(s2)
    row.pack(fill="x", pady=(8, 0))
    b2 = ttk.Button(row, text=f"打开下一批（{BATCH} 个）", style="Accent.TButton")
    b2.pack(side="left")
    b_check = ttk.Button(row, text="我存好了，检查下载文件夹", style="Accent.TButton")
    b_check.pack(side="left", padx=8)
    b_pick = ttk.Button(row, text="选择已下载的文件…")
    b_pick.pack(side="left")
    folder_lbl = ttk.Label(row, style="Muted.TLabel")
    folder_lbl.pack(side="left", padx=10)

    # ③ build
    s3 = ttk.LabelFrame(page, text="③ 建立题库（全部文件到齐后自动开始，约 1 分钟）", padding=10)
    s3.pack(fill="x", padx=16, pady=6)
    b3 = ttk.Button(s3, text="重新建库", style="Accent.TButton")  # only for a retry: building starts by itself
    b3.pack(side="left")
    s3_msg = ttk.Label(s3, style="Muted.TLabel")
    s3_msg.pack(side="left", padx=10)

    lists = ttk.Frame(page)
    lists.pack(fill="both", expand=True, padx=16, pady=(6, 12))
    table = ttk.Treeview(lists, columns=("file", "status"), show="headings", height=8)
    table.heading("file", text="还缺的文件（双击在浏览器打开）")
    table.heading("status", text="来源")
    table.column("file", width=520)
    table.column("status", width=160)
    sb = ttk.Scrollbar(lists, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    table.pack(side="left", fill="both", expand=True)
    log = k.get("ui.text")(lists, height=8)
    log.frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
    write = k.get("ui.write")

    def say(msg, *tags):
        write(log, msg + "\n", *tags)
        log.see("end")

    def toggle(subj):
        if picks[subj].get() and subj not in chosen:
            chosen.append(subj)
        elif not picks[subj].get() and subj in chosen:
            chosen.remove(subj)
        chosen.sort(key=offered.index)
        cfg["subjects"] = list(chosen)
        k.get("config.save")()
        refresh()
        if chosen and not state["busy"] and not state.get("downloading") and any(m[3] for m in missing()):
            download_archived()  # a newly chosen subject: its archived years start at once

    def refresh():
        miss, every = missing(), all_sources()
        have = len(every) - len(miss)
        count.configure(text=f"已导入 {have} / {len(every)} 个文件" if chosen else "先选择科目")
        bar.configure(value=have, maximum=max(1, len(every)))
        folder_lbl.configure(text=f"下载文件夹：{state['folder']}")
        table.delete(*table.get_children())
        for rel, url, official, arch in miss:
            table.insert("", "end", iid=rel, values=(rel, "Wayback 自动" if arch else "浏览器下载"))
        miss_arch = sum(1 for m in miss if m[3])
        miss_browser = sum(1 for m in miss if not m[3])
        s1_msg.configure(text="已全部下载 ✓" if not miss_arch else f"还缺 {miss_arch} 个")
        b2.state(["disabled"] if not miss_browser else ["!disabled"])
        s3_msg.configure(text="全部就绪 ✓" if not miss else f"还缺 {len(miss)} 个文件：全部到齐后自动开始")
        if not state["busy"]:
            b3.state(["disabled"] if miss or not chosen else ["!disabled"])  # never a partial bank
            b1.state(["disabled"] if not miss_arch or state.get("downloading") else ["!disabled"])
            if not chosen:
                b2.state(["disabled"])
        nxt.configure(text=next_step(miss_arch, miss_browser))
        return miss

    def next_step(miss_arch, miss_browser):
        if not chosen:
            return "先在上面勾选你读的科目（可以多选），只会下载这些科目的真题。"
        if state["busy"]:
            return "正在建立题库，约 1 分钟，完成后自动进入学习系统。请不要关闭窗口。"
        if not miss_arch and not miss_browser:
            return ("所选科目的文件已全部就绪：点「按所选科目重建题库」，或「返回学习系统」不作改动。" if managing
                    else "全部文件已到齐，马上自动建库。")
        if miss_arch and not state.get("downloading"):
            retry = f"第 ① 步还有 {miss_arch} 个存档没下载成功：点「开始下载」重试。"
            return retry + (f"　第 ② 步还差 {miss_browser} 个（浏览器保存）。" if miss_browser else "")
        if miss_browser:
            now = (f"第 ② 步：点「打开下一批」→ 浏览器里每个 PDF 按 {SAVE} → 保存 → 回来点「我存好了，检查下载文件夹」"
                   f"（存到别处就点「选择已下载的文件…」）。还差 {miss_browser} 个。")
            return now + (f"　（第 ① 步同时在自动下载，还差 {miss_arch} 个，不用管它。）" if miss_arch else "")
        return f"第 ① 步正在自动下载 2016–2019 存档，还差 {miss_arch} 个，不用操作，等它完成。"

    def check(quiet=False):
        """Look in the Downloads folder once: import every paper there (by name or content), build when all are in."""
        if state["busy"]:
            return
        wrong, skipped = [], []
        try:
            got = fetch.import_dir(state["folder"], root, wrong, skipped)
        except OSError as e:  # macOS keeps unsigned apps out of Downloads until the user allows it
            if not quiet:
                say(f"读不了下载文件夹（{type(e).__name__}）。" + (
                    "macOS 没有允许本程序访问「下载」：打开「系统设置 → 隐私与安全性 → 文件和文件夹」，"
                    "在 WTF 下面打开「下载文件夹」；或者直接点「选择已下载的文件…」选中这些 PDF（不需要任何授权）。"
                    if plat.MAC else "请点「选择已下载的文件…」直接选中这些 PDF。"), "warn")
            return
        skipped = [x for x in skipped if x[1] == "not-pdf"]  # other PDFs in Downloads are none of our business
        imported(got, wrong, skipped, quiet, "下载文件夹")

    def pick():
        """The student picks the saved papers in the system dialog, wherever they are."""
        if state["busy"]:
            return
        paths = filedialog.askopenfilenames(
            parent=k.get("ui.root"), title="选择下载好的真题 PDF（可以多选）", initialdir=state["folder"],
            filetypes=[("PDF", "*.pdf *.PDF"), ("全部文件", "*")])
        if paths:
            import_paths(paths)

    def have_folder():
        """Every PDF in a folder the user already has, subfolders included."""
        if state["busy"]:
            return
        folder = filedialog.askdirectory(parent=k.get("ui.root"), title="选择存有真题 PDF 的文件夹")
        if folder:
            import_folder(folder)

    def import_folder(folder):
        paths = [os.path.join(base, n) for base, _, names in os.walk(folder) for n in sorted(names) if n.lower().endswith(".pdf")]
        if not paths:
            say(f"「{folder}」里没有 PDF。", "warn")
            return
        say(f"在「{folder}」里找到 {len(paths)} 个 PDF，开始识别并导入…", "sub")
        wrong, skipped = [], []
        got = fetch.import_files(paths, root, wrong, skipped)
        skipped = [x for x in skipped if x[1] != "not-listed"] +             ([(f"另有 {sum(1 for x in skipped if x[1] == 'not-listed')} 个 PDF", "not-listed")] if any(x[1] == "not-listed" for x in skipped) else [])
        imported(got, wrong, skipped, False, "这个文件夹", picked=len(paths))

    def have_files():
        if state["busy"]:
            return
        paths = filedialog.askopenfilenames(parent=k.get("ui.root"), title="选择已有的真题 PDF（可以框选多个）",
                                            filetypes=[("PDF", "*.pdf *.PDF"), ("全部文件", "*")])
        if paths:
            import_paths(paths)

    def import_paths(paths):
        wrong, skipped = [], []
        got = fetch.import_files(paths, root, wrong, skipped)
        imported(got, wrong, skipped, False, "选中的文件", picked=len(paths))

    def imported(got, wrong, skipped, quiet, where, picked=None):
        for rel in got:
            say(f"✓ 导入 {rel}", "ok")
        for reason in wrong:  # e.g. an older upload of the same paper: its crops would land in the wrong place
            say(f"✗ {reason}。请删掉它，从向导打开的链接重新保存。", "warn")
        for name, why in skipped:
            say(f"✗ {name}：" + (NOT_PDF if why == "not-pdf" else "不是所选科目清单里的真题" if why == "not-listed"
                                 else "文件不存在"), "warn")
        miss = refresh()
        if not chosen:
            return
        if not miss and (got or not managing):  # managing: rebuild only when new papers completed a subject
            say("所有真题都已就绪，自动建立题库…", "sub")
            build()
        elif not quiet and not got and not skipped and any(not m[3] for m in miss):
            say(f"{where}里没有找到新的真题。\n" + (
                f"· 选中的 {picked} 个文件都已经导入过了。\n" if picked else
                f"· 是否只是在浏览器里打开了 PDF、还没按 {SAVE} 保存？\n"
                f"· 保存时是否换了位置？请存进「{state['folder']}」，或者点「选择已下载的文件…」直接选中它们。\n") +
                "· 页面要求验证：在浏览器里完成验证、等 PDF 显示出来后再保存（官网有防机器人保护）。", "warn")
        elif not quiet:
            say(f"这次导入 {len(got)} 个，还差 {sum(1 for m in miss if not m[3])} 个要用浏览器保存。", "sub")

    def open_batch():
        todo = [m for m in missing() if not m[3] and m[0] not in state["opened"]]
        if not todo:  # everything was opened once already: start over with what is still missing
            state["opened"].clear()
            todo = [m for m in missing() if not m[3]]
        for rel, url, _, _ in todo[:BATCH]:
            state["opened"].add(rel)
            webbrowser.open(url)
        say(f"已在浏览器打开 {min(BATCH, len(todo))} 个链接：每个按 {SAVE} 保存，然后点「我存好了，检查下载文件夹」")

    def download_archived():
        """Wayback copies, PARALLEL at a time (more makes the archive throttle harder); failures get a second
        round after a pause; a live 'n / N · about X min left' line so a slow archive never looks stuck."""
        b1.state(["disabled"])
        state["downloading"] = True
        todo = [m for m in missing() if m[3]]
        say(f"开始下载 {len(todo)} 个存档文件（同时 {PARALLEL} 个）…")
        t0, done, hinted = time.time(), [], set()

        def eta():
            if not done:
                return "估算剩余时间中…"
            left = (time.time() - t0) / len(done) * (len(todo) - len(done))
            return f"{len(done)} / {len(todo)} · 约 {max(1, round(left / 60))} 分钟" if left > 30 else                 f"{len(done)} / {len(todo)} · 马上完成"

        def one(item):
            rel, url, _, _ = item
            try:
                fetch.download(rel, url, root)
                done.append(rel)
                post(lambda r=rel: (say(f"✓ {r}", "ok"), refresh(), s1_msg.configure(text=eta())))
                return None
            except Exception as e:
                post(lambda m=f"✗ {rel}：{type(e).__name__} {e}（稍后自动再试）": say(m, "warn"))
                kind, advice = fetch.hint(e)
                if kind and kind not in hinted:  # each kind of trouble is explained once, not per file
                    hinted.add(kind)
                    post(lambda a=advice: say("怎么办：" + a, "sub"))
                return item

        def work():
            failed = todo
            for rnd in (1, 2):  # each file already retries itself; a second round catches longer outages
                with ThreadPoolExecutor(PARALLEL) as pool:
                    failed = [f for f in pool.map(one, failed) if f]
                if not failed:
                    break
                post(lambda n=len(failed): say(f"{n} 个文件暂时失败，20 秒后再试一轮…", "warn"))
                time.sleep(20)
            took = f"{(time.time() - t0) / 60:.0f} 分钟"
            post(lambda: (b1.state(["!disabled"]), state.update(downloading=False), refresh(),
                          say(f"存档下载完成（用时 {took}）。" if not failed else
                              f"存档下载结束，{len(failed)} 个仍失败：点「开始下载」再试。"),
                          chosen and not missing() and not state["busy"] and done and build()))  # last to arrive

        threading.Thread(target=work, daemon=True).start()

    def build():
        miss = missing()
        if not chosen:
            say("先选择至少一个科目。", "warn")
            return
        if miss:  # never a partial bank: the question bank always holds every paper of the chosen subjects
            say(f"还缺 {len(miss)} 个文件，到齐后会自动建库。", "warn")
            return
        state["busy"] = True
        refresh()
        for b in (b1, b2, b3, b_pick):
            b.state(["disabled"])
        say("开始建库…", "sub")

        def work():
            try:
                problems = build_all.run(list(chosen), log=lambda m: post(lambda m=m: say(m, "mono")))
                post(lambda: say(f"完成（{len(problems)} 条提示）。正在启动学习系统…", "ok"))
                post(lambda: k.get("ui.root").after(800, finish))
            except Exception as e:
                msg = f"建库失败：{type(e).__name__}: {e}"
                post(lambda: (say(msg, "warn"), state.update(busy=False), refresh()))

        threading.Thread(target=work, daemon=True).start()

    def finish():
        restart([])
        k.get("ui.root").destroy()

    b1.configure(command=download_archived)
    b2.configure(command=open_batch)
    b3.configure(command=build)
    b_check.configure(command=check)
    b_pick.configure(command=pick)
    b_have_dir.configure(command=have_folder)
    b_have_files.configure(command=have_files)
    table.bind("<Double-1>", lambda e: table.focus() and webbrowser.open(
        next(s[2] for s in all_sources() if s[0] == table.focus())))
    if managing:
        b3.configure(text="按所选科目重建题库")
        ttk.Button(s3, text="返回学习系统（不改动）", command=lambda: (restart([]), k.get("ui.root").destroy())).pack(
            side="right")

    def ready():
        refresh()
        if not chosen:
            return  # nothing to fetch until the student picks a subject
        k.get("ui.root").after(300, lambda: check(quiet=True))  # papers saved before the wizard was opened
        if managing:
            if any(m[3] for m in missing()):
                k.get("ui.root").after(800, download_archived)
            return
        if not missing():  # e.g. right after an update
            say("所有真题都已就绪，自动重建题库…", "sub")
            k.get("ui.root").after(800, build)
        elif [m for m in missing() if m[3]]:  # nothing to decide: start the archive downloads at once
            say("自动开始下载 2016–2019 存档真题…", "sub")
            k.get("ui.root").after(800, download_archived)

    def on_close():
        miss = missing()
        if state["busy"]:
            if not messagebox.askyesno("正在建库", "题库正在建立，现在关闭会中断，下次打开要重新建。确定关闭吗？"):
                return
        elif miss and chosen and not managing and not messagebox.askyesno(
                "还没导入完", f"还差 {len(miss)} 个文件，题库还没建立。\n已下载的文件都会保留，下次打开从这里继续。确定关闭吗？"):
            return
        k.get("ui.root").destroy()

    k.get("ui.root").protocol("WM_DELETE_WINDOW", on_close)
    k.on("ui.ready", ready)
    k.get("ui.status")("第一次使用：导入真题后自动进入学习系统")
    k.provide("setup.folder", lambda folder: (state.update(folder=folder), refresh()))  # tests: a stand-in Downloads
    k.provide("setup.check", check)
    k.provide("setup.import_paths", import_paths)  # tests: what 选择已下载的文件… does after the dialog
    k.provide("setup.import_folder", import_folder)  # tests: what 我已有资源 → 选择文件夹… does after the dialog
    k.provide("setup.choose", lambda subjects: [picks[s].set(s in subjects) or toggle(s) for s in SUBJECTS
                                                if s in offered])  # tests
    k.provide("setup.refresh", refresh)
