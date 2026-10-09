"""First-run wizard. One job: get the SCSA papers onto this computer, build the question bank, restart.

The papers are © SCSA and are not shipped with the app. 2016-2019 come from the Wayback Machine
automatically; 2020-2025 the student opens in their own browser (the site refuses scripts) and saves
anywhere in the watched folder — files are recognised by name or by content (tools/paperid.py).
"""
import ctypes, os, subprocess, sys, threading, uuid, webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

BATCH = 6  # links opened per click


def downloads_folder():
    """The user's real Downloads folder (it may have been moved off C:)."""
    try:
        guid = uuid.UUID("{374DE290-123F-4565-9164-39C4925E467B}")
        buf = ctypes.c_wchar_p()
        guid_buf = (ctypes.c_byte * 16).from_buffer_copy(guid.bytes_le)
        if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(guid_buf), 0, None, ctypes.byref(buf)) == 0:
            path = buf.value
            ctypes.windll.ole32.CoTaskMemFree(buf)
            return path
    except Exception:
        pass
    return os.path.join(os.path.expanduser("~"), "Downloads")


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

    state = {"folder": downloads_folder(), "seen": {}, "opened": set(), "busy": False}
    all_sources = fetch.sources(root)
    archived = [s for s in all_sources if s[3]]
    browser = [s for s in all_sources if not s[3]]

    head = ttk.Frame(page)
    head.pack(fill="x", padx=16, pady=(14, 4))
    count = ttk.Label(head, style="H.TLabel")
    count.pack(side="left")
    bar = ttk.Progressbar(head, length=320, maximum=len(all_sources))
    bar.pack(side="left", padx=12)

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
        f"点「打开下一批」会在浏览器里打开 {BATCH} 个官方链接。若浏览器直接显示 PDF，按 Ctrl+S 保存。"
        "保存到下面这个文件夹即可，文件名随意——程序每 2 秒检查一次，自动识别并导入。")).pack(anchor="w")
    row = ttk.Frame(s2)
    row.pack(fill="x", pady=(8, 0))
    b2 = ttk.Button(row, text=f"打开下一批（{BATCH} 个）", style="Accent.TButton")
    b2.pack(side="left")
    folder_lbl = ttk.Label(row, style="Muted.TLabel")
    folder_lbl.pack(side="left", padx=10)
    ttk.Button(row, text="更换监视文件夹…", command=lambda: choose()).pack(side="right")
    ttk.Button(row, text="从文件夹导入一次…", command=lambda: import_once()).pack(side="right", padx=6)

    # ③ build
    s3 = ttk.LabelFrame(page, text="③ 建立题库（约 1 分钟）", padding=10)
    s3.pack(fill="x", padx=16, pady=6)
    b3 = ttk.Button(s3, text="建立题库并启动", style="Accent.TButton")
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
        miss = fetch.missing(root)
        have = len(all_sources) - len(miss)
        count.configure(text=f"已导入 {have} / {len(all_sources)} 个文件")
        bar.configure(value=have)
        folder_lbl.configure(text=f"监视：{state['folder']}")
        table.delete(*table.get_children())
        for rel, url, official, arch in miss:
            table.insert("", "end", iid=rel, values=(rel, "Wayback 自动" if arch else "浏览器下载"))
        miss_arch = sum(1 for m in miss if m[3])
        miss_browser = sum(1 for m in miss if not m[3])
        s1_msg.configure(text="已全部下载 ✓" if not miss_arch else f"还缺 {miss_arch} 个")
        b2.state(["disabled"] if not miss_browser else ["!disabled"])
        core = [m for m in miss if "Sample" not in m[0]]  # 2016 sample papers are optional
        s3_msg.configure(text="全部就绪 ✓" if not core else f"还缺 {len(core)} 个必需文件（也可以先用已有的建库）")
        if not state["busy"]:
            b3.state(["!disabled"] if have else ["disabled"])
        return miss

    def scan():
        """Import new or changed PDFs from the watched folder (cheap: each file is examined once per version)."""
        folder = state["folder"]
        got = []
        try:
            names = os.listdir(folder)
        except OSError:
            names = []
        for name in names:
            path = os.path.join(folder, name)
            if not name.lower().endswith(".pdf"):
                continue
            try:
                stamp = os.stat(path).st_mtime
            except OSError:
                continue
            if state["seen"].get(path) == stamp:
                continue
            state["seen"][path] = stamp
            rel = fetch.import_file(path, root)
            if rel:
                got.append(rel)
        return got

    def tick():
        if not state["busy"]:
            for rel in scan():
                say(f"✓ 导入 {rel}", "ok")
            refresh()
        k.get("ui.root").after(2000, tick)

    def choose():
        d = filedialog.askdirectory(initialdir=state["folder"], title="选择你保存 PDF 的文件夹")
        if d:
            state["folder"], state["seen"] = d, {}
            refresh()

    def import_once():
        d = filedialog.askdirectory(initialdir=state["folder"], title="选择包含真题 PDF 的文件夹")
        if d:
            got = fetch.import_dir(d, root)
            say(f"从 {d} 导入 {len(got)} 个文件", "ok")
            refresh()

    def open_batch():
        todo = [m for m in fetch.missing(root) if not m[3] and m[0] not in state["opened"]]
        if not todo:  # everything was opened once already: start over with what is still missing
            state["opened"].clear()
            todo = [m for m in fetch.missing(root) if not m[3]]
        for rel, url, _, _ in todo[:BATCH]:
            state["opened"].add(rel)
            webbrowser.open(url)
        say(f"已在浏览器打开 {min(BATCH, len(todo))} 个链接；保存到「{state['folder']}」即可")

    def download_archived():
        b1.state(["disabled"])
        todo = [m for m in fetch.missing(root) if m[3]]
        say(f"开始下载 {len(todo)} 个存档文件…")

        def work():
            for rel, url, _, _ in todo:
                try:
                    fetch.download(rel, url, root)
                    post(lambda r=rel: say(f"✓ {r}", "ok"))
                except Exception as e:
                    msg = f"✗ {rel}：{type(e).__name__} {e}"
                    post(lambda m=msg: say(m, "warn"))
                post(refresh)
            post(lambda: (b1.state(["!disabled"]), say("存档下载结束。失败的可以再点一次重试。")))

        threading.Thread(target=work, daemon=True).start()

    def build():
        miss = [m for m in fetch.missing(root) if "Sample" not in m[0]]
        if miss and not messagebox.askyesno("还缺文件", f"还缺 {len(miss)} 个必需文件，对应年份的题目暂时不会出现。\n"
                                                          "现在先用已有文件建库吗？（之后补齐再重新建库即可）"):
            return
        state["busy"] = True
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
    table.bind("<Double-1>", lambda e: table.focus() and webbrowser.open(
        next(s[2] for s in all_sources if s[0] == table.focus())))
    k.on("ui.ready", lambda: (refresh(), k.get("ui.root").after(500, tick)))
    k.get("ui.status")("第一次使用：导入真题后自动进入学习系统")
    k.provide("setup.watch", lambda folder: (state.update(folder=folder, seen={}), refresh()))
    k.provide("setup.scan", scan)
    k.provide("setup.refresh", refresh)
