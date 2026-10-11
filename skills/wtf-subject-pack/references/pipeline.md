# Pipeline, stage by stage

`<S>` = subject code (MAM, MAS, MAA, CHE…), `<s>` = lower case. `py` = `<ROOT>\.venv\Scripts\python`.
Run tools from `<ROOT>`; set `WACE_MATHS_ROOT` to a temp copy when the user's WTF has `wace.db` open.

Contents: 1 Sources · 2 Segmentation · 3 Catalogue · 4 Labelling · 5 Mark points · 6 Evidence ·
7 Notes · 8 Build · 9 Cheat sheet · 10 Skill · 11 App and docs

---

## 1. Sources

**Files**: `sources.tsv` (one line per file: `<S>/papers/<name>.pdf<TAB><official URL>[ (wayback)]`),
`tools/fetch.py`, `tools/paperid.py`.

Canonical names: `<year>_<S>_Exam_<Section>.pdf`, `<year>_<S>_MarkingKey_<Section>.pdf`, `<year>_<S>_ExamReport.pdf`,
`<year>_<S>_FormulaSheet.pdf` (a data booklet gets its own kind, e.g. `DataBooklet` — add it to `paperid.py`).

Steps:
1. Find the official URLs: SCSA "Past ATAR course examinations" page for the course, plus the Wayback Machine
   for years the site no longer lists (`https://web.archive.org/web/2020id_/<url>` is what `fetch.py` uses for
   lines marked ` (wayback)`). Ask the user before downloading.
2. Add every exam, marking key, examination report and sheet. A year with no marking key cannot be labelled
   or checked — leave it out of the manifest and record why (MAA 2019: keys never published / unobtainable).
3. `py tools/fetch.py` downloads what is reachable. SCSA's live site returns 403 to scripts: the user opens the
   printed URLs in a browser, saves into Downloads, then `py tools/fetch.py --from <Downloads>` imports by
   content, whatever the file names.
4. Teach `paperid.identify` the subject: the course title on page 1 → `<S>`, plus any document-kind wording
   that differs (MAA 2016 says "Formulae and Data sheet"). Run `py tools/paperid.py` — its self-check must
   report 0 mismatches over every paper on disk.

Check: `fetch.missing(subjects=["<S>"])` is empty; every file opens; covers say what the name says.

Pitfalls: a stray paper not in the manifest got segmented once (MAA 2019 CF) — `segment.py` now only takes
exams listed in `sources.tsv`. Never disable certificate checks to get past a download error; `fetch.hint()`
explains cert / refused / network errors in plain words.

## 2. Segmentation and part marks

**Files**: `tools/segment.py` → `<S>/questions.json`; `tools/partmarks.py`; audits `tools/audit.py`,
`tools/audit_totals.py`.

`py tools/segment.py <S>` finds each "Question N" heading in the exam and the key, cuts regions
`[page, y0, y1]`, reads "(n marks)" and the stem text. Then:

- `py tools/audit.py <S>` — per paper: question range, summed marks, questions with no marks / no key region.
- `py tools/audit_totals.py <S>` — summed marks must equal the section total printed on the cover. 0 mismatches.
- `partmarks.split(stem, total)` gives `{part label: marks}` as printed; labels are `a`, `ai`, `b`, … and `""`
  for an unpartitioned question. Look at every question where it returns nothing.

Pitfalls MAA hit (all fixed in the shared code, keep the tests passing):
- `(i)` after `(h)` is part *i* when (h) already printed its own marks, else sub-part (h)(i).
- Function notation `f(a)`, `(n)` in a formula is not a label: labels start a line and come in order.
- Marks printed on the same visual row as the label, not after the text (handled by row matching).
- Sketch / figure detection is regex based (`SKETCH`, `SPARE`, `FIGURE` in `partmarks.py`) plus embedded
  images in the exam crop (`build_db.images_in`). A new subject needs its own words here (see subject-profiles.md).

## 3. Pattern catalogue

