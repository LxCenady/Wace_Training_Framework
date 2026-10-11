"""Chemistry GUI smoke test: a shared-paper science subject in the real window (offline mock provider).
Usage: python tests/smoke_che.py <out_dir>   — screenshots of the tree, a pattern, questions with their keys and the
data booklet pane; asserts the Chemistry-specific behaviour. Uses an in-memory generated.db like smoke_gui."""
import os, sqlite3, subprocess, sys, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from main import Kernel, find_root, plugin_names  # noqa: E402
from tests.safe_runtime import isolate  # noqa: E402
isolate()
sys.path.insert(0, os.path.join(find_root(), "tools"))
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


def find_all(w, cls):
    return ([w] if w.winfo_class() == cls else []) + [x for c in w.winfo_children() for x in find_all(c, cls)]


def pump(sec=0.6):
    end = time.time() + sec
    while time.time() < end:
        root.update()
        time.sleep(0.02)


def shot(name):
    pump()
    if os.name != "nt":
        return
    x, y, w, h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
    path = os.path.join(out, name + ".png")
    ps = ("Add-Type -Name D -Namespace W -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool "
          "SetProcessDPIAware();'; [W.D]::SetProcessDPIAware() | Out-Null; "
          f"Add-Type -AssemblyName System.Drawing;$b=New-Object System.Drawing.Bitmap {w},{h}; "
          f"$g=[System.Drawing.Graphics]::FromImage($b); $g.CopyFromScreen({x},{y},0,0,$b.Size); "
          f"$b.Save('{path}'); $g.Dispose(); $b.Dispose()")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)
    print("shot", path)


k.emit("ui.ready")
root.lift(); root.attributes("-topmost", True)
pump(1.0)
assert "CHE" in st.subjects(), st.subjects()
tree = find_all(root, "Treeview")[0]
che = next(i for i in tree.get_children() if "Chemistry" in tree.item(i, "text"))
tree.item(che, open=True)
print("CHE topics in tree:", len(tree.get_children(che)))
assert len(tree.get_children(che)) == 8
tree.see(tree.get_children(che)[-1])
shot("che_1_tree")

k.emit("select.pattern", ["CHE.EQ.4"])
pump(1.0)
shot("che_2_pattern")
combos = [w.get() for w in find_all(root, "TCombobox")]
print("drop-downs:", combos)
assert any(c.startswith("CHE") for c in combos), "the reference-sheet pane follows the subject"

for qid in ("CHE-2025S-Q30", "CHE-2019S-Q33"):  # key split per mark / key shown as an image
    k.emit("select.question", qid)
    pump(1.2)
    shot("che_3_" + qid.split("-", 1)[1])
combos = [w.get() for w in find_all(root, "TCombobox")]
assert "2019" in combos, f"a 2019 question shows the 2019 data booklet: {combos}"
print("paper totals CHE:", st.paper_totals("CHE"))
print("Chemistry GUI smoke OK")
