"""Build the portable Windows release. One job: repo -> dist/WTF-Windows-<version>.zip (no Python needed).

  python tools/package_win.py 1.3.0

Layout of the zip (the folder next to WTF.exe is the data root):
  WTF/WTF.exe, WTF/_internal/…           Python + PyMuPDF + Tk + app + build tools (PyInstaller --onedir)
  WTF/sources.tsv, tools/*.txt, MAM/ MAS/ methods, skills/, cheatsheet/, README.md, LICENSE
SCSA papers are NOT included; the first-run wizard fetches/imports them and builds the question bank.
"""
import glob, os, shutil, subprocess, sys, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP, TOOLS = os.path.join(ROOT, "app"), os.path.join(ROOT, "tools")
EXCLUDE = ["scipy", "numpy", "matplotlib", "pandas", "IPython", "PIL", "pytest", "setuptools"]
TOOL_MODULES = ["fetch", "paperid", "blueprint", "build_all", "segment", "build_docs", "build_bank", "build_db", "markpoints", "partmarks"]


def tracked():
    # -z: raw names (by default git quotes non-ASCII ones such as 01_Differentiation_解题思路.md)
    out = subprocess.run(["git", "ls-files", "-z"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8",
                         check=True)
    return [f for f in out.stdout.split("\0") if f]


def data_files():
    """Everything the running app reads from the data root (no code: that lives inside the exe)."""
    keep = []
    for f in tracked():
        if f.startswith("app/") or (f.startswith("tools/") and not f.endswith(".txt")) or f.startswith("."):
            continue
        if f in ("requirements.txt",):
            continue
        keep.append(f)
    return keep


def main(version):
    build, dist = os.path.join(ROOT, "build"), os.path.join(ROOT, "dist")
    plugins = [f"plugins.{os.path.basename(p)[:-3]}" for p in glob.glob(os.path.join(APP, "plugins", "*.py"))
               if not p.endswith("__init__.py")]
    sep = ";" if os.name == "nt" else ":"
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed", "--onedir", "--name", "WTF",
           "--distpath", dist, "--workpath", build, "--specpath", build,
           "--paths", APP, "--paths", TOOLS,
           "--add-data", f"{os.path.join(APP, 'plugins.txt')}{sep}.",
           "--add-data", f"{os.path.join(APP, 'setup.txt')}{sep}.",
           "--add-data", f"{os.path.join(APP, 'version.txt')}{sep}.",
           "--add-data", f"{os.path.join(APP, 'i18n', 'en.json')}{sep}i18n",
           "--hidden-import", "plat"]
    for m in plugins + TOOL_MODULES:
        cmd += ["--hidden-import", m]
    for m in ("ziamath", "ziafont", "ziaplot", "latex2mathml"):  # fonts / symbol tables they read at run time
        cmd += ["--collect-data", m]
    for m in EXCLUDE:  # optional extras SymPy would pull in; nothing in the app needs them (-75 MB)
        cmd += ["--exclude-module", m]
    subprocess.run(cmd + [os.path.join(APP, "main.py")], check=True)

    out = os.path.join(dist, "WTF")
    for f in data_files():
        dest = os.path.join(out, f)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, f), dest)
    with open(os.path.join(out, "先读我.txt"), "w", encoding="utf-8") as f:
        f.write("双击 WTF.exe 启动。第一次运行会带你导入 SCSA 真题（版权原因不随程序分发）并建立题库，约 10 分钟。\n"
                "之后的一切都在本机离线运行；AI 出题需要在「设置」里填你自己的 API key（默认 DeepSeek）。\n"
                "整个文件夹可以放在任何位置（包括 U 盘）；你的 AI 题和错题本保存在本文件夹的 generated.db。\n"
                "界面语言：设置 → 模型与 API key → 界面语言 / Language。\n")
    with open(os.path.join(out, "Read me first.txt"), "w", encoding="utf-8") as f:
        f.write("Double-click WTF.exe. The first run walks you through importing the SCSA past papers (not shipped "
                "for copyright reasons) and builds the question bank, about 10 minutes.\n"
                "Everything then runs offline on this computer; AI questions need your own API key in Settings "
                "(DeepSeek by default).\n"
                "For the English interface: 设置 (Settings) -> 模型与 API key -> 界面语言 / Language -> English, "
                "then restart.\n"
                "The folder can live anywhere (a USB stick works); your AI questions and mistakes are in generated.db "
                "here.\n")
    zpath = os.path.join(dist, f"WTF-Windows-v{version}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(out):
            for name in files:
                full = os.path.join(base, name)
                z.write(full, os.path.join("WTF", os.path.relpath(full, out)))
    print(zpath, f"{os.path.getsize(zpath) / 1e6:.1f} MB")

    # one-file installer carrying the zip: double-click, choose a folder, shortcuts, start (tools/installer.py)
    setup = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed", "--onefile",
             "--name", f"WTF-Setup-v{version}", "--distpath", dist, "--workpath", os.path.join(build, "setup"),
             "--specpath", build, "--add-data", f"{zpath}{sep}payload"]
    for m in EXCLUDE + ["pymupdf", "fitz", "sympy", "mpmath", "ziamath", "ziaplot", "ziafont", "latex2mathml"]:
        setup += ["--exclude-module", m]
    subprocess.run(setup + [os.path.join(TOOLS, "installer.py")], check=True)
    exe = os.path.join(dist, f"WTF-Setup-v{version}.exe")
    print(exe, f"{os.path.getsize(exe) / 1e6:.1f} MB")
    # the same installer under a fixed name: releases/latest/download/WTF-Setup.exe always fetches the newest
    shutil.copyfile(exe, os.path.join(dist, "WTF-Setup.exe"))


if __name__ == "__main__":
    # app/version.txt is the single source of the version (the updater compares it with GitHub releases)
    main(sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(APP, "version.txt")).read().strip())
