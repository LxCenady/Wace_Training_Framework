"""A Compiler pack in the question bank. One job: an active recipe -> rows of the bank schema + a subject profile.

WTF is the runtime of its packs, so a Compiler pack is a subject like any other: its topics, patterns, questions,
parts, scoring trees and marking-key criteria are written to compiler/bank.db with exactly the tables of bank.db
(tools/build_db.py SCHEMA), and its profile to compiler/profiles/<S>.json (tools/subjects.py reads both). The bank
reads them through one set of views (app/plugins/store.py). Rows never leave this computer: stems and criteria come
from the private content of the locally bound originals.
"""
import copy, json, os, re, sqlite3
from pathlib import Path

import pymupdf

import rubric
import subjects
from . import schema

YEAR = re.compile(r"\b(20\d\d)\b")


def code_of(course_id):
    """'CAIE9709' -> 'CAIE9709'; anything else is reduced to capitals and digits, starting with a letter."""
    code = re.sub(r"[^A-Z0-9]", "", str(course_id).upper())[:12]
    code = code if code[:1].isalpha() else ("C" + code)[:12]
    schema.require(subjects.CODE.fullmatch(code), f"Course id {course_id!r} gives no subject code")
    return code


def word(text):
    return re.sub(r"[^A-Za-z0-9]", "", str(text)) or "x"


def cover_year(path):
    """The first 20xx printed on a paper's cover (the recipe protocol has no session field yet), else 0."""
    try:
        with pymupdf.open(path) as pdf:
            m = YEAR.search(pdf[0].get_text())
        return int(m.group(1)) if m else 0
    except Exception:
        return 0


def connect(path):
    import build_db  # noqa: the bank schema is defined once, in tools/build_db.py
    fresh = not Path(path).exists()
    db = sqlite3.connect(path)
    if fresh:
        db.executescript(build_db.SCHEMA)
    return db


def remove(db, subject):
    for table, column in (("topics", "code"), ("patterns", "code"), ("knowledge", "code"), ("pattern_flags", "code"),
                          ("axis_codes", "code")):
        db.execute(f"DELETE FROM {table} WHERE {column} LIKE ?", (subject + ".%",))
    for table, column in (("questions", "id"), ("parts", "qid"), ("part_patterns", "qid"), ("points", "qid"),
                          ("award_tags", "qid"), ("rubrics", "qid")):
        db.execute(f"DELETE FROM {table} WHERE {column} LIKE ?", (subject + "-%",))


