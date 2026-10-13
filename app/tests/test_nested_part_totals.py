"""An optional table policy avoids counting a printed parent total and its internal allocations twice."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
from partmarks import split


class NestedTotals(unittest.TestCase):
    def test_table_allocations_preserve_part_totals(self):
        text = 'Question 20 (42 marks)\n(a) Prepare statement (30 marks)\n(b) Calculate ratios (10 marks)\nRatio A (4 marks) Ratio B (4 marks) Ratio C (2 marks)\n(c) Explain (2 marks)'
        self.assertIsNone(split(text, 42))
        self.assertEqual(split(text, 42, True), {'a': 30, 'b': 10, 'c': 2})

    def test_explicit_roman_children_replace_the_parent(self):
        text = 'Question 2 (7 marks)\n(a) Two actions (5 marks)\n(i) First (2 marks)\n(ii) Second (3 marks)\n(b) Explain (2 marks)'
        self.assertEqual(split(text, 7, True), {'ai': 2, 'aii': 3, 'b': 2})
        self.assertIsNone(split(text, 8, True))


if __name__ == '__main__':
    unittest.main()
