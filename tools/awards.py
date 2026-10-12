"""Stage 2b of the pack flow: mark points. One job: questions.json + marking keys -> every part's awards with stable ids.

  python tools/awards.py CHE      -> evidence/<s>/flow/awards.json, summary on stdout

An award is one scoring criterion of the key: its text, its marks and an id that never changes with crops,
  <year><section letter>-<q>-<part or 0>-<n>        e.g. 2016S-26-a-3
The subject's key parser (handlers.py) gives one entry per mark; consecutive identical entries of a part are one
multi-mark criterion (a 2-mark row stays indivisible). A part is "ok" when its awards add up to the marks printed
on the paper; otherwise it is "split" and goes to the AI job that reads the key (jobs/split.md) — nothing is
invented or truncated here. Multiple-choice questions are one 1-mark award, the key's letter.
The split job's checked answers (evidence/<s>/flow/split.json, written by flowjobs.py merge) are applied on every
run, so re-running this tool never loses them; an answer whose part marks no longer match is ignored.
"""
import json, os, sys

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pymupdf  # noqa: E402
import subjects  # noqa: E402
from build_db import key_text  # noqa: E402
from handlers import key_parser  # noqa: E402
from partmarks import split, texts  # noqa: E402


def qkey(subj, q):
    return f"{q['year']}{subjects.section_letter(subj, q['section'])}-{q['q']}"


def group(points):
    """[(label, text)] one per mark -> [(label, text, marks)] with consecutive repeats of a part merged."""
    out = []
    for label, text in points:
        text = " ".join(text.split())
        if out and out[-1][0] == label and out[-1][1] == text:
            out[-1][2] += 1
        else:
            out.append([label, text, 1])
    return out


def question(subj, q, parse, docs, done=None):
    """One questions.json record -> {id, year, section, q, marks, parts: [{label, marks, status, awards}]}."""
    rec = dict(id=qkey(subj, q), year=int(q["year"]), section=q["section"], q=int(q["q"]), marks=int(q["marks"] or 0))
    if "answer" in q:
        rec["parts"] = [dict(label="", marks=1, status="ok",
                             awards=[dict(id=rec["id"] + "-0-1", marks=1, text=f"Answer: {q['answer']}")],
                             stem=q["text"])]
        rec["stem"] = q["text"]
        return rec
    if q["key"] not in docs:
        docs[q["key"]] = pymupdf.open(os.path.join(ROOT, q["key"]))
    key = key_text(docs[q["key"]], q["key_regions"])
    printed = split(q["text"], rec["marks"]) or {"": rec["marks"]}
    entries = group(parse(key))
    stems = texts(q["text"])
    parts = []
    for label, marks in printed.items():
        mine = [e for e in entries if e[0] == label]
        awards = [dict(id=f"{rec['id']}-{label or 0}-{n}", marks=m, text=t) for n, (_, t, m) in enumerate(mine, 1)]
        ok = sum(a["marks"] for a in awards) == marks
        part = dict(label=label, marks=marks, status="ok" if ok else "split", awards=awards if ok else [],
                    stem=stems.get(label, ""))
        fixed = (done or {}).get(f"{rec['id']}-{label or 0}")
        if not ok and fixed and fixed["marks"] == marks:
            part.update(status="ok", source="split", structure=fixed["structure"], take=fixed.get("take"),
                        awards=[dict(id=f"{rec['id']}-{label or 0}-{a['n']}", marks=a["marks"], text=a["text"],
                                     kind=a.get("kind", "award")) for a in fixed["awards"]])
        elif not ok:
            part["parser_awards"] = [dict(marks=a["marks"], text=a["text"]) for a in awards]
        parts.append(part)
    rec["parts"] = parts
    if any(p["status"] == "split" for p in parts):
        rec["key_text"] = key  # local evidence only (git-ignored): the split job reads the whole key
    rec["stem"] = q["text"]
    return rec


def run(subj):
    parse, docs = key_parser(subjects.info(subj)), {}
    qs = [q for q in json.load(open(os.path.join(ROOT, subj, "questions.json"), encoding="utf-8"))
          if str(q["year"]).isdigit()]
    folder = os.path.join(ROOT, "evidence", subj.lower(), "flow")
    done_path = os.path.join(folder, "split.json")
    done = json.load(open(done_path, encoding="utf-8")) if os.path.isfile(done_path) else {}
    out = [question(subj, q, parse, docs, done) for q in qs]
    os.makedirs(folder, exist_ok=True)
    json.dump(out, open(os.path.join(folder, "awards.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return out


if __name__ == "__main__":
    for s in sys.argv[1:]:
        out = run(s.upper())
        parts = [p for q in out for p in q["parts"]]
        bad = [p for p in parts if p["status"] == "split"]
        print(f"{s}: {len(out)} questions, {len(parts)} parts, {sum(len(p['awards']) for p in parts)} awards; "
              f"{len(parts) - len(bad)} parts ok, {len(bad)} parts need the split job "
              f"({sum(p['marks'] for p in bad)} of {sum(p['marks'] for p in parts)} marks)")
