"""A missing heading dot must not silently discard the rest of an MC section."""
import sys
import unittest
from pathlib import Path
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import segment_mc


class BareHeading(unittest.TestCase):
    def test_consecutive_bare_number_and_answer_grid(self):
        exam, key = pymupdf.open(), pymupdf.open()
        page = exam.new_page()
        for y, num in ((100, '1.'), (200, '2'), (300, '3.')):
            page.insert_text((60, y), num)
            page.insert_text((110, y), 'A complete question')
        page.insert_text((300, 150), '2')  # unrelated number outside the question-number margin
        kp = key.new_page()
        kp.insert_text((60, 80), 'Question')
        kp.insert_text((160, 80), 'Answer')
        for y, num, answer in ((100, '1', 'a'), (120, '2', 'b'), (140, '3', 'c')):
            kp.insert_text((60, y), num)
            kp.insert_text((160, y), answer)
        result = segment_mc.questions(exam, [[0, 60, 400]], {0: (60, 400)}, key)
        self.assertEqual([x['q'] for x in result], [1, 2, 3])
        self.assertEqual([x['answer'] for x in result], ['a', 'b', 'c'])
        exam.close()
        key.close()


if __name__ == '__main__':
    unittest.main()
