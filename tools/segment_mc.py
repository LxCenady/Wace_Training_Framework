"""Multiple-choice sections. One job: an MC section of an exam + its key's answer grid -> one question per number.

Questions start at a number on its own line at the left margin ("1.", "2." …, in order). A shared stimulus
("Use the following information to answer Questions 3 and 4.", "For Question 7, consider …") is cut with every
question it serves, so each question is complete on its own. The key's grid row for the number is the question's
key region, and its answer cell ("c", or "c and d" when the key accepts either) is kept as the answer.
"""
import re
import pymupdf

NUMBER = re.compile(r"^(\d{1,2})\.?$")  # some official papers omit the dot on an otherwise identical heading
STIMULUS = re.compile(r"^(?:Use the (?:following )?information|For Questions?|Questions?\s+\d+\s+(?:and|to|–|-|refers?)|"
                      r"Refer to the (?:following )?information)", re.I)
SERVES = re.compile(r"Questions?\s+(\d+)(?:\s*(?:and|to|–|-)\s*(\d+))?", re.I)


def _lines(page, y0, y1):
    out = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            t = "".join(s["text"] for s in l["spans"]).strip()
            if t and y0 <= l["bbox"][1] < y1:
                out.append((l["bbox"], t))
    return sorted(out, key=lambda x: (x[0][1], x[0][0]))


def questions(edoc, block, bands, kdoc):
    """block: the MC section's exam regions [[page, y0, y1], …]; bands: content band per page.
    -> [{q, exam_regions, key_regions, answer}] in question order."""
    marks = []  # (kind, number(s), page, y): question heads and stimuli, in reading order
    for page, y0, y1 in block:
        for box, t in _lines(edoc[page], y0, y1):
            m = NUMBER.match(t)
            if m and box[0] < 90:
                n = int(m.group(1))
                if n == (max([x[1] for x in marks if x[0] == "q"], default=0) + 1):
                    marks.append(("q", n, page, box[1]))
            elif STIMULUS.match(t) and box[0] < 90:
                s = SERVES.search(t)
                if s:
                    a, b = int(s.group(1)), int(s.group(2) or s.group(1))
                    marks.append(("s", list(range(a, b + 1)), page, box[1]))
    end = (block[-1][0], block[-1][2])

    def span(i):
        """Regions from marks[i] to the next mark (or the end of the section)."""
        _, _, p, y = marks[i]
        ep, ey = (marks[i + 1][2], marks[i + 1][3]) if i + 1 < len(marks) else end
        regs = []
        for pg in range(p, ep + 1):
            top, bot = bands[pg]
            a = y - 3 if pg == p else top
            b = ey - 3 if pg == ep else bot
            if b - a > 12:
                regs.append([pg, round(a, 1), round(b, 1)])
        return regs

    stimulus = {}
    out = []
    for i, (kind, n, _, _) in enumerate(marks):
        if kind == "s":
            for q in n:
                stimulus[q] = span(i)
        else:
            out.append({"q": n, "exam_regions": stimulus.get(n, []) + span(i)})
    grid = answers(kdoc)
    for item in out:
        item["key_regions"], item["answer"] = grid.get(item["q"], ([], ""))
    return out


def answers(kdoc):
    """{number: (key region of its grid row, answer text)} from the key's Section One answer table."""
    found = {}
    for pg, page in enumerate(kdoc):
        ls = _lines(page, 0, page.rect.height)
        if any(t.startswith("Section Two") for _, t in ls) and found:
            break
        header = [b[1] for b, t in ls if re.match(r"Question(?: No\.?)?$", t)]  # the grid's "Question | Answer" head
        if not header:
            continue
        for box, t in ls:
            if not re.fullmatch(r"\d{1,2}", t) or box[0] > page.rect.width / 2 or box[1] <= min(header):
                continue
            n = int(t)
            mid = (box[1] + box[3]) / 2
            # answer cells to its right on the same row: "c", "c and d" (either accepted) or "All" (every option
            # accepted, e.g. a flawed question); the closest one vertically, never the "Answer" heading
            row = sorted(((b, s) for b, s in ls if b[0] > box[2] and min(b[3], box[3]) > max(b[1], box[1]) + 1
                          and re.fullmatch(r"(?:[a-dA-D](?:\s*(?:,|and|or|/)\s*[a-dA-D])*|All)\s*\*?", s)),
                         key=lambda x: abs((x[0][1] + x[0][3]) / 2 - mid))
            if row and n not in found:
                y0, y1 = min(box[1], row[0][0][1]) - 3, max(box[3], row[0][0][3]) + 3
                found[n] = ([[pg, round(y0, 1), round(y1, 1)]], row[0][1].rstrip(" *").lower())
    return found
