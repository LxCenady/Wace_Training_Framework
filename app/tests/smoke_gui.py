"""GUI smoke test: drives the real window with the offline mock provider and saves screenshots.
Usage: python tests/smoke_gui.py <out_dir>   (generated items go to an in-memory DB, not generated.db)"""
import os, sqlite3, subprocess, sys, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from main import Kernel, find_root, plugin_names  # noqa: E402
from plugins.store import GEN_SCHEMA  # noqa: E402

out = sys.argv[1]
k = Kernel(find_root())
k.load(plugin_names())
k.get("config")["provider"] = "mock"
st = k.get("store")
st.gen = sqlite3.connect(":memory:", check_same_thread=False)
st.gen.executescript(GEN_SCHEMA)
root = k.get("ui.root")
root.geometry("1400x880+20+20")


def find(w, cls):
    if w.winfo_class() == cls:
        return w
    for c in w.winfo_children():
        r = find(c, cls)
        if r:
            return r


def pump(sec=0.6):
    end = time.time() + sec
    while time.time() < end:
        root.update()
        time.sleep(0.02)


def shot(name):
    pump()
    x, y, w, h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
    path = os.path.join(out, name + ".png")
    ps = (f"Add-Type -AssemblyName System.Drawing; $b=New-Object System.Drawing.Bitmap {w},{h}; "
          f"$g=[System.Drawing.Graphics]::FromImage($b); $g.CopyFromScreen({x},{y},0,0,$b.Size); "
          f"$b.Save('{path}'); $g.Dispose(); $b.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    print("shot", path)


def button(text):
    def walk(w):
        if w.winfo_class() == "TButton" and w.cget("text") == text:
            return w
        for c in w.winfo_children():
            r = walk(c)
            if r:
                return r
    return walk(root)


k.emit("ui.ready")  # run() is not called: the test pumps the event loop itself
tree = find(root, "Treeview")
root.lift(); root.attributes("-topmost", True)
pump(1.0)
for node in ("T:MAM.D", "P:MAM.D.6"):
    tree.item(node, open=True)
tree.focus("P:MAM.D.6"); tree.event_generate("<<TreeviewOpen>>")
tree.selection_set("P:MAM.D.6"); tree.see("P:MAM.D.6")
shot("1_pattern")
q = tree.get_children("P:MAM.D.6")[0]
tree.selection_set(q); tree.see(q)
shot("2_question")
button("显示评分标准（拆分到每一分）").invoke()
shot("3_key")
tree.selection_set(("P:MAM.D.6", "P:MAM.D.4"))
pump(0.3)
button("AI 生成相似题").invoke()
for _ in range(100):
    pump(0.1)
    if button("显示得分点与解答"):
        break
shot("4_generated")
button("显示得分点与解答").invoke()
shot("5_points")
print("tree children of D.6:", tree.get_children("P:MAM.D.6")[:2])
root.destroy()
