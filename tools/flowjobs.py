"""The pack flow's AI jobs. One job: write each job's input batches, check what came back, merge it.

  python tools/flowjobs.py tasks  <S> <job> [--size N]   input batches -> evidence/<s>/flow/<job>/in/
  python tools/flowjobs.py prompt <S> <job> <batch>      the fixed prompt for one batch (give it to the agent as is)
  python tools/flowjobs.py check  <S> <job>              validate every output; exit 1 on any problem
  python tools/flowjobs.py merge  <S> <job> [--force]    checked outputs -> the flow's files (see each job)
  python tools/flowjobs.py run    <S> <job> [batch…]     run batches through WTF's configured model (DeepSeek)

Jobs and their specifications: skills/wtf-subject-pack/jobs/*.md — the specification is the prompt, so every runner
(a Haiku subagent, DeepSeek, you) does the same thing and every answer passes the same check. Inputs and outputs
live under evidence/ (git-ignored: they quote the SCSA papers); only merged codes leave it.
"""
import argparse, glob, json, os, random, re, sys

ROOT = os.environ.get("WACE_MATHS_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import subjects  # noqa: E402

SPEC = os.path.join(ROOT, "skills", "wtf-subject-pack", "jobs")
OPS = {"recall", "define", "identify", "name", "describe", "explain", "compare", "predict", "calculate",
       "write-equation", "draw", "interpret-data", "design-method", "evaluate", "state-units", "show-working",
       "justify-choice", "differentiate", "integrate", "solve", "sketch-graph", "prove", "model", "use-calculator"}
MD_JOBS = {"notes", "translate"}


# ---------------------------------------------------------------- files
def flow(subj, *parts):
    return os.path.join(ROOT, "evidence", subj.lower(), "flow", *parts)


def load(path, default=None):
    return json.load(open(path, encoding="utf-8")) if os.path.isfile(path) else default


def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def topics(subj):
    """{CODE: (file stem, zh, en)} in display order (the pack's topic table)."""
    from build_docs import TOPICS
    return TOPICS[subj]


def course(subj):
    info = subjects.info(subj)
    return info.get("course") or info["name"]["en"]


def catalogue(subj, proposed=False):
    return load(os.path.join(ROOT, "tools", f"catalogue_{subj}{'.proposed' if proposed else ''}.json"))


def awards(subj):
    """[(question, part, award)] for every award of every ok part; award["credit"] = its marks in statistics."""
    from marktags import credit
    out = []
    for q in load(flow(subj, "awards.json"), []):
        for p in q["parts"]:
            for a, c in zip(p["awards"], credit(p)):
                out.append((q, p, dict(a, credit=c)))
    return out


def part_id(q, p):
    return f"{q['id']}-{p['label'] or 0}"


def short(text, n):
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[:n] + " …"


def ref(q, p):
    """'2022 ER Q37(a)' — how notes cite a part."""
    sec = subjects.section_name(q.get("subject") or "", q["section"], "short") if q.get("subject") else q["section"]
    return f"{q['year']} {sec} Q{q['q']}" + (f"({p['label']})" if p["label"] else "")


# ---------------------------------------------------------------- inputs
def build_split(subj):
    return [dict(id=part_id(q, p), question=q["id"], label=p["label"], marks=p["marks"], stem=p["stem"] or q["stem"],
                 key_text=q.get("key_text", ""), parser_awards=p.get("parser_awards", []))
            for q in load(flow(subj, "awards.json"), []) for p in q["parts"] if p["status"] == "split"]


def build_label(subj):
    return [dict(id=a["id"], marks=a["marks"], award=a["text"], part_stem=short(p["stem"] or q["stem"], 900),
                 question_context=short(q["stem"], 300)) for q, p, a in awards(subj)]


def label_header(subj):
    return dict(syllabus_topics={c: en for c, (_, _, en) in topics(subj).items()})


def build_atomise(subj):
    labels, cat = load(flow(subj, "labels.json"), {}), catalogue(subj) or {}
    by_id = {a["id"]: (q, p, a) for q, p, a in awards(subj)}
    out = []
    for code, (_, _, en) in topics(subj).items():
        mine = [dict(id=i, marks=by_id[i][2]["marks"], **{k: l[k] for k in ("skill", "operation", "knowledge")},
                     part_stem=short(by_id[i][1]["stem"] or by_id[i][0]["stem"], 160))
                for i, l in labels.items() if l["topic"] == code and i in by_id]
        existing = [p for p in cat.get("patterns", []) if re.fullmatch(code + r"\d+", p["id"])]
        out.append(dict(id=code, topic=dict(code=code, name=en), syllabus=cat.get("syllabus_sources", {}),
                        labels=mine, existing=existing))
    return out


def build_assign(subj, sample=None):
    cat, labels = catalogue(subj), load(flow(subj, "labels.json"), {})
    if not cat or cat.get("catalogue_status") != "approved":
        raise SystemExit(f"tools/catalogue_{subj}.json is not approved: run packflow.py {subj} approve first")
    items = [dict(id=a["id"], marks=a["marks"], award=a["text"], part_stem=short(p["stem"] or q["stem"], 900),
                  label={k: labels[a["id"]][k] for k in ("topic", "skill", "operation", "knowledge")}
                  if a["id"] in labels else None) for q, p, a in awards(subj)]
    return [i for i in items if sample is None or i["id"] in sample]


def assign_header(subj):
    cat = catalogue(subj)
    return dict(catalogue=dict(patterns=[{k: p.get(k) for k in ("id", "name_en", "definition", "not")}
                                         for p in cat["patterns"]],
                               knowledge=[{k: x.get(k) for k in ("id", "name_en", "definition")}
                                          for x in cat.get("knowledge", [])]))


def review_sample(subj):
    """Every award assigned below 0.8, and a fixed 20% of the rest in every topic (seed: the subject code)."""
    done, rng = load(flow(subj, "assign.json"), {}), random.Random(subj)
    low = {i for i, a in done.items() if a["confidence"] < 0.8}
    rest = sorted(set(done) - low)
    by_topic = {}
    for i in rest:
        by_topic.setdefault(re.match(r"[A-Z]+", (done[i]["patterns"] or ["?"])[0]).group(0), []).append(i)
    pick = {i for ids in by_topic.values() for i in rng.sample(ids, max(1, len(ids) // 5))}
    return low | pick


def pattern_stats(subj):
    """Per pattern code: years seen, parts, marks (award marks, so a part's marks are not split by guesswork)."""
    assigned = load(flow(subj, "assign.json"), {})
    years = sorted({q["year"] for q in load(flow(subj, "awards.json"), [])})
    total = {y: 0 for y in years}
    st = {}
    for q, p, a in awards(subj):
        total[q["year"]] += a["credit"]
        for code in assigned.get(a["id"], {}).get("patterns", []):
            s = st.setdefault(code, dict(years=set(), parts={}, marks=0.0))
            share = a["credit"] / len(assigned[a["id"]]["patterns"])
            s["years"].add(q["year"])
            s["parts"].setdefault(part_id(q, p), 0)
            s["parts"][part_id(q, p)] += share
            s["marks"] += share
    out = {}
    for code, s in st.items():
        out[code] = dict(years_seen=len(s["years"]), years=len(years), parts=len(s["parts"]), marks=round(s["marks"], 1),
                         mean_marks=round(s["marks"] / len(s["years"]), 1),
                         share_of_paper=f"{100 * s['marks'] / max(1, sum(total.values())):.1f}%")
    return out


def reports(subj):
    """{year: [paragraphs]} of the examination reports (local PDFs)."""
    import pymupdf
    out = {}
    for path in glob.glob(os.path.join(ROOT, subj, "papers", f"*_{subj}_ExamReport.pdf")):
        year = int(os.path.basename(path)[:4])
        with pymupdf.open(path) as doc:
            text = "\n".join(pg.get_text() for pg in doc)
        out[year] = [" ".join(x.split()) for x in re.split(r"\n\s*\n", text) if len(x.split()) > 6]
    return out


def build_notes(subj):
    cat, assigned, stats, rep = catalogue(subj), load(flow(subj, "assign.json"), {}), pattern_stats(subj), reports(subj)
    by_part = {}
    for q, p, a in awards(subj):
        for code in assigned.get(a["id"], {}).get("patterns", []):
            by_part.setdefault(code, {}).setdefault(part_id(q, p), (q, p, []))[2].append(a["text"])
    out = []
    for code, (fname, _, en) in topics(subj).items():
        pats = []
        for pat in [p for p in cat["patterns"] if re.fullmatch(code + r"\d+", p["id"])]:
            parts = sorted(by_part.get(pat["id"], {}).values(), key=lambda x: (-x[0]["year"], x[0]["q"]))
            said = [para for q, _, _ in parts for para in rep.get(q["year"], [])
                    if re.search(rf"\bQuestion\s+{q['q']}\b", para)]
            pats.append(dict(n=int(pat["id"][len(code):]), id=pat["id"], name_en=pat["name_en"],
                             definition=pat.get("definition") or pat.get("description", ""),
                             stats=stats.get(pat["id"], {}),
                             parts=[dict(ref=ref(dict(q, subject=subj), p), marks=p["marks"], stem=short(p["stem"] or q["stem"], 500),
                                         awards=[short(t, 160) for t in texts]) for q, p, texts in parts],
                             reports=list(dict.fromkeys(short(x, 600) for x in said))[:12]))
        out.append(dict(id=code, topic=dict(code=code, file=fname, name=en), patterns=pats))
    return out


def build_translate(subj):
    out = []
    for code, (fname, _, _) in topics(subj).items():
        path = os.path.join(ROOT, subj, "methods_en", f"{fname}_Methods.md")
        if os.path.isfile(path):
            out.append(dict(id=code, file=fname, english=open(path, encoding="utf-8").read()))
    return out


BUILD = {"split": (build_split, 15, None), "label": (build_label, 40, label_header),
         "atomise": (build_atomise, 1, None), "assign": (build_assign, 40, assign_header),
         "review": (lambda s: build_assign(s, review_sample(s)), 40, assign_header),
         "notes": (build_notes, 1, None), "translate": (build_translate, 1, None)}


def tasks(subj, job, size=None):
    build, default, header = BUILD[job]
    items, size = build(subj), size or default
    folder = flow(subj, job, "in")
    for old in glob.glob(os.path.join(folder, "*.json")):
        os.remove(old)
    head = dict(subject=subj, course=course(subj), **(header(subj) if header else {}))
    names = []
    for i in range(0, len(items), size):
        batch = items[i:i + size]
        name = batch[0]["id"] if size == 1 else f"{i // size + 1:03d}"
        save(os.path.join(folder, name + ".json"), dict(head, items=batch) if size > 1 else dict(head, **batch[0]))
        names.append(name)
    return names


def out_path(subj, job, batch):
    return flow(subj, job, "out", batch + (".md" if job in MD_JOBS else ".json"))


def prompt(subj, job, batch):
    return (f"Repository E:\\WACE_Maths (read-only for you). Follow exactly the job specification "
            f"skills/wtf-subject-pack/jobs/{job}.md and the shared rules in skills/wtf-subject-pack/jobs/README.md.\n"
            f"Input: {os.path.relpath(flow(subj, job, 'in', batch + '.json'), ROOT)}\n"
            f"Write your output to: {os.path.relpath(out_path(subj, job, batch), ROOT)}\n"
            f"Write nothing else anywhere. Then reply in Chinese as README.md says.")


# ---------------------------------------------------------------- checks
def words(text):
    return len(str(text).split())


def check_item(subj, job, inp, out, ctx):
    """Problems of one output item against its input item."""
    bad = []
    if job == "split":
        aw = out.get("awards", [])
        if not aw:
            return [f"{inp['id']}: no awards ({out.get('note', '')})"]
        total = sum(a["marks"] for a in aw if a.get("kind", "award") == "award")
        choice = [a for a in aw if a.get("kind") == "choice"]
        if out.get("structure") == "any":
            per = {a["marks"] for a in choice}
            if len(per) != 1 or not out.get("take") or total + out["take"] * per.pop() != inp["marks"]:
                bad.append(f"{inp['id']}: 'any' does not add up to {inp['marks']}")
        elif total != inp["marks"] or choice:
            bad.append(f"{inp['id']}: awards add up to {total}, the paper prints {inp['marks']}")
        if [a["n"] for a in aw] != list(range(1, len(aw) + 1)):
            bad.append(f"{inp['id']}: n is not 1..{len(aw)}")
        bad += [f"{inp['id']}-{a['n']}: text over 25 words" for a in aw if words(a["text"]) > 25]
    elif job == "label":
        if out.get("topic") not in ctx["topics"]:
            bad.append(f"{inp['id']}: unknown topic {out.get('topic')}")
        if out.get("operation") not in OPS:
            bad.append(f"{inp['id']}: unknown operation {out.get('operation')}")
        if not 0 < words(out.get("skill", "")) <= 12:
            bad.append(f"{inp['id']}: skill must be 1-12 words")
        kn = out.get("knowledge") or []
        if not 1 <= len(kn) <= 3 or any(words(k) > 5 for k in kn):
            bad.append(f"{inp['id']}: knowledge must be 1-3 names of at most 5 words")
    elif job in ("assign", "review"):
        pats, kn = out.get("patterns") or [], out.get("knowledge") or []
        if not 1 <= len(pats) <= 2 or any(p not in ctx["patterns"] for p in pats):
            bad.append(f"{inp['id']}: patterns {pats} (1-2 codes from the catalogue)")
        if not 1 <= len(kn) <= 3 or any(k not in ctx["knowledge"] for k in kn):
            bad.append(f"{inp['id']}: knowledge {kn} (1-3 codes from the catalogue)")
    if job in ("split", "label", "assign", "review") and not 0 <= float(out.get("confidence", -1)) <= 1:
        bad.append(f"{inp['id']}: confidence missing")
    return bad


def check_atomise(inp, out):
    code, ids = inp["topic"]["code"], {l["id"] for l in inp["labels"]}
    bad, seen = [], {}
    for p in out.get("patterns", []):
        if not re.fullmatch(code + r"[1-9]\d*", p.get("id", "")):
            bad.append(f"{code}: pattern id {p.get('id')}")
        for f in ("name_en", "name_zh", "definition", "not"):
            if not p.get(f):
                bad.append(f"{p.get('id')}: no {f}")
        for i in p.get("members", []):
            seen.setdefault(i, []).append(p["id"])
    for x in out.get("knowledge", []):
        if not re.fullmatch(re.escape(code) + r"\.K[1-9]\d*", x.get("id", "")) or not x.get("name_en"):
            bad.append(f"{code}: knowledge atom {x.get('id')}")
    for u in out.get("unplaced", []):
        seen.setdefault(u["id"], []).append("unplaced")
    nums = sorted(int(p["id"][len(code):]) for p in out.get("patterns", []) if re.fullmatch(code + r"\d+", p["id"]))
    if nums != list(range(1, len(nums) + 1)):
        bad.append(f"{code}: patterns are not numbered 1..{len(nums)}")
    bad += [f"{code}: {i} placed twice {w}" for i, w in seen.items() if len(w) > 1]
    bad += [f"{code}: {len(ids - set(seen))} awards placed nowhere, e.g. {sorted(ids - set(seen))[:3]}"] \
        if ids - set(seen) else []
    bad += [f"{code}: unknown member {i}" for i in sorted(set(seen) - ids)][:5]
    return bad


def md_check(inp, text, job, subj):
    from build_db import method_sections
    tmp = flow(subj, job, "out", "_parse.md")
    write(tmp, text)
    found = method_sections(tmp)
    os.remove(tmp)
    if job == "notes":
        want = {p["n"]: {x["ref"] for x in p["parts"]} for p in inp["patterns"]}
    else:
        en = flow(subj, job, "in", "_en.md")
        write(en, inp["english"])
        want = {n: refs(b) for n, (_, b) in method_sections(en).items()}
        os.remove(en)
    bad = [f"{inp['id']}: patterns {sorted(found)} but expected {sorted(want)}"] if set(found) != set(want) else []
    for n, (_, body) in found.items():
        got = refs(body)
        if n in want and got - want[n]:
            bad.append(f"{inp['id']} pattern {n}: cites parts that are not its own: {sorted(got - want[n])[:4]}")
        if job == "translate" and n in want and want[n] - got:
            bad.append(f"{inp['id']} pattern {n}: lost references {sorted(want[n] - got)[:4]}")
    return bad


def refs(body):
    """Question references cited in a notes section: '2022 ER Q37(a)'."""
    return set(re.findall(r"\b20\d\d \w+ Q\d+(?:\([a-z]+\))?", body))


def outputs(subj, job):
    """[(batch name, input, output or None)]."""
    res = []
    for path in sorted(glob.glob(flow(subj, job, "in", "*.json"))):
        name = os.path.basename(path)[:-5]
        if name.startswith("_"):
            continue
        out = out_path(subj, job, name)
        body = None
        if os.path.isfile(out):
            body = open(out, encoding="utf-8").read() if job in MD_JOBS else load(out)
        res.append((name, load(path), body))
    return res


def check(subj, job):
    ctx = {}
    if job == "label":
        ctx["topics"] = set(topics(subj))
    if job in ("assign", "review"):
        cat = catalogue(subj)
        ctx["patterns"] = {p["id"] for p in cat["patterns"]}
        ctx["knowledge"] = {k["id"] for k in cat.get("knowledge", [])}
    problems, missing, low = [], [], 0
    for name, inp, out in outputs(subj, job):
        if out is None:
            missing.append(name)
            continue
        if job == "atomise":
            problems += check_atomise(inp, out)
            continue
        if job in MD_JOBS:
            problems += md_check(inp, out, job, subj)
            continue
        got = {o.get("id"): o for o in out.get("items", [])}
        want = {i["id"]: i for i in inp["items"]}
        problems += [f"{name}: no answer for {i}" for i in want if i not in got]
        problems += [f"{name}: answer for unknown {i}" for i in got if i not in want]
        for i, item in want.items():
            if i in got:
                problems += check_item(subj, job, item, got[i], ctx)
                low += float(got[i].get("confidence", 0)) < 0.7
    return problems, missing, low


# ---------------------------------------------------------------- merge
def merge(subj, job, force=False):
    problems, missing, _ = check(subj, job)
    if problems or missing:
        raise SystemExit(f"not merged: {len(problems)} problems, {len(missing)} batches missing — run check")
    done = outputs(subj, job)
    if job == "split":
        answers = {o["id"]: dict(o, marks=i["marks"]) for _, inp, out in done
                   for i in inp["items"] for o in out["items"] if o["id"] == i["id"]}
        save(flow(subj, "split.json"), answers)  # local, with the award texts
        save(os.path.join(ROOT, "tools", f"splits_{subj}.json"),  # the pack's copy: shape only (marktags.py)
             {i: dict(marks=a["marks"], structure=a.get("structure", "sum"), take=a.get("take"),
                      awards=[dict(n=x["n"], marks=x["marks"], kind=x.get("kind", "award")) for x in a["awards"]])
              for i, a in sorted(answers.items())})
        return f"evidence/…/flow/split.json and tools/splits_{subj}.json — re-run tools/awards.py to apply"
    if job == "label":
        save(flow(subj, "labels.json"), {o["id"]: o for _, _, out in done for o in out["items"]})
        return "evidence/…/flow/labels.json"
    if job == "atomise":
        return merge_atomise(subj, done)
    if job == "assign":
        save(flow(subj, "assign.json"), {o["id"]: o for _, _, out in done for o in out["items"]})
        return "evidence/…/flow/assign.json — next: tasks review"
    if job == "review":
        return merge_review(subj, done)
    written = []
    for _, inp, text in done:
        folder, suffix = ("methods_en", "_Methods.md") if job == "notes" else ("methods", "_解题思路.md")
        fname = inp["topic"]["file"] if job == "notes" else inp["file"]
        path = os.path.join(ROOT, subj, folder, fname + suffix)
        if os.path.isfile(path) and open(path, encoding="utf-8").read() != text and not force:
            raise SystemExit(f"{path} exists and differs: compare, then merge --force")
        write(path, text)
        written.append(os.path.relpath(path, ROOT))
    return ", ".join(written)


def merge_atomise(subj, done):
    """Topic answers -> tools/catalogue_<S>.proposed.json; a person approves it (packflow.py approve)."""
    by_id = {a["id"]: (q, a) for q, _, a in awards(subj)}
    cat = dict(catalogue(subj) or {}, schema_version=2, course=course(subj), catalogue_status="proposed",
               topic_codes={c: en for c, (_, _, en) in topics(subj).items()}, patterns=[], knowledge=[], unplaced=[])
    for _, inp, out in sorted(done, key=lambda x: list(topics(subj)).index(x[1]["topic"]["code"])):
        for p in out["patterns"]:
            members = [by_id[i] for i in p["members"] if i in by_id]
            cat["patterns"].append(dict({k: v for k, v in p.items() if k != "members"},
                                        marks=round(sum(a["credit"] for _, a in members), 1), awards=len(members),
                                        years=len({q["year"] for q, _ in members})))
        cat["knowledge"] += out["knowledge"]
        cat["unplaced"] += out.get("unplaced", [])
    save(os.path.join(ROOT, "tools", f"catalogue_{subj}.proposed.json"), cat)
    # the members are the bottom-up assignment: the assign job starts from them as hints
    save(flow(subj, "atomise_members.json"), {i: p["id"] for _, _, out in done for p in out["patterns"]
                                              for i in p["members"]})
    return f"tools/catalogue_{subj}.proposed.json ({len(cat['patterns'])} patterns, {len(cat['knowledge'])} atoms)"


def merge_review(subj, done):
    first = load(flow(subj, "assign.json"), {})
    second = {o["id"]: o for _, _, out in done for o in out["items"]}
    agree = [i for i in second if set(second[i]["patterns"]) == set(first[i]["patterns"])]
    disputes = [dict(id=i, first=first[i], second=second[i]) for i in second if i not in agree]
    save(flow(subj, "review.json"), dict(sample=len(second), agree=len(agree), disputes=disputes))
    rate = len(agree) / max(1, len(second))
    verdict = "ready" if rate >= 0.9 else "NOT ready: fix the catalogue definitions and re-run assign"
    return f"pattern agreement {len(agree)}/{len(second)} = {rate:.0%} ({verdict}); disputes in evidence/…/flow/review.json"


# ---------------------------------------------------------------- run through WTF's model
def run(subj, job, batches=None):
    from translate import kernel
    chat = kernel().get("llm.chat")
    spec = open(os.path.join(SPEC, "README.md"), encoding="utf-8").read() + "\n\n" + \
        open(os.path.join(SPEC, job + ".md"), encoding="utf-8").read()
    for name, inp, out in outputs(subj, job):
        if out is not None or (batches and name not in batches):
            continue
        reply = chat(spec + "\n\nReply with the output file's content only.", json.dumps(inp, ensure_ascii=False))
        text = re.sub(r"^```\w*\n|\n```\s*$", "", reply.strip())
        path = out_path(subj, job, name)
        write(path, text if job in MD_JOBS else json.dumps(json.loads(text), ensure_ascii=False, indent=1))
        print("wrote", os.path.relpath(path, ROOT))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["tasks", "prompt", "check", "merge", "run"])
    ap.add_argument("subject")
    ap.add_argument("job", choices=list(BUILD))
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--size", type=int)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    S = a.subject.upper()
    if a.cmd == "tasks":
        names = tasks(S, a.job, a.size)
        print(f"{len(names)} batches in {os.path.relpath(flow(S, a.job, 'in'), ROOT)}: {', '.join(names[:12])}"
              + (" …" if len(names) > 12 else ""))
    elif a.cmd == "prompt":
        print(prompt(S, a.job, a.rest[0]))
    elif a.cmd == "check":
        problems, missing, low = check(S, a.job)
        print("\n".join(problems[:60]))
        print(f"{a.job}: {len(problems)} problems, {len(missing)} batches without output"
              + (f" ({', '.join(missing[:8])})" if missing else "") + f", {low} answers below 0.7")
        sys.exit(1 if problems or missing else 0)
    elif a.cmd == "merge":
        print("merged ->", merge(S, a.job, a.force))
    else:
        run(S, a.job, a.rest)
