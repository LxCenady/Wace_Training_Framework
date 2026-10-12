"""A range-table row may wrap after its marks; preserve its full condition without adding marks."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import handlers


class BandContinuation(unittest.TestCase):
    def test_wrapped_band_and_following_part(self):
        text = '(a)\nDescription\nMarks\nIdentifies a source (one mark alone).\n1–2\nExplains its physical mechanism.\nTotal\n2\n(b)\nDescription\nMarks\nCalculates a value.\n1\nTotal\n1'
        legacy = handlers.key_parser(dict(key_style='description-marks', checker='none'))(text)
        parsed = handlers.key_parser(dict(key_style='description-marks', checker='none', key_band_continuation=True))(text)
        self.assertEqual([p for p, _ in parsed], ['a', 'a', 'b'])
        self.assertEqual(len(parsed), len(legacy))
        self.assertNotIn('physical mechanism', legacy[0][1])
        self.assertIn('physical mechanism', parsed[0][1])
        self.assertNotIn('physical mechanism', parsed[-1][1])

    def test_next_numbered_row_is_not_a_continuation(self):
        text = 'Description\nMarks\nFirst complete condition.\n1–2\nSeparate condition.\n1\nTotal\n3'
        rows = handlers.key_parser(dict(key_style='description-marks', checker='none', key_band_continuation=True))(text)
        self.assertEqual(len(rows), 3)
        self.assertNotIn('Separate condition', rows[0][1])
        self.assertIn('Separate condition', rows[-1][1])

    def test_only_table_handler_accepts_option(self):
        with self.assertRaises(ValueError):
            handlers.key_parser(dict(key_style='ticks', checker='sympy', key_band_continuation=True))


if __name__ == '__main__':
    unittest.main()
