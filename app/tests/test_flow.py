"""Pack flow: job checks and the award -> part/question tag export, on invented data (no owner files touched)."""
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import flowjobs as fj
import packflow


class Checks(unittest.TestCase):
    def test_split_marks_must_add_up(self):
        inp = {'id': '2019E-40-a', 'marks': 3}
        good = {'awards': [{'n': 1, 'marks': 2, 'text': 'x'}, {'n': 2, 'marks': 1, 'text': 'y'}], 'confidence': 0.9}
        self.assertEqual(fj.check_item('CHE', 'split', inp, good, {}), [])
        short = {'awards': [{'n': 1, 'marks': 2, 'text': 'x'}], 'confidence': 0.9}
        self.assertTrue(fj.check_item('CHE', 'split', inp, short, {}))

    def test_split_any_n(self):
        inp = {'id': '2016S-26-a', 'marks': 2}
        out = {'structure': 'any', 'take': 2, 'confidence': 0.8,
               'awards': [{'n': i, 'marks': 1, 'kind': 'choice', 'text': 'option'} for i in (1, 2, 3, 4)]}
        self.assertEqual(fj.check_item('CHE', 'split', inp, out, {}), [])
        self.assertTrue(fj.check_item('CHE', 'split', inp, dict(out, take=3), {}))

    def test_label_fields(self):
        ctx = {'topics': {'RX'}}
        ok = {'topic': 'RX', 'operation': 'write-equation', 'skill': 'write a reduction half-equation',
              'knowledge': ['half-equations'], 'confidence': 0.9}
        self.assertEqual(fj.check_item('CHE', 'label', {'id': 'a'}, ok, ctx), [])
        for bad in ({'operation': 'guess'}, {'topic': 'XX'}, {'knowledge': []},
                    {'skill': ' '.join(['word'] * 13)}, {'knowledge': ['one two three four five six']}):
            self.assertTrue(fj.check_item('CHE', 'label', {'id': 'a'}, dict(ok, **bad), ctx), bad)

    def test_assign_codes_from_catalogue(self):
        ctx = {'patterns': {'RX1', 'RX2'}, 'knowledge': {'RX.K1'}}
        ok = {'patterns': ['RX1'], 'knowledge': ['RX.K1'], 'confidence': 0.9}
        self.assertEqual(fj.check_item('CHE', 'assign', {'id': 'a'}, ok, ctx), [])
        self.assertTrue(fj.check_item('CHE', 'assign', {'id': 'a'}, dict(ok, patterns=['RX9']), ctx))
        self.assertTrue(fj.check_item('CHE', 'assign', {'id': 'a'}, dict(ok, patterns=['RX1', 'RX2', 'RX1']), ctx))

    def test_atomise_places_every_award_once(self):
        inp = {'topic': {'code': 'RX'}, 'labels': [{'id': 'a1'}, {'id': 'a2'}, {'id': 'a3'}]}
        pat = {'name_en': 'n', 'name_zh': 'n', 'definition': 'd', 'not': 'n'}
        out = {'patterns': [dict(pat, id='RX1', members=['a1', 'a2']), dict(pat, id='RX2', members=['a3'])],
               'knowledge': [{'id': 'RX.K1', 'name_en': 'k'}]}
        self.assertEqual(fj.check_atomise(inp, out), [])
        out['patterns'][1]['members'] = ['a2']
        problems = fj.check_atomise(inp, out)
        self.assertTrue(any('twice' in p for p in problems) and any('nowhere' in p for p in problems))
        out['patterns'][1].update(id='RX3', members=['a3'])
        self.assertTrue(any('numbered' in p for p in fj.check_atomise(inp, out)))

    def test_references(self):
        self.assertEqual(fj.refs('**Past questions**: 2022 ER Q37(a), 2019 SA Q30, 2016 CA Q4(bi)'),
                         {'2022 ER Q37(a)', '2019 SA Q30', '2016 CA Q4(bi)'})


class Export(unittest.TestCase):
    def test_part_and_question_tags_come_from_awards(self):
        q = {'id': '2022E-37', 'year': 2022}
        pa, pb = {'label': 'a'}, {'label': 'b'}
        rows = [(q, pa, {'id': '2022E-37-a-1', 'marks': 1, 'credit': 1}), (q, pa, {'id': '2022E-37-a-2', 'marks': 2, 'credit': 2}),
                (q, pb, {'id': '2022E-37-b-1', 'marks': 1, 'credit': 1})]
        assigned = {'2022E-37-a-1': {'patterns': ['QNT2'], 'knowledge': ['QNT.K1'], 'confidence': 0.9},
                    '2022E-37-a-2': {'patterns': ['RX3'], 'knowledge': ['RX.K4'], 'confidence': 0.9},
                    '2022E-37-b-1': {'patterns': ['RX3'], 'knowledge': ['RX.K4'], 'confidence': 0.8}}
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / 'tools').mkdir()
            with patch.object(packflow, 'ROOT', tmp), patch.object(fj, 'awards', lambda s: rows), \
                    patch.object(fj, 'load', lambda path, default=None: assigned if path.endswith('assign.json') else default):
                packflow.export('CHE')
            tools = Path(tmp) / 'tools'
            parttags = (tools / 'parttags_CHE.txt').read_text(encoding='utf-8').splitlines()
            self.assertIn('2022E 37 a=RX3+QNT2 b=RX3', parttags)  # most marks first
            self.assertIn('2022E 37:RX,QNT', (tools / 'tags_CHE.txt').read_text(encoding='utf-8'))
            marktags = json.loads((tools / 'marktags_CHE.json').read_text(encoding='utf-8'))
            self.assertEqual(marktags['awards']['2022E-37-a-2'], {'marks': 2, 'patterns': ['RX3'],
                                                                  'knowledge': ['RX.K4'], 'confidence': 0.9})


