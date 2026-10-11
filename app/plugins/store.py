"""Data access. One job: queries over wace.db (read-only past papers) and generated.db (AI items)."""
import json, os, sqlite3, threading, time

SUBJECT_NAMES = {"MAM": "Mathematics Methods 数学方法", "MAS": "Mathematics Specialist 专业数学",
                 "MAA": "Mathematics Applications 数学应用"}

GEN_SCHEMA = """
CREATE TABLE IF NOT EXISTS generated (id INTEGER PRIMARY KEY, created TEXT, patterns TEXT, provider TEXT,
    model TEXT, section TEXT, marks INT, question TEXT, parts TEXT, solution TEXT, points TEXT, log TEXT,
    difficulty TEXT DEFAULT '标准', focus TEXT DEFAULT '', figure TEXT DEFAULT 'null');
CREATE TABLE IF NOT EXISTS mistakes (id INTEGER PRIMARY KEY, created TEXT, source TEXT, ref TEXT, label TEXT,
    part_marks INT, lost INT, patterns TEXT, missed TEXT, note TEXT, explain TEXT DEFAULT '',
    box INT DEFAULT 0, due TEXT DEFAULT '', UNIQUE (source, ref, label));
CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY, created TEXT, source TEXT, ref TEXT, label TEXT,
    marks INT, patterns TEXT, UNIQUE (source, ref, label));
CREATE TABLE IF NOT EXISTS exams (id INTEGER PRIMARY KEY, created TEXT, subject TEXT, section TEXT, source TEXT,
    refs TEXT, total INT, started TEXT DEFAULT '', submitted TEXT DEFAULT '');
CREATE TABLE IF NOT EXISTS workspace (ord INTEGER, kind TEXT, ref TEXT);
"""


INTERVALS = (1, 3, 7, 14, 30)


def day(offset):
    return time.strftime("%Y-%m-%d", time.localtime(time.time() + offset * 86400))


