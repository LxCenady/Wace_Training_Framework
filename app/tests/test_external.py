"""External-library invariants, using synthetic private PDFs and temporary databases only."""
from pathlib import Path
import json
import math
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kernel import Kernel
from plugins.external_store import ExternalStore
from plugins.external_tagger import classify


def fixtures(folder):
    """Mixed widths, a continuation, unnumbered scans, a missing answer and a supplementary page."""
    exam, answer = Path(folder) / "source.pdf", Path(folder) / "answers.pdf"
    with pymupdf.open() as doc:
        pg = doc.new_page(width=700, height=600)
        pg.insert_text((40, 70), "Question 1 (4 marks)")
        pg.insert_text((580, 160), "velocity")  # beyond the SCSA pipeline's fixed clip width
        pg = doc.new_page(width=500, height=700)
        pg.insert_text((30, 70), "Question 1 (continued)")
        pg.insert_text((30, 120), "Find displacement by integrating the given velocity.")
        pg.insert_text((30, 350), "Question 2 (2 marks)")
        pg.insert_text((30, 390), "Differentiate a displacement function.")
        pg.insert_text((30, 460), "End of questions")
        pg = doc.new_page()
        pg.insert_text((30, 100), "Supplementary working space")
        doc.save(exam)
    with pymupdf.open() as doc:
        pg = doc.new_page(width=650, height=500)
        pg.insert_text((30, 70), "Question 1 (4 marks)")
        pg.insert_text((30, 100), "Integrate velocity and apply the initial displacement.")
        doc.save(answer)
    return exam, answer


class ExternalTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name)
        self.exam, self.answer = fixtures(self.folder)
        self.k = Kernel(str(self.folder))
        self.k.load(["external_pdf"])
        self.store = ExternalStore(self.folder, lambda name: self.k.get("external.pdf." + name),
                                   lambda subj: [subj + ".M.1", subj + ".M.2"])
        self.original = (self.exam.read_bytes(), self.answer.read_bytes())
        self.paper = self.store.import_pair(str(self.exam), str(self.answer), "School trial 2026", "Synthetic school", "MAM", "CalcFree")

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def test_paired_crops_and_originals(self):
        rows = self.store.search()
        self.assertEqual([r["label"] for r in rows], ["Q1", "Q2"])
        self.assertEqual(len(rows[0]["exam_regions"]), 2)
        self.assertIn("velocity", rows[0]["stem"])
        self.assertIn("integrating", rows[0]["stem"])
        self.assertNotIn("Supplementary", rows[1]["stem"])
        self.assertEqual(rows[1]["answer_regions"], [])
        self.assertTrue(all(not r["confirmed"] for r in rows))
        paper = self.store.paper(self.paper)
        self.assertEqual(Path(self.store.asset(paper["exam"])).read_bytes(), self.original[0])
        self.assertEqual((self.exam.read_bytes(), self.answer.read_bytes()), self.original)
        self.assertFalse((self.folder / "wace.db").exists())
        self.assertFalse((self.folder / "generated.db").exists())

    def test_confirmation_search_and_reload(self):
        q = self.store.search()[0]
        self.store.save_question(self.paper, "Q1", 4, q["exam_regions"], q["answer_regions"], ["MAM.M.2"], True, q["id"])
        self.assertEqual(len(self.store.search(tags=["MAM.M"], confirmed=True)), 1)
        self.assertEqual(len(self.store.search(tags=["MAM.M.1"])), 0)
        self.assertEqual(len(self.store.search(subject="MAS")), 0)
        self.assertEqual(len(self.store.search(words="synthetic school")), 2)
        self.assertEqual(len(self.store.search(section="CalcAssumed")), 0)
        with self.assertRaises(ValueError):
            self.store.save_question(self.paper, "Q2", 2, self.store.search()[1]["exam_regions"], [], ["MAM.M.1"], True, self.store.search()[1]["id"])
        self.store.close()
        self.store = ExternalStore(self.folder, lambda name: self.k.get("external.pdf." + name), lambda _: ["MAM.M.1", "MAM.M.2"])
        self.assertTrue(self.store.question(q["id"])["confirmed"])

    def test_invalid_edits_and_duplicate_import(self):
        q = self.store.search()[0]
        for regions in ([[0, 0, 0, 701, 200]], [[0, 0, math.nan, 20, 200]], [[99, 0, 0, 20, 200]]):
            with self.assertRaises(ValueError):
                self.store.save_question(self.paper, "Q1", 4, regions, q["answer_regions"], [], qid=q["id"])
        with self.assertRaises(ValueError):
            self.store.save_question(self.paper, "Q1", 4, q["exam_regions"], q["answer_regions"], ["MAS.M.2"], qid=q["id"])
        with self.assertRaises(ValueError):
            self.store.save_question(self.paper, "Q2", 4, q["exam_regions"], q["answer_regions"], [], qid=q["id"])
        with self.assertRaises(ValueError):
            self.store.import_pair(str(self.exam), str(self.answer), "Duplicate", "School", "MAM", "CalcFree")
        with self.assertRaises(ValueError):
            self.store.import_pair(str(self.exam), str(self.exam), "Same file", "School", "MAM", "CalcFree")
        self.assertEqual(self.store.question(q["id"]), q)
        self.assertEqual(len(self.store.papers()), 1)
        self.assertEqual(len(list((self.folder / "external").iterdir())), 1)
        with self.assertRaises(ValueError):
            self.store.asset("../private.pdf")

    def test_unrecognised_scan_manual_crop(self):
        scan = self.folder / "scan.pdf"
        with pymupdf.open() as doc:
            doc.new_page(width=500, height=500)
            doc.save(scan)
        paper = self.store.import_pair(str(scan), str(self.answer), "Scanned trial", "School", "MAM", "CalcFree")
        self.assertEqual(self.store.search(paper=paper), [])
        qid = self.store.save_question(paper, "Q1(a)", 3, [[0, 10, 10, 400, 400]], [[0, 10, 10, 400, 400]],
            ["MAM.M.2"], True, stem="Integrate the given velocity.", answer_text="Use an initial position to fix the constant.")
        self.assertIn("Integrate", self.store.question(qid)["stem"])
        self.assertEqual(len(self.store.search(words="initial")), 0)  # searches questions, not hidden answers

    def test_rotated_page_manual_crop_matches_preview_text(self):
        path = self.folder / "rotated.pdf"
        with pymupdf.open() as doc:
            page = doc.new_page(width=700, height=500)
            page.insert_text((40, 100), "Question 1 (3 marks)")
            page.set_rotation(90)
            doc.save(path)
        with pymupdf.open(path) as doc:
            box = pymupdf.Rect(doc[0].get_text("blocks")[0][:4]) * doc[0].rotation_matrix
        region = [0, *box]
        self.assertEqual(self.k.get("external.pdf.suggest")(str(path)), [])
        self.assertIn("Question 1", self.k.get("external.pdf.text")(str(path), [region]))
        self.assertTrue(self.k.get("external.pdf.render")(str(path), 0, list(box)).startswith(b"\x89PNG"))

    def test_api_drafts_validation_and_conflict(self):
        catalogue = [dict(code="MAM.M.2", title="Velocity to displacement", method="Integrate with an initial value")]
        calls = []
        proposal = dict(tags=["MAM.M.2"], reason="Integrate velocity with an initial displacement.", uncertain=False)

        def chat(system, user):
            calls.append((system, json.loads(user)))
            return json.dumps(proposal)

        skill = (Path(__file__).resolve().parents[2] / "skills/wace-external-tagging/SKILL.md").read_text(encoding="utf-8")
        got = classify(chat, skill, catalogue, "Find displacement from velocity", "Integrate then use the initial value")
        self.assertEqual(got, proposal)
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0][1]["catalogue"], catalogue)
        q = self.store.search()[0]
        self.store.save_proposal(q["id"], got, q)
        now = self.store.question(q["id"])
        self.assertFalse(now["confirmed"])
        self.assertEqual(now["tags"], ["MAM.M.2"])
        with self.assertRaises(ValueError):
            self.store.save_proposal(q["id"], got, q)  # stale snapshot cannot overwrite edits
        for bad in ("invalid JSON", json.dumps(dict(proposal, tags=["MAS.M.2"])), json.dumps(dict(proposal, uncertain="no"))):
            with self.assertRaises(ValueError):
                classify(lambda *_: bad, skill, catalogue, "question", "answer")
        with self.assertRaises(ValueError):
            classify(chat, skill, catalogue, "", "answer")
        self.store.save_question(self.paper, "Q1", 4, now["exam_regions"], now["answer_regions"], now["tags"], True, q["id"])
        with self.assertRaises(ValueError):
            self.store.save_proposal(q["id"], got, self.store.question(q["id"]))

    def test_batch_script_uses_configured_api_and_skips_confirmed(self):
        repo = Path(__file__).resolve().parents[2]
        skill = self.folder / "skills/wace-external-tagging/SKILL.md"
        skill.parent.mkdir(parents=True)
        shutil.copyfile(repo / "skills/wace-external-tagging/SKILL.md", skill)
        with sqlite3.connect(self.folder / "wace.db") as db:
            db.execute("CREATE TABLE patterns (code TEXT, title TEXT, method TEXT, topic TEXT, n INTEGER)")
            db.execute("INSERT INTO patterns VALUES ('MAM.M.2','Velocity to displacement','Integrate with initial position','MAM.M',2)")
        db.close()
        q, missing = self.store.search()
        self.store.delete_question(missing["id"])
        seen = []

        class Fake(BaseHTTPRequestHandler):
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                seen.append((self.path, self.headers["Authorization"], body))
                content = json.dumps(dict(tags=["MAM.M.2"], reason="Integrate given velocity.", uncertain=False))
                reply = json.dumps(dict(choices=[dict(message=dict(content=content))])).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(reply)

            def log_message(self, *_):
                pass

        server = HTTPServer(("127.0.0.1", 0), Fake)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        profile = self.folder / "profile/wace-maths"
        profile.mkdir(parents=True)
        (profile / "config.json").write_text(json.dumps(dict(provider="openai", openai=dict(
            base_url=f"http://127.0.0.1:{server.server_port}/v1", model="external-test-model", api_key="fake-external-key", extra_body={}))), encoding="utf-8")
        env = dict(os.environ, APPDATA=str(self.folder / "profile"), PYTHONUTF8="1")
        command = [sys.executable, str(repo / "tools/tag_external.py"), "--root", str(self.folder)]
        try:
            listing = subprocess.run(command + ["--list"], env=env, capture_output=True, text=True, encoding="utf-8", timeout=15)
            self.assertEqual(listing.returncode, 0, listing.stderr)
            self.assertEqual(seen, [])
            run = subprocess.run(command + ["--paper", self.paper], env=env, capture_output=True, text=True, encoding="utf-8", timeout=15)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertEqual(len(seen), 1)
            path, auth, body = seen[0]
            self.assertEqual(path, "/v1/chat/completions")
            self.assertEqual(auth, "Bearer fake-external-key")
            self.assertEqual(body["model"], "external-test-model")
            self.assertIn("External-paper tagging", body["messages"][0]["content"])
            now = self.store.question(q["id"])
            self.assertEqual(now["tags"], ["MAM.M.2"])
            self.assertFalse(now["confirmed"])
            self.store.save_question(self.paper, "Q1", 4, now["exam_regions"], now["answer_regions"], now["tags"], True, q["id"])
            again = subprocess.run(command + ["--paper", self.paper], env=env, capture_output=True, text=True, encoding="utf-8", timeout=15)
            self.assertEqual(again.returncode, 0, again.stderr)
            self.assertEqual(len(seen), 1)
            self.assertFalse((self.folder / "generated.db").exists())
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == "__main__":
    unittest.main()
