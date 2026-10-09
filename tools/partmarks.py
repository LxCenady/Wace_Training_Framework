"""Part marks from the exam paper. One job: a question's stem text -> {part label: marks} as printed.

WACE papers print "(n marks)" after every part. Part labels sit at the start of a line — (a), (b), … and
(i), (ii), … within a part — and must come in order, so function notation such as f(a) or (x) is never taken
for a label. Labels match the tag files: "a", "ai", "b", … ("" for a question without parts).
"""
import re

ROMAN = ["i", "ii", "iii", "iv", "v", "vi"]
TOKEN = re.compile(r"(?m)^\s*\(([a-h])\)|^\s*\((i{1,3}|iv|v|vi)\)|\((\d+)\s*marks?\)", re.I)


def split(stem, total):
    """{label: marks} or None when the printed marks do not add up to the question total."""
    letter, roman, out, header = "", "", {}, True
    for m in TOKEN.finditer(stem):
        lt, rm, mk = m.group(1), m.group(2), m.group(3)
        if mk:
            if header and not out and not letter and int(mk) == total:
                header = False  # "Question 7 (8 marks)"
                continue
            label = letter + roman
            out[label] = out.get(label, 0) + int(mk)
        elif lt and ord(lt) == (ord(letter) + 1 if letter else ord("a")):
            letter, roman, header = lt, "", False
        elif rm and letter and rm == ROMAN[ROMAN.index(roman) + 1 if roman else 0]:
            roman = rm
    if not out and not header:  # only the header's marks: a question without parts
        out = {"": total}
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
