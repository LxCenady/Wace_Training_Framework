"""Profiles may add a shared science paper without changing maths or trusting bad metadata."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import subjects


class Profiles(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = copy.deepcopy(subjects.info('MAM'))
        self.profile['scoring'] = {'mode': 'raw'}
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
        self.assertEqual(subjects.section_minutes('CHE', 'MC', self.root), [10, 180])
        installed = list(subjects.names())
        self.assertEqual(installed[:3], ['MAM', 'MAS', 'MAA'])  # bundled maths order stays stable as packs are added
        self.assertIn('CHE', installed)
        for code in ('PHY', 'ACF'):
            if (Path(__file__).resolve().parents[2] / code / 'pack.json').exists():
                self.assertIn(code, installed)
        with self.assertRaises(ValueError):
            subjects.section_letter('CHE', 'CalcFree', self.root)

    def test_three_science_sections(self):
        self.profile['sections'] += [dict(code='SA', letter='S', zh='第二部分', en='Section Two', minutes=None),
                                     dict(code='ER', letter='E', zh='第三部分', en='Section Three', minutes=None)]
        self.write()
        self.assertEqual(subjects.section_codes('CHE', self.root), ['MC', 'SA', 'ER'])
        self.assertEqual(subjects.section_options('CHE', root=self.root)['第二部分 (SA)'], 'SA')
        self.assertEqual(subjects.section_minutes('CHE', 'ER', self.root), [10, 180])

    def test_shared_segmentation_preserves_mc_block_and_figures(self):
        import segment
        self.profile['paper_layout'] = 'shared'
        self.profile['sections'] = [
            dict(code='MC', letter='M', zh='选择题', en='Multiple choice', minutes=None,
                 headings=['Section One'], question_mode='section-only'),
            dict(code='SA', letter='S', zh='简答题', en='Short answer', minutes=None, headings=['Section Two']),
            dict(code='ER', letter='E', zh='综合题', en='Extended answer', minutes=None, headings=['Section Three'])]
        self.write()
        papers = self.root / 'CHE/papers'
        papers.mkdir()
        for kind in ('Exam', 'MarkingKey'):
            with pymupdf.open() as doc:
                for heading, question in [('Section One', '1. Choose an answer.'),
                                          ('Section Two', 'Question 26 (4 marks)'),
                                          ('Section Three', 'Question 27 (6 marks)')]:
                    page = doc.new_page()
                    page.insert_text((60, 80), heading)
                    if heading == 'Section One':
                        page.insert_text((60, 105), 'Question 24 refers to the following diagram.')
                    else:
                        page.insert_text((60, 105), 'Supplementary pages for planning your answers are provided.')
                    page.insert_text((60, 130), question)
                    page.draw_rect(pymupdf.Rect(70, 150, 270, 260), color=(0, 0, 0))
                page = doc.new_page()
                page.insert_text((60, 100), 'Published by the School Curriculum and Standards Authority')
                page.insert_text((60, 140), 'Copyright')
                doc.save(papers / f'2025_CHE_{kind}.pdf')
        (self.root / 'sources.tsv').write_text('CHE/papers/2025_CHE_Exam.pdf\thttps://example.invalid/exam\n', encoding='utf-8')
        with patch.object(segment, 'ROOT', str(self.root)), patch.dict('os.environ', WACE_MATHS_ROOT=str(self.root)):
            segment.main('CHE')
        questions = json.loads((self.root / 'CHE/questions.json').read_text(encoding='utf-8'))
        self.assertEqual([(q['q'], q['section']) for q in questions], [(26, 'SA'), (27, 'ER')])
        self.assertNotIn('Section Three', questions[0]['text'])
        self.assertNotIn('Supplementary pages', questions[0]['text'])
        self.assertTrue(all(r[0] < 3 for q in questions for r in q['key_regions']))
        blocks = json.loads((self.root / 'CHE/sections.json').read_text(encoding='utf-8'))
        self.assertEqual(list(blocks[0]['sections']), ['MC', 'SA', 'ER'])
        for question in questions:
            page, top, bottom = question['exam_regions'][0]
            self.assertLess(top, 150)
            self.assertGreater(bottom, 260)

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
