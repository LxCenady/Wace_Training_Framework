"""Profiles may add a shared science paper without changing maths or trusting bad metadata."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import subjects


class Profiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = copy.deepcopy(subjects.info('MAM'))
        self.profile.update(subject='CHE', course='Chemistry ATAR', order=3,
                            recognise={'title': ['chemistry']}, paper_minutes=[10, 180])
        self.profile['sections'] = [dict(code='MC', letter='M', zh='第一部分',
                                        en='Section One', minutes=None, share=0.25)]
        (self.root / 'CHE').mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self):
        (self.root / 'CHE/pack.json').write_text(json.dumps(self.profile), encoding='utf-8')

    def test_shared_paper_and_separate_roots(self):
        self.write()
        self.assertEqual(list(subjects.names(self.root)), ['CHE'])
        self.assertEqual(subjects.section_letter('CHE', 'MC', self.root), 'M')
        self.assertEqual(list(subjects.names()), ['MAM', 'MAS', 'MAA'])
        with self.assertRaises(ValueError):
            subjects.section_letter('CHE', 'CalcFree', self.root)

    def test_refuse_bad_metadata(self):
        for change in ({'subject': 'OTHER'}, {'wtf_pack': 99}, {'paper_minutes': [-1, 180]},
                       {'recognise': {'title': []}}, {'topics': [{}]}, {'order': 'first'}):
            original = copy.deepcopy(self.profile)
            self.profile.update(change)
            self.write()
            with self.assertRaises(ValueError):
                subjects.profiles(self.root)
            self.profile = original


if __name__ == '__main__':
    unittest.main()
