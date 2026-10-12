"""Build the indexable subject database. One job: sources -> wace.db (SQLite).

Sources (all under ROOT):
  <subj>/questions.json          question crops (exam + marking-key regions) and stem text
  tools/parttags_<subj>.txt      per-part (sub-question) topic+pattern tags
  <subj>/methods/*_解题思路.md    pattern titles + method text ("## 题型 N：...")
  marking-key PDFs               split into one row per mark (tools/markpoints.py)
  "(n marks)" in the stems       marks of every part as printed on the paper (tools/partmarks.py); the key's
                                 tick count per part is the fallback and the cross-check
  stems + exam crops             questions.figure (the question shows a graph / diagram / axes) and parts.sketch
                                 (the part asks the student to sketch, draw, plot, shade or mark on a diagram)

Question-level topics/patterns are the union of its part tags (view q_patterns). View pattern_marks maps every
real question to the marks each pattern carried in it (parts with several patterns share their marks evenly).
"""
import json, os, re, sqlite3, sys
import pymupdf

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from build_docs import TOPICS  # noqa: E402
from handlers import key_parser  # noqa: E402
from partmarks import for_tags, has_figure, is_sketch, split, tagged_texts, texts  # noqa: E402

import subjects as subject_registry
SCHEMA = """
CREATE TABLE topics   (code TEXT PRIMARY KEY, subject TEXT, ord INT, file TEXT, zh TEXT, en TEXT);
CREATE TABLE patterns (code TEXT PRIMARY KEY, topic TEXT, n INT, title TEXT, method TEXT,
                       title_en TEXT DEFAULT '', method_en TEXT DEFAULT '');
CREATE TABLE questions(id TEXT PRIMARY KEY, subject TEXT, year INT, section TEXT, q INT, marks INT,
                       exam TEXT, exam_regions TEXT, key TEXT, key_regions TEXT, stem TEXT, points_ok INT,
                       figure INT);
CREATE TABLE parts    (qid TEXT, label TEXT, ord INT, marks INT, marks_src TEXT, sketch INT,
                       PRIMARY KEY (qid, label));
CREATE TABLE part_patterns (qid TEXT, label TEXT, pattern TEXT);
CREATE TABLE points   (qid TEXT, label TEXT, ord INT, text TEXT);
CREATE TABLE knowledge (code TEXT PRIMARY KEY, topic TEXT, name_en TEXT, name_zh TEXT, definition TEXT);
CREATE TABLE award_tags (qid TEXT, label TEXT, n INT, marks REAL, kind TEXT, code TEXT);
CREATE VIEW q_patterns AS SELECT DISTINCT qid, pattern FROM part_patterns;
CREATE VIEW pattern_marks AS
  SELECT q.id AS qid, q.subject, q.section, q.year, q.marks AS question_marks, pp.pattern,
         rtrim(rtrim(pp.pattern, '0123456789'), '.') AS topic,
         SUM(p.marks * 1.0 / (SELECT COUNT(*) FROM part_patterns x WHERE x.qid = pp.qid AND x.label = pp.label))
           AS marks
  FROM part_patterns pp JOIN parts p ON p.qid = pp.qid AND p.label = pp.label JOIN questions q ON q.id = pp.qid
  WHERE p.marks IS NOT NULL GROUP BY q.id, pp.pattern;
CREATE INDEX pp_pattern ON part_patterns(pattern);
CREATE INDEX pt_qid ON points(qid);
CREATE INDEX at_code ON award_tags(code);
"""
HEAD = re.compile(r"^## (?:题型|Pattern)\s*(\d+)\s*[：:]\s*(.+)$")


def images_in(doc, regions):
    """Does the exam crop contain an embedded picture (how the 2016 and 2024-25 papers ship their diagrams)?"""
    for pg, y0, y1 in regions:
        clip = pymupdf.Rect(0, y0, doc[pg].rect.width, y1)
        if any(pymupdf.Rect(i["bbox"]).intersects(clip) for i in doc[pg].get_image_info()):
            return True
    return False


def method_sections(md_path):
    """'## 题型 N：title' blocks -> {N: (title, text)}."""
    out, cur = {}, None
    for line in open(md_path, encoding="utf-8").read().splitlines():
        m = HEAD.match(line)
        if m:
            cur = int(m.group(1))
            out[cur] = [m.group(2).strip(), []]
        elif line.startswith("## "):
            cur = None
        elif cur is not None:
            out[cur][1].append(line)
    return {n: (t, "\n".join(b).strip()) for n, (t, b) in out.items()}


