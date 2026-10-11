"""Synthetic external-library UI smoke test, both language modes, isolated user databases/settings.

Usage: python tests/smoke_external.py <empty out dir> [zh|en]
"""
import os
from pathlib import Path
import re
import sys
import tempfile
import time
import subprocess
from tkinter import filedialog

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
from tests.safe_runtime import isolate
isolate()
from main import Kernel, find_root, plugin_names
sys.path.insert(0, str(Path(find_root()) / "tools"))
from tests.test_external import fixtures
import plugins.config as config
from plugins.external_store import ExternalStore

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
language = sys.argv[2] if len(sys.argv) > 2 else "zh"
real_load = config.load
config.load = lambda: dict(real_load(), language=language, provider="mock")
k = Kernel(find_root())
k.load(plugin_names())
root = k.get("ui.root")
root.geometry("1450x900+10+10")
k.emit("ui.ready")
temp = tempfile.TemporaryDirectory(prefix="wtf-external-smoke-")
folder = Path(temp.name)
exam, answer = fixtures(folder)
store = ExternalStore(folder, lambda name: k.get("external.pdf." + name),
            lambda subject: [p[0] for p in k.get("store").q("SELECT code FROM patterns WHERE code LIKE ?", subject + ".%")])
k.provide("external.store", lambda: store)


def pump(sec=0.3):
    end = time.time() + sec
    while time.time() < end:
        root.update()
        time.sleep(0.02)


def walk(w):
    yield w
    for child in w.winfo_children():
        yield from walk(child)


def button(parent, source_text):
    wanted = k.get("i18n.tr")(source_text)
    return next(w for w in walk(parent) if w.winfo_class() == "TButton" and w.cget("text") == wanted)


def shot(name, window=root):
    if os.name != "nt":
        return
    window.lift()
    window.attributes("-topmost", True)
    pump()
    x, y, w, h = window.winfo_rootx(), window.winfo_rooty(), window.winfo_width(), window.winfo_height()
    path = out / (name + ".png")
    ps = ("Add-Type -Name D -Namespace W -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool "
          "SetProcessDPIAware();'; [W.D]::SetProcessDPIAware() | Out-Null; "
          f"Add-Type -AssemblyName System.Drawing;$b=New-Object System.Drawing.Bitmap {w},{h}; "
          f"$g=[System.Drawing.Graphics]::FromImage($b); $g.CopyFromScreen({x},{y},0,0,$b.Size); "
          f"$b.Save('{path}'); $g.Dispose(); $b.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


past_count = len(k.get("store").past_index())
totals = k.get("store").paper_totals("MAM")
import_window = k.get("external.import_dialog")()
pump()
entries = [w for w in walk(import_window) if w.winfo_class() == "TEntry" and str(w.cget("state")) != "readonly"]
entries[0].insert(0, "Synthetic school trial")
entries[1].insert(0, "Synthetic source")
real_choose = filedialog.askopenfilename
files = iter((str(exam), str(answer)))
filedialog.askopenfilename = lambda **kw: next(files)
try:
    button(import_window, "选择试卷 PDF").invoke()
    button(import_window, "选择答案 PDF").invoke()
finally:
    filedialog.askopenfilename = real_choose
button(import_window, "导入并自动切块").invoke()
for _ in range(100):
    pump(0.05)
    if store.papers():
        break
assert len(store.papers()) == 1, "The import dialog must save the paired paper"
paper = store.papers()[0]["id"]
assert len(k.get("store").past_index()) == past_count
assert k.get("store").paper_totals("MAM") == totals
k.get("external.show")()
pump()
table = k.get("external.table")
ids = table.get_children()
assert len(ids) == 2
assert table.bbox(ids[0]), "The first result row must be visible in the external library"
sx, sy, sw, sh = table.bbox(ids[0], "state")
assert sx + sw <= table.winfo_width(), "The review status column must be visible"
shot("library")
table.selection_set(ids[0])
qid = int(ids[0])

# Use the registered mock provider through llm.chat; inspect a real draft and manual confirmation.
k.get("llm.providers")["mock"] = lambda settings, system, user, timeout: '{"tags":["MAM.M.2"],"reason":"Integrate velocity with the initial position.","uncertain":false}'
button(root, "AI 标注选中项").invoke()
for _ in range(100):
    pump(0.05)
    if store.question(qid)["tags"]:
        break
q = store.question(qid)
assert q["tags"] == ["MAM.M.2"] and not q["confirmed"], q
dlg = k.get("external.edit")(paper, qid)
pump()
check = next(w for w in walk(dlg) if w.winfo_class() == "TCheckbutton")
check.invoke()
button(dlg, "保存标注").invoke()
pump()
assert store.question(qid)["confirmed"]
k.emit("select.external", qid)
pump()
button(root, "显示外源答案").invoke()
pump()
assert any(w.winfo_class() == "Label" and w.cget("image") for w in walk(root))
shot("question_and_answer")

# Drag a real rectangle; the selector must preserve coordinates for mixed-width PDF pages.
picked = []
crop = k.get("external.crop.open")(store.asset(store.paper(paper)["exam"]), [], lambda r: picked.extend(r))
pump()
canvas = next(w for w in walk(crop) if w.winfo_class() == "Canvas")
canvas.event_generate("<ButtonPress-1>", x=20, y=25)
canvas.event_generate("<B1-Motion>", x=150, y=160)
canvas.event_generate("<ButtonRelease-1>", x=150, y=160)
pump()
shot("crop", crop)
button(crop, "应用切块").invoke()
pump()
assert len(picked) == 1
k.get("external.pdf.validate")(store.asset(store.paper(paper)["exam"]), picked)

# Keep import/editor/crop dialogs open together for a complete English boundary check.
import_dlg = k.get("external.import_dialog")()
edit_dlg = k.get("external.edit")(paper, qid)
crop_dlg = k.get("external.crop.open")(store.asset(store.paper(paper)["exam"]), q["exam_regions"], lambda r: None)
pump()
shot("import", import_dlg)
shot("editor", edit_dlg)
if language == "en":
    found = []
    cjk = re.compile(r"[一-鿿]+")
    for w in walk(root):
        strings = []
        try:
            strings.append(str(w.cget("text")))
        except Exception:
            pass
        if w.winfo_class() == "Treeview":
            strings.extend(str(w.item(i, "values")) for i in w.get_children())
        if w.winfo_class() == "Text":
            strings.append(w.get("1.0", "end"))
        if w.winfo_class() == "Toplevel":
            strings.append(w.title())
        found.extend(r for text in strings for r in cjk.findall(text))
    print(len(found), "external UI CJK runs")
    assert not found, found

print("external UI OK:", language, "paired import, draft API tags, manual confirmation, crop drag, source isolation", past_count, totals)
root.destroy()
store.close()
temp.cleanup()
