"""Choice sections preserve available questions without doubling attainable marks."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import paper_selection
import scoring


class PaperSelection(unittest.TestCase):
    def test_whole_paper_requires_an_explicit_choice(self):
        profile = {'sections': [{'code': 'MC', 'share': .15}, {'code': 'SA', 'share': .7},
                                {'code': 'EA', 'share': .15, 'answer_count': 1}],
                   'scoring': {'mode': 'section-weighted'}}
        results = {'MC': (15, 15), 'SA': (156, 156), 'EA': (30, 30)}
        self.assertIsNone(scoring.score(profile, results)['paper_percent'])
        self.assertEqual(scoring.score(profile, results, answered={'EA': ['q22']})['paper_percent'], 100)
        with self.assertRaises(ValueError):
            scoring.score(profile, results, answered={'EA': ['q22', 'q23']})

    def test_pool_and_explicit_answer(self):
        section = {'answer_count': 1}
        questions = [('a', 30), ('b', 30)]
        self.assertEqual(paper_selection.total(section, [30, 30]), 30)
        self.assertEqual(paper_selection.select(section, questions, ['b']), [('b', 30)])
        self.assertEqual(len(questions), 2)
        for ids in (None, [], ['a', 'b'], ['c'], ['a', 'a']):
            with self.assertRaises(ValueError):
                paper_selection.select(section, questions, ids)

    def test_default_all_and_multi_choice_maximum(self):
        self.assertEqual(paper_selection.total({}, [50, 100]), 150)
        self.assertEqual(paper_selection.select({}, [('a', 1)]), [('a', 1)])
        self.assertEqual(paper_selection.total({'answer_count': 2}, [10, 20, 30]), 50)
        for count in (0, -1, True, 1.5):
            with self.assertRaises(ValueError):
                paper_selection.validate({'answer_count': count})
        with self.assertRaises(ValueError):
            paper_selection.total({'answer_count': 3}, [30, 30])


if __name__ == '__main__':
    unittest.main()