def project(library, pack):
    """Write the active version of `pack` into compiler/bank.db and its profile; -> {subject, questions, parts}."""
    recipe, content, fingerprint = library.load(pack)
    home = library.projects.root          # <data root>/compiler
    data_root = home.parent
    assets = library.projects.assets
    course = recipe["course"]
    s = code_of(course["id"])
    tax = recipe["taxonomy"]
    names = course["name"]

    topic_code = {t["id"]: f"{s}.{word(t['id'])}" for t in tax["topics"]}
    pattern_code, knowledge_code, counters = {}, {}, {}
    for p in tax["patterns"]:
        counters[p["topic"]] = counters.get(p["topic"], 0) + 1
        pattern_code[p["id"]] = (f"{topic_code[p['topic']]}.{counters[p['topic']]}", counters[p["topic"]])
    kcount = {}
    for k in tax["knowledge"]:
        kcount[k["topic"]] = kcount.get(k["topic"], 0) + 1
        knowledge_code[k["id"]] = f"{topic_code[k['topic']]}.K{kcount[k['topic']]}"

    sources = {d["id"]: d for d in recipe["sources"]}
    path_of = {d: assets.path(sources[d]["sha256"]) for d in sources}
    rel = {d: os.path.relpath(path_of[d], data_root).replace(os.sep, "/") for d in sources}
    years = {}

    def regions(refs, document):
        return [dict(page=r["page"], bbox=r["bbox"], rotate=r.get("rotate", 0)) for r in refs if r["document"] == document]

    def remap(node):
        node = copy.deepcopy(node)
        for n in rubric.validate(node)[0].values():
            if n.get("kind") == "award":
                n["patterns"] = [pattern_code[c][0] for c in n.get("patterns", []) if c in pattern_code]
                n["knowledge"] = [knowledge_code[c] for c in n.get("knowledge", []) if c in knowledge_code]
        return node

    db = connect(home / "bank.db")
    try:
        with db:
            remove(db, s)
            for i, t in enumerate(tax["topics"]):
                db.execute("INSERT INTO topics VALUES (?,?,?,?,?,?)",
                           (topic_code[t["id"]], s, i, word(t["id"]), t["name"], t["name"]))
            for p in tax["patterns"]:
                code, n = pattern_code[p["id"]]
                db.execute("INSERT INTO patterns VALUES (?,?,?,?,?,?,?)",
                           (code, topic_code[p["topic"]], n, p["name"], p.get("definition", ""), p["name"], p.get("definition", "")))
            for k in tax["knowledge"]:
                db.execute("INSERT INTO knowledge VALUES (?,?,?,?,?)",
                           (knowledge_code[k["id"]], topic_code[k["topic"]], k["name"], k["name"], k.get("definition", "")))
            parts_total = 0
            for order, q in enumerate(recipe["questions"]):
                exam = q["source"][0]["document"]
                key = q["key_source"][0]["document"] if q.get("key_source") else exam
                if exam not in years:
                    years[exam] = cover_year(path_of[exam])
                digits = re.sub(r"\D", "", str(q["label"]))
                number = int(digits) if digits else order + 1
                qid = f"{s}-{years[exam]:04d}{word(q['section'])}{word(exam)}-Q{word(q['label'])}"
                private = content[q["id"]]
                db.execute("INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                           (qid, s, years[exam], q["section"], number, q["marks"], rel[exam],
                            json.dumps(regions(q["source"], exam)), rel[key],
                            json.dumps(regions(q.get("key_source", []), key)), private["stem"], 1, 0, "compiler"))
                point = 0
                for j, part in enumerate(q["parts"]):
                    label = str(part["label"])
                    tree = remap(part["rubric"])
                    awards = [n for n in rubric.validate(tree)[0].values() if n.get("kind") == "award"]
                    db.execute("INSERT INTO parts VALUES (?,?,?,?,?,?)", (qid, label, j, part["marks"], "paper", 0))
                    for code in sorted({c for a in awards for c in a.get("patterns", [])}):
                        db.execute("INSERT INTO part_patterns VALUES (?,?,?)", (qid, label, code))
                    for n, a in enumerate(awards, 1):
                        text = private["criteria"].get(a["id"], "")
                        marks = a.get("max_marks", 1)
                        db.execute("INSERT INTO points VALUES (?,?,?,?)",
                                   (qid, label, point, text + (f" ({marks} marks)" if marks != 1 else "")
                                    + (" [teacher only]" if a.get("manual_only") else "")))
                        point += 1
                        for kind in ("patterns", "knowledge"):
                            for c in a.get(kind, []):
                                db.execute("INSERT INTO award_tags VALUES (?,?,?,?,?,?)",
                                           (qid, label, n, marks, "pattern" if kind == "patterns" else "knowledge", c))
                    db.execute("INSERT INTO rubrics VALUES (?,?,?)", (qid, label, json.dumps(tree, ensure_ascii=False)))
                    parts_total += 1
    finally:
        db.close()

    profile = {"wtf_pack": 1, "subject": s, "name": {"zh": names.get("zh") or names.get("en"), "en": names.get("en")},
               "course": names.get("en"), "order": 200,
               "topics": [{"code": word(t["id"]), "file": word(t["id"]), "zh": t["name"], "en": t["name"]}
                          for t in tax["topics"]],
               "sections": [{"code": sec["id"], "letter": word(sec["id"]).upper()[:4], "zh": sec["name"], "en": sec["name"],
                             "short": sec["id"], "minutes": [0, int(sec.get("minutes") or 0)]} for sec in course["sections"]],
               "recognise": {"title": [names.get("en")]}, "key_style": "ticks", "checker": "none",
               "sketch_words": ["sketch", "draw", "plot", "shade"], "sheets": [],
               "notes": recipe.get("notes") or {}, "skill": recipe.get("skill") or "",
               "compiler": {"pack_id": pack, "version": recipe["version"],
                                                                "recipe_hash": fingerprint}}
    folder = home / "profiles"
    folder.mkdir(exist_ok=True)
    path = folder / f"{s}.json"
    subjects.validate_profile(profile, path, "compiler")
    path.write_text(json.dumps(profile, ensure_ascii=False, indent=1), encoding="utf-8")
    return dict(subject=s, questions=len(recipe["questions"]), parts=parts_total)


def project_all(library):
    """Every active pack (e.g. after an update, when compiler/bank.db does not exist yet)."""
    return [project(library, p["pack_id"]) for p in library.list()]
