"""A reviewed scoring shape replaces a coincidentally correct parser total."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import awards


class ReviewedShape(unittest.TestCase):
    def test_equal_total_is_not_equal_shape(self):
        q = dict(year=2020, section='SR', q=1, marks=3, key='fake.pdf',
                 key_regions=[], text='invented question')
        fixed = {'2020R-1-0': dict(marks=3, structure='sum', awards=[
            dict(n=n, marks=1, text=f'criterion {n}') for n in (1, 2, 3)])}
        parser = lambda text: [('', 'merged criterion'), ('', 'merged criterion'), ('', 'final criterion')]
        with patch.object(awards.subjects, 'section_letter', return_value='R'), \
                patch.object(awards, 'key_text', return_value='invented key'), \
                patch.object(awards, 'split', return_value={'': 3}), \
                patch.object(awards, 'texts', return_value={'': 'invented stem'}):
            baseline = awards.question('PHY', q, parser, {'fake.pdf': object()})
            reviewed = awards.question('PHY', q, parser, {'fake.pdf': object()}, fixed)
            stale = awards.question('PHY', q, parser, {'fake.pdf': object()},
                                    {'2020R-1-0': dict(fixed['2020R-1-0'], marks=4)})
        self.assertEqual([a['marks'] for a in baseline['parts'][0]['awards']], [2, 1])
        self.assertEqual([a['marks'] for a in reviewed['parts'][0]['awards']], [1, 1, 1])
        self.assertEqual(reviewed['parts'][0]['source'], 'split')
        self.assertEqual(stale, baseline)


if __name__ == '__main__':
    unittest.main()
