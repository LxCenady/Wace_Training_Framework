"""First-run wizard smoke test: a fresh data root with no papers, a 'Downloads' folder of renamed PDFs,
the wizard watching it, then 建立题库. Usage: python tests/smoke_setup.py <work dir> <folder with the real papers>"""
import glob, os, random, shutil, subprocess, sys, time

work, papers_root = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data, downloads = os.path.join(work, "data"), os.path.join(work, "Downloads")
shutil.rmtree(work, ignore_errors=True)
os.makedirs(downloads)
for f in subprocess.run(["git", "ls-files"], cwd=REPO, capture_output=True, text=True, encoding="utf-8").stdout.split():
    if not f.startswith("app/"):
        os.makedirs(os.path.dirname(os.path.join(data, f)) or data, exist_ok=True)
        shutil.copyfile(os.path.join(REPO, f), os.path.join(data, f))
os.environ["WACE_MATHS_ROOT"] = data
sys.path.insert(0, os.path.join(REPO, "app"))
import main  # noqa: E402
import tempfile as _tf, plugins.config as _config  # noqa: E402
_config.PATH = os.path.join(_tf.gettempdir(), "wtf-test-config.json")  # never touch the user's settings

sys.path.insert(0, os.path.join(data, "tools"))
from kernel import Kernel  # noqa: E402
import plugins.ui_setup as ui_setup  # noqa: E402
import fetch  # noqa: E402


def offline(*a, **kw):  # the wizard starts archive downloads by itself: keep the test offline
    raise OSError("offline test")


fetch.download = offline

restarted = []
ui_setup.restart = lambda: restarted.append(True)
k = Kernel(data)
k.load(main.plugin_names(os.path.join(REPO, "app", "setup.txt")))
root = k.get("ui.root")
k.emit("ui.ready")


def pump(sec):
    end = time.time() + sec
    while time.time() < end:
        try:
            root.update()
        except Exception:
            return
        time.sleep(0.02)


k.get("setup.watch")(downloads)
pump(1)
random.seed(7)
pdfs = sorted(glob.glob(os.path.join(papers_root, "*", "papers", "*.pdf")))
for i, f in enumerate(pdfs):  # like a browser: random names, arriving a few at a time
    shutil.copyfile(f, os.path.join(downloads, f"download_{random.randint(0, 10**9)}.pdf"))
    if i % 20 == 0:
        pump(0.3)
for _ in range(60):  # the wizard polls every 2 s
    pump(1)
    if len(__import__("fetch").missing(data)) <= 1:
        break
left = __import__("fetch").missing(data)
print("missing after watching Downloads:", [m[0] for m in left])
assert all("Sample_MAS_MarkingKey" in m[0] for m in left), left  # only the scanned sample keys can't be recognised

ui_setup.messagebox.askyesno = lambda *a, **kw: True


def ui_setup_busy(r):
    try:
        b = find(r, "建立题库并启动")
        return b is not None and b.instate(["disabled"])
    except Exception:  # window already gone: the build finished and the app restarted
        return True


def find(w, text):
    for c in w.winfo_children():
        if c.winfo_class() == "TButton" and c.cget("text") == text:
            return c
        r = find(c, text)
        if r:
            return r


# the last paper arriving starts the build by itself; press the button only if it has not
auto = bool(restarted) or ui_setup_busy(root)
if not auto:
    find(root, "建立题库并启动").invoke()
print("build started automatically:", auto)
for _ in range(600):
    pump(0.5)
    if restarted:
        break
assert restarted and os.path.isfile(os.path.join(data, "wace.db")), "build did not finish"
import sqlite3  # noqa: E402
db = sqlite3.connect(os.path.join(data, "wace.db"))
print("built:", db.execute("SELECT COUNT(*) FROM questions").fetchone()[0], "questions,",
      db.execute("SELECT COUNT(*) FROM points").fetchone()[0], "mark points")
