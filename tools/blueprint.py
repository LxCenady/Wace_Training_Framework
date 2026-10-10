"""Paper blueprints from the past papers. One job: wace.db -> how real papers are built, per subject and section.

  topic_share     share of marks per topic
  question_marks  marks of every question since 2020 (the distribution new papers sample from)
  question_count  questions per paper since 2020
  cross_topic     pattern pairs from different topics that appear in the same past question, with counts
  own_marks       marks each pattern carried within one real question (wace.db view pattern_marks: the parts'
                  marks as printed on the paper, shared evenly when a part has several patterns)
  skeletons       every real question as {pattern: marks it carried}: the shapes new papers are built from

python tools/blueprint.py  rewrites the "Paper blueprint" block of both question-generation skills.
"""
import os, re, sqlite3, sys
from collections import Counter, defaultdict
from itertools import combinations

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def round_split(own, total):
    """{pattern: float marks} -> integers >= 1 summing to `total` (largest remainder)."""
    scale = total / sum(own.values())
    out = {p: max(1, int(v * scale)) for p, v in own.items()}
    for p in sorted(own, key=lambda p: -(own[p] * scale - int(own[p] * scale))):
        if sum(out.values()) >= total:
            break
        out[p] += 1
    while sum(out.values()) > total and max(out.values()) > 1:
        out[max(out, key=out.get)] -= 1
    return out


def blueprint(db, subj, section, since=2020):
    q = lambda sql, *a: db.execute(sql, a).fetchall()  # noqa: E731
    share, pattern_share, cross = defaultdict(float), defaultdict(float), Counter()
    by_question, own = defaultdict(set), defaultdict(lambda: defaultdict(float))
    rows = q("""SELECT qid, pattern, topic, marks, question_marks FROM pattern_marks
                WHERE subject = ? AND section = ?""", subj, section)  # wace.db: marks as printed on the paper
    q_marks = {}
    for qid, pattern, t, marks, qm in rows:
        share[t] += marks
        pattern_share[pattern] += marks
        own[qid][pattern] += marks
        by_question[qid].add(pattern)
        q_marks[qid] = qm
    skeletons = [round_split(o, q_marks[qid]) for qid, o in own.items()]
    own_marks = defaultdict(list)
    for sk in skeletons:
        for p, m in sk.items():
            own_marks[p].append(m)
    for pats in by_question.values():
        for a, b in combinations(sorted(pats), 2):
            if a.rsplit(".", 1)[0] != b.rsplit(".", 1)[0]:
                cross[(a, b)] += 1
    total = sum(share.values())
    topics_of = {qid: {p.rsplit(".", 1)[0] for p in pats} for qid, pats in by_question.items()}
    multi = sum(1 for ts in topics_of.values() if len(ts) > 1)
    # topic association in multi-topic questions: how often a topic's questions span two topics, and with which
    seen, crossed, pair = Counter(), Counter(), Counter()
    for ts in topics_of.values():
        seen.update(ts)
        if len(ts) > 1:
            crossed.update(ts)
            pair.update((a, b) for a in ts for b in ts if a != b)
    return {
        "cross_rate": multi / max(1, len(by_question)),  # share of real questions that span two topics
        "topic_cross_rate": {t: crossed[t] / seen[t] for t in seen},  # P(cross-topic | the question has t)
        "topic_partner": {a: {b: n / crossed[a] for (x, b), n in pair.items() if x == a}  # P(b | a, cross)
                          for a in crossed},
        "topic_pair_count": {tuple(sorted(k)): n for k, n in pair.items()},
        "topic_share": {t: v / total for t, v in sorted(share.items(), key=lambda x: -x[1])},
        "pattern_share": dict(pattern_share),
        "question_marks": [m for (m,) in q("SELECT marks FROM questions WHERE subject = ? AND section = ? AND year >= ?",
                                           subj, section, since)],
        "question_count": [n for (n,) in q("""SELECT COUNT(*) FROM questions WHERE subject = ? AND section = ?
                                              AND year >= ? GROUP BY year""", subj, section, since)],
        "cross_topic": cross.most_common(),
        "own_marks": {p: sorted(v) for p, v in own_marks.items()},
        "skeletons": skeletons,
    }


