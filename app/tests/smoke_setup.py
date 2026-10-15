"""First-run wizard smoke test: a fresh data root with no papers, a 'Downloads' folder of renamed PDFs,
the wizard watching it, then 建立题库. Usage: python tests/smoke_setup.py <work dir> <folder with the real papers>"""
import glob, os, random, shutil, subprocess, sys, time

work, papers_root = sys.argv[1], sys.argv[2]
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data, downloads = os.path.join(work, "data"), os.path.join(work, "Downloads")
desktop = os.path.join(work, "Desktop")  # where a Mac's Safari may save instead: picked with 选择已下载的文件…
shutil.rmtree(work, ignore_errors=True)
os.makedirs(downloads)
os.makedirs(desktop)
for f in subprocess.run(["git", "ls-files", "-z"], cwd=REPO, capture_output=True, text=True,
                        encoding="utf-8").stdout.split("\0"):
    if f and not f.startswith("app/"):
        os.makedirs(os.path.dirname(os.path.join(data, f)) or data, exist_ok=True)
        shutil.copyfile(os.path.join(REPO, f), os.path.join(data, f))
os.environ["WACE_MATHS_ROOT"] = data
sys.path.insert(0, os.path.join(REPO, "app"))
import main  # noqa: E402
from tests.safe_runtime import isolate  # noqa: E402
isolate()

sys.path.insert(0, os.path.join(data, "tools"))
from kernel import Kernel  # noqa: E402
import plugins.ui_setup as ui_setup  # noqa: E402
import fetch  # noqa: E402


def offline(*a, **kw):  # the wizard starts archive downloads by itself: keep the test offline
    raise OSError("offline test")


fetch.download = offline

restarted = []
ui_setup.restart = lambda args=None: restarted.append(True)
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


k.get("setup.folder")(downloads)  # stands in for the user's Downloads folder
k.get("setup.choose")(["MAM", "MAS", "MAA"])  # a fresh install asks for the subjects first
pump(1)
random.seed(7)
pdfs = sorted(glob.glob(os.path.join(papers_root, "*", "papers", "*.pdf")))


def find(w, text):
    for c in w.winfo_children():
        if c.winfo_class() == "TButton" and c.cget("text") == text:
            return c
        r = find(c, text)
        if r:
            return r


def log_text(w):
    """Everything the wizard has written to its log."""
    out = ""
    for c in w.winfo_children():
        if c.winfo_class() == "Text":
            out += c.get("1.0", "end")
        out += log_text(c)
    return out


def banner(w):
    for c in w.winfo_children():
        if c.winfo_class() == "Label" and str(c.cget("text")).startswith("第"):
            return c.cget("text")
        r = banner(c)
        if r:
            return r


check = find(root, "我存好了，检查下载文件夹")
assert find(root, "选择已下载的文件…"), "the wizard must offer picking the files wherever they were saved"
# a saved verification page with a .pdf name: the student must be told, not left wondering
open(os.path.join(downloads, "2024_Exam.pdf"), "w").write("<html>Checking your browser…</html>")
elsewhere = pdfs[-8:]  # the last ones were saved to the Desktop
for i, f in enumerate(pdfs[:-8]):  # like a browser: random names in the Downloads folder
    shutil.copyfile(f, os.path.join(downloads, f"download_{random.randint(0, 10**9)}.pdf"))
    if i == 30:  # half the papers saved, then the button: imported, but never a partial bank
        pump(4)
        assert len(__import__("fetch").missing(data)) == len(__import__("fetch").missing(data)), "nothing is watched"
        check.invoke()
        pump(1)
        print("half imported, banner:", banner(root))
        assert find(root, "重新建库").instate(["disabled"]) and not restarted, "a partial bank must not be built"
        assert "第" in (banner(root) or ""), "the banner must say what to do next"
        assert "不是 PDF" in log_text(root), "a saved web page must be reported"
        k.get("setup.folder")(os.path.join(work, "no access"))  # macOS: Downloads not allowed / gone
        check.invoke()
        pump(1)
        assert "读不了下载文件夹" in log_text(root), "an unreadable Downloads folder must be explained"
        k.get("setup.folder")(downloads)
before = len(__import__("fetch").missing(data))
pump(4)  # no watching: nothing arrives until the button is pressed
assert len(__import__("fetch").missing(data)) == before, "the wizard must not import without the button"
check.invoke()
pump(1)
saved_elsewhere = []
for f in elsewhere:
    saved_elsewhere.append(os.path.join(desktop, f"Screenshot {random.randint(0, 10**9)}.pdf"))
    shutil.copyfile(f, saved_elsewhere[-1])
k.get("setup.import_paths")(saved_elsewhere + [os.path.join(downloads, "2024_Exam.pdf")])  # what the dialog returns
pump(1)
left = __import__("fetch").missing(data)
print("missing after checking Downloads and picking the Desktop files:", [m[0] for m in left])
assert all("Sample_MAS_MarkingKey" in m[0] for m in left), left  # only the scanned sample keys can't be recognised

ui_setup.messagebox.askyesno = lambda *a, **kw: True


def ui_setup_busy(r):
    try:
        b = find(r, "重新建库")
        return b is not None and b.instate(["disabled"])
    except Exception:  # window already gone: the build finished and the app restarted
        return True


# the last paper arriving starts the build by itself; press the button only if it has not
auto = bool(restarted) or ui_setup_busy(root)
if not auto:
    find(root, "重新建库").invoke()
print("build started automatically:", auto)
for _ in range(600):
    pump(0.5)
    if restarted:
        break
assert restarted and os.path.isfile(os.path.join(data, "bank.db")), "build did not finish"
import sqlite3  # noqa: E402
db = sqlite3.connect(os.path.join(data, "bank.db"))
print("built:", db.execute("SELECT COUNT(*) FROM questions").fetchone()[0], "questions,",
      db.execute("SELECT COUNT(*) FROM points").fetchone()[0], "mark points")
