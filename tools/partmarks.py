"""Part marks from the exam paper. One job: a question's stem text -> {part label: marks} as printed.

WACE papers print "(n marks)" after every part. Part labels sit at the start of a line — (a), (b), … and
(i), (ii), … within a part — and must come in order, so function notation such as f(a) or (x) is never taken
for a label. Labels match the tag files: "a", "ai", "b", … ("" for a question without parts).
"""
import re

ROMAN = ["i", "ii", "iii", "iv", "v", "vi"]
# letters a–h and j–l; "(i)" goes through the roman branch, which decides between part i and sub-part (i)
TOKEN = re.compile(r"(?m)^\s*\(([a-hj-l])\)|^\s*\((i{1,3}|iv|v|vi)\)|\((\d+)\s*marks?\)", re.I)


def split(stem, total, nested_totals=False):
    """{label: marks} or None when the printed marks do not add up to the question total."""
    letter, roman, out, header, has_marks = "", "", {}, True, False
    first = {}
    for m in TOKEN.finditer(stem):
        lt, rm, mk = m.group(1), m.group(2), m.group(3)
        if mk:
            if header and not out and not letter and int(mk) == total:
                header = False  # "Question 7 (8 marks)"
                continue
            label = letter + roman
            first.setdefault(label, int(mk))
            out[label] = out.get(label, 0) + int(mk)
            has_marks = True  # current letter part has printed marks
        elif lt and ord(lt) == (ord(letter) + 1 if letter else ord("a")):
            letter, roman, header, has_marks = lt, "", False, False
        elif rm and letter:
            # (i) after letter "h" with printed marks is letter i, not roman sub-part
            if has_marks and not roman and rm == "i" and letter == "h":
                letter, roman, header, has_marks = "i", "", False, False
            elif rm == ROMAN[ROMAN.index(roman) + 1 if roman else 0]:
                roman = rm
    if not out and not header:  # only the header's marks: a question without parts
        out = {"": total}
    if out and sum(out.values()) != total and nested_totals:
        candidate = dict(first)
        for label in list(first):
            children = [k for k in first if len(label) == 1 and len(k) > 1 and k[:1] == label]
            if children:
                if sum(first[k] for k in children) != first[label]:
                    return None
                candidate.pop(label, None)
        if sum(candidate.values()) == total:
            return candidate
    if not out or sum(out.values()) != total:
        return None
    return out


def for_tags(found, labels):
    """Marks for the tagged labels: a tag on "a" sums (a)(i), (a)(ii)…; None when a tag finds no marks."""
    out = {}
    for label in labels:
        n = found.get(label) if label in found else sum(v for k, v in found.items() if k[:1] == label and label)
        if not label:
            n = sum(found.values())
        if not n:
            return None
        out[label] = n
    return out if sum(out.values()) == sum(found.values()) else None


def texts(stem):
    """{part label: its text as printed} — same label rules as split(); text before (a) is left out."""
    letter, roman, out, label, start, has_marks = "", "", {}, None, 0, False
    for m in TOKEN.finditer(stem):
        lt, rm, mk = m.group(1), m.group(2), m.group(3)
        new = None
        if mk:
            has_marks = True  # current letter part has printed marks
        if lt and ord(lt) == (ord(letter) + 1 if letter else ord("a")):
            letter, roman, has_marks = lt, "", False
            new = letter
        elif rm and letter:
            # (i) after letter "h" with printed marks is letter i, not roman sub-part
            if has_marks and not roman and rm == "i" and letter == "h":
                letter, roman, has_marks = "i", "", False
                new = "i"
            elif rm == ROMAN[ROMAN.index(roman) + 1 if roman else 0]:
                roman = rm
                new = letter + roman
        if new:
            if label is not None:
                out[label] = out.get(label, "") + stem[start:m.start()]
            label, start = new, m.start()
    out[label if label is not None else ""] = out.get(label if label is not None else "", "") + stem[start:]
    return out


def preamble(stem):
    """The lead-in every part shares: the text before (a) (the whole stem when there are no parts)."""
    found = texts(stem)
    if "" in found:
        return stem
    return stem[:min(stem.index(t) for t in found.values() if t)]


def tagged_texts(found, labels):
    """Text for the tagged labels: a tag on "a" gets (a) and its (i), (ii)…; a tag on "ai" gets (a)(i) only;
    "" gets the whole stem."""
    def text(label):
        if not label:
            return "".join(found.values())
        if len(label) > 1:  # a sub-part
            return found.get(label, "")
        return "".join(v for k, v in found.items() if k[:1] == label)
    return {label: text(label) for label in labels}


SKETCH = re.compile(
    r"(?<!the )\b(?:sketch|draw|plot|shade)\b(?![^.\n]{0,40}\b(?:is|are|was|were)\b)"
    r"|\b(?:show(?! that)|add|represent|mark|label|indicate|illustrate|locate)\b[^.\n]{0,80}"
    r"\bon (?:the|this|an?|your) (?:axes|grid|argand diagram|diagram|graph|number line|slope field)"
    r"|\bcomplete the (?:graph|graphical|diagram|sketch)", re.I)
SPARE = re.compile(r"redrawn it on the spare", re.I)  # the paper's note under parts answered on a grid / diagram


FIGURE = re.compile(
    r"\b(?:shown|graphed|plotted|drawn|sketched|displayed|illustrated|pictured)\b[^.\n]{0,40}\b(?:below|above|opposite)\b"
    r"|\b(?:diagram|graph|axes|figure|argand (?:diagram|plane)|complex plane|slope field|grid)\s+"
    r"(?:below|above|shown|provided|opposite)"
    r"|\bthe (?:diagram|figure)\b|\bon the axes\b|\bslope field\b|\bhistogram\b"
    r"|\b(?:is|are|been|as) shown\b|\bshown (?:along|with|for|in)\b|\bcoordinate system shown\b", re.I)


def has_figure(stem):
    """True when the question shows a figure: a graph, diagram, Argand diagram, slope field or axes to draw on."""
    return bool(FIGURE.search(stem) or SPARE.search(stem))


def is_sketch(text, subject=None):
    """True when the part asks the student to draw: sketch / draw / plot / shade / mark or label on a diagram."""
    if subject is not None:
        import subjects
        profile = subjects.info(subject)
        if profile.get('sketch_mode', 'words') != 'legacy-maths':
            return any(re.search(r'\b' + re.escape(word) + r'\b', text, re.I)
                       for word in profile.get('sketch_words', []))
    return bool(SKETCH.search(text) or SPARE.search(text))
