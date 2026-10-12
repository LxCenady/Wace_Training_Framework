"""Opt-in answer boundaries exclude the next section without moving exam crops."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
import segment
import subjects


class KeySectionBoundaries(unittest.TestCase):
    def test_optional_headings_preserve_answers_and_legacy_boundaries(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            papers = root / 'CHE/papers'
            papers.mkdir(parents=True)
            profile = copy.deepcopy(subjects.info('MAM'))
            profile.update(subject='CHE', course='Chemistry ATAR', paper_layout='shared',
                           recognise={'title': ['chemistry']}, scoring={'mode': 'raw'}, paper_minutes=[10, 180])
            profile['sections'] = [
                dict(code='SA', letter='S', zh='简答题', en='Short answer', minutes=None, headings=['Section One']),
                dict(code='ER', letter='E', zh='综合题', en='Extended answer', minutes=None, headings=['Section Two'])]
            for kind in ('Exam', 'MarkingKey'):
                with pymupdf.open() as doc:
                    for number, section in enumerate(('Section One', 'Section Two'), 1):
                        page = doc.new_page()
                        page.insert_text((60, 80), section)
                        page.insert_text((60, 105), 'Instructions for this section.')
                        page.insert_text((60, 130), f'Question {number} (2 marks)')
                        page.insert_text((60, 160), f'Answer content for question {number}.')
                    doc.save(papers / f'2025_CHE_{kind}.pdf')
            (root / 'CHE/sources.tsv').write_text(
                'CHE/papers/2025_CHE_Exam.pdf\thttps://example.invalid/exam.pdf\n', encoding='utf-8')
            def run():
                (root / 'CHE/pack.json').write_text(json.dumps(profile), encoding='utf-8')
                with patch.object(segment, 'ROOT', str(root)), patch.dict('os.environ', WACE_MATHS_ROOT=str(root)):
                    segment.main('CHE')
                return json.loads((root / 'CHE/questions.json').read_text(encoding='utf-8'))
            legacy = run()
            for section in profile['sections']:
                section['key_headings'] = section['headings']
            trimmed = run()
            with pymupdf.open(papers / '2025_CHE_MarkingKey.pdf') as key:
                old = segment.text_of(key, legacy[0]['key_regions'])
                new = segment.text_of(key, trimmed[0]['key_regions'])
                self.assertIn('Section Two', old)
                self.assertNotIn('Section Two', new)
                self.assertIn('Answer content for question 1.', new)
                self.assertIn('Answer content for question 2.', segment.text_of(key, trimmed[1]['key_regions']))
            self.assertEqual([q['exam_regions'] for q in legacy], [q['exam_regions'] for q in trimmed])


if __name__ == '__main__':
    unittest.main()
