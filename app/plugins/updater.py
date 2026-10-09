"""Updates from GitHub. One job: tell the student when a newer release exists and install it on request.

Check: the latest release of the repo (GitHub API, no account needed), at start-up at most once a day
(config "update_check"), or from 帮助 → 检查更新. Install (packaged app only): download the Windows zip,
check its SHA-256 when GitHub publishes one, make sure it really contains WTF.exe, then a small PowerShell
script waits for the app to exit, copies the new files over this folder — never the student's papers,
generated.db (AI questions, mistakes, exams) or WTF.log — removes wace.db and restarts; the first-run
wizard then sees every paper present and rebuilds the bank by itself (tags or tools may have changed).
A source checkout is only told about the new release (update it with git).
"""
import hashlib, json, os, shutil, subprocess, sys, threading, time, urllib.error, urllib.request, webbrowser, zipfile
import tkinter as tk
from tkinter import ttk

REPO = "LxCenady/Wace_Training_Framework"
API = f"https://api.github.com/repos/{REPO}/releases/latest"
FROZEN = getattr(sys, "frozen", False)
SCRIPT = r"""param($procId, $src, $dst, $log)
Wait-Process -Id $procId -Timeout 120 -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1
robocopy $src $dst /E /R:5 /W:1 /XF generated.db WTF.log /XD papers /NFL /NDL /NJH /NJS | Out-Null
$code = $LASTEXITCODE
Add-Content -Path $log -Value ("`n--- update: copied new files (robocopy exit " + $code + ") ---")
if ($code -lt 8) { Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $dst 'wace.db') }
Start-Process (Join-Path $dst 'WTF.exe')
"""


def version_tuple(v):
    return tuple(int(x) for x in v.lstrip("vV").split("-")[0].split(".") if x.isdigit())


def current_version():
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        return open(os.path.join(base, "version.txt"), encoding="utf-8").read().strip()
    except OSError:
        return "0"


def latest_release(timeout=15):
    """-> {"version", "notes", "page", "asset": {"url", "size", "sha256"} | None}."""
    req = urllib.request.Request(API, headers={"accept": "application/vnd.github+json", "user-agent": "WTF-updater"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        rel = json.loads(r.read())
    asset = next((a for a in rel.get("assets", []) if a["name"].startswith("WTF-Windows") and a["name"].endswith(".zip")),
                 None)
    return {"version": rel["tag_name"].lstrip("vV"), "notes": rel.get("body") or "", "page": rel["html_url"],
            "asset": asset and {"url": asset["browser_download_url"], "size": asset.get("size", 0),
                                "sha256": (asset.get("digest") or "").removeprefix("sha256:")}}


def download(asset, dest, progress=lambda done, total: None, tries=6, wait=time.sleep):
    """Stream the zip to dest, resuming after a dropped connection (HTTP Range) with growing pauses;
    then verify SHA-256 when known and that it is the WTF package."""
    total = asset.get("size") or 0
    for attempt in range(1, tries + 1):
        have = os.path.getsize(dest) if os.path.exists(dest) else 0
        if total and have >= total:
            break
        headers = {"user-agent": "WTF-updater"}
        if have:
            headers["range"] = f"bytes={have}-"
        try:
            with urllib.request.urlopen(urllib.request.Request(asset["url"], headers=headers), timeout=60) as r:
                resumed = have and r.status == 206
                with open(dest, "ab" if resumed else "wb") as f:
                    done = have if resumed else 0
                    while chunk := r.read(1 << 16):
                        f.write(chunk)
                        done += len(chunk)
                        progress(done, total)
            if not total or os.path.getsize(dest) >= total:
                break
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if attempt == tries:
                raise
        wait(min(2 ** attempt, 30))
    digest = hashlib.sha256()
    with open(dest, "rb") as f:
        while chunk := f.read(1 << 20):
            digest.update(chunk)
    if asset.get("sha256") and digest.hexdigest() != asset["sha256"]:
        os.remove(dest)
        raise ValueError("下载的文件校验失败（SHA-256 不一致），已放弃更新")
    with zipfile.ZipFile(dest) as z:
        if "WTF/WTF.exe" not in z.namelist():
            raise ValueError("下载的压缩包里没有 WTF/WTF.exe，已放弃更新")


def stage(zip_path, work):
    """Extract into work/new; returns the folder holding the new WTF.exe."""
    new = os.path.join(work, "new")
    shutil.rmtree(new, ignore_errors=True)
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(new)
    return os.path.join(new, "WTF")


def launch_apply(src, dst, work):
    """Start the copy-and-restart script; it waits for this process to exit first."""
    script = os.path.join(work, "apply.ps1")
    open(script, "w", encoding="utf-8-sig").write(SCRIPT)
    subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File",
                      script, str(os.getpid()), src, dst, os.path.join(dst, "WTF.log")],
                     creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0), close_fds=True)


