"""markpoints.rubric on small synthetic Description/Marks key texts (no SCSA text).

Each test covers one rule: reduced awards, parenthesised notes, mark rows without a description,
lower rows reconciled against the table Total, roman labels before any letter part, and (h)/(i).
"""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
import markpoints  # noqa: E402


def parts(text):
    return [part for part, _ in markpoints.rubric(text)]


class RubricKeys(unittest.TestCase):
    def test_reduced_award_with_wording_is_not_a_mark(self):
        text = """(a)
Description
Marks
Structure has a bond
2
Has one minor error or omission
1
Total
2"""
        self.assertEqual(parts(text), ["a", "a"])

    def test_parenthesised_reduction_note_is_not_a_description(self):
        text = """(a)
Description
Marks
(one minor error)
2
(1)
Total
2"""
        self.assertEqual(parts(text), ["a", "a"])

    def test_mark_row_without_description_counts_when_total_agrees(self):
        text = """(a)
Description
Marks
Shape drawn correctly
2
Total
2"""
        self.assertEqual(parts(text), ["a", "a"])
        imagery = """(a)
Description
Marks
2
Total
2"""
        self.assertEqual(parts(imagery), ["a", "a"])

    def test_mark_row_without_description_is_dropped_when_total_disagrees(self):
        # a bare number inside a calculation (an exponent on its own line), not a mark
        text = """(a)
Description
Marks
Mass worked out
1
5
Moles worked out
1
Total
2"""
        self.assertEqual(parts(text), ["a", "a"])

    def test_lower_rows_are_dropped_at_total_when_needed(self):
        text = """(a)
Description
Marks
Gives three properties
3
Gives two properties
2
Gives one property
1
Total
3"""
        self.assertEqual(parts(text), ["a", "a", "a"])

    def test_lower_rows_are_kept_when_total_agrees(self):
        text = """(a)
Description
Marks
Gives the first point
2
Gives a second point
1
Total
3"""
        self.assertEqual(parts(text), ["a", "a", "a"])

    def test_roman_labels_before_a_letter_part_are_text(self):
        text = """(i)
Write the equation
(ii)
Name the product
Description
Marks
Product named
1
Total
1"""
        self.assertEqual(parts(text), [""])

    def test_h_then_i_is_part_i_not_sub_part(self):
        text = """(h)
Description
Marks
First result
1
Total
1
(i)
Description
Marks
Second result
1
Total
1"""
        self.assertEqual(parts(text), ["h", "i"])

    def test_second_table_after_total_is_an_alternative(self):
        text = """(a)
Description
Marks
Method one
1
Total
1
Alternative
Description
Marks
Method two
1
Total
1"""
        self.assertEqual(parts(text), ["a"])


if __name__ == "__main__":
    unittest.main()
