"""Scoring algebra and overlapping atomic associations; no databases or settings."""
import copy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import rubric


def award(ident, marks=1, **extra):
    return dict(id=ident, kind='award', max_marks=marks, **extra)


class Rubrics(unittest.TestCase):
    def test_kernel_services_without_database_access(self):
        from kernel import Kernel
        from plugins import store
        kernel = Kernel('unused-test-root')
        kernel.provide('config', {'language': 'en'})
        with patch.object(store, 'Store', return_value=object()):
            store.setup(kernel)
        root = award('criterion', 2, knowledge=['ratio'], patterns=['calculate'])
        self.assertEqual(kernel.get('score.rubric')(root, {'criterion': 1})['earned'], 1)
        self.assertEqual(kernel.get('score.atom_coverage')(root), {'ratio': 2})

    def test_alternatives_shared_credit_and_any_two(self):
        root = dict(id='part', kind='sum', children=[
            award('shared'),
            dict(id='routes', kind='best', children=[
                dict(id='route-a', kind='sum', children=[award('a1'), award('a2')]),
                award('route-b', 2)]),
            dict(id='choices', kind='select', take=2, children=[award('c1'), award('c2'), award('c3')])])
        rubric.validate(root, 5)
        result = rubric.score(root, {'shared': 1, 'a1': 1, 'a2': 1, 'route-b': 2, 'c1': 1, 'c2': 1, 'c3': 1})
        self.assertEqual(result['earned'], 5)
        self.assertEqual(result['selections'], {'routes': ['route-a'], 'choices': ['c1', 'c2']})
        self.assertEqual(rubric.score(root, {'a1': 1, 'route-b': 1})['earned'], 1)

    def test_atomic_coverage_is_not_equal_split(self):
        root = dict(id='part', kind='best', children=[
            award('formula', 2, knowledge=['moles', 'ratio'], patterns=['calculate']),
            award('alternative', 2, knowledge=['mass'], patterns=['calculate'])])
        self.assertEqual(rubric.coverage(root), {'mass': 2, 'moles': 2, 'ratio': 2})
        self.assertEqual(rubric.coverage(root, 'patterns'), {'calculate': 2})
        self.assertEqual(rubric.score(root, {'formula': 2, 'alternative': 2})['earned'], 2)
        dependent = dict(id='part', kind='sum', children=[
            award('basis', knowledge=['foundation']),
            award('interpret', knowledge=['interpretation'], requires=['basis'])])
        self.assertEqual(rubric.coverage(dependent), {'foundation': 1, 'interpretation': 1})
        rubric.validate_associations(root, {'moles', 'ratio', 'mass'}, {'calculate'})
        with self.assertRaises(ValueError):
            rubric.validate_associations(root, {'moles'}, {'calculate'})
        with self.assertRaises(ValueError):
            rubric.validate_associations(award('untagged'), {'moles'}, {'calculate'})

    def test_bands_dependencies_and_pending_review(self):
        root = dict(id='part', kind='sum', children=[
            award('diagram', 2, positive_band=[1, 2], conditions=['diagram-reviewed']),
            award('reason', requires=['diagram'])], conditional_caps=[{'condition': 'wrong-units', 'cap': 2}])
        result = rubric.score(root, {'diagram': 2, 'reason': 1})
        self.assertIsNone(result['earned'])
        self.assertEqual((result['lower'], result['upper']), (0, 3))
        self.assertEqual(rubric.score(root, {'diagram': 2, 'reason': 1},
                                     {'diagram-reviewed': True, 'wrong-units': True})['earned'], 2)
        self.assertEqual(rubric.score(root, {'diagram': 2, 'reason': 1},
                                     {'diagram-reviewed': False, 'wrong-units': False})['earned'], 0)
        with self.assertRaises(ValueError):
            rubric.score(root, {'diagram': .5})
        with self.assertRaises(ValueError):
            rubric.score(root, {}, {'misspelled-condition': True})

    def test_reject_bad_trees_and_credit(self):
        root = dict(id='part', kind='sum', children=[award('a'), award('b')])
        bad = [dict(id='x', kind='execute'),
               dict(id='x', kind='sum', children=[award('a'), award('a')]),
               award('a', requires=['missing']),
               dict(id='x', kind='select', take=True, children=[award('a')]),
               award('a', float('nan')),
               award('a', patterns=['same', 'same']),
               dict(id='x', kind='sum', children=[award('a', requires=['x'])])]
        for tree in bad:
            with self.subTest(tree=tree), self.assertRaises(ValueError):
                rubric.validate(tree)
        cycle = copy.deepcopy(root)
        cycle['children'][0]['requires'] = ['b']
        cycle['children'][1]['requires'] = ['a']
        with self.assertRaises(ValueError):
            rubric.validate(cycle)
        with self.assertRaises(ValueError):
            rubric.validate(root, 3)
        for credit in ({'unknown': 1}, {'a': 2}, {'a': True}, {'a': float('inf')}):
            with self.assertRaises(ValueError):
                rubric.score(root, credit)


if __name__ == '__main__':
    unittest.main()
