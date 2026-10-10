"""First-run wizard. One job: get the SCSA papers onto this computer, build the question bank, restart.

The papers are © SCSA and are not shipped with the app. Everything is fixed, nothing is watched:
2016-2019 come from the Wayback Machine straight into the bank's papers folders; 2020-2025 the student opens in
their own browser (the site refuses scripts) and saves with the browser's default — the Downloads folder — then
presses one button that checks that folder once (files are recognised by name or by content, tools/paperid.py).
The bank is built only when every paper is in, and then by itself.
"""
import ctypes, os, subprocess, sys, threading, time, uuid, webbrowser
import tkinter as tk
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox, ttk
import plat

BATCH = 6  # links opened per click
PARALLEL = 3  # archive downloads at the same time
FONT = plat.UI_FONT
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


def restart():
    main = [] if getattr(sys, "frozen", False) else [os.path.abspath(sys.modules["__main__"].__file__)]
    subprocess.Popen([sys.executable, *main], close_fds=True)


def setup(k):
    import fetch, build_all  # tools/, on sys.path via main.py
    root, post = k.root, k.get("ui.post")
    C = k.get("ui.colors")
    page = k.get("ui.tab")("setup", "第一次使用：导入真题")
    k.get("ui.root").title("WACE Maths 学习系统 — 导入真题")
    left = k.get("ui.left")
    ttk.Label(left, text="欢迎", style="H.TLabel").pack(anchor="w", padx=12, pady=(12, 4))
    ttk.Label(left, wraplength=400, justify="left", text=(
        "SCSA的真题、评分标准和公式表受版权保护，不随程序分发；需要你自己从官方网站下载一次，"
        "之后所有功能（知识图谱、按小问标注的真题、每一分的评分标准、AI 出题）都在本机离线可用。\n\n"
        "全部文件约 75 MB，下载与建库只需做一次。")).pack(anchor="w", padx=12)

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
    def needed(items):  # the 2016 sample papers never enter the bank: the wizard ignores them
        return [x for x in items if "Sample" not in x[0]]

    def missing():
        return needed(fetch.missing(root))

    all_sources = needed(fetch.sources(root))
    archived = [s for s in all_sources if s[3]]
    browser = [s for s in all_sources if not s[3]]

    head = ttk.Frame(page)
    head.pack(fill="x", padx=16, pady=(14, 4))
    count = ttk.Label(head, style="H.TLabel")
    count.pack(side="left")
    bar = ttk.Progressbar(head, length=320, maximum=len(all_sources))
    bar.pack(side="left", padx=12)
    nxt = tk.Label(page, anchor="w", justify="left", wraplength=1000, bg=C["accent"], fg="#ffffff", padx=12, pady=8,
                   font=(FONT, 11, "bold"))  # what to do now, in one line
    nxt.pack(fill="x", padx=16, pady=(4, 2))

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
        "2. 在每个 PDF 页面按 Ctrl+S（或点浏览器的下载按钮），直接点「保存」——不要改位置，存进「下载」文件夹；"
        "文件名随意。\n"
        "3. 这一批存好后，点「我存好了，检查下载文件夹」。全部到齐后自动建库并进入学习系统。")).pack(anchor="w")
    row = ttk.Frame(s2)
    row.pack(fill="x", pady=(8, 0))
    b2 = ttk.Button(row, text=f"打开下一批（{BATCH} 个）", style="Accent.TButton")
    b2.pack(side="left")
    b_check = ttk.Button(row, text="我存好了，检查下载文件夹", style="Accent.TButton")
    b_check.pack(side="left", padx=8)
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

    def refresh():
        miss = missing()
        have = len(all_sources) - len(miss)
        count.configure(text=f"已导入 {have} / {len(all_sources)} 个文件")
        bar.configure(value=have)
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
            b3.state(["disabled"] if miss else ["!disabled"])  # never a partial bank
        nxt.configure(text=next_step(miss_arch, miss_browser))
        return miss

    def next_step(miss_arch, miss_browser):
        if state["busy"]:
            return "正在建立题库，约 1 分钟，完成后自动进入学习系统。请不要关闭窗口。"
        if not miss_arch and not miss_browser:
            return "全部文件已到齐，马上自动建库。"
        if miss_arch and not state.get("downloading"):
            retry = f"第 ① 步还有 {miss_arch} 个存档没下载成功：点「开始下载」重试。"
            return retry + (f"　第 ② 步还差 {miss_browser} 个（浏览器保存）。" if miss_browser else "")
        if miss_browser:
            now = (f"第 ② 步：点「打开下一批」→ 浏览器里每个 PDF 按 Ctrl+S → 保存 → 回来点「我存好了，检查下载文件夹」。"
                   f"还差 {miss_browser} 个。")
            return now + (f"　（第 ① 步同时在自动下载，还差 {miss_arch} 个，不用管它。）" if miss_arch else "")
        return f"第 ① 步正在自动下载 2016–2019 存档，还差 {miss_arch} 个，不用操作，等它完成。"

    def check(quiet=False):
        """Look in the Downloads folder once: import every paper there (by name or content), build when all are in."""
        if state["busy"]:
            return
        got = fetch.import_dir(state["folder"], root)
        for rel in got:
            say(f"✓ 导入 {rel}", "ok")
        miss = refresh()
        if not miss:
            say("所有真题都已就绪，自动建立题库…", "sub")
            build()
        elif not quiet and not got and any(not m[3] for m in miss):
            say(f"下载文件夹里没有找到新的真题。\n"
                "· 是否只是在浏览器里打开了 PDF、还没按 Ctrl+S 保存？\n"
                f"· 保存时是否换了位置？请存进「{state['folder']}」。\n"
                "· 页面要求验证：在浏览器里完成验证后再保存即可（官网有防机器人保护）。", "warn")
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
        say(f"已在浏览器打开 {min(BATCH, len(todo))} 个链接：每个按 Ctrl+S 保存，然后点「我存好了，检查下载文件夹」")

    def download_archived():
        """Wayback copies, PARALLEL at a time (more makes the archive throttle harder); failures get a second
        round after a pause; a live 'n / N · about X min left' line so a slow archive never looks stuck."""
        b1.state(["disabled"])
        state["downloading"] = True
        todo = [m for m in missing() if m[3]]
        say(f"开始下载 {len(todo)} 个存档文件（同时 {PARALLEL} 个）…")
        t0, done = time.time(), []

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
                          not missing() and not state["busy"] and build()))  # the archive was the last to arrive

        threading.Thread(target=work, daemon=True).start()

    def build():
        miss = missing()
        if miss:  # never a partial bank: the question bank always holds every paper
            say(f"还缺 {len(miss)} 个文件，到齐后会自动建库。", "warn")
            return
        state["busy"] = True
        refresh()
        for b in (b1, b2, b3):
            b.state(["disabled"])
        say("开始建库…", "sub")

        def work():
            try:
                problems = build_all.run(log=lambda m: post(lambda m=m: say(m, "mono")))
                post(lambda: say(f"完成（{len(problems)} 条提示）。正在启动学习系统…", "ok"))
                post(lambda: k.get("ui.root").after(800, finish))
            except Exception as e:
                msg = f"建库失败：{type(e).__name__}: {e}"
                post(lambda: (say(msg, "warn"), state.update(busy=False), refresh()))

        threading.Thread(target=work, daemon=True).start()

    def finish():
        restart()
        k.get("ui.root").destroy()

    b1.configure(command=download_archived)
    b2.configure(command=open_batch)
    b3.configure(command=build)
    b_check.configure(command=check)
    table.bind("<Double-1>", lambda e: table.focus() and webbrowser.open(
        next(s[2] for s in all_sources if s[0] == table.focus())))
    def ready():
        k.get("ui.root").after(300, lambda: check(quiet=True))  # papers saved before the wizard was opened
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
        elif miss and not messagebox.askyesno(
                "还没导入完", f"还差 {len(miss)} 个文件，题库还没建立。\n已下载的文件都会保留，下次打开从这里继续。确定关闭吗？"):
            return
        k.get("ui.root").destroy()

    k.get("ui.root").protocol("WM_DELETE_WINDOW", on_close)
    k.on("ui.ready", ready)
    k.get("ui.status")("第一次使用：导入真题后自动进入学习系统")
    k.provide("setup.folder", lambda folder: (state.update(folder=folder), refresh()))  # tests: a stand-in Downloads
    k.provide("setup.check", check)
    k.provide("setup.refresh", refresh)
