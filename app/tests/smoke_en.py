"""English-interface smoke test: every main view opened with language = en; screenshots + the CJK left on screen.
Usage: python tests/smoke_en.py <out_dir>   (mock provider, in-memory generated.db)"""
import os, re, sqlite3, subprocess, sys, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from main import Kernel, find_root, plugin_names  # noqa: E402
import tempfile as _tf, plugins.config as _config  # noqa: E402
_config.PATH = os.path.join(_tf.gettempdir(), "wtf-test-config.json")  # never touch the user's settings
sys.path.insert(0, os.path.join(find_root(), "tools"))  # like main(): tools/ modules are importable

out = sys.argv[1]
root_dir = find_root()
os.environ["WACE_MATHS_ROOT"] = root_dir
sys.path.insert(0, os.path.join(root_dir, "tools"))
import plugins.config as config  # noqa: E402
real_load = config.load
config.load = lambda: dict(real_load(), language="en", provider="mock")  # do not touch the user's config file
k = Kernel(root_dir)
k.load(plugin_names())
from plugins.store import GEN_SCHEMA  # noqa: E402
st = k.get("store")
st.gen = sqlite3.connect(":memory:", check_same_thread=False)
st.gen.executescript(GEN_SCHEMA)
root = k.get("ui.root")
root.geometry("1500x900+10+10")
CJK = re.compile(r"[一-鿿]+")


def pump(sec=0.6):
    end = time.time() + sec
    while time.time() < end:
        root.update()
        time.sleep(0.02)


def shot(name):
    pump()
    x, y, w, h = root.winfo_rootx(), root.winfo_rooty(), root.winfo_width(), root.winfo_height()
    path = os.path.join(out, name + ".png")
    ps = ("Add-Type -Name D -Namespace W -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool "
          "SetProcessDPIAware();'; [W.D]::SetProcessDPIAware() | Out-Null; "
          f"Add-Type -AssemblyName System.Drawing; $b=New-Object System.Drawing.Bitmap {w},{h}; "
          f"$g=[System.Drawing.Graphics]::FromImage($b); $g.CopyFromScreen({x},{y},0,0,$b.Size); $b.Save('{path}')")
    subprocess.run(["powershell", "-NoProfile", "-Command", ps], check=True)


def visible_cjk(w=None, found=None):
    """CJK runs still shown by any widget (texts, labels, buttons, tree items, tabs)."""
    w, found = w or root, found if found is not None else {}
    for c in w.winfo_children():
        texts = []
        try:
            texts.append(str(c.cget("text")))
        except Exception:
            pass
        cls = c.winfo_class()
        if cls == "TCombobox":
            texts.append(c.get())
            texts.extend(map(str, c.cget("values")))
        if cls == "Text":
            texts.append(c.get("1.0", "end"))
        if cls == "Treeview":
            def walk(item=""):
                for i in c.get_children(item):
                    texts.append(c.item(i, "text"))
                    texts.extend(map(str, c.item(i, "values")))
                    walk(i)
            walk()
        if cls == "TNotebook":
            texts.extend(c.tab(t, "text") for t in c.tabs())
        for t in texts:
            for r in CJK.findall(t):
                found[r] = t[:80]
        visible_cjk(c, found)
    return found


k.emit("ui.ready")
root.lift()
root.attributes("-topmost", True)
pump(1)
k.emit("select.pattern", ["MAM.D.6"])
shot("en_1_pattern")
k.emit("select.question", "MAM-2025A-Q12")
shot("en_2_question")
item = k.get("generator.run")(["MAM.D.6"])
k.emit("select.generated", item["id"])
shot("en_3_ai")
st.save_mistake("gen", item["id"], "b", 4, 2, ["MAM.D.6"], [], "")
k.get("mistakes.show")()
shot("en_4_mistakes")
k.get("mastery.show")()
shot("en_5_mastery")
k.get("exam.show")()
shot("en_6_exam")
k.emit("select.topic", "MAM.D")
shot("en_7_unit")
k.get("search.show")()
shot("en_8_search")
k.get("mybank.show")()
shot("en_9_mybank")
left = visible_cjk()
print(len(left), "CJK runs still visible")
for r, ctx in sorted(left.items())[:40]:
    print(f"  {r!r:24} in {ctx!r}")
root.destroy()
