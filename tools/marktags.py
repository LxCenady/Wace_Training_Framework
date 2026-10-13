"""Award-level tags in a subject pack. One job: decide whether marktags / splits / a catalogue are valid data, and
turn valid marktags into database rows for the awards a local build reproduces.

Files (all hand-made or flow-made data, no SCSA text — only ids, numbers and catalogue codes):
  tools/catalogue_<S>.json  schema 1: patterns; schema 2 adds knowledge atoms {"id": "RX.K4", "name_en", …} and may
                            declare "axes": a topic code whose atoms label another axis of an award (PHY: the award
                            skill, SKL.K1-K11) — carried in the awards' knowledge lists, built into axis_codes
  tools/marktags_<S>.json   {"schema": 1, "subject", "awards": {award id: {marks, patterns, knowledge, confidence}},
                             "questions": {question id: fingerprint}}
  tools/splits_<S>.json     {part id: {marks, structure, take, awards: [{n, marks, kind}]}} — the shape of the parts
                            whose key the parser cannot divide (the split job), so every install numbers them alike
A fingerprint is the part labels and award marks of a question as tools/awards.py numbers them ("a:1,1,2;b:3").
A build applies a question's award tags only when its own fingerprint is the same; otherwise the question keeps
its part tags and the build lists it (the key or the parser changed: re-run the flow for it).
"""
import re

AWARD = re.compile(r"(20\d\d)([A-Z])-(\d+)-([a-z]+|0)-([1-9]\d*)")
PART = re.compile(r"(20\d\d)([A-Z])-(\d+)-([a-z]+|0)")
QUESTION = re.compile(r"(20\d\d)([A-Z])-(\d+)")
FINGERPRINT = re.compile(r"[a-z0]+:\d+(?:,\d+)*(?:;[a-z0]+:\d+(?:,\d+)*)*")
PATTERN = re.compile(r"([A-Z]{1,4})([1-9]\d*)")
ATOM = re.compile(r"([A-Z]{1,4})\.K([1-9]\d*)")
FIRST_FLOW_WTF = (2, 0, 1)  # packs carrying marktags or splits need this WTF or newer


def fail(message):
    raise ValueError(message)


def short(value, limit=200):
    """Names and definitions are the pack's own words; this keeps any one field from carrying a copied passage."""
    if not isinstance(value, str) or len(value) > limit:
        fail(f"Text field too long or not text: {str(value)[:40]}")
    return value


def validate_catalogue(cat):
    """-> (pattern ids, atom ids). Schema 1 (patterns only, as MAA/CHE) or 2 (patterns + knowledge atoms)."""
    if not isinstance(cat, dict) or cat.get("schema_version") not in (1, 2):
        fail("Catalogue needs schema_version 1 or 2")
    topics = cat.get("topic_codes")
    if not isinstance(topics, dict) or not all(re.fullmatch(r"[A-Z]{1,4}", t) for t in topics):
        fail("Catalogue topic_codes must map 1-4 capital letters to names")
    pats, atoms = set(), set()
    for p in cat.get("patterns", []):
        m = PATTERN.fullmatch(str(p.get("id", "")))
        if not m or m.group(1) not in topics or p["id"] in pats or not isinstance(p.get("name_en"), str):
            fail(f"Catalogue pattern {p.get('id')}: bad id, unknown topic, duplicate or no name_en")
        pats.add(p["id"])
    if cat["schema_version"] == 2:
        for a in cat.get("knowledge", []):
            m = ATOM.fullmatch(str(a.get("id", "")))
            if not m or m.group(1) not in topics or a["id"] in atoms:
                fail(f"Catalogue knowledge atom {a.get('id')}: bad id, unknown topic or duplicate")
            short(a.get("name_en", ""))
            short(a.get("definition", ""), 600)
            atoms.add(a["id"])
        if not atoms:
            fail("Catalogue schema 2 has no knowledge atoms")
    if not pats:
        fail("Catalogue has no patterns")
    axes(cat, atoms)
    return pats, atoms


def axes(cat, atoms=None):
    """Optional "axes": [{"id", "prefix", "name_en", "name_zh", "codes": {atom: {"key", "group"}}}] -> {atom: (axis id,
    key, group)}. An axis owns its prefix's atoms; old WTF versions simply see them as knowledge atoms."""
    out = {}
    spec = cat.get("axes", [])
    if not isinstance(spec, list):
        fail("Catalogue axes must be a list")
    for ax in spec:
        if not isinstance(ax, dict) or not re.fullmatch(r"[a-z]{1,20}", str(ax.get("id", "")))                 or ax.get("prefix") not in cat.get("topic_codes", {}) or not isinstance(ax.get("codes"), dict):
            fail(f"Catalogue axis {ax.get('id') if isinstance(ax, dict) else ax}: id, a topic-code prefix and codes needed")
        for atom, v in ax["codes"].items():
            if not atom.startswith(ax["prefix"] + ".K") or (atoms is not None and atom not in atoms)                     or not isinstance(v, dict) or not isinstance(v.get("key"), str):
                fail(f"Catalogue axis {ax['id']}: bad code {atom}")
            out[atom] = (ax["id"], v["key"], str(v.get("group", "")))
    return out


