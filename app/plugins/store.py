"""Data access. One job: queries over wace.db (read-only past papers) and generated.db (AI items)."""
import json, os, sqlite3, threading, time

GEN_SCHEMA = """
CREATE TABLE IF NOT EXISTS generated (id INTEGER PRIMARY KEY, created TEXT, patterns TEXT, provider TEXT,
    model TEXT, section TEXT, marks INT, question TEXT, parts TEXT, solution TEXT, points TEXT, log TEXT);
"""


class Store:
    def __init__(self, root):
        self.db = sqlite3.connect(os.path.join(root, "wace.db"), check_same_thread=False)
        self.gen = sqlite3.connect(os.path.join(root, "generated.db"), check_same_thread=False)
        self.gen.executescript(GEN_SCHEMA)
        self.lock = threading.Lock()

    def q(self, sql, *args, db=None):
        with self.lock:
            return (db or self.db).execute(sql, args).fetchall()

    # ---- knowledge tree
    def subjects(self):
        return [r[0] for r in self.q("SELECT DISTINCT subject FROM topics ORDER BY subject")]

    def topics(self, subj):
        return self.q("""SELECT t.code, t.zh, t.en, COUNT(DISTINCT pp.qid) FROM topics t
                         LEFT JOIN patterns p ON p.topic = t.code LEFT JOIN part_patterns pp ON pp.pattern = p.code
                         WHERE t.subject = ? GROUP BY t.code ORDER BY t.ord""", subj)

    def patterns(self, topic):
        return self.q("""SELECT p.code, p.n, p.title, COUNT(DISTINCT pp.qid) FROM patterns p
                         LEFT JOIN part_patterns pp ON pp.pattern = p.code
                         WHERE p.topic = ? GROUP BY p.code ORDER BY p.n""", topic)

    def pattern(self, code):
        r = self.q("""SELECT p.code, p.n, p.title, p.method, t.zh, t.en, t.subject, t.file
                      FROM patterns p JOIN topics t ON t.code = p.topic WHERE p.code = ?""", code)[0]
        return dict(zip(("code", "n", "title", "method", "topic_zh", "topic_en", "subject", "file"), r))

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

    def examples(self, codes, n=3):
        """Most recent past questions covering the patterns (verified mark points preferred)."""
        marks = ",".join("?" * len(codes))
        ids = [r[0] for r in self.q(f"""SELECT q.id FROM questions q JOIN part_patterns pp ON pp.qid = q.id
                   WHERE pp.pattern IN ({marks}) GROUP BY q.id
                   ORDER BY COUNT(DISTINCT pp.pattern) DESC, q.points_ok DESC, q.year DESC LIMIT ?""", *codes, n)]
        return [self.question(i) for i in ids]

    # ---- generated items
    def save_generated(self, item):
        cols = ("created", "patterns", "provider", "model", "section", "marks", "question", "parts", "solution",
                "points", "log")
        row = dict(item, created=time.strftime("%Y-%m-%d %H:%M"))
        vals = [row[c] if isinstance(row[c], (str, int)) else json.dumps(row[c], ensure_ascii=False) for c in cols]
        with self.lock:
            cur = self.gen.execute(f"INSERT INTO generated ({','.join(cols)}) VALUES ({','.join('?' * len(cols))})",
                                   vals)
            self.gen.commit()
        return cur.lastrowid

    def generated_for(self, code):
        return self.q("SELECT id, created, marks FROM generated WHERE patterns LIKE ? ORDER BY id DESC",
                      f'%"{code}"%', db=self.gen)

    def generated(self, gid):
        cur = self.gen.execute("SELECT * FROM generated WHERE id = ?", (gid,))
        d = dict(zip([c[0] for c in cur.description], cur.fetchone()))
        for c in ("patterns", "parts", "points", "log"):
            d[c] = json.loads(d[c])
        return d


def setup(k):
    k.provide("store", Store(k.root))
