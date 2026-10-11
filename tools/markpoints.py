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


def rubric(text):
    """Description/Marks tables (science keys): one entry per mark, the description repeated for a 2-mark row.

    Each part's first table counts; a second table after its "Total" is an alternative solution and is skipped,
    and "Total"/"Subtotal" rows are sums, not marks. Descriptions keep their "Alternatively …" wording."""
    out, part, desc, done, skip_number = [], "", [], False, False
    for raw in text.splitlines():
        t = raw.strip()
        if not t:
            continue
        m = PART.match(t)
        if m:
            g = m.group(1)
            sub = g in ("i", "ii", "iii", "iv", "v", "vi") and part[:1].isalpha() and part[:1] not in "iv"
            part = part[:1] + g if sub else g
            desc, done = [], False
            continue
        if done:
            continue
        if re.fullmatch(r"(Sub)?[Tt]otal", t):
            if t == "Total":
                done = True
            skip_number, desc = True, []
            continue
        if re.fullmatch(r"Description|Marks|Description\s+Marks", t) or JUNK.fullmatch(t) or t.startswith("©"):
            desc = [] if t.startswith("Description") else desc
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
            if text_ and marks and not PARTIAL.match(text_):
                note = f" ({marks} marks)" if marks > 1 else ""
                out += [[part, text_ + note] for _ in range(marks)]
            desc = []
            continue
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