def pattern_marks(db, subj, section):
    """{pattern: (low, high)} — the middle of the marks each pattern carried in one real question of that section
    (all sections when section is not CalcFree/CalcAssumed)."""
    secs = [section] if section in ("CalcFree", "CalcAssumed") else ["CalcFree", "CalcAssumed"]
    pooled = defaultdict(list)
    for sec in secs:
        for p, v in blueprint(db, subj, sec)["own_marks"].items():
            pooled[p] += v
    out = {}
    for p, v in pooled.items():
        v = sorted(v)
        out[p] = (v[len(v) // 4], v[(3 * len(v)) // 4])
    return out


LEVELS = ("基础", "标准", "拔高")


def pattern_drawing(db, subj, section):
    """{pattern: (figure rate, drawing rate, questions)} from real questions of that section (all sections when
    section is not CalcFree/CalcAssumed): how often a question on the pattern shows a figure, and how often a part
    on it asks the student to sketch / draw / plot / shade / mark on a diagram."""
    secs = ("CalcFree", "CalcAssumed") if section not in ("CalcFree", "CalcAssumed") else (section,)
    rows = db.execute(f"""SELECT pp.pattern, q.id, MAX(q.figure), MAX(p.sketch) FROM part_patterns pp
                           JOIN parts p ON p.qid = pp.qid AND p.label = pp.label JOIN questions q ON q.id = pp.qid
                           WHERE q.subject = ? AND q.section IN ({",".join("?" * len(secs))})
                           GROUP BY pp.pattern, q.id""", (subj, *secs)).fetchall()
    acc = defaultdict(lambda: [0, 0, 0])
    for pattern, _, fig, sketch in rows:
        a = acc[pattern]
        a[0] += fig or 0
        a[1] += sketch or 0
        a[2] += 1
    return {p: (f / n, s / n, n) for p, (f, s, n) in acc.items()}


def topic(code):
    return code.rsplit(".", 1)[0]


def plan(bp, total, rng, swap=0.35, tries=300):
    """A random paper that follows the blueprint -> [(pattern codes, marks, difficulty, {pattern: marks})].

    Every question is built on the shape of a real question of the same section: its patterns and the marks
    each carried. A big question is therefore several patterns' parts, never one pattern stretched to 12 marks.
    Randomness: the shape is drawn from the topic the paper needs most (its historical share of marks), each
    pattern may be swapped for another of the same topic that has carried about that many marks (within one) in a
    real question,
    and marks move by one inside each pattern's observed range. Cross-topic questions come from real
    cross-topic shapes, so their rate and pairings follow the real papers. Question count stays inside the
    real range; difficulty rises through the paper with some jitter."""
    for _ in range(tries):
        paper = attempt(bp, total, rng, swap)
        if paper:
            return paper
    raise RuntimeError("no paper fits the blueprint")


def attempt(bp, total, rng, swap):
    own = bp["own_marks"]
    rng_of = {p: (v[0], v[-1]) for p, v in own.items()}
    cap = max(bp["question_marks"])
    by_topic = defaultdict(dict)
    for code, w in bp["pattern_share"].items():
        by_topic[topic(code)][code] = w
    lead = lambda sk: max({topic(p) for p in sk}, key=lambda t: sum(m for p, m in sk.items() if topic(p) == t))  # noqa: E731
    deficit = {t: share * total for t, share in bp["topic_share"].items()}
    left, used, qs = total, set(), []
    while left >= 3:
        t = max(deficit, key=lambda t: deficit[t] + rng.uniform(0, 4))
        cands = [sk for sk in bp["skeletons"] if sum(sk.values()) <= left and lead(sk) == t] or                 [sk for sk in bp["skeletons"] if sum(sk.values()) <= left]
        if not cands:
            break
        sk = rng.choices(cands, weights=[1 / (1 + len(used & sk.keys())) ** 2 for sk in cands])[0]
        split = {}
        for p, m in sk.items():
            alt = {c: w for c, w in by_topic[topic(p)].items()
                   if c not in used and c not in sk and c not in split and any(abs(x - m) <= 1 for x in own[c])}
            if alt and rng.random() < swap:
                p = rng.choices(list(alt), weights=list(alt.values()))[0]
            split[p] = split.get(p, 0) + m
        if rng.random() < 0.3:  # one mark more or less on one pattern, inside what it has carried
            p, d = rng.choice(list(split)), rng.choice((-1, 1))
            if rng_of[p][0] <= split[p] + d <= rng_of[p][1] and 0 < sum(split.values()) + d <= min(cap, left):
                split[p] += d
        for p, m in split.items():
            deficit[topic(p)] -= m
        used |= split.keys()
        left -= sum(split.values())
        qs.append(split)
    while left > 0:  # absorb the last marks inside each pattern's range and the largest real question
        room = [(i, p) for i, sp in enumerate(qs) for p in sp if sp[p] < rng_of[p][1] and sum(sp.values()) < cap]
        if not room:
            return None
        i, p = rng.choice(room)
        qs[i][p] += 1
        left -= 1
    if not min(bp["question_count"]) <= len(qs) <= max(bp["question_count"]):
        return None
    qs.sort(key=lambda sp: sum(sp.values()))
    for i in range(len(qs) - 1):  # mostly small-to-large, like the papers, but not strictly
        if rng.random() < 0.3:
            qs[i], qs[i + 1] = qs[i + 1], qs[i]
    paper = []
    for pos, sp in enumerate(qs):
        x = pos / max(1, len(qs) - 1) + rng.uniform(-0.12, 0.12)
        codes = sorted(sp, key=lambda p: -sp[p])
        paper.append((codes, sum(sp.values()), LEVELS[0] if x < 0.3 else LEVELS[2] if x > 0.75 else LEVELS[1], sp))
    return paper


def markdown(db, subj):
    names = dict(db.execute("SELECT code, en FROM topics").fetchall())
    cols = {r[1] for r in db.execute("PRAGMA table_info(patterns)")}
    title = "COALESCE(NULLIF(title_en, ''), title)" if "title_en" in cols else "title"
    titles = dict(db.execute(f"SELECT code, {title} FROM patterns").fetchall())
    short = lambda c: f"{c} {titles.get(c, '').split('★')[0].split('（')[0].strip()}"  # noqa: E731
    out = ["<!-- blueprint:start (generated by tools/blueprint.py from wace.db — do not edit by hand) -->",
           "## Paper blueprint (from the 2016–2025 papers)", "",
           "Use this when writing a set or a mock paper: **randomise** (vary question count, marks per question, "
           "which patterns appear, and order within the difficulty ramp — never the same paper twice), but keep the "
           "**topic mark distribution** close to the real one below, and make the stated share of questions "
           "**cross-topic** (two topics in one question), using only pairings that real papers use.", ""]
    for section, label in (("CalcFree", "Calculator-free"), ("CalcAssumed", "Calculator-assumed")):
        bp = blueprint(db, subj, section)
        marks = sorted(bp["question_marks"])
        out += [f"### {label}", "",
                f"- Questions per paper (2020–2025): {min(bp['question_count'])}–{max(bp['question_count'])}; "
                f"marks per question: {marks[0]}–{marks[-1]} (median {marks[len(marks) // 2]}).",
                "- Share of marks by topic: " + ", ".join(f"{names.get(t, t)} {v:.0%}" for t, v in
                                                          bp["topic_share"].items()) + ".",
                f"- Cross-topic questions: {bp['cross_rate']:.0%} of real questions combine two topics. "
                "How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic "
                "questions):", ""]
        for t, rate in sorted(bp["topic_cross_rate"].items(), key=lambda x: -x[1]):
            partners = bp["topic_partner"].get(t, {})
            if partners:
                out.append(f"  - **{names.get(t, t)}** — {rate:.0%} of its questions are cross-topic; pairs with "
                           + ", ".join(f"{names.get(b, b)} {p:.0%}" for b, p in
                                       sorted(partners.items(), key=lambda x: -x[1])) + ".")
        own = bp["own_marks"]
        by_t = defaultdict(list)
        for c in sorted(own, key=lambda c: (topic(c), int(c.rsplit(".", 1)[1]))):
            v = own[c]
            lo, hi = v[len(v) // 4], v[(3 * len(v)) // 4]
            by_t[topic(c)].append(f"`{c}` {lo}" + (f"–{hi}" if hi != lo else "") + f" (max {v[-1]})")
        out += ["", "- **Marks one pattern carries within a question** (middle half of real questions, and the "
                "largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four "
                "patterns' parts, or one pattern that real papers really do run that long — never one routine "
                "step inflated to fill the marks:", ""]
        out += [f"  - {names.get(t, t)}: " + ", ".join(v) for t, v in by_t.items()]
        draw = pattern_drawing(db, subj, section)
        figs = [f"`{c}` {f:.0%}" for c, (f, d, n) in sorted(draw.items(), key=lambda x: -x[1][0]) if f >= 0.5 and n >= 2]
        sketch = [f"`{c}` {d:.0%}" for c, (f, d, n) in sorted(draw.items(), key=lambda x: -x[1][1]) if d >= 0.2 and n >= 2]
        out += ["", "- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of "
                "questions): " + (", ".join(figs) or "none") + ". Patterns whose real questions often ask the "
                "student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an "
                "Argand diagram, mark a point (share of questions): " + (", ".join(sketch) or "none") + ". Give these "
                "a figure (the axes or diagram the student works on) and, about as often as real papers do, a "
                "drawing part whose marks reward visible features; put the completed drawing in the marking key."]
        out += ["", "- Tag combinations real questions used (pattern codes, count), by topic pair — combine "
                "patterns like these; other patterns of the same two topics are fine when the pairing is natural:", ""]
        by_pair = defaultdict(list)
        for (a, b), n in bp["cross_topic"]:
            by_pair[tuple(sorted((a.rsplit(".", 1)[0], b.rsplit(".", 1)[0])))].append((a, b, n))
        for (ta, tb), combos in sorted(by_pair.items(), key=lambda x: -bp["topic_pair_count"].get(x[0], 0)):
            out.append(f"  - {names.get(ta, ta)} + {names.get(tb, tb)}: " + "; ".join(
                f"`{a}` {short(a)[len(a) + 1:]} + `{b}` {short(b)[len(b) + 1:]} ({n})" for a, b, n in combos[:4]))
        out.append("")
    out.append("<!-- blueprint:end -->")
    return "\n".join(out)


def write_skills(db):
    for subj in ("MAM", "MAS"):
        path = os.path.join(ROOT, "skills", f"wace-{subj.lower()}-questions", "SKILL.md")
        s = open(path, encoding="utf-8").read()
        block = markdown(db, subj)
        if "<!-- blueprint:start" in s:
            s = re.sub(r"<!-- blueprint:start.*?<!-- blueprint:end -->", lambda m: block, s, flags=re.S)
        else:
            s = s.rstrip() + "\n\n" + block + "\n"
        open(path, "w", encoding="utf-8").write(s)
        print("updated", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    db = sqlite3.connect(os.path.join(ROOT, "wace.db"))
    if sys.argv[1:] == ["--print"]:
        for subj in ("MAM", "MAS"):
            print(markdown(db, subj), "\n")
    else:
        write_skills(db)
