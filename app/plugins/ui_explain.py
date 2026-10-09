"""一键讲解. One job: explain one recorded mistake in Chinese, using the question, its verified answer /
official marking points, the points the student missed, their note, and the pattern's method notes.

The explanation is cached on the mistake row (re-marking the part clears it); 「重新讲解」 asks again.
"""
import re, threading
import tkinter as tk
from tkinter import ttk

SYSTEM = ("[STAGE:EXPLAIN]\nYou are a patient WACE mathematics tutor explaining a marked mistake to a Year 12 student "
          "in Western Australia. Write in Simplified Chinese, keeping mathematical terms and exam wording in English "
          "where the exam uses them. Write mathematics in LaTeX between $...$ (inline) or $$...$$ (a displayed "
          "line); write money as \\$5. No Markdown tables.\n"
          "Structure, with these headings:\n"
          "1. 这一问考什么 — the pattern and what the examiner is checking.\n"
          "2. 你丢的分 — for each missed mark point: what the marker wanted and the likely reason it was missed "
          "(use the student's note if given).\n"
          "3. 正确做法 — the full working for this part, step by step, marking where each mark is earned (✓).\n"
          "4. 下次怎么避免 — 2-4 concrete habits or checks.\n"
          "Base everything on the given answer and marking points; do not invent different answers.")


def material(store, m):
    """The question, its key for this part, the misses and the method notes, as plain text."""
    if m["source"] == "gen":
        item = store.generated(int(m["ref"]))
        part = next((p for p in item["parts"] if p["label"] == m["label"]), {})
        key = "\n".join(f"- {t}" for l, t in item["points"] if l == m["label"])
        body = (f"Question (AI-generated, verified):\n{item['question']}\n\nPart ({m['label']}) — {m['part_marks']} "
                f"marks. Verified answer: {part.get('answer', '')}\nMarking points for this part:\n{key}\n\n"
                f"Worked solution (whole question):\n{item['solution']}")
    else:
        d = store.question(m["ref"])
        key = "\n".join(f"- {t}" for l, t in d["points"] if l == m["label"]) if d["points_ok"] else \
            "(official key not split cleanly — infer the marks from the question)"
        body = (f"Question (WACE {d['year']} {d['subject']}, "
                f"{'calculator-free' if d['section'] == 'CalcFree' else 'calculator-assumed'}, Q{d['q']}):\n"
                f"{d['stem']}\n\nPart ({m['label'] or 'whole question'}) — {m['part_marks']} marks.\n"
                f"Official marking points for this part:\n{key}")
    notes = "\n\n".join(f"Method notes for {store.pattern_name(c)}:\n{store.pattern(c)['method']}"
                        for c in m["patterns"])
    missed = "\n".join(f"- {t}" for t in m["missed"]) or "(not specified)"
    return (f"{body}\n\nThe student lost {m['lost']} of {m['part_marks']} marks on this part.\n"
            f"Mark points the student missed:\n{missed}\nStudent's note: {m['note'] or '(none)'}\n\n{notes}")


def lines(text):
    """Light Markdown -> (line, is_heading): models add '##' and '**' even when asked not to."""
    for line in text.splitlines():
        heading = line.lstrip().startswith("#")
        line = re.sub(r"\*\*(.+?)\*\*", r"\1", line.lstrip("# ") if heading else line)
        yield re.sub(r"`([^`]+)`", r"\1", line), heading


def setup(k):
    store, root = k.get("store"), k.get("ui.root")
    w, ui_text = k.get("ui.write"), k.get("ui.text")

    def show_text(t, text):
        math = k.get("math.write", None)
        pending = ""  # a $$…$$ block spanning several lines is rendered as one piece
        for line, heading in lines(text):
            pending += line + "\n"
            if pending.count("$$") % 2:
                continue
            tags = ("sub",) if heading else ()
            math(t, pending, *tags) if math else w(t, pending, *tags)
            pending = ""
        if pending:
            w(t, pending)

    def explain(m, again=False):
        top = tk.Toplevel(root)
        title = (f"AI #{m['ref']}" if m["source"] == "gen" else m["ref"]) + f" ({m['label'] or '整题'})"
        top.title(f"错题讲解 — {title}")
        top.geometry("860x760")
        bar = ttk.Frame(top)
        bar.pack(fill="x", padx=8, pady=6)
        t = ui_text(top)
        t.frame.pack(fill="both", expand=True)
        w(t, f"错题讲解 · {title} · 扣 {m['lost']} / {m['part_marks']} 分\n", "h")
        w(t, "题型：" + "；".join(store.pattern_name(c) for c in m["patterns"]) + "\n\n", "muted")
        ttk.Button(bar, text="重新讲解", command=lambda: (top.destroy(), explain(m, again=True))).pack(side="left")
        cached = (store.mistake(m["source"], m["ref"], m["label"]) or {}).get("explain")
        if cached and not again:
            w(t, cached + "\n")
            return
        w(t, "正在讲解…（使用设置里的模型）\n", "muted")
        post = k.get("ui.post")

        def work():
            try:
                text = k.get("llm.chat")(SYSTEM, material(store, m)).strip()
                store.set_explanation(m["id"], text)

                def done():
                    if t.winfo_exists():
                        k.get("ui.clear")(t)
                        w(t, f"错题讲解 · {title} · 扣 {m['lost']} / {m['part_marks']} 分\n", "h")
                        w(t, "题型：" + "；".join(store.pattern_name(c) for c in m["patterns"]) + "\n\n", "muted")
                        w(t, text + "\n")
                    k.emit("mistakes.changed")
                post(done)
            except Exception as e:
                msg = f"讲解失败：{type(e).__name__}: {e}"
                post(lambda: t.winfo_exists() and w(t, msg + "\n", "warn"))

        threading.Thread(target=work, daemon=True).start()

    k.provide("mistakes.explain", explain)
