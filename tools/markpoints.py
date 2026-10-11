"""Split a marking-key text block into one entry per mark (one tick = one mark).

One job: key text -> [(part, behaviour)]. Only lines starting with the tick glyph
(U+F050 Wingdings-2 check, U+F0FC Wingdings check, or ✓) inside 'Specific behaviours' blocks count;
'Alternative solution' blocks are skipped so marks are not double counted.
"""
import re

TICK = re.compile(r"^[✓✔]\s*")  # Wingdings-2 check (MAM/MAS), Wingdings check (MAA 2020+)
JUNK = re.compile(r"\s*(Question \d+ \(continued\)|Copyright|See next page|End of questions).*$")
PART = re.compile(r"^\(([a-hj-l]|i{1,3}|iv|v|vi)\)$")  # part letters a–l ("(n)" is a formula, not a part)


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
