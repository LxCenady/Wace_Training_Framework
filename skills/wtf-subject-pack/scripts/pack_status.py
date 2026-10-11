"""Parity checklist for one WTF subject pack. One job: <root> + subject code -> a ✓/✗ table on stdout.

  python pack_status.py MAA [--root E:\\WACE_Maths]

Read-only: opens wace.db read-only, never writes anything. Exit code 0 when every item passes.
"""
import argparse, glob, json, os, re, sqlite3, sys

p = argparse.ArgumentParser()
p.add_argument("subject")
p.add_argument("--root", default=os.environ.get("WACE_MATHS_ROOT") or r"E:\WACE_Maths")
a = p.parse_args()
S, R = a.subject.upper(), a.root
rows = []


def check(name, ok, detail=""):
    rows.append((ok, name, detail))


def text(path):
    return open(path, encoding="utf-8").read() if os.path.isfile(path) else ""


# 1 sources
lines = [l.split("\t")[0] for l in text(os.path.join(R, "sources.tsv")).splitlines() if l.startswith(S + "/")]
missing = [l for l in lines if not os.path.isfile(os.path.join(R, l))]
check("sources listed", bool(lines), f"{len(lines)} files")
check("papers on disk", bool(lines) and not missing, f"missing {len(missing)}: {missing[:3]}" if missing else "")
check("formula/data sheets listed", any(re.search(r"Sheet|Booklet", l) for l in lines))

# 2 questions
qpath = os.path.join(R, S, "questions.json")
qs = [q for q in json.load(open(qpath, encoding="utf-8")) if str(q["year"]).isdigit()] if os.path.isfile(qpath) else []
check("questions.json", bool(qs), f"{len(qs)} questions")
check("every question has marks + key", bool(qs) and all(q.get("marks") and q.get("key_regions") for q in qs),
      ", ".join(f"{q['year']}{q['section'][4:5]} Q{q['q']}" for q in qs if not (q.get("marks") and q.get("key_regions")))[:80])

# 3 catalogue + topics
cat_path = os.path.join(R, "tools", f"catalogue_{S}.json")
cat = json.load(open(cat_path, encoding="utf-8")) if os.path.isfile(cat_path) else None
codes = {x["id"] for x in cat["patterns"]} if cat else set()
check("pattern catalogue", bool(codes), f"{len(codes)} patterns" if cat else "tools/catalogue_%s.json (MAM/MAS predate catalogues)" % S)
sys.path.insert(0, os.path.join(R, "tools"))
os.environ["WACE_MATHS_ROOT"] = R
try:
    from build_docs import TOPICS
    topics = TOPICS.get(S, {})
except Exception as e:  # noqa: BLE001
    topics = {}
check("build_docs.TOPICS entry", bool(topics), f"{len(topics)} topics")

# 4 tags
pt = text(os.path.join(R, "tools", f"parttags_{S}.txt"))
tagged = {}
for l in pt.splitlines():
    f = l.split("#")[0].split()
    if f:
        tagged[(f[0], int(f[1]))] = [c for tok in f[2:] for c in tok.split("=")[1].split("+")]
want = {(f"{q['year']}{'A' if q['section'] == 'CalcAssumed' else 'F' if q['section'] == 'CalcFree' else q['section'][:1]}", q["q"]) for q in qs}
check("every question part-tagged", bool(want) and want <= set(tagged), f"{len(want - set(tagged))} untagged" if want - set(tagged) else f"{len(tagged)} lines")
used = {c for v in tagged.values() for c in v}
if codes:
    check("tags use catalogue codes only", used <= codes, str(sorted(used - codes))[:80])
    check("every pattern has a past question", codes <= used, f"unused: {sorted(codes - used)}" if codes - used else "")
flag = re.search(r"still flagged for review:(.*)", pt)
check("no questions flagged for review", not (flag and flag.group(1).strip()), flag.group(1).strip() if flag else "")

# 7 notes
for d, head, suffix in (("methods", r"^## 题型\s*\d+", "_解题思路"), ("methods_en", r"^## Pattern\s*\d+", "_Methods")):
    n_md = n_pdf = n_pat = 0
    for fname, *_ in topics.values():
        md = os.path.join(R, S, d, fname + suffix + ".md")
        n_md += os.path.isfile(md)
        n_pdf += os.path.isfile(md[:-3] + ".pdf")
        n_pat += len(re.findall(head, text(md), re.M))
    target = len(codes) or n_pat
    check(f"notes {d}: one section per pattern", bool(topics) and n_md == len(topics) and n_pat == target,
          f"{n_md}/{len(topics)} files, {n_pat}/{target} patterns")
    check(f"notes {d}: PDFs", bool(topics) and n_pdf == len(topics), f"{n_pdf}/{len(topics)}")
check("review log 审校记录.md", os.path.isfile(os.path.join(R, S, "methods", "审校记录.md")))

# 9 cheat sheet
for f in (f"{S}_CheatSheet", f"{S}_CheatSheet_EN"):
    check(f"cheatsheet {f}", all(os.path.isfile(os.path.join(R, "cheatsheet", f + e)) for e in (".md", ".pdf")))

# 10 question skill
sk = text(os.path.join(R, "skills", f"wace-{S.lower()}-questions", "SKILL.md"))
block = re.search(r"blueprint:start.*?-->(.*?)<!-- blueprint:end", sk, re.S)
check("question skill", bool(sk), f"{len(glob.glob(os.path.join(R, 'skills', f'wace-{S.lower()}-questions', 'topics', '*.md')))} topic files")
check("skill blueprint block filled", bool(block and len(block.group(1).strip()) > 200))

# 11 app hooks
for f, what in (("app/plugins/store.py", "SUBJECT_NAMES"), ("app/plugins/ui_setup.py", "SUBJECTS"),
                ("app/plugins/generator.py", "SUBJECT"), ("tools/paperid.py", "identify")):
    check(f"app hook {what} ({f})", f'"{S}"' in text(os.path.join(R, f)))

# 8 database
db_path = os.path.join(R, "wace.db")
if os.path.isfile(db_path):
    db = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    n, ok = db.execute("SELECT COUNT(*), SUM(points_ok) FROM questions WHERE subject=?", (S,)).fetchone()
    check("wace.db questions", bool(n) and n == len(qs), f"{n} in db, {len(qs)} in questions.json")
    check("mark points ≥95% points_ok", bool(n) and (ok or 0) >= 0.95 * n, f"{ok}/{n}")
    pn, pe = db.execute("SELECT COUNT(*), SUM(method_en != '') FROM patterns WHERE topic LIKE ?", (S + ".%",)).fetchone()
    check("db patterns with zh+en notes", bool(pn) and pn == pe, f"{pe}/{pn}")
else:
    check("wace.db", False, "not built")

# 12 pack
check("pack.json (subject profile)", os.path.isfile(os.path.join(R, S, "pack.json")), "see references/pack-format.md")

w = max(len(r[1]) for r in rows)
for ok, name, detail in rows:
    print(("✓" if ok else "✗"), name.ljust(w), detail)
bad = sum(1 for r in rows if not r[0])
print(f"\n{S}: {len(rows) - bad}/{len(rows)} items pass")
sys.exit(1 if bad else 0)
