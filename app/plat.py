"""Operating-system differences. One job: everything Windows and macOS do differently, in one place.

Fonts (Tk and PDF), where a packaged app keeps its data, opening a file, the right mouse button and the
shortcut modifier. Plugins call these instead of testing the platform themselves.
"""
import os, shutil, subprocess, sys

MAC = sys.platform == "darwin"
WINDOWS = os.name == "nt"
FROZEN = getattr(sys, "frozen", False)

UI_FONT = "PingFang SC" if MAC else "Microsoft YaHei UI"  # Tk font family with CJK glyphs
MOD = "Command" if MAC else "Control"  # shortcut modifier key
MOD_NAME = "⌘" if MAC else "Ctrl+"

# PDF fonts: (folder, CJK font file, symbol font file) — first existing set wins
_PDF_FONTS = ([("/System/Library/Fonts", "Hiragino Sans GB.ttc", "Apple Symbols.ttf"),
               ("/System/Library/Fonts", "STHeiti Light.ttc", "Apple Symbols.ttf"),
               ("/Library/Fonts", "Arial Unicode.ttf", "Arial Unicode.ttf")] if MAC else
              [(os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts"), "msyh.ttc", "seguisym.ttf")])


def pdf_fonts():
    """(folder, CJK font file name, symbol font file name) for PDF output on this computer."""
    for folder, cjk, sym in _PDF_FONTS:
        if os.path.isfile(os.path.join(folder, cjk)):
            return folder, cjk, sym if os.path.isfile(os.path.join(folder, sym)) else cjk
    return _PDF_FONTS[0]


def user_dir(name):
    """Per-user settings folder: %APPDATA%\\<name> on Windows, ~/Library/Application Support/<name> on macOS."""
    if MAC:
        return os.path.join(os.path.expanduser("~"), "Library", "Application Support", name)
    return os.path.join(os.environ.get("APPDATA") or os.path.expanduser("~"), name)


def frozen_root(bundle):
    """Data folder of a packaged app. Windows: the folder next to WTF.exe (portable, a USB stick works).
    macOS: an .app must stay read-only (and may run from a translocated copy), so the data lives in
    ~/Library/Application Support/WTF; the notes and tags shipped inside the app (`bundle`/data) are copied
    there when this version runs for the first time, and an older question bank is dropped to be rebuilt."""
    if not MAC:
        return os.path.dirname(sys.executable)
    root = user_dir("WTF")
    shipped = os.path.join(bundle, "data")
    version = open(os.path.join(bundle, "version.txt"), encoding="utf-8").read().strip()
    stamp = os.path.join(root, ".version")
    if not os.path.isfile(stamp) or open(stamp, encoding="utf-8").read().strip() != version:
        for folder, _, files in os.walk(shipped):
            for f in files:
                src = os.path.join(folder, f)
                dest = os.path.join(root, os.path.relpath(src, shipped))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copyfile(src, dest)
        if os.path.isfile(stamp) and os.path.isfile(os.path.join(root, "wace.db")):
            os.remove(os.path.join(root, "wace.db"))  # rebuilt by the wizard with this version's tools and tags
        open(stamp, "w", encoding="utf-8").write(version)
    return root


def open_file(path):
    """Open a file (an exported PDF) with the system's default program."""
    if WINDOWS:
        os.startfile(path)
    elif MAC:
        subprocess.Popen(["open", path])
    else:
        subprocess.Popen(["xdg-open", path])


def on_right_click(widget, handler):
    """Bind the context-menu click: button 3 on Windows; button 2 and Control-click on macOS."""
    for seq in (["<Button-2>", "<Control-Button-1>"] if MAC else ["<Button-3>"]):
        widget.bind(seq, handler)


def shortcut(root, key, handler):
    """Bind Ctrl+<key> on Windows, ⌘<key> on macOS (and Ctrl+<key> there too)."""
    root.bind_all(f"<Control-{key}>", handler)
    if MAC:
        root.bind_all(f"<Command-{key}>", handler)
