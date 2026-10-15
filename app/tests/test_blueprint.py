"""Paper drawing (tools/blueprint.py) on a tiny in-memory database: catalogue flags keep removed and
non-diagnostic patterns out of new papers, and a one-mark multiple-choice section is drawn to its full total."""
import os, random, sqlite3, sys, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import blueprint  # noqa: E402
from build_db import SCHEMA  # noqa: E402


def database(flags=True):
    db = sqlite3.connect(":memory:")
    db.executescript(SCHEMA if flags else SCHEMA.replace("CREATE TABLE pattern_flags", "CREATE TABLE unused_flags"))
    n = 0
    for year in range(2020, 2026):
        for q in range(1, 16):  # fifteen one-mark questions a year; every fifth on a removed pattern
            n += 1
            qid = f"ACF-{year}M-Q{q}"
            pattern = "ACF.OUT.1" if q % 5 == 0 else f"ACF.CST.{q % 4 + 1}"
            db.execute("INSERT INTO questions (id, subject, year, section, q, marks) VALUES (?,?,?,?,?,?)",
                       (qid, "ACF", year, "MC", q, 1))
            db.execute("INSERT INTO parts (qid, label, ord, marks) VALUES (?,?,?,?)", (qid, "", 0, 1))
            db.execute("INSERT INTO part_patterns VALUES (?,?,?)", (qid, "", pattern))
    if flags:
        db.execute("INSERT INTO pattern_flags VALUES ('ACF.OUT.1', 1, 1, 1)")
    return db


class Drawing(unittest.TestCase):
    def test_flags_exclude_historical_patterns(self):
        db = database()
        self.assertEqual(blueprint.excluded(db), {"ACF.OUT.1"})
        bp = blueprint.blueprint(db, "ACF", "MC")
        self.assertNotIn("ACF.OUT.1", bp["pattern_share"])
        for seed in range(10):
            paper = blueprint.plan(bp, 15, random.Random(seed))
            self.assertEqual(sum(m for _, m, _, _ in paper), 15)
            self.assertFalse({c for codes, _, _, _ in paper for c in codes} & {"ACF.OUT.1"})

    def test_database_without_flags_draws_everything(self):
        db = database(flags=False)
        self.assertEqual(blueprint.excluded(db), set())
        self.assertIn("ACF.OUT.1", blueprint.blueprint(db, "ACF", "MC")["pattern_share"])


if __name__ == "__main__":
    unittest.main()