def read_parttags(subj):
    """-> {(yearsec, q): [(label, [pattern codes])]} with codes like 'MAM.D.6'."""
    out = {}
    for line in open(os.path.join(ROOT, "tools", f"parttags_{subj}.txt"), encoding="utf-8"):
        line = line.split("#")[0].split()
        if not line:
            continue
        ys, q, rest = line[0], int(line[1]), line[2:]
        parts = []
        for tok in rest:
            label, codes = tok.split("=")
            pats = []
            for c in codes.split("+"):
                m = re.fullmatch(r"([A-Z]+)(\d+)", c)
                pats.append(f"{subj}.{m.group(1)}.{m.group(2)}")
            parts.append(("" if label == "-" else label, pats))
        out[(ys, q)] = parts
    return out


def key_text(doc, regs):
    return "\n".join(doc[p].get_text("text", clip=pymupdf.Rect(20, y0, 575, y1)) for p, y0, y1 in regs)


def award_level(db, subj, docs):
    """tools/marktags_<S>.json (pack flow) -> knowledge + award_tags rows, for the questions whose awards this build
    numbers exactly as the pack did (marktags.py fingerprints). Subjects without the file get no rows."""
    path = os.path.join(ROOT, "tools", f"marktags_{subj}.json")
    if not os.path.isfile(path):
        return []
    import awards, marktags  # awards.py imports this module: import it late
    with open(path, encoding="utf-8") as f:
        tags = json.load(f)
    with open(os.path.join(ROOT, "tools", f"catalogue_{subj}.json"), encoding="utf-8") as f:
        cat = json.load(f)
    try:
        marktags.validate_marktags(tags, cat, subj)
    except ValueError as e:
        return [f"{subj}: marktags not used: {e}"]
    for a in cat["knowledge"]:
        db.execute("INSERT INTO knowledge VALUES (?,?,?,?,?)", (marktags.db_code(subj, a["id"]),
                   f"{subj}.{a['id'].split('.')[0]}", a["name_en"], a.get("name_zh", ""), a.get("definition", "")))
    parse, splits, problems = key_parser(subject_registry.info(subj)), awards.splits(subj), []
    for q in json.load(open(os.path.join(ROOT, subj, "questions.json"), encoding="utf-8")):
        if not q["year"].isdigit():
            continue
        qid = f"{subj}-{q['year']}{subject_registry.section_letter(subj, q['section'])}-Q{q['q']}"
        rows, problem = marktags.rows(subj, qid, awards.question(subj, q, parse, docs, splits), tags)
        db.executemany("INSERT INTO award_tags VALUES (?,?,?,?,?,?)", rows)
        problems += [problem] if problem else []
    return problems


