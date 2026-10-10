"""Build the macOS app. One job: repo -> dist/WTF.app and a drag-to-Applications disk image (runs on a Mac).

Layout: WTF.app holds Python + PyMuPDF + Tk + app + build tools (PyInstaller --windowed --onedir) and, under
data/, the same original files the Windows zip carries (notes, tags, skills, sources.tsv …). The app never
writes inside itself: plat.frozen_root copies data/ to ~/Library/Application Support/WTF on first start of each
version, and papers, wace.db and generated.db live there.

dist/WTF-macOS-<arch>-v<version>.dmg, and the same image as WTF-macOS-<arch>.dmg so
releases/latest/download/WTF-macOS-<arch>.dmg always fetches the newest. <arch> is arm64 (Apple silicon) or
x86_64 (Intel), whichever Mac builds it. The app is not signed: first open with right-click -> Open.
"""
import os, platform, shutil, subprocess, sys

from package_win import APP, EXCLUDE, ROOT, TOOL_MODULES, TOOLS, data_files


def main(version):
    build, dist = os.path.join(ROOT, "build"), os.path.join(ROOT, "dist")
    arch = platform.machine()  # arm64 | x86_64
    staged = os.path.join(build, "data")
    shutil.rmtree(staged, ignore_errors=True)
    for f in data_files():
        dest = os.path.join(staged, f)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, f), dest)
    plugins = [f"plugins.{n[:-3]}" for n in os.listdir(os.path.join(APP, "plugins"))
               if n.endswith(".py") and n != "__init__.py"]
    cmd = [sys.executable, "-m", "PyInstaller", "--noconfirm", "--clean", "--windowed", "--onedir", "--name", "WTF",
           "--osx-bundle-identifier", "io.github.lxcenady.wtf",
           "--distpath", dist, "--workpath", build, "--specpath", build,
           "--paths", APP, "--paths", TOOLS,
           "--add-data", f"{os.path.join(APP, 'plugins.txt')}:.",
           "--add-data", f"{os.path.join(APP, 'setup.txt')}:.",
           "--add-data", f"{os.path.join(APP, 'version.txt')}:.",
           "--add-data", f"{os.path.join(APP, 'i18n', 'en.json')}:i18n",
           "--add-data", f"{staged}:data",
           "--hidden-import", "plat"]
    for m in plugins + TOOL_MODULES:
        cmd += ["--hidden-import", m]
    for m in ("ziamath", "ziafont", "ziaplot", "latex2mathml"):  # fonts / symbol tables they read at run time
        cmd += ["--collect-data", m]
    for m in EXCLUDE:
        cmd += ["--exclude-module", m]
    subprocess.run(cmd + [os.path.join(APP, "main.py")], check=True)

    app = os.path.join(dist, "WTF.app")
    image = os.path.join(build, "dmg")  # what the disk image shows: the app and a link to drag it onto
    shutil.rmtree(image, ignore_errors=True)
    os.makedirs(image)
    subprocess.run(["ditto", app, os.path.join(image, "WTF.app")], check=True)
    os.symlink("/Applications", os.path.join(image, "Applications"))
    with open(os.path.join(image, "先读我 Read me.txt"), "w", encoding="utf-8") as f:
        f.write("把 WTF 拖进「应用程序」。第一次打开：在「应用程序」里右键 WTF → 打开 → 打开（程序没有 Apple 签名）。\n"
                "第一次运行会带你导入 SCSA 真题并建立题库；数据保存在 ~/Library/Application Support/WTF。\n\n"
                "Drag WTF onto Applications. First open: right-click WTF in Applications -> Open -> Open (the app is "
                "not signed by Apple).\nThe first run walks you through importing the SCSA past papers and builds "
                "the question bank; data lives in ~/Library/Application Support/WTF.\n")
    dmg = os.path.join(dist, f"WTF-macOS-{arch}-v{version}.dmg")
    if os.path.exists(dmg):
        os.remove(dmg)
    subprocess.run(["hdiutil", "create", "-volname", "WTF", "-srcfolder", image, "-ov", "-format", "UDZO", dmg],
                   check=True)
    shutil.copyfile(dmg, os.path.join(dist, f"WTF-macOS-{arch}.dmg"))
    print(dmg, f"{os.path.getsize(dmg) / 1e6:.1f} MB")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else open(os.path.join(APP, "version.txt")).read().strip())
