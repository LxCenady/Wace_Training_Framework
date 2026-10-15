"""Recognise a past paper from its content. One job: PDF path -> canonical name like 'MAM/papers/2024_MAM_Exam_CalcFree.pdf'.

Browsers rename downloads ("(1)", case, the student's own name), so imports match on what the
first page says — subject, document type, section, year — not on the file name. What each document says is the
subject pack's business (pack.json "recognise"); a pack that says nothing gets SCSA's wording (DEFAULTS).
"""
import re
import pymupdf
import subjects

# SCSA's covers. A pack for another exam board names its own phrases in pack.json "recognise" (same keys).
DEFAULTS = {
    "exam": ["question/answer booklet"],              # the paper students write in
    "report": ["examination report", "summary report"],
    "key": ["marking key"],
    "year": [r"(20\d\d) atar course examination report", r"examination,? (20\d\d)"],  # first group = the year
    "sample": [r"sample (wace )?examination"],         # a sample paper: year "<sample_year>"
    "sample_year": "2016Sample",
}


def rule(profile, name):
    return profile["recognise"].get(name, DEFAULTS[name])


def year_of(low, profile, words=()):
    """The year printed next to the document's own name (a reference sheet's), else by the pack's year patterns."""
    patterns = ["(?:" + "|".join(re.escape(w.lower()) for w in words) + r"),? (20\d\d)"] if words else []
    for pattern in patterns + rule(profile, "year"):
        m = re.search(pattern, low)
        if m:
            return m
    return None


def kind_of(low, profile):
    """-> (kind, year match) from the lower-cased text, or None."""
    # order matters: an exam's cover lists "Formula sheet" among materials; reports quote "marking key"
    for kind, name in (("Exam", "exam"), ("ExamReport", "report"), ("MarkingKey", "key")):
        if any(w.lower() in low for w in rule(profile, name)):
            return kind, year_of(low, profile)
    # the pack's reference sheets: {"FormulaSheet": ["formula sheet", …], "DataBooklet": ["data booklet"]}
    kinds = [(k, words) for k, words in profile['recognise'].get('kinds', {}).items()
             if any(w.lower() in low for w in words)]
    if not kinds:
        return None
    kind, words = kinds[0]
    return kind, year_of(low, profile, words)  # "ATAR course examination, 2025 … booklet" too


def identify(path):
    """Return the canonical relative path, or None if this is not a recognisable paper of an installed subject."""
    try:
        with pymupdf.open(path) as doc:
            pages = [doc[i].get_text() for i in range(min(2, doc.page_count))]
    except Exception:
        return None
    low = re.sub(r"\s+", " ", " ".join(pages)).lower()
    matches = [s for s, p in subjects.profiles(engine="flow").items()
               if any(title.lower() in low for title in p['recognise']['title'])]
    if len(matches) != 1:
        return None
    subj = matches[0]
    profile = subjects.info(subj)
    # the cover says what the document is; the second page only when the cover alone does not (a booklet's second
    # page can mention the question/answer booklet it goes with)
    for text in (re.sub(r"\s+", " ", pages[0]).lower(), low):
        found = kind_of(text, profile)
        if found:
            kind, m = found
            break
    else:
        return None
    if any(re.search(p, low) for p in rule(profile, "sample")) and kind in ("Exam", "MarkingKey"):
        year = rule(profile, "sample_year")
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
