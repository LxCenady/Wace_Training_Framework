"""MC worked examples must not hide later written questions in a shared key."""
from pathlib import Path
import sys
import tempfile
import unittest
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import segment


class WorkedExamples(unittest.TestCase):
    def test_first_written_question_excludes_mc_workings(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'key.pdf'
            with pymupdf.open() as doc:
                page = doc.new_page()
                for y, text in [(80, 'Question 2'), (130, 'Question 12'),
                                (230, 'Question 16 (3 marks)'), (330, 'Question 17 (4 marks)')]:
                    page.insert_text((60, y), text)
                doc.save(path)
            doc, heads, _, _ = segment.scan(str(path), shared=True, first_question=16)
            try:
                self.assertEqual([(h[0], h[3]) for h in heads], [(16, 3), (17, 4)])
            finally:
                doc.close()


if __name__ == '__main__':
    unittest.main()