def setup(k):
    root, cfg = k.get("ui.root"), k.get("config")
    post = k.get("ui.post")
    work = os.path.join(k.root, "_update")
    shutil.rmtree(work, ignore_errors=True)  # leftovers of a finished update
    here = current_version()

    def check(manual=False):
        def run():
            try:
                info = latest_release()
            except Exception as e:
                if manual:
                    post(lambda: k.get("ui.status")(f"检查更新失败：{type(e).__name__}: {str(e)[:80]}"))
                return
            if version_tuple(info["version"]) > version_tuple(here):
                post(lambda: offer(info))
            elif manual:
                post(lambda: k.get("ui.status")(f"已是最新版本 v{here}"))
        threading.Thread(target=run, daemon=True).start()

    def offer(info):
        top = tk.Toplevel(root)
        top.title("发现新版本")
        top.geometry("640x460")
        f = ttk.Frame(top, padding=14)
        f.pack(fill="both", expand=True)
        ttk.Label(f, text=f"WTF v{info['version']} 已发布（你现在是 v{here}）", style="H.TLabel").pack(anchor="w")
        notes = k.get("ui.text")(f, height=14)
        notes.frame.pack(fill="both", expand=True, pady=8)
        k.get("ui.write")(notes, info["notes"] or "（没有更新说明）")
        status = ttk.Label(f, style="Muted.TLabel", wraplength=600, justify="left")
        status.pack(anchor="w")
        bar = ttk.Progressbar(f, maximum=100)
        btns = ttk.Frame(f)
        btns.pack(fill="x", pady=(8, 0))
        ttk.Button(btns, text="以后再说", command=top.destroy).pack(side="right")
        ttk.Button(btns, text="打开发布页", command=lambda: webbrowser.open(info["page"])).pack(side="right", padx=6)
        if FROZEN and info["asset"]:
            go = ttk.Button(btns, text="下载并安装", style="Accent.TButton")
            go.pack(side="right")
            status.configure(text="安装时会保留你的真题、AI 题库、错题本和设置；程序会自动重启，并在约 1 分钟内重建题库。")
            go.configure(command=lambda: install(info, go, bar, status))
        elif not FROZEN:
            status.configure(text="你在用源码版：请用 git pull 更新（或从发布页下载免安装版）。")

    def install(info, go, bar, status):
        go.state(["disabled"])
        bar.pack(fill="x", pady=4)
        os.makedirs(work, exist_ok=True)
        zip_path = os.path.join(work, f"WTF-Windows-v{info['version']}.zip")

        def progress(done, total):
            post(lambda: bar.winfo_exists() and bar.configure(value=100 * done / total if total else 0))

        def run():
            try:
                post(lambda: status.configure(text="正在下载…"))
                download(info["asset"], zip_path, progress)
                post(lambda: status.configure(text="正在解压并校验…"))
                src = stage(zip_path, work)
                launch_apply(src, k.root, work)
                post(lambda: (status.configure(text="即将重启完成更新…"), root.after(800, root.destroy)))
            except Exception as e:
                msg = f"更新失败：{type(e).__name__}: {e}"
                post(lambda: (status.configure(text=msg), go.state(["!disabled"])))
        threading.Thread(target=run, daemon=True).start()

    def startup_check():
        today = time.strftime("%Y-%m-%d")
        if cfg.get("update_check", True) and cfg.get("update_last_check") != today:
            cfg["update_last_check"] = today
            k.get("config.save")()
            check(manual=False)

    menu = tk.Menu(k.get("ui.menu"), tearoff=False)
    menu.add_command(label="检查更新", command=lambda: check(manual=True))
    menu.add_command(label="打开发布页", command=lambda: webbrowser.open(f"https://github.com/{REPO}/releases"))
    menu.add_separator()
    menu.add_command(label=f"关于 WTF v{here}", command=lambda: webbrowser.open(f"https://github.com/{REPO}"))
    k.get("ui.menu").add_cascade(label="帮助", menu=menu)
    k.on("ui.ready", lambda: root.after(3000, startup_check))
    k.provide("updater.check", check)
    k.provide("updater.version", here)
