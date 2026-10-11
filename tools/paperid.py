"""Recognise an SCSA paper from its content. One job: PDF path -> canonical name like 'MAM/papers/2024_MAM_Exam_CalcFree.pdf'.

Browsers rename downloads ("(1)", case, the student's own name), so imports match on what the
first page says — subject, document type, section, year — not on the file name.
"""
import re
import pymupdf
import subjects


def identify(path):
    """Return the canonical relative path, or None if this is not a recognisable MAM/MAS/MAA paper."""
    try:
        with pymupdf.open(path) as doc:
            text = " ".join(doc[i].get_text() for i in range(min(2, doc.page_count)))
    except Exception:
        return None
    t = re.sub(r"\s+", " ", text)
    low = t.lower()
    matches = [s for s, p in subjects.profiles().items()
               if any(title.lower() in low for title in p['recognise']['title'])]
    if len(matches) != 1:
        return None
    subj = matches[0]
    profile = subjects.info(subj)
    # order matters: an exam's cover lists "Formula sheet" among materials; reports quote "marking key"
    if "question/answer booklet" in low:
        kind, m = "Exam", re.search(r"examination,? (20\d\d)", low)
    elif "examination report" in low or "summary report" in low:
        kind, m = "ExamReport", re.search(r"(20\d\d) atar course examination report", low)
    elif "marking key" in low:
        kind, m = "MarkingKey", re.search(r"examination,? (20\d\d)", low)
    else:  # the pack's reference sheets: {"FormulaSheet": ["formula sheet", …], "DataBooklet": ["data booklet"]}
        kinds = [(k, words) for k, words in profile['recognise'].get('kinds', {}).items()
                 if any(w.lower() in low for w in words)]
        if not kinds:
            return None
        kind, words = kinds[0]
        m = re.search("(?:" + "|".join(re.escape(w.lower()) for w in words) + r"),? (20\d\d)", low)
    if re.search(r"sample (wace )?examination", low) and kind in ("Exam", "MarkingKey"):
        year = "2016Sample"
    elif m:
        year = m.group(1)
    else:
        return None
    if kind in ("Exam", "MarkingKey"):
        if profile.get('paper_layout') == 'shared':
            return f"{subj}/papers/{year}_{subj}_{kind}.pdf"
        found = [(low.find(word.lower()), section['code']) for section in profile['sections']
                 for word in section.get('recognise', [section['en']]) if word.lower() in low]
        if not found:
            return None
        sec = min(found)[1]
        return f"{subj}/papers/{year}_{subj}_{kind}_{sec}.pdf"
    return f"{subj}/papers/{year}_{subj}_{kind}.pdf"


if __name__ == "__main__":  # self-check: every paper on disk must be recognised as itself
    import glob, os, sys
    root = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    bad = 0
    for f in sorted(glob.glob(os.path.join(root, "*", "papers", "*.pdf"))):
        rel = os.path.relpath(f, root).replace(os.sep, "/")
        got = identify(f)
        if got is None and not "".join(p.get_text() for p in pymupdf.open(f)).strip():
            print("skip (scanned image, no text layer)", rel)
        elif got != rel:
            bad += 1
            print("MISMATCH", rel, "->", got)
    print(bad, "mismatches")
    sys.exit(1 if bad else 0)
