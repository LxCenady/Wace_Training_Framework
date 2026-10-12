"""Split a marking-key text block into one entry per mark (one tick = one mark).

One job: key text -> [(part, behaviour)]. Only lines starting with the tick glyph
(U+F050 Wingdings-2 check, U+F0FC Wingdings check, or ✓) inside 'Specific behaviours' blocks count;
'Alternative solution' blocks are skipped so marks are not double counted.
"""
import re

TICK = re.compile(r"^[✓✔]\s*")  # Wingdings-2 check (MAM/MAS), Wingdings check (MAA 2020+)
JUNK = re.compile(r"\s*(Question \d+ \(continued\)|Copyright|See next page|End of questions).*$")
PART = re.compile(r"^\(([a-hj-l]|i{1,3}|iv|v|vi)\)$")  # part letters a–l ("(n)" is a formula, not a part)


MARKS = re.compile(r"^(\d{1,2})(?:\s*[–-]\s*(\d{1,2}))?$")  # "1", or a range "1–2" (the upper bound counts)
# a reduced award for the row above ("One error or omission  1"), not a further mark
PARTIAL = re.compile(r"^(?:One|Two|1|2|Any one|A single|Minor) (?:error|omission|mistake)s?\b|^(?:Partially|Partial)\b"
                     r"|^(?:Some|Limited) (?:relevant|correct)", re.I)


# wording of a reduced award ("correct species but not balanced  2", "Has one minor error or omission  1")
REDUCED = re.compile(r"\b(?:minor|partial|partially|incorrect|incomplete|missing|errors?|omissions?|mistakes?"
                     r"|not balanced|but not)\b", re.I)
# the lead-in of a part's roman sub-parts: "(i) writing …" is instruction text in the key, not a part
ROMAN_LABEL = ("i", "ii", "iii", "iv", "v", "vi")


def rubric(text, band_continuation=False):
    """Description/Marks tables (science keys): one entry per mark, the description repeated for a 2-mark row.

    Each part's first table counts; a second table after its "Total" is an alternative solution and is skipped,
    and "Total"/"Subtotal" rows are sums, not marks. Descriptions keep their "Alternatively …" wording.
    A row with fewer marks than the row above it, worded as a reduced award, is skipped. A mark row with no
    description text (a structure drawn in the key) still counts. Roman labels before any letter part are text."""
    out, part, desc, done, skip_number, top = [], "", [], False, False, 0
    band = None  # last range row; an unnumbered tail before Total can continue its description
    lines = [raw.strip() for raw in text.splitlines()]
    lines = [t for t in lines if t]
    start, pending, soft = 0, [], []  # pending: mark rows with no description, counted only if the table's Total agrees
    # soft: (start, end) of rows worth fewer marks than the row above; dropped at the Total when that makes it agree
    for i, t in enumerate(lines):
        m = PART.match(t)
        if m and not (m.group(1) in ROMAN_LABEL and not part):
            g = m.group(1)
            sub = g in ("i", "ii", "iii", "iv", "v", "vi") and part[:1].isalpha() and part[:1] not in "iv"
            if g == "i" and part == "h" and any(p == "h" for p, _ in out):
                part = "i"  # (h) already has its own marks: this is part (i), not (h)(i)
            else:
                part = part[:1] + g if sub else g
            desc, done, top, start, pending, soft = [], False, 0, len(out), [], []
            band = None
            continue
        if done:
            continue
        if re.fullmatch(r"(Sub)?[Tt]otal", t):
            if band_continuation and band and desc:
                tail = " ".join(desc).strip()
                for row in out[band[0]:band[1]]:
                    row[1] += " " + tail
            band = None
            value = int(lines[i + 1]) if i + 1 < len(lines) and lines[i + 1].isdigit() else None
            if soft and value is not None and len(out) - start > value:
                drop, left = set(), len(out) - start
                for a, b in reversed(soft):  # the lower rows are reduced awards: drop them, last first, while over the Total
                    if left <= value:
                        break
                    drop.update(range(a, b))
                    left -= b - a
                if left == value:
                    out = [e for j, e in enumerate(out) if j not in drop]
            if pending and value is not None and len(out) - start + sum(pending) == value:
                out += [[part, "(a drawn answer: see the marking key image)"] for _ in range(sum(pending))]
            if t == "Total":
                done = True
            skip_number, desc, top, start, pending, soft = True, [], 0, len(out), [], []
            continue
        if re.fullmatch(r"Description|Marks|Description\s+Marks", t) or JUNK.fullmatch(t) or t.startswith("©"):
            if t.startswith("Description"):
                desc, start, pending, soft = [], len(out), [], []
                band = None
            continue
        n = MARKS.match(t)
        if n:
            if skip_number:
                skip_number = False
                continue
            marks = int(n.group(2) or n.group(1))
            text_ = " ".join(desc).strip()
            if marks > 8 or (desc and re.search(r"(?:×|x|\*)\s*10\s*[–-]?$", desc[-1])):
                desc.append(t)  # the exponent of "× 10⁹" split onto its own line, not a mark
                continue
            if not text_:
                if marks:
                    pending.append(marks)
                continue
            reduced = bool(top and marks < top and REDUCED.search(text_))
            lower = bool(top and marks < top) and not reduced
            row_start = len(out)
            if marks and not reduced and not PARTIAL.match(text_):
                note = f" ({marks} marks)" if marks > 1 else ""
                if lower:
                    soft.append((len(out), len(out) + marks))
                out += [[part, text_ + note] for _ in range(marks)]
            band = (row_start, len(out)) if n.group(2) and len(out) > row_start else None
            if marks and not reduced and not lower:
                top = marks
            desc = []
            continue
        if re.fullmatch(r"\(.*\)", t) and REDUCED.search(t):
            continue  # "(one minor error)": the note that goes with a reduced award, not a description
        skip_number = False
        desc.append(t)
    return out


def points(text):
    out, part, on, alt = [], "", False, False
    for raw in text.splitlines():
        t = raw.strip()
        if not t:
            continue
        m = PART.match(t)
        if m:
            g = m.group(1)
            if g == "i" and part == "h" and any(p == "h" for p, _ in out):
                part = "i"  # (h) already has its own ticks: this is part (i), not (h)(i)
            else:
                sub = g in ("i", "ii", "iii", "iv", "v", "vi") and part[:1].isalpha() and part[:1] not in "iv"
                part = part[:1] + g if sub else g
            on = alt = False
            continue
        if re.match(r"(Alternative|Alternate)", t, re.I):
            alt = True
            continue
        if re.match(r"Specific behaviou?rs", t, re.I):
            on = True
            continue
        if re.match(r"Solution\b", t):
            on = False
            continue
        if not on or alt:
            continue
        if TICK.match(t):
            out.append([part, TICK.sub("", t)])
        elif out and len(t) > 1 and not t.startswith("©"):
            out[-1][1] += " " + t  # wrapped behaviour line
    return [[part, JUNK.sub("", b).strip()] for part, b in out]
