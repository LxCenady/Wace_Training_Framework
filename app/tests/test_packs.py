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
        self.payload = {'sources.tsv': b'MAM/papers/2025_MAM_Exam_CalcFree.pdf\thttps://example.invalid/exam.pdf\n',
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
