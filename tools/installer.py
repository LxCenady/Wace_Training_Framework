"""WTF installer. One job: put the packaged app on this computer, with shortcuts, and start it.

Built by tools/package_win.py into a single WTF-Setup-v<ver>.exe that carries the portable zip as payload.
Installs per user (no administrator rights) into %LOCALAPPDATA%\\Programs\\WTF by default. Installing over an
existing copy is an upgrade: the student's papers, generated.db (AI questions, mistakes, exams) and WTF.log
are never in the payload, so they stay; wace.db is removed so the new version rebuilds the bank (≈1 min).
"""
import os, subprocess, sys, threading, zipfile
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP = "WTF — WACE Training Framework"


def payload():
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    zips = [f for f in os.listdir(os.path.join(base, "payload")) if f.endswith(".zip")]
    return os.path.join(base, "payload", zips[0])


def version_of(zip_path):
    with zipfile.ZipFile(zip_path) as z:
        return z.read("WTF/_internal/version.txt").decode().strip()


def running_in(folder):
    """True if a WTF.exe from this folder is running (its files would be locked)."""
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
                          f"(Get-Process WTF -ErrorAction SilentlyContinue | Where-Object Path -like '{folder}*').Id"],
                         capture_output=True, text=True, creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return bool(out.stdout.strip())


def shortcut(path, target, workdir):
    ps = (f"$s = (New-Object -ComObject WScript.Shell).CreateShortcut('{path}'); $s.TargetPath = '{target}'; "
          f"$s.WorkingDirectory = '{workdir}'; $s.Description = '{APP}'; $s.Save()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True,
                   creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))


def install(zip_path, folder, desktop, start_menu, progress):
    os.makedirs(folder, exist_ok=True)
    upgrade = os.path.exists(os.path.join(folder, "WTF.exe"))
    with zipfile.ZipFile(zip_path) as z:
        names = [n for n in z.namelist() if n.startswith("WTF/") and not n.endswith("/")]
        for i, name in enumerate(names, 1):
            dest = os.path.join(folder, *name[4:].split("/"))
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            with z.open(name) as src, open(dest, "wb") as out:
                out.write(src.read())
            if i % 25 == 0 or i == len(names):
                progress(i / len(names))
    if upgrade and os.path.exists(os.path.join(folder, "wace.db")):
        os.remove(os.path.join(folder, "wace.db"))  # rebuilt on first start with the new tags and tools
    exe = os.path.join(folder, "WTF.exe")
    links = []
    if desktop:
        links.append(os.path.join(os.path.expanduser("~"), "Desktop"))
        try:  # the Desktop may have been moved (e.g. to D:)
            import ctypes, uuid
            buf = ctypes.c_wchar_p()
            guid = (ctypes.c_byte * 16).from_buffer_copy(uuid.UUID("{B4BFCC3A-DB2C-424C-B029-7FE99A87C641}").bytes_le)
            if ctypes.windll.shell32.SHGetKnownFolderPath(ctypes.byref(guid), 0, None, ctypes.byref(buf)) == 0:
                links[-1] = buf.value
        except Exception:
            pass
    if start_menu:
        links.append(os.path.join(os.environ.get("APPDATA", ""), "Microsoft", "Windows", "Start Menu", "Programs"))
    for d in links:
        shortcut(os.path.join(d, "WACE 学习系统 (WTF).lnk"), exe, folder)
    return exe, upgrade


def main():
    zip_path = payload()
    version = version_of(zip_path)
    root = tk.Tk()
    root.title(f"安装 / Install  WTF v{version}")
    root.resizable(False, False)
    f = ttk.Frame(root, padding=16)
    f.pack(fill="both", expand=True)
    ttk.Label(f, text=f"{APP}  v{version}", font=("Microsoft YaHei UI", 13, "bold")).pack(anchor="w")
    ttk.Label(f, text="WACE 数学方法 / 专业数学 学习系统 · Study system for WACE Mathematics Methods & Specialist",
              foreground="#666").pack(anchor="w", pady=(0, 10))
    folder = tk.StringVar(value=os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Programs", "WTF"))
    row = ttk.Frame(f)
    row.pack(fill="x")
    ttk.Label(row, text="安装位置 / Folder").pack(side="left")
    ttk.Entry(row, textvariable=folder, width=52).pack(side="left", padx=6)
    ttk.Button(row, text="…", width=3, command=lambda: folder.set(
        filedialog.askdirectory(initialdir=folder.get()) or folder.get())).pack(side="left")
    desktop, start = tk.BooleanVar(value=True), tk.BooleanVar(value=True)
    ttk.Checkbutton(f, text="桌面快捷方式 / Desktop shortcut", variable=desktop).pack(anchor="w", pady=(8, 0))
    ttk.Checkbutton(f, text="开始菜单 / Start menu", variable=start).pack(anchor="w")
    ttk.Label(f, foreground="#666", justify="left", wraplength=560, text=(
        "装在你的用户目录，不需要管理员权限。已经装过的话会直接升级：你的真题、AI 题和错题本都会保留。\n"
        "Installs for you only, no administrator rights needed. Installing again upgrades and keeps your papers, "
        "AI questions and mistakes.")).pack(anchor="w", pady=8)
    bar = ttk.Progressbar(f, maximum=1.0, length=560)
    bar.pack(fill="x")
    status = ttk.Label(f, foreground="#1f3a73")
    status.pack(anchor="w", pady=(6, 0))
    go = ttk.Button(f, text="安装 / Install")
    go.pack(anchor="e", pady=(10, 0))

    def run():
        target = folder.get().strip()
        if running_in(target):
            messagebox.showwarning("WTF", "请先关闭正在运行的学习系统，再点安装。\nPlease close the running app first.")
            return
        go.state(["disabled"])
        status.configure(text="正在安装… / Installing…")

        def work():
            try:
                exe, upgrade = install(zip_path, target, desktop.get(), start.get(),
                                       lambda x: root.after(0, bar.configure, {"value": x}))
                root.after(0, status.configure, {"text": ("已升级" if upgrade else "安装完成") + "，正在启动… / Done, starting…"})
                subprocess.Popen([exe], cwd=target, close_fds=True)
                root.after(1500, root.destroy)
            except Exception as e:
                root.after(0, lambda: (status.configure(text=f"安装失败 / Failed: {e}"), go.state(["!disabled"])))
        threading.Thread(target=work, daemon=True).start()

    go.configure(command=run)
    root.mainloop()


if __name__ == "__main__":
    main()
