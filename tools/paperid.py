"""Recognise an SCSA paper from its content. One job: PDF path -> canonical name like 'MAM/papers/2024_MAM_Exam_CalcFree.pdf'.

Browsers rename downloads ("(1)", case, the student's own name), so imports match on what the
first page says — subject, document type, section, year — not on the file name.
"""
import re
import pymupdf


def identify(path):
    """Return the canonical relative path, or None if this is not a recognisable MAM/MAS paper."""
    try:
        with pymupdf.open(path) as doc:
            text = " ".join(doc[i].get_text() for i in range(min(2, doc.page_count)))
    except Exception:
        return None
    t = re.sub(r"\s+", " ", text)
    low = t.lower()
    if "mathematics methods" in low:
        subj = "MAM"
    elif "mathematics specialist" in low:
        subj = "MAS"
    else:
        return None
    # order matters: an exam's cover lists "Formula sheet" among materials; reports quote "marking key"
    if "question/answer booklet" in low:
        kind, m = "Exam", re.search(r"examination,? (20\d\d)", low)
    elif "examination report" in low or "summary report" in low:
        kind, m = "ExamReport", re.search(r"(20\d\d) atar course examination report", low)
    elif "marking key" in low:
        kind, m = "MarkingKey", re.search(r"examination,? (20\d\d)", low)
    elif "formula sheet" in low:
        kind, m = "FormulaSheet", re.search(r"formula sheet (20\d\d)", low)
    else:
        return None
    if re.search(r"sample (wace )?examination", low) and kind in ("Exam", "MarkingKey"):
        year = "2016Sample"
    elif m:
        year = m.group(1)
    else:
        return None
    if kind in ("Exam", "MarkingKey"):
        free, assumed = low.find("calculator-free"), low.find("calculator-assumed")
        if free < 0 and assumed < 0:
            return None
        sec = "CalcFree" if assumed < 0 or 0 <= free < assumed else "CalcAssumed"
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