**File**: `tools/catalogue_<S>.json` (MAA's is the template):
```json
{"schema_version": 1, "course": "...", "catalogue_status": "draft_for_review",
 "topic_codes": {"BIV": "Bivariate data analysis", ...},
 "syllabus_sources": {"2025": "<syllabus PDF url>"},
 "patterns": [{"id": "BIV1", "name_zh": "...", "name_en": "...", "syllabus": ["3.1.x"],
               "definition": "what a part must ask for to get this tag", "not": "near-misses that belong elsewhere"}]}
```

Do this yourself; it decides everything downstream.
- Topics follow the syllabus units/sub-topics (3–8 per subject); codes are 2–4 capital letters, unique across
  subjects only within a subject (`<S>.<CODE>.<n>` in the DB).
- Patterns are *what the student is asked to do* (an operation with a recognisable mark scheme), not content
  headings. Aim for 8–16 per topic. Write the `definition` and the boundary to its neighbours — reviewers cite
  them, and most later disputes (MAA: FIN1 vs FIN7, GRF6 vs GRF9, NDM6 vs NDM7) were boundary questions.
- Read 2–3 recent papers end to end before finalising; then show the user the list of topics and pattern
  names for sign-off.
- Add the topics to `build_docs.TOPICS["<S>"] = {CODE: ("NN_File_Name", "中文名", "English name")}` — the
  order is the display order, the file stem names the notes and topic PDFs.

## 4. Labelling, review, audit, export

**Files**: `evidence/<s>/labels.json` (git-ignored), `tools/audit_<s>.py` (copy `audit_maa.py`), exports
`tools/tags_<S>.txt` (question → topics) and `tools/parttags_<S>.txt` (part → patterns).

Label record (one per question):
```json
{"year": 2016, "section": "CalcAssumed", "q": 7, "topics": ["SEQ"],
 "parts": [{"label": "a", "marks": 2, "tags": ["SEQ4"], "reason": "...", "confidence": 0.99, "visual_checked": true}],
 "exam_total": 9, "key_total": 9, "primary_reviewed": true, "review_notes": ["..."], "needs_review": false}
```
`parttags_<S>.txt` line: `2016A 7 a=SEQ4 b=SEQ5 c=SEQ5` (`<year><section letter> <q> <label>=<CODE>[+<CODE>]…`,
`-` for an unpartitioned question, `#` comments). Tag a part with the pattern(s) whose marks it actually earns
in the key — not everything it mentions.

Rounds (MAA's actual sequence, which worked):
1. **Pilot**: you label one paper by hand with the catalogue; fix catalogue definitions that were unclear.
2. **Haiku labellers** in parallel by year range (template in delegation.md), each reading stem + key + rendered
   crops when a figure matters, writing `reason` and `confidence` per part.
3. **Primary review** (you): ≥20% of questions, chosen to cover every topic and every low-confidence part.
   Set `primary_reviewed`, write `review_corrections`. If you change >10% of the sample, fix the catalogue and
   re-run the labellers on what they got wrong.
4. **Audit script**: every question present, part labels = `partmarks.split` labels, part marks sum to the
   question total, every code exists in the catalogue. 0 problems before export.
5. **Independent tag review**: Haiku reviewers per year range, proposing changes with key evidence and confidence.
   Apply ≥0.6 directly (with a backup of labels.json and a `review_notes` line each); send <0.6 to one arbiter
   agent that sees both sides and the catalogue; you decide ties. Keep conventions consistent across years —
   reviewers sometimes propose a change that contradicts an earlier accepted one (check the merged list for
   A→B in one place and B→A in another).
6. Export tags/parttags; record questions still in doubt as a `# still flagged for review:` header line.

## 5. Mark points

`tools/markpoints.py`: key text → `[(part, behaviour)]`, one entry per mark. `build_db` sets `points_ok` when the
count equals the question's marks **and** per-part counts equal the printed part marks; otherwise the app shows
the key as an image. Target ≥95% `points_ok`; list every exception with the reason (MAA 2021 CA Q9: key text
runs out of order).

Maths keys: tick glyphs U+F050 / U+F0FC / ✓ under "Specific behaviours", "Alternative solution" blocks skipped.
Other key styles need another parser selected by the subject profile — do not loosen the maths one.

## 6. Evidence packs

`py tools/evidence.py <S>` → per topic `evidence/<S>_<topic>.txt` (stem + key behaviours for every tagged
question) and `<S>_reports.txt` (examination-report comments). MAA's richer packs were built by
`evidence/maa/build_notes_evidence.py` into `evidence/maa/notes/<TOPIC>.txt` + `INDEX.md` (per pattern: the parts
that carry it, marks, key lines, report remarks). Note writers read only these, so they are complete and
nothing is invented.

## 7. Notes (解题思路)

Format — copy MAM/MAS exactly, the app parses it (`build_db.method_sections`):
```
# NN Topic 解题思路
（intro）
## 题型 1：<title>
**识别**… **步骤**… **易错点（考试报告）**… **真题** 2024 CA Q9(b)、…
```
One `## 题型 N：` per catalogue pattern, N matching the code number. English edition uses `## Pattern N: title`.

Process:
1. 3 Haiku writers in parallel, two topics each, from the evidence packs only, using MAM notes as the model.
2. 2 Haiku reviewers, independent, each over all topics: correctness against the keys, every 真题 reference
   exists and carries that pattern, no copied paragraphs from SCSA reports beyond short quotes, structure parse.
3. You fix, write `<S>/methods/审校记录.md` (what was checked, what changed).
4. After tags change, sync the 真题 lists with the final parttags (a Haiku job; give it the export).
5. `py tools/translate.py docs` → `methods_en/*_Methods.md` (DeepSeek, cached). Read a sample; fix by hand
   terms the model gets wrong (真题 = "past questions").
6. `py tools/render_methods.py <S>` → PDFs next to the md files.

## 8. Build and non-regression

`py tools/build_all.py` (or `build_all.run(["<S>"])` for one subject) runs segment → build_docs → build_bank →
build_db. Build into a temp root first. Then:
- `build_db` prints counts and problems — every problem must be intended and listed in `<S>/README.md`.
- Non-regression: for each existing subject, `questions`, `parts`, `part_patterns`, `points` rows must be
  identical to the previous `wace.db` (compare with a small sqlite script; MAA's check: 0 differing rows).
- `points_ok` per subject, number of patterns, every pattern has zh and en notes.

## 9. Cheat sheet, formula/data sheets

`cheatsheet/<S>_CheatSheet.md` (+ `_EN.md`), 2–3 dense pages, rendered with `py tools/render_cheat.py <md>`.
Content: per topic the formulas/facts *not* on the official sheet, the calculator/procedure steps, and the top
traps from examination reports. The official sheets themselves are just manifest lines (stage 1).

## 10. Question-generation skill

`skills/wace-<s>-questions/SKILL.md` + `topics/NN_Topic.md`, same structure as MAM's (the app's generator reads
it via `skill_text()`). End SKILL.md with the empty markers
`<!-- blueprint:start ... -->` / `<!-- blueprint:end -->` and run `py tools/blueprint.py` — it writes real-paper
statistics (marks per question, topic shares, cross-topic pairs, pattern marks) into every subject's skill.
Check the generated block reads sensibly (e.g. MAA: CA ≈ 65% of marks; cross-topic questions are rare, 6/138).

## 11. App hooks, tests, docs

See subject-profiles.md "Where the assumptions live" for the code list. Minimum for a maths-shaped subject:
`store.SUBJECT_NAMES`, `ui_setup.SUBJECTS`, `generator.SUBJECT`, `build_docs.TOPICS`, `paperid`. Then
`py tools/translate.py ui` for new UI strings, the full test suite (`app/tests/`: unit tests, `smoke_gui`,
`smoke_en`, `smoke_setup` with all subjects ticked), README / AGENTS.md / `<S>/README.md`, and a local commit
without any SCSA-derived file (`git status` check).