class Store:
    def __init__(self, root, lang="zh"):
        self.en = lang == "en"  # English names and method notes where translated (falls back to Chinese)
        self.db = sqlite3.connect(os.path.join(root, "wace.db"), check_same_thread=False)
        cols = {r[1] for r in self.db.execute("PRAGMA table_info(patterns)")}
        self.title = "COALESCE(NULLIF(p.title_en, ''), p.title)" if self.en and "title_en" in cols else "p.title"
        self.method = "COALESCE(NULLIF(p.method_en, ''), p.method)" if self.en and "method_en" in cols else "p.method"
        self.topic = "t.en" if self.en else "t.zh"
        self.gen = sqlite3.connect(os.path.join(root, "generated.db"), check_same_thread=False)
        self.gen.executescript(GEN_SCHEMA)
        cols = [r[1] for r in self.gen.execute("PRAGMA table_info(generated)")]
        for col, ddl in (("difficulty", "TEXT DEFAULT '标准'"), ("focus", "TEXT DEFAULT ''"),
                         ("figure", "TEXT DEFAULT 'null'")):  # older databases
            if col not in cols:
                self.gen.execute(f"ALTER TABLE generated ADD COLUMN {col} {ddl}")
        mcols = [r[1] for r in self.gen.execute("PRAGMA table_info(mistakes)")]
        for col, ddl in (("explain", "TEXT DEFAULT ''"), ("box", "INT DEFAULT 0"), ("due", "TEXT DEFAULT ''")):
            if col not in mcols:
                self.gen.execute(f"ALTER TABLE mistakes ADD COLUMN {col} {ddl}")
        self.gen.commit()
        self.lock = threading.Lock()

    def q(self, sql, *args, db=None):
        with self.lock:
            return (db or self.db).execute(sql, args).fetchall()

    # ---- knowledge tree
    def subjects(self):
        """Subjects in this bank, in the order of SUBJECT_NAMES (Methods, Specialist, Applications)."""
        order = list(SUBJECT_NAMES)
        have = [r[0] for r in self.q("SELECT DISTINCT subject FROM topics")]
        return sorted(have, key=lambda s: order.index(s) if s in order else len(order))

    def topics(self, subj):
        return self.q(f"""SELECT t.code, {self.topic}, t.en, COUNT(DISTINCT pp.qid) FROM topics t
                         LEFT JOIN patterns p ON p.topic = t.code LEFT JOIN part_patterns pp ON pp.pattern = p.code
                         WHERE t.subject = ? GROUP BY t.code ORDER BY t.ord""", subj)

    def patterns(self, topic):
        return self.q(f"""SELECT p.code, p.n, {self.title}, COUNT(DISTINCT pp.qid) FROM patterns p
                         LEFT JOIN part_patterns pp ON pp.pattern = p.code
                         WHERE p.topic = ? GROUP BY p.code ORDER BY p.n""", topic)

    def pattern(self, code):
        r = self.q(f"""SELECT p.code, p.n, {self.title}, {self.method}, {self.topic}, t.en, t.subject, t.file
                      FROM patterns p JOIN topics t ON t.code = p.topic WHERE p.code = ?""", code)[0]
        return dict(zip(("code", "n", "title", "method", "topic_zh", "topic_en", "subject", "file"), r))

    def pattern_name(self, code):
        """'MAM.D.6 优化' — code plus the short title (falls back to the bare code)."""
        r = self.q(f"SELECT {self.title} FROM patterns p WHERE code = ?", code)
        return f"{code} {r[0][0].split('★')[0].split('（')[0].strip()}" if r else code

    def past_index(self):
        """Every past question for searching: dicts with id, subject, year, section, q, marks, stem, figure (shows a
        figure), sketch (has a drawing part) and split {pattern: marks it carried}, in paper order."""
        cols = {r[1] for r in self.q("PRAGMA table_info(questions)")}
        pcols = {r[1] for r in self.q("PRAGMA table_info(parts)")}
        rows = self.q(f"""SELECT q.id, q.subject, q.year, q.section, q.q, q.marks, q.stem,
                                 {'q.figure' if 'figure' in cols else '0'},
                                 (SELECT MAX({'p.sketch' if 'sketch' in pcols else '0'}) FROM parts p WHERE p.qid = q.id)
                          FROM questions q ORDER BY q.subject, q.year DESC, q.section DESC, q.q""")
        split = {}
        for qid, pattern, marks in self.q("SELECT qid, pattern, marks FROM pattern_marks"):
            split.setdefault(qid, {})[pattern] = round(marks)
        keys = ("id", "subject", "year", "section", "q", "marks", "stem", "figure", "sketch")
        return [dict(zip(keys, r), split=split.get(r[0], {})) for r in rows]

    # ---- 工作区: an ordered basket of questions, [("past", qid) | ("gen", gid as str)], kept across restarts
    def workspace(self):
        return [(kind, ref) for kind, ref in self.q("SELECT kind, ref FROM workspace ORDER BY ord", db=self.gen)]

    def save_workspace(self, items):
        with self.lock:
            self.gen.execute("DELETE FROM workspace")
            self.gen.executemany("INSERT INTO workspace VALUES (?,?,?)",
                                 [(i, kind, str(ref)) for i, (kind, ref) in enumerate(items)])
            self.gen.commit()

    def item_info(self, kind, ref):
        """A workspace row: dict(subject, section, marks, patterns, label) for a past or an AI question (None if
        it no longer exists)."""
        if kind == "past":
            r = self.q("SELECT subject, year, section, q, marks FROM questions WHERE id = ?", ref)
            if not r:
                return None
            subj, year, sec, q, marks = r[0]
            pats = [p for (p,) in self.q("SELECT DISTINCT pattern FROM part_patterns WHERE qid = ?", ref)]
            return dict(subject=subj, section=sec, marks=marks, patterns=pats,
                        label=f"{year} {'CF' if sec == 'CalcFree' else 'CA'} Q{q}")
        r = self.q("SELECT patterns, section, marks FROM generated WHERE id = ?", int(ref), db=self.gen)
        if not r:
            return None
        pats = json.loads(r[0][0])
        return dict(subject=pats[0].split(".")[0] if pats else "", section=r[0][1] or "", marks=r[0][2],
                    patterns=pats, label=f"AI #{ref}")

    def paper_totals(self, subj, since=2020):
        """{section: marks of a real paper} — the median over recent years (what a full CF / CA paper is worth)."""
        out = {}
        for sec in ("CalcFree", "CalcAssumed"):
            totals = sorted(t for (t,) in self.q("""SELECT SUM(marks) FROM questions WHERE subject = ? AND
                                                    section = ? AND year >= ? GROUP BY year""", subj, sec, since))
            if totals:
                out[sec] = totals[len(totals) // 2]
        return out

    def related(self, code, top=5, least=2):
        """Patterns that share past questions with `code`: (its question count, [(pattern, shared), …]) — only
        pairs seen in at least `least` questions (one shared question is a coincidence), strongest first."""
        if not hasattr(self, "_index"):
            self._index = self.past_index()
        with_code = [r for r in self._index if code in r["split"]]
        together = {}
        for r in with_code:
            for p in r["split"]:
                if p != code:
                    together[p] = together.get(p, 0) + 1
        best = sorted(((n, p) for p, n in together.items() if n >= least), key=lambda x: (-x[0], x[1]))[:top]
        return len(with_code), [(p, n) for n, p in best]

    def topic_name(self, code):
        """'MAM.D 微分及其应用' — the unit's code plus its name (falls back to the bare code)."""
        r = self.q(f"SELECT {self.topic} FROM topics t WHERE code = ?", code)
        return f"{code} {r[0][0]}" if r else code

    def questions_for(self, code):
        """Past questions with at least one part tagged `code`, newest first; labels = matching parts."""
        return self.q("""SELECT q.id, q.year, q.section, q.q, q.marks, GROUP_CONCAT(pp.label, ',')
                         FROM part_patterns pp JOIN questions q ON q.id = pp.qid WHERE pp.pattern = ?
                         GROUP BY q.id ORDER BY q.year DESC, q.section = 'CalcFree' DESC, q.q""", code)

    # ---- one past question
    def question(self, qid):
        cols = ("id", "subject", "year", "section", "q", "marks", "exam", "exam_regions", "key", "key_regions",
                "stem", "points_ok")
        d = dict(zip(cols, self.q("SELECT * FROM questions WHERE id = ?", qid)[0]))
        d["exam_regions"], d["key_regions"] = json.loads(d["exam_regions"]), json.loads(d["key_regions"])
        d["parts"] = [(label, marks, [r[0] for r in self.q(
            "SELECT pattern FROM part_patterns WHERE qid = ? AND label = ?", qid, label)])
            for label, marks in self.q("SELECT label, marks FROM parts WHERE qid = ? ORDER BY ord", qid)]
        d["points"] = self.q("SELECT label, text FROM points WHERE qid = ? ORDER BY ord", qid)
        return d

    def example_pool(self, codes):
        """Every past question using any of the patterns: [(qid, year, section, how many of them it uses)]."""
        marks = ",".join("?" * len(codes))
        return self.q(f"""SELECT q.id, q.year, q.section, COUNT(DISTINCT pp.pattern) FROM questions q
                          JOIN part_patterns pp ON pp.qid = q.id WHERE pp.pattern IN ({marks}) GROUP BY q.id""",
                      *codes)

    # ---- generated items
    def save_generated(self, item):
        cols = ("created", "patterns", "provider", "model", "section", "marks", "question", "parts", "solution",
                "points", "log", "difficulty", "focus", "figure")
        row = dict(item, created=time.strftime("%Y-%m-%d %H:%M"))
        row.setdefault("difficulty", "标准")
        row.setdefault("figure", None)
        row["focus"] = row.get("focus") or ""
        vals = [row[c] if isinstance(row[c], (str, int)) else json.dumps(row[c], ensure_ascii=False) for c in cols]
        with self.lock:
            cur = self.gen.execute(f"INSERT INTO generated ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                                   vals)
            self.gen.commit()
        return cur.lastrowid

    def generated_for(self, code):
        return self.q("SELECT id, created, marks, difficulty FROM generated WHERE patterns LIKE ? ORDER BY id DESC",
                      f'%"{code}"%', db=self.gen)

    def generated_all(self):
        """Every AI item, newest first: (id, created, [patterns], section, marks, provider, model, question,
        difficulty, focus)."""
        rows = self.q("""SELECT id, created, patterns, section, marks, provider, model, question, difficulty, focus
                         FROM generated ORDER BY id DESC""", db=self.gen)
        return [(r[0], r[1], json.loads(r[2]), *r[3:]) for r in rows]

    def generated_stems(self, codes, n=8, length=240):
        """Openings of the newest AI questions sharing a pattern with `codes` (so new ones avoid repeating them)."""
        out = []
        for r in self.generated_all():
            if set(r[2]) & set(codes):
                out.append(" ".join(r[7].split())[:length])
                if len(out) == n:
                    break
        return out

    # ---- self-marking: mistakes (one row per sub-question; marking it again replaces the row)
    def save_mistake(self, source, ref, label, part_marks, lost, patterns, missed, note=""):
        with self.lock:
            self.gen.execute("""INSERT INTO mistakes (created, source, ref, label, part_marks, lost, patterns, missed, note)
                                VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT (source, ref, label) DO UPDATE SET
                                created=excluded.created, part_marks=excluded.part_marks, lost=excluded.lost,
                                patterns=excluded.patterns, missed=excluded.missed, note=excluded.note,
                                explain='', box=0, due=excluded.due""",
                             (time.strftime("%Y-%m-%d %H:%M"), source, str(ref), label, part_marks, lost,
                              json.dumps(patterns), json.dumps(missed, ensure_ascii=False), note))
            self.gen.execute("UPDATE mistakes SET due = ? WHERE source=? AND ref=? AND label=?",
                             (day(1), source, str(ref), label))
            self.gen.commit()
        self.record_attempt(source, ref, [(label, part_marks, patterns)])  # a marked part was attempted

    # ---- spaced review (Leitner boxes): review again after 1, 3, 7, 14, 30 days; passing the last box = mastered
    def review(self, mistake_id, passed):
        m = next(x for x in self.mistakes() if x["id"] == mistake_id)
        box = m["box"] + 1 if passed else 0
        due = "" if box >= len(INTERVALS) else day(INTERVALS[box])
        with self.lock:
            self.gen.execute("UPDATE mistakes SET box = ?, due = ? WHERE id = ?", (box, due, mistake_id))
            self.gen.commit()
        return box, due

    def due_mistakes(self):
        today = day(0)
        return [m for m in self.mistakes() if m["due"] and m["due"] <= today]

    # ---- attempts (a part whose answer the student revealed counts as attempted) and mastery
    def record_attempt(self, source, ref, parts):
        with self.lock:
            for label, marks, patterns in parts:
                self.gen.execute("""INSERT INTO attempts (created, source, ref, label, marks, patterns)
                                    VALUES (?,?,?,?,?,?) ON CONFLICT (source, ref, label) DO NOTHING""",
                                 (time.strftime("%Y-%m-%d %H:%M"), source, str(ref), label, marks or 0,
                                  json.dumps(patterns)))
            self.gen.commit()

    def mastery(self):
        """{pattern: {"attempted": marks, "lost": marks, "parts": n}} over everything the student has revealed."""
        out = {}
        for marks, pats in self.gen.execute("SELECT marks, patterns FROM attempts").fetchall():
            for c in json.loads(pats):
                g = out.setdefault(c, {"attempted": 0, "lost": 0, "parts": 0})
                g["attempted"] += marks or 0
                g["parts"] += 1
        for m in self.mistakes():
            for c in m["patterns"]:
                out.setdefault(c, {"attempted": 0, "lost": 0, "parts": 0})["lost"] += m["lost"]
        return out

    def exam_weights(self, subj):
        """Marks each pattern carried across all past papers of a subject (how much it matters)."""
        return dict(self.q("SELECT pattern, SUM(marks) FROM pattern_marks WHERE subject = ? GROUP BY pattern", subj))

    def pattern_marks(self, code):
        """{section: sorted marks the pattern carried in each real question of that section} (as printed)."""
        out = {}
        for sec, m in self.q("SELECT section, marks FROM pattern_marks WHERE pattern = ? ORDER BY marks", code):
            out.setdefault(sec, []).append(m)
        return out

    def set_explanation(self, mistake_id, text):
        with self.lock:
            self.gen.execute("UPDATE mistakes SET explain = ? WHERE id = ?", (text, mistake_id))
            self.gen.commit()

    def delete_mistake(self, source, ref, label):
        with self.lock:
            self.gen.execute("DELETE FROM mistakes WHERE source=? AND ref=? AND label=?", (source, str(ref), label))
            self.gen.commit()

    def mistakes(self):
        """-> list of dicts, newest first."""
        cur = self.gen.execute("SELECT * FROM mistakes ORDER BY id DESC")
        names = [c[0] for c in cur.description]
        out = [dict(zip(names, r)) for r in cur.fetchall()]
        for d in out:
            d["patterns"], d["missed"] = json.loads(d["patterns"]), json.loads(d["missed"])
        return out

    def mistake(self, source, ref, label):
        return next((m for m in self.mistakes() if (m["source"], m["ref"], m["label"]) == (source, str(ref), label)),
                    None)

    # ---- mock exams: refs = [["past", qid] | ["gen", id], …]; score = total − marks lost on them since start
    def paper(self, subj, year, section):
        return self.q("SELECT id, marks FROM questions WHERE subject = ? AND year = ? AND section = ? ORDER BY q",
                      subj, int(year), section)

    def save_exam(self, subject, section, source, refs, total):
        with self.lock:
            cur = self.gen.execute("INSERT INTO exams (created, subject, section, source, refs, total) "
                                   "VALUES (?,?,?,?,?,?)", (time.strftime("%Y-%m-%d %H:%M"), subject, section,
                                                            source, json.dumps(refs), total))
            self.gen.commit()
        return cur.lastrowid

    def update_exam(self, eid, **fields):
        with self.lock:
            for col, val in fields.items():
                if col in ("started", "submitted"):
                    self.gen.execute(f"UPDATE exams SET {col} = ? WHERE id = ?", (val, eid))
            self.gen.commit()

    def exams(self):
        cur = self.gen.execute("SELECT * FROM exams ORDER BY id DESC")
        names = [c[0] for c in cur.description]
        out = [dict(zip(names, r)) for r in cur.fetchall()]
        for e in out:
            e["refs"] = json.loads(e["refs"])
            e["lost"] = self.exam_lost(e)
        return out

    def exam(self, eid):
        return next(e for e in self.exams() if e["id"] == eid)

    def exam_lost(self, e):
        refs = {(s, str(r)) for s, r in e["refs"]}
        since = e.get("started") or e["created"]
        return sum(m["lost"] for m in self.mistakes() if (m["source"], m["ref"]) in refs and m["created"] >= since)

    def generated(self, gid):
        cur = self.gen.execute("SELECT * FROM generated WHERE id = ?", (gid,))
        d = dict(zip([c[0] for c in cur.description], cur.fetchone()))
        for c in ("patterns", "parts", "points", "log", "figure"):
            d[c] = json.loads(d[c])
        return d


def setup(k):
    k.provide("store", Store(k.root, k.get("config").get("language", "zh")))