def validate_marktags(data, cat, subject):
    pats, atoms = validate_catalogue(cat)
    if cat["schema_version"] != 2:
        fail("marktags need a schema 2 catalogue (knowledge atoms)")
    if not isinstance(data, dict) or data.get("schema") != 1 or data.get("subject") != subject:
        fail("marktags: schema 1 for this subject expected")
    if set(data) - {"schema", "subject", "awards", "questions"}:
        fail("marktags: unknown fields")
    questions = data.get("questions")
    if not isinstance(questions, dict) or not all(QUESTION.fullmatch(q) and isinstance(f, str) and FINGERPRINT.fullmatch(f)
                                                 for q, f in questions.items()):
        fail("marktags: questions must map question ids to fingerprints")
    awards = data.get("awards")
    if not isinstance(awards, dict) or not awards:
        fail("marktags: no awards")
    for aid, a in awards.items():
        m = AWARD.fullmatch(aid)
        if not m or not isinstance(a, dict) or set(a) - {"marks", "patterns", "knowledge", "confidence"}:
            fail(f"marktags: bad award {aid}")
        if f"{m.group(1)}{m.group(2)}-{m.group(3)}" not in questions:
            fail(f"marktags: {aid} has no question fingerprint")
        if type(a.get("marks")) is not int or not 1 <= a["marks"] <= 40:
            fail(f"marktags: {aid} marks")
        p, k = a.get("patterns"), a.get("knowledge")
        if not isinstance(p, list) or not 1 <= len(p) <= 2 or any(x not in pats for x in p):
            fail(f"marktags: {aid} patterns {p} not in the catalogue")
        if not isinstance(k, list) or not 1 <= len(k) <= 3 or any(x not in atoms for x in k):
            fail(f"marktags: {aid} knowledge {k} not in the catalogue")
        c = a.get("confidence")
        if not isinstance(c, (int, float)) or not 0 <= c <= 1:
            fail(f"marktags: {aid} confidence")


def validate_splits(data):
    if not isinstance(data, dict):
        fail("splits: an object of parts expected")
    for pid, s in data.items():
        if not PART.fullmatch(pid) or not isinstance(s, dict) or set(s) - {"marks", "structure", "take", "awards"}:
            fail(f"splits: bad part {pid}")
        aw = s.get("awards")
        if type(s.get("marks")) is not int or s.get("structure") not in ("sum", "any", "best") or not isinstance(aw, list) or not aw:
            fail(f"splits: {pid} needs marks, structure and awards")
        for i, a in enumerate(aw, 1):
            if not isinstance(a, dict) or set(a) != {"n", "marks", "kind"} or a["n"] != i or type(a["marks"]) is not int \
                    or a["marks"] < 1 or a["kind"] not in ("award", "choice"):
                fail(f"splits: {pid} award {i}: only n, marks, kind (award|choice)")
        total = sum(a["marks"] for a in aw if a["kind"] == "award")
        choice = [a["marks"] for a in aw if a["kind"] == "choice"]
        if s["structure"] == "any":
            take = s.get("take")
            if type(take) is not int or len(set(choice)) != 1 or total + take * choice[0] != s["marks"]:
                fail(f"splits: {pid} 'any' does not add up")
        elif choice or total != s["marks"]:
            fail(f"splits: {pid} awards add up to {total}, not {s['marks']}")


def credit(part):
    """Marks each award of a part stands for in statistics, adding up to the part's printed marks: an "any N of"
    list shares its take × choice marks equally among its options (4 options, any 2, 1 mark each -> 0.5 each)."""
    aw = part["awards"]
    choice = [a for a in aw if a.get("kind") == "choice"]
    if not choice:
        return [a["marks"] for a in aw]
    pool = (part.get("take") or len(choice)) * choice[0]["marks"]
    return [pool / len(choice) if a.get("kind") == "choice" else a["marks"] for a in aw]


def fingerprint(parts):
    """awards.py parts of one question -> 'a:1,1,2;b:3' (empty part label written 0)."""
    return ";".join(f"{p['label'] or 0}:{','.join(str(a['marks']) for a in p['awards'])}" for p in parts)


def db_code(subject, code):
    """'RX3' -> 'CHE.RX.3', 'RX.K4' -> 'CHE.RX.K4' (the database's codes)."""
    m = PATTERN.fullmatch(code)
    return f"{subject}.{m.group(1)}.{m.group(2)}" if m else f"{subject}.{code}"


def rows(subject, qid, record, tags):
    """One awards.py question record -> ([award_tags rows], problem or None) for database question id `qid`."""
    want = tags["questions"].get(record["id"])
    if want is None:
        return [], None
    if fingerprint(record["parts"]) != want:
        return [], f"{qid}: awards differ from the pack's ({fingerprint(record['parts'])} vs {want}); part tags only"
    out = []
    for p in record["parts"]:
        for a, marks in zip(p["awards"], credit(p)):
            t = tags["awards"].get(a["id"])
            if not t:
                return [], f"{qid}: award {a['id']} has no tags; part tags only"
            n = int(a["id"].rsplit("-", 1)[1])
            out += [(qid, p["label"], n, marks, "pattern", db_code(subject, c)) for c in t["patterns"]]
            out += [(qid, p["label"], n, marks, "knowledge", db_code(subject, c)) for c in t["knowledge"]]
    return out, None
