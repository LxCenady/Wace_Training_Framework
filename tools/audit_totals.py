"""Compare summed question marks with the section total printed in each paper."""
import json, re, sys, os, collections, pymupdf
import subjects
ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOTAL = re.compile(r'(Section\s+(?:One|Two|Three|Four).{0,140}?)\((\d+)\s*Marks\)', re.I | re.S)


def printed_totals(text, section):
    normal = lambda value: re.sub(r'[\s-]+', ' ', value).lower()
    words = section.get('recognise', [section['en']])
    return sorted({int(m.group(2)) for m in TOTAL.finditer(text)
                   if any(normal(word) in normal(m.group(1)) for word in words)})


def audit(subject):
    with open(f'{ROOT}/{subject}/questions.json', encoding='utf-8') as file:
        questions = json.load(file)
    by = collections.defaultdict(list)
    for question in questions:
        by[question['exam'], question['section']].append(question)
    bad = 0
    shared = subjects.info(subject).get('paper_layout') == 'shared'  # totals at each section's entrance
    for (exam, code), rows in sorted(by.items()):
        with pymupdf.open(os.path.join(ROOT, exam)) as doc:
            text = ' '.join(doc[i].get_text() for i in range(doc.page_count if shared else min(6, doc.page_count)))
        section = next(s for s in subjects.sections(subject) if s['code'] == code)
        printed = printed_totals(text, section)
        total = sum(q['marks'] for q in rows)
        ok = total in printed
        bad += not ok
        print('OK' if ok else 'BAD', os.path.basename(exam), code, 'sum', total, 'printed', printed)
    return bad


if __name__ == '__main__':
    bad = sum(audit(subject) for subject in sys.argv[1:])
    print('mismatches:', bad)
    sys.exit(bool(bad))
