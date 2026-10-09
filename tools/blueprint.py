"""Paper blueprints from the past papers. One job: wace.db -> how real papers are built, per subject and section.

  topic_share     share of marks per topic (a part's marks are split evenly over its patterns)
  question_marks  marks of every question since 2020 (the distribution new papers sample from)
  question_count  questions per paper since 2020
  cross_topic     pattern pairs from different topics that appear in the same past question, with counts

python tools/blueprint.py  rewrites the "Paper blueprint" block of both question-generation skills.
"""
import os, re, sqlite3, sys
from collections import Counter, defaultdict
from itertools import combinations

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def blueprint(db, subj, section, since=2020):
    q = lambda sql, *a: db.execute(sql, a).fetchall()  # noqa: E731
    share, pattern_share, cross = defaultdict(float), defaultdict(float), Counter()
    by_question = defaultdict(set)
    rows = q("""SELECT pp.qid, pp.label, pp.pattern, COALESCE(p.marks, 1), q.year FROM part_patterns pp
                JOIN parts p ON p.qid = pp.qid AND p.label = pp.label JOIN questions q ON q.id = pp.qid
                WHERE q.subject = ? AND q.section = ?""", subj, section)
    per_part = Counter((qid, label) for qid, label, *_ in rows)
    for qid, label, pattern, marks, year in rows:
        share[pattern.rsplit(".", 1)[0]] += marks / per_part[(qid, label)]
        pattern_share[pattern] += marks / per_part[(qid, label)]
        by_question[qid].add(pattern)
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
    }


LEVELS = ("基础", "标准", "拔高")


def pick_partner(bp, primary, topic, by_topic, used, rng, direct=3.0):
    """Partner pattern for a cross-topic question: real pattern pairings weigh `direct` times more than a
    pattern merely drawn from an associated topic (P(B | A) x the pattern's weight within B)."""
    weights = defaultdict(float)
    for b, p_b in bp["topic_partner"].get(topic, {}).items():
        free = {c: w for c, w in by_topic[b].items() if c not in used}
        norm = sum(free.values())
        for c, w in free.items():
            weights[c] += p_b * w / norm
    for (a, b), n in bp["cross_topic"]:
        other = b if a == primary else a if b == primary else None
        if other and other not in used:
            weights[other] += direct * n / max(1, sum(n2 for (x, y), n2 in bp["cross_topic"] if primary in (x, y)))
    if not weights:
        return None
    return rng.choices(list(weights), weights=list(weights.values()))[0]


def plan(bp, total, rng, boost=1.08):
    """A random paper that follows the blueprint -> [(pattern codes, marks, difficulty)] in paper order.

    Question count and per-question marks are drawn from recent papers (then nudged to the exact total);
    topics get questions in proportion to their historical share of marks; patterns are drawn by their
    historical weight within the topic. Cross-topic questions follow the topic association of real papers:
    a question on topic A becomes cross-topic with A's own real rate, its partner topic B is drawn with
    P(B | A) from real multi-topic questions, and the partner pattern prefers pairings real questions used
    (pattern pairs), else B's patterns by weight. Difficulty rises through the paper with some jitter."""
    # each topic keeps its own relative tendency to pair, scaled so the paper as a whole matches the real rate
    mean = sum(share * bp["topic_cross_rate"].get(t, 0) for t, share in bp["topic_share"].items())
    scale = boost * bp["cross_rate"] / mean if mean else 0
    count = rng.choice(bp["question_count"])
    pool = [m for m in bp["question_marks"] if m >= 3]
    lo, hi = min(pool), max(pool)
    marks = [rng.choice(pool) for _ in range(count)]
    while sum(marks) != total:  # nudge to the exact total, staying inside the observed range
        i = rng.randrange(count)
        step = 1 if sum(marks) < total else -1
        if lo <= marks[i] + step <= hi:
            marks[i] += step
    marks.sort()
    for i in range(count - 1):  # mostly small-to-large, like the papers, but not strictly
        if rng.random() < 0.3:
            marks[i], marks[i + 1] = marks[i + 1], marks[i]
    deficit = {t: share * total for t, share in bp["topic_share"].items()}
    by_topic = defaultdict(dict)
    for code, w in bp["pattern_share"].items():
        by_topic[code.rsplit(".", 1)[0]][code] = w
    used, out = set(), []
    for pos, m in sorted(enumerate(marks), key=lambda x: -x[1]):  # big questions claim topics first
        topic = max(deficit, key=lambda t: deficit[t] + rng.uniform(0, 0.3 * m) if by_topic[t].keys() - used else -1e9)
        free = {c: w for c, w in by_topic[topic].items() if c not in used}
        primary = rng.choices(list(free), weights=list(free.values()))[0]
        codes = [primary]
        partner = None
        if m >= 4 and rng.random() < min(0.95, scale * bp["topic_cross_rate"].get(topic, 0)):
            partner = pick_partner(bp, primary, topic, by_topic, used, rng)
        if partner:
            codes.append(partner)
            deficit[partner.rsplit(".", 1)[0]] -= 0.4 * m
            deficit[topic] -= 0.6 * m
        else:
            deficit[topic] -= m
        used.update(codes)
        out.append((pos, codes, m))
    out.sort()
    paper = []
    for pos, codes, m in out:
        x = pos / max(1, count - 1) + rng.uniform(-0.12, 0.12)
        paper.append((codes, m, LEVELS[0] if x < 0.3 else LEVELS[2] if x > 0.75 else LEVELS[1]))
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
