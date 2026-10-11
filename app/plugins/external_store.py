"""Independent external-paper database and private PDF assets. No writes to the SCSA or generated stores."""
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import threading
import uuid
from plugins.store import SUBJECT_NAMES

SCHEMA = """
CREATE TABLE IF NOT EXISTS papers (
    id TEXT PRIMARY KEY, title TEXT NOT NULL, source TEXT NOT NULL, subject TEXT NOT NULL,
    section TEXT NOT NULL, exam TEXT NOT NULL, answer TEXT NOT NULL, digest TEXT NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY, paper TEXT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
    label TEXT NOT NULL, marks INTEGER, exam_regions TEXT NOT NULL, answer_regions TEXT NOT NULL,
    stem TEXT NOT NULL, tags TEXT NOT NULL, confirmed INTEGER NOT NULL DEFAULT 0,
    answer_text TEXT NOT NULL DEFAULT '', tag_note TEXT NOT NULL DEFAULT '',
    UNIQUE(paper, label));
"""


class ExternalStore:
    def __init__(self, root, pdf, patterns):
        self.root, self.pdf, self.patterns = Path(root), pdf, patterns
        self.lock = threading.RLock()
        self.db = sqlite3.connect(self.root / "external.db", check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA)

    def asset(self, relative):
        path = (self.root / relative).resolve()
        if not path.is_relative_to((self.root / "external").resolve()):
            raise ValueError("外源文件路径无效")
        return str(path)

    def papers(self):
        with self.lock:
            return [dict(r) for r in self.db.execute("SELECT p.*, COUNT(q.id) AS count FROM papers p "
                    "LEFT JOIN questions q ON q.paper=p.id GROUP BY p.id ORDER BY p.rowid DESC")]

    def paper(self, paper_id):
        with self.lock:
            row = self.db.execute("SELECT * FROM papers WHERE id=?", (paper_id,)).fetchone()
            if row is None:
                raise ValueError("外源试卷不存在")
            return dict(row)

    def import_pair(self, exam, answer, title, source, subject, section):
        title, source = title.strip(), source.strip()
        if not title or not source:
            raise ValueError("请填写试卷名称和来源")
        if subject not in SUBJECT_NAMES or section not in ("CalcFree", "CalcAssumed"):
            raise ValueError("科目或卷型无效")
        if Path(exam).resolve() == Path(answer).resolve():
            raise ValueError("试卷和答案必须是不同的文件")
        for path in (exam, answer):
            self.pdf("inspect")(path)
        digest = hashlib.sha256(Path(exam).read_bytes()).hexdigest() + hashlib.sha256(Path(answer).read_bytes()).hexdigest()
        paper_id = uuid.uuid4().hex
        folder = self.root / "external" / paper_id
        with self.lock:
            if self.db.execute("SELECT id FROM papers WHERE digest=?", (digest,)).fetchone():
                raise ValueError("这对试卷与答案已导入")
            folder.mkdir(parents=True)
            try:
                for path, name in ((exam, "exam.pdf"), (answer, "answer.pdf")):
                    shutil.copyfile(path, folder / name)
                ex, ans = (f"external/{paper_id}/{name}.pdf" for name in ("exam", "answer"))
                with self.db:
                    self.db.execute("INSERT INTO papers VALUES (?,?,?,?,?,?,?,?)",
                                    (paper_id, title, source, subject, section, ex, ans, digest))
                    answer_crops = {q["label"]: q["regions"] for q in self.pdf("suggest")(self.asset(ans))}
                    for q in self.pdf("suggest")(self.asset(ex)):
                        self.db.execute("INSERT INTO questions (paper,label,marks,exam_regions,answer_regions,stem,tags) "
                            "VALUES (?,?,?,?,?,?,?)", (paper_id, q["label"], q["marks"], json.dumps(q["regions"]),
                            json.dumps(answer_crops.get(q["label"], [])), self.pdf("text")(self.asset(ex), q["regions"]), "[]"))
            except Exception:
                if folder.resolve().is_relative_to((self.root / "external").resolve()):
                    shutil.rmtree(folder)
                raise
        return paper_id

    def question(self, qid):
        with self.lock:
            row = self.db.execute("SELECT q.*, p.title,p.source,p.subject,p.section,p.exam,p.answer FROM questions q "
                                  "JOIN papers p ON p.id=q.paper WHERE q.id=?", (qid,)).fetchone()
            if row is None:
                raise ValueError("外源题目不存在")
            d = dict(row)
            for name in ("exam_regions", "answer_regions", "tags"):
                d[name] = json.loads(d[name])
            return d

    def save_question(self, paper_id, label, marks, exam_regions, answer_regions, tags, confirmed=False,
                      qid=None, stem=None, answer_text="", tag_note=""):
        """Manual edits never become confirmed without paired crops, marks and valid same-subject tags."""
        paper = self.paper(paper_id)
        label = label.strip()
        if not label:
            raise ValueError("请填写题号或小问")
        if marks is not None and (type(marks) is not int or marks <= 0):
            raise ValueError("分值必须是正整数")
        tags = sorted(set(tags))
        allowed = set(self.patterns(paper["subject"]))
        if any(tag not in allowed for tag in tags):
            raise ValueError("题型必须属于该科目的已有题型")
        ex = self.pdf("validate")(self.asset(paper["exam"]), exam_regions)
        ans = self.pdf("validate")(self.asset(paper["answer"]), answer_regions)
        if not ex or (confirmed and (not ans or not marks or not tags)):
            raise ValueError("确认前需配齐题目切块、答案切块、分值和题型")
        stem = self.pdf("text")(self.asset(paper["exam"]), ex) if stem is None else stem.strip()
        with self.lock, self.db:
            if qid is not None:
                previous = self.question(qid)
                if previous["paper"] != paper_id:
                    raise ValueError("外源题目不存在")
                changed = (previous["exam_regions"] != ex or previous["answer_regions"] != ans
                           or previous["stem"] != stem or previous["answer_text"] != answer_text.strip()
                           or previous["tags"] != tags)
                if changed and tag_note == previous["tag_note"]:
                    tag_note = ""  # a reason based on old evidence must not look current
            fields = (label, marks, json.dumps(ex), json.dumps(ans), stem, json.dumps(tags), int(confirmed), answer_text.strip(), tag_note)
            try:
                if qid is None:
                    cur = self.db.execute("INSERT INTO questions (label,marks,exam_regions,answer_regions,stem,tags,confirmed,answer_text,tag_note,paper) "
                                          "VALUES (?,?,?,?,?,?,?,?,?,?)", (*fields, paper_id))
                    qid = cur.lastrowid
                else:
                    cur = self.db.execute("UPDATE questions SET label=?,marks=?,exam_regions=?,answer_regions=?,stem=?,tags=?,confirmed=?,answer_text=?,tag_note=? "
                                          "WHERE id=? AND paper=?", (*fields, qid, paper_id))
                    if not cur.rowcount:
                        raise ValueError("外源题目不存在")
            except sqlite3.IntegrityError as exc:
                raise ValueError("此试卷中已有同名题号或小问") from exc
        return qid

    def save_proposal(self, qid, proposal, expected):
        with self.lock:
            current = self.question(qid)
            if current != expected:
                raise ValueError("标注期间题目已修改，请重新标注")
            if current["confirmed"]:
                raise ValueError("已确认的标注不能自动覆盖")
            allowed = set(self.patterns(current["subject"]))
            if any(tag not in allowed for tag in proposal["tags"]):
                raise ValueError("题型必须属于该科目的已有题型")
            note = ("? " if proposal["uncertain"] else "") + proposal["reason"]
            with self.db:
                self.db.execute("UPDATE questions SET tags=?,tag_note=?,confirmed=0 WHERE id=?",
                                (json.dumps(proposal["tags"]), note, qid))

    def search(self, subject="", section="", words="", tags=(), paper="", confirmed=False):
        with self.lock:
            ids = [r[0] for r in self.db.execute("SELECT q.id FROM questions q JOIN papers p ON p.id=q.paper "
                "WHERE (?='' OR p.subject=?) AND (?='' OR p.section=?) AND (?='' OR q.paper=?) "
                "AND (?=0 OR q.confirmed=1) ORDER BY p.rowid DESC,q.id", (subject, subject, section, section, paper, paper, int(confirmed)))]
            rows = [self.question(qid) for qid in ids]
        out = []
        for row in rows:
            haystack = " ".join(str(row[name]) for name in ("title", "source", "label", "stem")).casefold()
            if words.strip().casefold() in haystack and all(t in row["tags"] or any(p.startswith(t + ".") for p in row["tags"]) for t in tags):
                out.append(row)
        return out

    def delete_question(self, qid):
        with self.lock, self.db:
            self.db.execute("DELETE FROM questions WHERE id=?", (qid,))

    def close(self):
        self.db.close()


def setup(k):
    state = []  # lazy: merely launching WTF does not create or modify an external library
    init_lock = threading.Lock()

    def get_store():
        with init_lock:
            if not state:
                state.append(ExternalStore(k.root, lambda name: k.get("external.pdf." + name),
                    lambda subject: [p[0] for p in k.get("store").q("SELECT code FROM patterns WHERE code LIKE ?", subject + ".%")]))
        return state[0]

    k.provide("external.store", get_store)
