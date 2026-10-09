"""Split a marking-key text block into one entry per mark (one tick = one mark).

One job: key text -> [(part, behaviour)]. Only lines starting with the tick glyph
(U+F050 Wingdings-2 check, or ✓) inside 'Specific behaviours' blocks count;
'Alternative solution' blocks are skipped so marks are not double counted.
"""
import re

TICK = re.compile(r"^[✓✔]\s*")
JUNK = re.compile(r"\s*(Question \d+ \(continued\)|Copyright|See next page|End of questions).*$")
PART = re.compile(r"^\(([a-z]|i{1,3}|iv|v)\)$")


def points(text):
    out, part, on, alt = [], "", False, False
    for raw in text.splitlines():
        t = raw.strip()
        if not t:
            continue
        m = PART.match(t)
        if m:
            g = m.group(1)
            sub = g in ("i", "ii", "iii", "iv", "v") and part[:1].isalpha() and part[:1] not in "iv"
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
