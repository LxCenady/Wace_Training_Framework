"""Synthetic fixtures only: identity rejection and annotation export format."""
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import audit_maa
import fetch_maa
import segment


class MAADataTests(unittest.TestCase):
    def pdf(self, folder, text):
        path = Path(folder) / "synthetic.pdf"
        with pymupdf.open() as doc:
            page = doc.new_page()
            page.insert_text((50, 50), text)
            doc.save(path)
        return path

    def test_identity_rejects_wrong_course_section_kind_and_sample(self):
        rel = "MAA/papers/2020_MAA_Exam_CalcFree.pdf"
        with tempfile.TemporaryDirectory() as folder:
            for text in ("Mathematics Methods ATAR course examination 2020 Calculator-free Question/Answer booklet",
                         "Mathematics Applications ATAR course examination 2021 Calculator-free Question/Answer booklet",
                         "Mathematics Applications ATAR course examination 2019 2020/123 Calculator-free Question/Answer booklet",
                         "Mathematics Applications ATAR course examination 2020 Calculator-assumed Question/Answer booklet",
                         "Mathematics Applications ATAR course examination 2020 Calculator-free Marking key",
                         "Mathematics Applications ATAR course examination 2020 Calculator-free Sample examination"):
                with self.subTest(text=text), self.assertRaises(ValueError):
                    fetch_maa.validate(self.pdf(folder, text), rel)
            fetch_maa.validate(self.pdf(folder, "Mathematics Applications ATAR course examination 2020 Calculator-free Question/Answer booklet"), rel)
            # The shared structure table lists both sections: identity comes from the cover.
            path = self.pdf(folder, "Mathematics Applications ATAR course examination 2020 Calculator-assumed Question/Answer booklet")
            with pymupdf.open(path) as doc:
                doc.new_page().insert_text((50, 50), "Structure: Section One Calculator-free; Section Two Calculator-assumed")
                doc.saveIncr()
            with self.assertRaisesRegex(ValueError, "Section mismatch"):
                fetch_maa.validate(path, rel)
            path = Path(folder) / "synthetic.pdf"
            path.write_bytes(path.read_bytes().split(b"%%EOF")[0])
            with self.assertRaisesRegex(ValueError, "Truncated PDF"):
                fetch_maa.validate(path, rel)

    def test_manifest_has_all_twenty_paired_exams(self):
        names = {row[0] for row in fetch_maa.sources()}
        core = {f"MAA/papers/{year}_MAA_{kind}_{section}.pdf" for year in range(2016, 2026)
                for kind in ("Exam", "MarkingKey") for section in ("CalcFree", "CalcAssumed")}
        self.assertTrue(core <= names)

    def test_heading_marks_match_overlapping_row_with_mixed_fonts(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'key.pdf'
            with pymupdf.open() as doc:
                page = doc.new_page()
                page.insert_text((50, 80), 'Question 17', fontsize=20)
                page.insert_text((450, 80), '(8 marks)', fontsize=11)
                page.insert_text((450, 120), '(2 marks)', fontsize=11)
                doc.save(path)
            doc, heads, _, _ = segment.scan(str(path))
            try:
                self.assertEqual(heads[0][3], 8)
            finally:
                doc.close()

    def test_partial_export_skips_pending_and_keeps_legacy_delimiters(self):
        labels = [{"year": 2020, "section": "CalcFree", "q": 1, "topics": ["GRF", "NDM"],
                   "parts": [{"label": "a", "tags": ["GRF2", "NDM1"]}]},
                  {"year": 2020, "section": "CalcFree", "q": 2, "topics": ["BIV"],
                   "parts": [{"label": "", "tags": ["BIV1"]}]}]
        with tempfile.TemporaryDirectory() as folder, patch.object(audit_maa, "ROOT", Path(folder)):
            (Path(folder) / "tools").mkdir()
            audit_maa.export_tags(labels, {"errors": [], "pending": [["2020", "CalcFree", 2]]})
            self.assertIn("2020F 1:GRF,NDM", (Path(folder) / "tools/tags_MAA.txt").read_text())
            parts = (Path(folder) / "tools/parttags_MAA.txt").read_text()
            self.assertIn("2020F 1 a=GRF2+NDM1", parts)
            self.assertNotIn("2020F 2", parts)
            with self.assertRaises(ValueError):
                audit_maa.export_tags(labels, {"errors": ["bad marks"], "pending": []})


if __name__ == "__main__":
    unittest.main()
