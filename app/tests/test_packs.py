"""Pack integrity, install rollback and weighted/partial scores, without owner data writes."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import pack
import scoring
import subjects


class Packs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.profile = copy.deepcopy(subjects.info('MAM'))
        self.payload = {'sources.tsv': b'#path\turl\tmethod\tcapture\tsha256\tbytes\tpages\tneed\n'
                                       b'MAM/papers/2025_MAM_Exam_CalcFree.pdf\thttps://example.invalid/exam.pdf\tbrowser\t\t'
                                       + b'0' * 64 + b'\t1000\t12\trequired\n',
                        'tags.txt': b'original tags', 'parttags.txt': b'original part tags', 'skill/SKILL.md': b'original skill'}

    def tearDown(self):
        self.tmp.cleanup()

    def archive(self, mutate=None):
        profile = copy.deepcopy(self.profile)
        profile['files'] = {name: 'sha256:' + hashlib.sha256(data).hexdigest() for name, data in self.payload.items()}
        payload = dict(self.payload)
        if mutate:
            mutate(profile, payload)
        file = self.root / 'test.wtfpack'
        with zipfile.ZipFile(file, 'w') as archive:
            archive.writestr('pack.json', json.dumps(profile))
            for name, data in payload.items():
                archive.writestr(name, data)
        return file

    def test_install_and_no_partial_registration(self):
        file = self.archive()
        target = self.root / 'installed'
        pack.install(file, target)
        self.assertEqual(list(subjects.names(target)), ['MAM'])
        before = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
        with self.assertRaises(ValueError):
            pack.install(file, target)
        replace = pack.os.replace
        calls = []
        def fail_last(source, dest):
            calls.append(dest)
            if Path(dest).name == 'pack.json':
                raise OSError('simulated disk failure')
            replace(source, dest)
        self.payload['tags.txt'] = b'changed'
        file = self.archive()
        with patch.object(pack.os, 'replace', fail_last), self.assertRaises(OSError):
            pack.install(file, target, overwrite=True)
        after = {p.relative_to(target): p.read_bytes() for p in target.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_refuse_unsafe_and_incompatible_packs(self):
        mutations = [
            lambda p, d: d.update({'../escape.txt': b'x'}),
            lambda p, d: d.update({'papers/exam.pdf': b'x'}),
            lambda p, d: d.update({'skill/code.py': b'x'}),
            lambda p, d: d.update({'tags.txt': b'tampered'}),
            lambda p, d: p.update(wtf_pack=999),
            lambda p, d: p.update(checker='unknown'),
            lambda p, d: p.update(requires_wtf='>=99.0.0'),
            lambda p, d: p['topics'][0].update(file='../secret')]
        for mutate in mutations:
            with self.subTest(mutate=mutate), self.assertRaises(ValueError):
                pack.inspect(self.archive(mutate))
        for path in ('../secret', 'methods/CON.md', 'methods/a\\b.md', '/methods/a.md', 'methods/../a.md'):
            with self.assertRaises(ValueError):
                pack.destination(path, 'MAM')
        with self.assertRaises(ValueError):
            pack.validate_sources(b'MAM/papers/NUL.pdf\thttps://example.invalid/null.pdf', 'MAM')
        good = b'MAM/papers/2025_MAM_Exam_CalcFree.pdf\thttps://example.invalid/e.pdf\t%s\t%s\t' + b'0' * 64 + b'\t1\t1\t%s'
        pack.validate_sources(good % (b'wayback', b'20250101000000', b'required'), 'MAM')
        for bad in (good % (b'wayback', b'', b'required'), good % (b'browser', b'20250101000000', b'required'),
                    good % (b'ftp', b'', b'required'), good % (b'browser', b'', b'maybe'),
                    b'MAM/papers/2025_MAM_Exam_CalcFree.pdf\thttps://example.invalid/e.pdf'):  # no metadata
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                pack.validate_sources(bad, 'MAM')

    def test_manifest_metadata_and_wrong_version_refused(self):
        import fetch
        root = self.root / 'manifest'
        (root / 'MAM').mkdir(parents=True)
        right = b'%PDF-1.4 the copy the tags were made on'
        (root / 'MAM/sources.tsv').write_text(
            '#' + '\t'.join(fetch.COLUMNS) + '\n'
            f'MAM/papers/2017_MAM_Exam_CalcFree.pdf\thttps://example.invalid/a.pdf\twayback\t20180326152405\t'
            f'{hashlib.sha256(right).hexdigest()}\t{len(right)}\t1\trequired\n'
            'MAM/papers/2017_MAM_ExamReport.pdf\thttps://example.invalid/r.pdf\tbrowser\t\t' + '0' * 64 + '\t1\t1\toptional\n',
            encoding='utf-8')
        (root / 'sources.tsv').write_text('MAM/papers/2016_MAM_Exam_CalcFree.pdf\thttps://example.invalid/old.pdf (wayback)\n',
                                          encoding='utf-8')  # a legacy root manifest of an old install still reads
        rows = {e['path']: e for e in fetch.entries(root)}
        self.assertEqual(rows['MAM/papers/2016_MAM_Exam_CalcFree.pdf']['method'], 'wayback')
        self.assertEqual(fetch.download_url(rows['MAM/papers/2017_MAM_Exam_CalcFree.pdf']),
                         'https://web.archive.org/web/20180326152405id_/https://example.invalid/a.pdf')
        missing = [m[0] for m in fetch.missing(root)]  # optional reports never block the bank
        self.assertNotIn('MAM/papers/2017_MAM_ExamReport.pdf', missing)
        self.assertIn('MAM/papers/2017_MAM_ExamReport.pdf', [m[0] for m in fetch.missing(root, optional=True)])
        downloads = self.root / 'downloads'
        downloads.mkdir()
        (downloads / 'a.pdf').write_bytes(b'%PDF-1.4 a re-issued copy')
        wrong = []
        self.assertEqual(fetch.import_dir(downloads, root, wrong), [])
        self.assertEqual(len(wrong), 1)
        (downloads / 'a.pdf').write_bytes(right)
        self.assertEqual(fetch.import_dir(downloads, root), ['MAM/papers/2017_MAM_Exam_CalcFree.pdf'])

    def test_weights_and_partial_chemistry(self):
        maths = scoring.score(self.profile, {'CalcFree': (50, 50), 'CalcAssumed': (0, 100)}, 2025)
        self.assertEqual(maths['paper_percent'], 35)
        chem = {'scoring': {'mode': 'section-weighted'}, 'sections': [
            {'code': 'MC', 'share': .25}, {'code': 'SA', 'share': .35}, {'code': 'ER', 'share': .40}]}
        result = scoring.score(chem, {'SA': (32.5, 65), 'ER': (56.5, 113)})
        self.assertIsNone(result['paper_percent'])
        self.assertEqual(result['coverage'], .75)
        self.assertEqual(result['practice_percent'], 50)
        self.assertEqual(result['weighted_contribution'], 37.5)
        chem['sections'][0]['share'] = .5
        with self.assertRaises(ValueError):
            scoring.validate(chem)
        with self.assertRaises(ValueError):
            scoring.score(self.profile, {'CalcFree': (1, 2)}, 2016)
        for values in ({'CalcFree': (3, 2)}, {'CalcFree': (0, 0)}, {'CalcFree': (float('nan'), 2)}):
            with self.assertRaises(ValueError):
                scoring.score(self.profile, values)

    def test_import_dialog_confirmation_and_restart(self):
        from kernel import Kernel
        from plugins import subject_import
        file = self.archive()
        target = self.root / 'dialog-install'
        kernel = Kernel(str(target))
        config = {'subjects': ['MAS']}
        events = []
        kernel.provide('config', config)
        kernel.provide('config.save', lambda: events.append('save'))
        kernel.provide('subjects.manage', lambda: events.append('wizard'))
        subject_import.setup(kernel)
        with patch.object(subject_import.filedialog, 'askopenfilename', return_value=str(file)), \
             patch.object(subject_import.messagebox, 'askyesno', return_value=False):
            kernel.get('subjects.import')()
        self.assertFalse(target.exists())
        self.assertEqual(events, [])
        with patch.object(subject_import.filedialog, 'askopenfilename', return_value=str(file)), \
             patch.object(subject_import.messagebox, 'askyesno', return_value=True):
            kernel.get('subjects.import')()
        self.assertEqual(events, ['save', 'wizard'])
        self.assertEqual(config['subjects'], ['MAS', 'MAM'])
        self.assertTrue((target / 'MAM/pack.json').is_file())


if __name__ == '__main__':
    unittest.main()
