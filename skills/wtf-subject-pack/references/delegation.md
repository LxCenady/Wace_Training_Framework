# Delegation templates (Haiku 5.5)

Spawn with the Agent tool, `model: "haiku"`, `run_in_background: true`, one agent per independent slice
(year range, topic pair). Every prompt starts with the common block, then the job block. Fill `<…>`.
Agents report in Chinese because the user reads their summaries.

## Common block (paste first)

```
Repo: E:\WACE_Maths (Python: E:\WACE_Maths\.venv\Scripts\python). Subject <S> (<course name>).
Read-only everywhere EXCEPT the output paths named below. Do not edit tools/, app/, labels.json, wace.db,
config files; do not commit or push; do not download anything. Do not use shell heredocs for Python that
contains backslashes — write a .py file and run it. Delete your scratch files at the end.
The SCSA papers are copyrighted: quote at most a short phrase from them in any output.
State the model you are (expected: claude-haiku-5-5) on the first line of your final report, in Chinese.
Sources of truth: <S>/questions.json (stems, regions), <S>/papers/*.pdf (render a crop with pymupdf when a
figure or table matters), tools/catalogue_<S>.json (pattern definitions — cite them).
```

## Labeller (stage 4, one per year range)

```
Job: label every question of <years> (both sections) with catalogue patterns, per part.
For each question read the stem AND the marking key region; a part gets the pattern(s) whose marks it earns
in the key, not every idea it mentions. Part labels and marks must equal tools/partmarks.py split() output.
Write <out>.json: list of records {year, section, q, topics, parts:[{label, marks, tags, reason (≤30 字),
confidence 0–1, visual_checked}], exam_total, key_total, needs_review}. Mark needs_review when confidence <0.7
or no pattern fits (say which definition is missing). Report: counts, low-confidence list, catalogue gaps.
```

## Tag reviewer (stage 4 round 5, one per year range)

```
Job: independently review the current tags of <years> in evidence/<s>/labels.json against the key.
Do not trust the labels' "reason" text. For each part: keep or propose a change, with evidence (the key
behaviour that earns the marks, ≤30 字) and confidence 0–1. Follow the conventions already used in
evidence/<s>/notes/ and earlier years; if you propose breaking a convention, say so explicitly.
Write evidence/<s>/tag_review/<years>.json ({year, section, q, label, current, verdict, proposed, evidence,
confidence}) and .md (counts + change table). Do not modify labels.json.
```

## Arbiter (low-confidence proposals)

```
Job: decide each disputed tag below. You get the part, the current tags, the proposed tags, both reasons,
the catalogue definitions of every code involved, and the key. Answer per item: current | proposed | other
(<codes>), one-line reason, confidence. Prefer consistency with the accepted decisions listed at the end.
Items: <list>  Accepted decisions so far: <list>
```

## Note writer (stage 7, two topics each)

```
Job: write <S>/methods/<NN_Topic>_解题思路.md for topics <A>, <B>, in Chinese, modelled exactly on
MAM/methods/01_Differentiation_解题思路.md (read it first): "# title", intro, then one "## 题型 N：title" per
catalogue pattern of the topic, N = the pattern number, in order; under each: 识别 / 步骤 / 易错点（考试报告） /
真题 (the questions carrying the pattern, from evidence/<s>/notes/INDEX.md, written like 2024 CA Q9(b)).
Use only the evidence pack evidence/<s>/notes/<TOPIC>.txt and the catalogue; paraphrase the reports.
Report: patterns written, any pattern with no past question, anything in the evidence you found contradictory.
```

## Note reviewer (two, independent)

```
Job: review all <S>/methods/*_解题思路.md. Check: every catalogue pattern has exactly one section with the right
number; steps are mathematically/scientifically right against the keys; every 真题 reference exists in
tools/parttags_<S>.txt with that pattern; no copied report paragraphs; the file parses with
tools/build_db.py method_sections(). Write <S>/methods/审校_<reviewer>.md: issue list with file, pattern, problem,
suggested fix, severity. Do not edit the notes.
```

## Others

- **真题 list sync**: give it the final parttags export; it rewrites only the 真题 lines (zh + en) and reports diffs.
- **Cheat sheet**: model on `cheatsheet/MAM_CheatSheet.md`; facts not on the official sheet, procedures, report traps; ≤3 pages rendered.
- **Question skill**: model on `skills/wace-mam-questions/`; per-topic files with patterns, real-paper calibration, traps; leave the blueprint markers empty.
- **Key parser fixes** ("keyfix"): give it the failing question ids and the parser; it proposes a patch and a test, you apply it.

## After an agent finishes

Read its output file, spot-check 2–3 claims against the papers, and check it did not write outside its paths
(`git status`). Then tell the user in a sentence what came back.
