"""Operating-system differences. One job: everything Windows and macOS do differently, in one place.

Fonts (Tk and PDF), where a packaged app keeps its data, opening a file, the right mouse button and the
shortcut modifier. Plugins call these instead of testing the platform themselves.
"""
import os, re, shutil, subprocess, sys

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


def use_system_certificates():
    """HTTPS trusts what the operating system trusts (macOS Keychain, Windows certificate store), like the browser.
    A packaged Python otherwise only knows its own CA list: on a school network, behind a VPN or an antivirus
    that inspects HTTPS, every download then fails with CERTIFICATE_VERIFY_FAILED although the browser works.
    Certificates the system does not trust are still refused. Without truststore, nothing changes."""
    try:
        import truststore
        truststore.inject_into_ssl()
        return True
    except Exception:
        return False


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


_ILLEGAL = re.compile(r'[<>:"/\|?*\x00-\x1f]')
_RESERVED = re.compile(r"^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\..*)?$", re.I)


def safe_filename(name, limit=150):
    """A file name every system accepts: illegal characters become "_", no trailing dot or space, no reserved
    Windows device name, at most `limit` characters (Chinese names are kept)."""
    name = _ILLEGAL.sub("_", str(name)).strip().rstrip(". ") or "_"
    if _RESERVED.match(name):
        name = "_" + name
    return name[:limit].rstrip(". ") or "_"


def same_file(a, b):
    """Two paths naming the same file (case-insensitive on Windows and macOS)."""
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def inside(path, folder):
    """`path` is `folder` or lies inside it (after resolving "..", case as the system compares names)."""
    p, f = os.path.normcase(os.path.realpath(path)), os.path.normcase(os.path.realpath(folder))
    return p == f or p.startswith(f.rstrip(os.sep) + os.sep)


def _webview():
    """The desktop web window (WTF Studio), or None in a Tk app or a browser preview."""
    try:
        import webview
    except ImportError:
        return None
    return webview if webview.windows else None


def _tk_dialog(ask):
    """Run a Tk file dialog: on the app's own Tk window when there is one (WTF), else on a hidden one (preview)."""
    import tkinter as tk
    if tk._default_root is not None:
        return ask(tk._default_root)
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    try:
        return ask(root)
    finally:
        root.destroy()


def pick_folder(title="Choose a folder"):
    """A native folder dialog -> path or None."""
    wv = _webview()
    if wv:
        got = wv.windows[0].create_file_dialog(wv.FOLDER_DIALOG)
        return (got[0] if isinstance(got, (list, tuple)) else got) if got else None
    from tkinter import filedialog
    return _tk_dialog(lambda root: filedialog.askdirectory(parent=root, title=title)) or None


def pick_files(kind="pdf", save=False):
    """Compiler's explicit user file selection (PDFs or a .wtfpack); does not read any file itself -> [paths]."""
    extension = ".wtfpack" if kind == "pack" else ".pdf"
    label = "WTF recipe" if kind == "pack" else "PDF"
    wv = _webview()
    if wv:
        got = wv.windows[0].create_file_dialog(wv.SAVE_DIALOG if save else wv.OPEN_DIALOG, allow_multiple=not save,
                                               file_types=(f"{label} (*{extension})",))
        return list(got) if isinstance(got, (list, tuple)) else [got] if got else []
    from tkinter import filedialog
    types = [(label, "*" + extension)]
    if save:
        path = _tk_dialog(lambda root: filedialog.asksaveasfilename(parent=root, title="WTF Compiler",
                                                                     defaultextension=extension, filetypes=types))
        return [path] if path else []
    return list(_tk_dialog(lambda root: filedialog.askopenfilenames(parent=root, title="WTF Compiler", filetypes=types)))
