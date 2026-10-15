"""Export/import three maths packs, rebuild offline, compare every original database row."""
from collections import Counter
import os
from pathlib import Path
import shutil
import sqlite3
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import pack
import fetch

with tempfile.TemporaryDirectory(prefix='wtf-pack-roundtrip-') as temporary:
    work = Path(temporary)
    data = work / 'data'
    for subject in ('MAM', 'MAS', 'MAA'):
        archive = pack.export(subject, ROOT, work / 'archives', draft=True)
        profile = pack.install(archive, data)
        print('import', subject, profile['quality'])
        for relative, *_ in fetch.sources(ROOT, [subject]):
            source = ROOT / relative
            if source.exists():
                target = data / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
    os.environ['WACE_MATHS_ROOT'] = str(data)
    import build_all
    build_all.run(['MAM', 'MAS', 'MAA'])
    import subjects
    old_bank = Path(subjects.bank_path(ROOT)).as_uri() + '?mode=ro'
    with sqlite3.connect(old_bank, uri=True) as old, sqlite3.connect(subjects.bank_path(data)) as new:
        for subject in ('MAM', 'MAS', 'MAA'):
            for table in ('questions', 'parts', 'part_patterns', 'points', 'patterns'):
                if table == 'questions':
                    sql = ('SELECT id, subject, year, section, q, marks, exam, exam_regions, key, key_regions, stem, '
                           'points_ok, figure FROM questions WHERE subject=?')  # a bank before 2.1 has no source column
                elif table == 'patterns':
                    sql = 'SELECT p.* FROM patterns p JOIN topics t ON p.topic=t.code WHERE t.subject=?'
                else:
                    sql = f'SELECT p.* FROM {table} p JOIN questions q ON p.qid=q.id WHERE q.subject=?'
                before, after = (Counter(db.execute(sql, (subject,))) for db in (old, new))
                difference = sum((before-after).values()) + sum((after-before).values())
                print(subject, table, 'rows', sum(before.values()), 'differences', difference)
                assert not difference
    # Windows connections must close before TemporaryDirectory removes its output.
    old.close()
    new.close()
print('Pack roundtrip OK: 15 table/subject comparisons, zero differing rows')
