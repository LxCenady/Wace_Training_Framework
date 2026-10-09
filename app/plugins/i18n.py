"""Interface language. One job: show the (Chinese-source) interface in English when config["language"] == "en".

No string in the code base is wrapped or duplicated. Tk is patched once, at the few places text reaches the
screen (widget/menu/canvas options, ttk option dicts, Text.insert, StringVar.set, window titles), and every
run of CJK characters is replaced by its entry in i18n/en.json (built by `tools/translate.py ui`). Chinese
punctuation becomes ASCII; a run with no entry is shown as is and appended to i18n/missing.txt, so the
next `translate.py ui` picks it up. Load it right after config, before any UI plugin.
"""
import json, os, re, sys
import tkinter as tk
from tkinter import ttk

CJK = re.compile(r"[㐀-鿿　-〿＀-￯“”‘’·★☆]+")
HAS_CJK = re.compile(r"[㐀-鿿]")
PUNCT = {"：": ": ", "，": ", ", "。": ". ", "；": "; ", "（": " (", "）": ") ", "、": ", ", "「": "“", "」": "”",
         "？": "? ", "！": "! ", "【": "[", "】": "]", "《": "“", "》": "”", "　": " "}
TEXT_KEYS = ("text", "label", "title", "message", "detail")


def folder():
    base = getattr(sys, "_MEIPASS", None) or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "i18n")


def make_translator(table, missing_path):
    seen = set()

    def run(m, s):
        r = m.group(0)
        if r in table:
            out = table[r]
        elif not HAS_CJK.search(r):  # punctuation only
            out = "".join(PUNCT.get(c, c) for c in r)
        else:
            out = "".join(PUNCT.get(c, c) for c in r)
            if r not in seen:
                seen.add(r)
                try:
                    with open(missing_path, "a", encoding="utf-8") as f:
                        f.write(f"{r}\t{s[:160]}\n")
                except OSError:
                    pass
            return out
        before = s[m.start() - 1] if m.start() > 0 else " "
        after = s[m.end()] if m.end() < len(s) else " "
        if (before.isalnum() or before in ")]") and out[:1].isalnum():
            out = " " + out
        if after.isalnum() and out[-1:].isalnum():
            out += " "
        return out

    def tr(s):
        if not isinstance(s, str) or not CJK.search(s):
            return s
        return re.sub(r"  +", " ", CJK.sub(lambda m: run(m, s), s))

    return tr


def patch(tr):
    """Translate text on its way into Tk (idempotent per process)."""
    if getattr(tk.Misc, "_i18n_patched", False):
        return
    tk.Misc._i18n_patched = True

    def fix(d):
        if not d:
            return d
        d = dict(d)
        for key in list(d):
            if key.rstrip("_").lstrip("-") in TEXT_KEYS and isinstance(d[key], str):
                d[key] = tr(d[key])
        return d

    options = tk.Misc._options
    tk.Misc._options = lambda self, cnf, kw=None: options(self, fix(cnf) if isinstance(cnf, dict) else cnf, fix(kw))

    fmt = ttk._format_optdict

    def format_optdict(optdict, script=False, ignore=None):
        optdict = dict(optdict)
        if isinstance(optdict.get("text"), str):
            optdict["text"] = tr(optdict["text"])
        if isinstance(optdict.get("values"), (list, tuple)):
            optdict["values"] = [tr(v) for v in optdict["values"]]
        return fmt(optdict, script, ignore)
    ttk._format_optdict = format_optdict

    insert = tk.Text.insert
    tk.Text.insert = lambda self, index, chars, *args: insert(self, index, tr(chars), *args)
    setter = tk.StringVar.set
    tk.StringVar.set = lambda self, value: setter(self, tr(value))
    title = tk.Wm.wm_title
    tk.Wm.wm_title = tk.Wm.title = lambda self, string=None: title(self, tr(string))


def choices(tr):
    """For comboboxes whose values the code also uses: (shown values, shown -> internal value)."""
    def make(values):
        shown = [tr(v) for v in values]
        back = dict(zip(shown, values))
        return shown, lambda s: back.get(s, s)
    return make


def setup(k):
    lang = k.get("config").get("language", "zh")
    k.provide("i18n.lang", lang)
    if lang != "en":
        k.provide("i18n.tr", lambda s: s)
        k.provide("i18n.choices", choices(lambda s: s))
        return
    path = os.path.join(folder(), "en.json")
    table = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    writable = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "i18n")
    tr = make_translator(table, os.path.join(writable if os.access(writable, os.W_OK) else k.root, "missing.txt"))
    patch(tr)
    k.provide("i18n.tr", tr)
    k.provide("i18n.choices", choices(tr))