class PackTags(unittest.TestCase):
    """The pack protocol's award-level files (marktags.py) and how pack.py gates them."""
    def setUp(self):
        import marktags
        self.mt = marktags
        self.cat = {'schema_version': 2, 'topic_codes': {'RX': 'Redox'},
                    'patterns': [{'id': 'RX1', 'name_en': 'Half-equations'}, {'id': 'RX2', 'name_en': 'Cells'}],
                    'knowledge': [{'id': 'RX.K1', 'name_en': 'Oxidation numbers', 'definition': 'own words'}]}
        self.tags = {'schema': 1, 'subject': 'CHE', 'questions': {'2022E-37': 'a:1,2'},
                     'awards': {'2022E-37-a-1': {'marks': 1, 'patterns': ['RX1'], 'knowledge': ['RX.K1'], 'confidence': 0.9},
                                '2022E-37-a-2': {'marks': 2, 'patterns': ['RX2'], 'knowledge': ['RX.K1'], 'confidence': 0.8}}}

    def test_valid_marktags(self):
        self.mt.validate_marktags(self.tags, self.cat, 'CHE')

    def test_refuse_bad_marktags(self):
        import copy
        bad = [lambda t, c: t['awards']['2022E-37-a-1'].update(text='copied key wording'),
               lambda t, c: t['awards']['2022E-37-a-1'].update(patterns=['RX9']),
               lambda t, c: t['awards']['2022E-37-a-1'].update(knowledge=[]),
               lambda t, c: t['questions'].clear(),
               lambda t, c: t.update(subject='MAM'),
               lambda t, c: t['awards'].update({'2022E-37-a-x': {}}),
               lambda t, c: c.update(schema_version=1),
               lambda t, c: c['knowledge'][0].update(definition='x' * 601)]
        for mutate in bad:
            t, c = copy.deepcopy(self.tags), copy.deepcopy(self.cat)
            mutate(t, c)
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                self.mt.validate_marktags(t, c, 'CHE')

    def test_splits_shape_only(self):
        good = {'2019S-35-aii': {'marks': 2, 'structure': 'any', 'take': 2,
                                 'awards': [{'n': i, 'marks': 1, 'kind': 'choice'} for i in (1, 2, 3, 4)]}}
        self.mt.validate_splits(good)
        for bad in ({'2019S-35-aii': dict(good['2019S-35-aii'], take=3)},
                    {'2019S-35-aii': dict(good['2019S-35-aii'], awards=[{'n': 1, 'marks': 2, 'kind': 'award', 'text': 'x'}])},
                    {'../x': good['2019S-35-aii']}):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.mt.validate_splits(bad)

    def test_any_n_credit_adds_up_to_the_part(self):
        part = {'take': 2, 'awards': [{'marks': 1, 'kind': 'choice'}] * 4}
        self.assertEqual(self.mt.credit(part), [0.5] * 4)
        self.assertEqual(self.mt.credit({'awards': [{'marks': 2}, {'marks': 1}]}), [2, 1])

    def test_rows_only_when_the_build_numbers_awards_alike(self):
        rec = {'id': '2022E-37', 'parts': [{'label': 'a', 'awards': [{'id': '2022E-37-a-1', 'marks': 1},
                                                                     {'id': '2022E-37-a-2', 'marks': 2}]}]}
        rows, problem = self.mt.rows('CHE', 'CHE-2022E-Q37', rec, self.tags)
        self.assertIsNone(problem)
        self.assertIn(('CHE-2022E-Q37', 'a', 2, 2, 'pattern', 'CHE.RX.2'), rows)
        self.assertIn(('CHE-2022E-Q37', 'a', 1, 1, 'knowledge', 'CHE.RX.K1'), rows)
        rec['parts'][0]['awards'][1]['marks'] = 1  # the local key now divides differently
        rows, problem = self.mt.rows('CHE', 'CHE-2022E-Q37', rec, self.tags)
        self.assertEqual(rows, [])
        self.assertIn('part tags only', problem)

    def test_pack_needs_wtf_2_1_for_award_files(self):
        import pack
        payload = {'catalogue.json': json.dumps(self.cat).encode(), 'marktags.json': json.dumps(self.tags).encode()}
        pack.validate_tags(payload, 'CHE', (2, 1, 0))
        with self.assertRaises(ValueError):
            pack.validate_tags(payload, 'CHE', (2, 0, 0))
        with self.assertRaises(ValueError):
            pack.validate_tags({'marktags.json': payload['marktags.json']}, 'CHE', (2, 1, 0))


if __name__ == '__main__':
    unittest.main()
