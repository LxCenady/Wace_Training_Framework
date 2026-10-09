"""GUI smoke test: drives the real window with the offline mock provider and saves screenshots.
Usage: python tests/smoke_gui.py <out_dir>   (generated items go to an in-memory DB, not generated.db)"""
import os, sqlite3, subprocess, sys, time
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
from main import Kernel, find_root, plugin_names  # noqa: E402
import tempfile as _tf, plugins.config as _config  # noqa: E402
_config.PATH = os.path.join(_tf.gettempdir(), "wtf-test-config.json")  # never touch the user's settings
sys.path.insert(0, os.path.join(find_root(), "tools"))  # like main(): tools/ modules are importable
from plugins.store import GEN_SCHEMA  # noqa: E402

out = sys.argv[1]
WORK_PDF = os.path.join(out, "smoke_export.pdf")


def text_widgets_of(w):
    for c in w.winfo_children():
        if c.winfo_class() == "Text":
            yield c
        yield from text_widgets_of(c)
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
    ps = ("Add-Type -Name D -Namespace W -MemberDefinition '[DllImport(\"user32.dll\")] public static extern bool "
          "SetProcessDPIAware();'; [W.D]::SetProcessDPIAware() | Out-Null; "
          f"Add-Type -AssemblyName System.Drawing;$b=New-Object System.Drawing.Bitmap {w},{h}; "
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
# batch: 3 hard questions on the same two patterns, then 2 on another pattern
finished = []
k.on("gen.finished", lambda ok, n: finished.append((ok, n)))


def batch(codes, level, n):
    k.get("generator.start")(codes, "any", 0, level, n)
    for _ in range(300):
        pump(0.1)
        if len(finished) and finished[-1][1] == n and len(finished) == batch.calls + 1:
            break
    batch.calls += 1


batch.calls = 0
batch(["MAM.D.6", "MAM.D.4"], "拔高", 3)
shot("6_batch_log")
assert finished[-1] == (3, 3), finished
batch(["MAM.D.1"], "基础", 2)
assert finished[-1] == (2, 2), finished

# 我的 AI 题库: same tags fold into one group
k.get("mybank.show")()


def tables(w):
    for c in w.winfo_children():
        if c.winfo_class() == "Treeview" and "headings" in str(c.cget("show")):
            yield c
        yield from tables(c)


table = next(tables(root))
groups = table.get_children()
sizes = sorted(len(table.get_children(g)) for g in groups)
assert sizes == [2, 4], sizes  # D.4+D.6: 1 single + 3 batch; D.1: 2
table.item(groups[0], open=True)
shot("7_mybank")
first = table.get_children(groups[0])[0]
table.selection_set(first)
table.see(first)
pump(0.3)
x, y, w, h = table.bbox(first)  # a double-click needs no keyboard focus (the desktop may be in use)
for _ in range(2):  # two quick clicks = Tk's <Double-1>
    table.event_generate("<ButtonPress-1>", x=x + w // 2, y=y + h // 2)
    table.event_generate("<ButtonRelease-1>", x=x + w // 2, y=y + h // 2)
pump()
texts = []


def all_text(w):
    for c in w.winfo_children():
        if c.winfo_class() == "Text":
            texts.append(c.get("1.0", "end"))
        all_text(c)


all_text(root)
assert any(f"AI 题 #{first}" in t for t in texts), "opening a bank row must show that item"
if not button("显示得分点与解答"):
    def all_buttons(w):
        for c in w.winfo_children():
            if c.winfo_class() == "TButton":
                yield c.cget("text")
            yield from all_buttons(c)
    print("buttons now:", list(all_buttons(root)))
assert button("显示得分点与解答"), "answers must still be hidden behind the button"
print("mybank groups:", [(table.item(g, "text"), table.item(g, "values")[2], len(table.get_children(g)))
                         for g in groups])

# self-marking: right-click part (b) of the open AI item -> the popup gets that part's context
button("显示得分点与解答").invoke()
pump()
hits = []
real_popup = k.get("mistakes.popup")
k.provide("mistakes.popup", lambda e, ctx: hits.append(ctx))  # tk_popup is modal on Windows: record instead
text_widgets = []


def find_texts(w):
    for c in w.winfo_children():
        if c.winfo_class() == "Text" and "part:b" in c.tag_names():
            text_widgets.append(c)
        find_texts(c)


find_texts(root)
t = text_widgets[0]
t.see(t.tag_ranges("part:b")[0])
pump(0.3)
x, y, _, _ = t.bbox(t.tag_ranges("part:b")[0])
t.event_generate("<Button-3>", x=x + 5, y=y + 3)
pump(0.3)
assert hits and hits[-1]["label"] == "b" and hits[-1]["part_marks"] == 4 and len(hits[-1]["points"]) == 4, hits
k.provide("mistakes.popup", real_popup)
ctx = hits[-1]

# the marking dialog: tick two missed points, save
k.get("mistakes.dialog")(ctx)
pump(0.5)
dlg = [w for w in root.winfo_children() if w.winfo_class() == "Toplevel"][-1]
boxes = []


def find_checks(w):
    for c in w.winfo_children():
        if c.winfo_class() == "TCheckbutton":
            boxes.append(c)
        find_checks(c)


find_checks(dlg)
boxes[1].invoke()
boxes[3].invoke()
pump(0.2)
shot("8_marking")
next(b for b in dlg.winfo_children()[0].winfo_children()[-1].winfo_children() if b.cget("text") == "记入错题本").invoke()
pump()
m = st.mistake("gen", ctx["ref"], "b")
assert m and m["lost"] == 2 and len(m["missed"]) == 2, m

# a past question too (no dialog: store directly), then the 错题本 and a targeted drill
st.save_mistake("past", "MAM-2025A-Q12", "b", 4, 3, ["MAM.D.6"], [], "忘了验证最大值")
k.get("mistakes.show")()
pump()
book = k.get("mistakes.table")
top_group = book.get_children()[0]
print("错题本:", [(book.item(g, "text"), book.item(g, "values")[:2]) for g in book.get_children()])
assert top_group == "p:MAM.D.6", top_group  # D.6 has the most lost marks (2 + 3)
shot("9_mistakes")
before = len(finished)
drill = button("生成错题加强题（未选中时针对最弱题型）")
drill.invoke()
for _ in range(300):
    pump(0.1)
    if len(finished) > before:
        break
newest = st.generated(st.generated_all()[0][0])
assert newest["focus"] and newest["patterns"] == ["MAM.D.6"], (newest["focus"], newest["patterns"])
print("drill focus:", newest["focus"].splitlines()[:3])

# 一键讲解: one past-paper mistake and one AI-question mistake; the explanation is cached on the row
for src, ref, label in (("past", "MAM-2025A-Q12", "b"), ("gen", ctx["ref"], "b")):
    k.get("mistakes.explain")(st.mistake(src, ref, label))
    for _ in range(100):
        pump(0.1)
        if st.mistake(src, ref, label)["explain"]:
            break
    assert "这一问考什么" in st.mistake(src, ref, label)["explain"], src
shot("10_explain")
print("explained:", [m["ref"] for m in st.mistakes() if m["explain"]])

# 模拟考试: a real paper (timer, questions), submit, mark one part, score updates; then an AI-assembled paper
k.get("exam.show")()
pump()
k.get("exam.start")("MAM", "CalcFree", "past", "2025", type("M", (), {"configure": lambda *a, **kw: None})())
pump(1.5)
shot("11_exam_sitting")
exam = st.exams()[0]
assert exam["source"] == "past:2025" and exam["total"] == 47 and len(exam["refs"]) == 7, exam
k.get("exam.submit")()
pump()
first_q = exam["refs"][0][1]
d = st.question(first_q)
st.save_mistake("past", first_q, d["parts"][0][0], d["parts"][0][1] or 1, 1, d["parts"][0][2], [], "")
k.emit("mistakes.changed")
pump()
shot("12_exam_marking")
assert st.exam(exam["id"])["lost"] == 1, st.exam(exam["id"])
k.get("exam.start")("MAM", "CalcAssumed", "ai", "", type("M", (), {"configure": lambda *a, **kw: None})())
pump(0.4)
shot("12b_exam_progress")
for _ in range(300):
    pump(0.1)
    if st.exams()[0]["source"] == "ai":
        break
ai_exam = st.exams()[0]
assert ai_exam["source"] == "ai" and 9 <= len(ai_exam["refs"]) <= 10, ai_exam  # count follows real papers
print("exams:", [(e["source"], e["total"], e["lost"], bool(e["submitted"])) for e in st.exams()])

# export both kinds of paper (file dialogs replaced)
import plugins.ui_exam as ui_exam  # noqa: E402
ui_exam.filedialog.asksaveasfilename = lambda **kw: os.path.join(out, "smoke_ai_paper.pdf")
ui_exam.filedialog.askdirectory = lambda **kw: out
ui_exam.os.startfile = lambda p: None
k.get("exam.export")(ai_exam)
k.get("exam.export")(exam)
import pymupdf  # noqa: E402
ai_pdf = pymupdf.open(os.path.join(out, "smoke_ai_paper.pdf"))
assert "阅读时间 10 分钟 + 作答时间 100 分钟" in ai_pdf[0].get_text().replace(chr(160), " "), ai_pdf[0].get_text()[:200]
assert os.path.exists(os.path.join(out, "smoke_ai_paper_答案.pdf"))
past = [f for f in os.listdir(out) if f.startswith("WTF_MAM_CalcFree_2025") and f.endswith(".pdf")]
assert len(past) == 2, past
print("exam export:", ai_pdf.page_count, "pages AI paper + answers;", sorted(past))

# 掌握度 + 间隔复习
mastery = st.mastery()
print("mastery D.6:", mastery.get("MAM.D.6"), " D.1:", mastery.get("MAM.D.1"))
assert mastery["MAM.D.6"]["lost"] >= 3 and mastery["MAM.D.6"]["attempted"] >= mastery["MAM.D.6"]["lost"]
k.get("mastery.show")()
pump(1)
shot("13_mastery")
m = st.mistake("past", "MAM-2025A-Q12", "b")
assert m["due"] and m["box"] == 0, m  # new mistakes are due tomorrow
st.gen.execute("UPDATE mistakes SET due = '2000-01-01' WHERE id = ?", (m["id"],))
assert any(x["id"] == m["id"] for x in st.due_mistakes())
box, due = st.review(m["id"], True)
assert box == 1 and due > m["due"], (box, due)
box, due = st.review(m["id"], False)
assert box == 0, box
print("review: passed -> box 1, failed -> box 0, due", due)

# LaTeX + figures: the mock question has $…$, $$…$$, money (\$2) and a figure; open it and reveal
gid = st.generated_all()[0][0]
item = st.generated(gid)
assert item["figure"] and "$f(x) = x^3 - 3x + 1$" in item["question"], item["question"][:80]
k.emit("select.generated", gid)
pump()
button("显示得分点与解答").invoke()
pump()
gen_text = next(w for w in text_widgets_of(root) if "AI 题 #" in w.get("1.0", "3.0"))
images = gen_text.image_names()
print("AI view: rendered images =", len(images), "| raw '$' left in text:", gen_text.get("1.0", "end").count("$"))
assert len(images) >= 5, images  # 4 formulas in the stem + the figure (+ more in the key)
assert "Entry costs $2" in gen_text.get("1.0", "end"), "money must show as $2, not as maths"
shot("14_latex")
q_pdf, a_pdf = k.get("export.worksheet")([gid], WORK_PDF, "LaTeX 导出测试")
import pymupdf  # noqa: E402
d = pymupdf.open(q_pdf)
print("export:", d.page_count, "pages,", len(d[0].get_images()), "images on page 1")
assert len(d[0].get_images()) >= 4
d[0].get_pixmap(dpi=80).save(WORK_PDF[:-4] + "_p1.png")
root.destroy()