def build(db_path, subjects=None):
    """Everything -> a fresh wace.db for `subjects` (default: every subject build_docs knows)."""
    if os.path.exists(db_path):
        os.remove(db_path)
    db = sqlite3.connect(db_path)
    db.executescript(SCHEMA)
    problems = []
    for subj, topics in TOPICS.items():
        if subjects is not None and subj not in subjects:
            continue
        for i, (letter, (fname, zh, en)) in enumerate(topics.items()):
            tcode = f"{subj}.{letter}"
            db.execute("INSERT INTO topics VALUES (?,?,?,?,?,?)", (tcode, subj, i, fname, zh, en))
            md = os.path.join(ROOT, subj, "methods", f"{fname}_解题思路.md")
            md_en = os.path.join(ROOT, subj, "methods_en", f"{fname}_Methods.md")  # tools/translate.py docs
            english = method_sections(md_en) if os.path.exists(md_en) else {}
            for n, (title, text) in method_sections(md).items():
                title_en, text_en = english.get(n, ("", ""))
                db.execute("INSERT INTO patterns VALUES (?,?,?,?,?,?,?)",
                           (f"{tcode}.{n}", tcode, n, title, text, title_en, text_en))
            if english and set(english) != set(method_sections(md)):
                problems.append(f"{subj} {fname}: English notes have patterns {sorted(english)}")
        known = {r[0] for r in db.execute("SELECT code FROM patterns WHERE topic LIKE ?", (subj + ".%",))}
        tags = read_parttags(subj)
        docs = {}
        for q in json.load(open(os.path.join(ROOT, subj, "questions.json"), encoding="utf-8")):
            if not q["year"].isdigit():
                continue  # 2016 Sample papers are excluded
            ys = q["year"] + subject_registry.section_letter(subj, q["section"])
            qid = f"{subj}-{ys}-Q{q['q']}"
            parts = tags.pop((ys, q["q"]), None)
            if parts is None:
                problems.append(f"{qid}: no part tags")
                parts = []
            if q["key"] not in docs:
                docs[q["key"]] = pymupdf.open(os.path.join(ROOT, q["key"]))
            if "answer" in q:  # multiple choice (tools/segment_mc.py): the key's answer is the one mark
                pts, printed = [["", f"Answer: {q['answer']}"]], None  # options (a)–(d) are not parts
            else:
                pts = key_parser(subject_registry.info(subj))(key_text(docs[q["key"]], q["key_regions"]))
                printed = split(q["text"], q["marks"])
            paper = for_tags(printed, [l for l, _ in parts]) if printed else None
            # one tick per mark, and per part as printed: a key whose text runs out of order (MAA 2021 CA Q9) would
            # otherwise hang its marks on the wrong parts; such keys are shown as the original image instead
            ok = int(len(pts) == q["marks"])
            if ok and paper and any(sum(1 for p in pts if p[0] == l) != m for l, m in paper.items()):
                ok = 0
                problems.append(f"{qid}: key ticks per part differ from the printed part marks (key shown as image)")
            if q["exam"] not in docs:
                docs[q["exam"]] = pymupdf.open(os.path.join(ROOT, q["exam"]))
            figure = int(has_figure(q["text"]) or images_in(docs[q["exam"]], q["exam_regions"]))
            db.execute("INSERT INTO questions VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                       (qid, subj, int(q["year"]), q["section"], q["q"], q["marks"], q["exam"],
                        json.dumps(q["exam_regions"]), q["key"], json.dumps(q["key_regions"]), q["text"], ok, figure))
            for j, (label, text) in enumerate(pts):
                db.execute("INSERT INTO points VALUES (?,?,?,?)", (qid, label, j, text.strip()))
            if printed and not paper:
                problems.append(f"{qid}: paper has parts {sorted(printed)}, tags have {[l for l, _ in parts]}")
            part_text = tagged_texts(texts(q["text"]), [l for l, _ in parts])
            for j, (label, pats) in enumerate(parts):
                ticks = sum(1 for p in pts if p[0] == label) if ok else None
                if paper and ticks is not None and ticks != paper[label]:
                    problems.append(f"{qid} ({label}): paper says {paper[label]} marks, key has {ticks} ticks")
                n, src = (paper[label], "paper") if paper else (ticks, "key") if ticks is not None else (None, None)
                db.execute("INSERT INTO parts VALUES (?,?,?,?,?,?)",
                           (qid, label, j, n, src, int(is_sketch(part_text[label], subj))))
                for p in pats:
                    if p not in known:
                        problems.append(f"{qid} {label}: unknown pattern {p}")
                    db.execute("INSERT INTO part_patterns VALUES (?,?,?)", (qid, label, p))
            if ok and parts and {p[0] for p in pts} != {l for l, _ in parts}:
                problems.append(f"{qid}: part labels tags={[l for l, _ in parts]} key={sorted({p[0] for p in pts})}")
        problems += [f"{subj} {k}: tag line has no question" for k in tags]
        problems += award_level(db, subj, docs)
    db.commit()
    return db, problems


if __name__ == "__main__":
    db, problems = build(os.path.join(ROOT, "wace.db"))
    for t in ("questions", "parts", "part_patterns", "points", "patterns"):
        print(t, db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0])
    print("points_ok", db.execute("SELECT SUM(points_ok), COUNT(*) FROM questions").fetchone())
    print("part marks by source", db.execute("SELECT marks_src, COUNT(*) FROM parts GROUP BY marks_src").fetchall())
    print("questions with a figure", db.execute("SELECT SUM(figure) FROM questions").fetchone()[0],
          "| parts asking for a drawing", db.execute("SELECT SUM(sketch) FROM parts").fetchone()[0])
    print(len(problems), "problems")
    print("\n".join(problems))
