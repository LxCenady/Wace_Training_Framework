# The subject pack file (`.wtfpack`) — protocol v1

The end product of this workflow is **one file** that WTF imports in one click to become a subject:
`<S>-<version>.wtfpack`, a zip with `pack.json` at its root. The pack carries everything hand-made
(catalogue, tags, notes, cheat sheets, skill, subject profile) and only *references* the papers: SCSA papers
and anything cut from them are never inside a pack, so a pack can be shared and committed. On import WTF
reads the manifest, fetches the papers listed (the wizard's usual download / save-in-browser flow), and runs
`build_all` for that subject.

Packs are WTF's main mods: a subject is added by publishing a pack, never by editing the framework. Packs are **data only** — no code. Behaviour a subject needs (a key parser, an answer checker) is a built-in handler of WTF that the pack names; a new kind of handler is the one case that needs a WTF release, and `requires_wtf` says which.

Status: local archive export/inspection/import implemented in `tools/pack.py`; GUI entry in
题库 → 管理科目 → 导入学科包, also available in the setup wizard. Online index/distribution is not implemented.
Only built-in `ticks` marking and `sympy`/`none` checkers are supported; unknown handlers are refused.
MAM/MAS have known parity gaps: strict export refuses them. `--draft` is for local regression, stores
`quality: draft`, and is explicitly shown in GUI confirmation; it does not declare publication readiness.

## Layout

```
pack.json                      the index (below)
sources.tsv                    the subject's paper manifest with download metadata (below); installed as <S>/sources.tsv
catalogue.json                 pattern catalogue (tools/catalogue_<S>.json)
tags.txt  parttags.txt         tools/tags_<S>.txt, tools/parttags_<S>.txt
methods/NN_Topic_解题思路.md    notes, zh   (+ 审校记录.md; PDFs optional — the importer can render)
methods_en/NN_Topic_Methods.md notes, en
cheatsheet/<S>_CheatSheet.md, <S>_CheatSheet_EN.md (+ PDFs optional)
skill/SKILL.md, skill/topics/*.md   → skills/wace-<s>-questions/ (blueprint block is regenerated after build)
```

## sources.tsv (paper manifest)

Every subject — bundled or imported — has its own `<S>/sources.tsv`; there is no shared root manifest any more
(a legacy root `sources.tsv` in an old install is still read, and a subject's own file supersedes it). One paper per line,
tab-separated, first line `#path url method capture sha256 bytes pages need`:

| column | meaning |
|---|---|
| `path` | `<S>/papers/<year>_<S>_<Kind>[_<Section>].pdf` |
| `url` | the official SCSA address (even when the copy comes from the Wayback Machine) |
| `method` | `wayback` (downloaded automatically from the capture below), `browser` (the student saves it from the official site — scripts get HTTP 403), `direct` |
| `capture` | Wayback timestamp (14 digits) of the exact copy; only for `wayback` |
| `sha256` | of the exact copy the tags and crops were made on. A download or import with another hash is refused with 「不是题库标注所用的那一版 PDF」: a re-issued or truncated PDF would put every crop in the wrong place |
| `bytes` `pages` | progress, and a quick check for truncated archive copies |
| `need` | `required` (the bank is built from it; the wizard waits for every one) or `optional` (sample papers, examination reports) |

`tools/sources_meta.py <S>` fills method/capture/sha256/bytes/pages/need from the papers on disk; it finds the capture by
matching the Wayback content digest (base32 SHA-1) against the local file. A pack's manifest must have all eight columns.

## pack.json

```json
{
  "wtf_pack": 1,
  "subject": "CHE",
  "version": "2026.11.0",
  "name": {"zh": "Chemistry 化学", "en": "Chemistry ATAR"},
  "course": "Chemistry ATAR (Units 3-4)",
  "requires_wtf": ">=2.0.0",
  "recognise": {"title": ["chemistry"], "kinds": {"DataBooklet": ["data booklet"]}},
  "papers": {"years": [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025],
             "excluded": {"2016Sample": "not an exam"}},
  "sections": [
    {"code": "MC",  "letter": "M", "zh": "选择题",   "en": "Multiple-choice", "minutes": null, "share": 0.25},
    {"code": "SA",  "letter": "S", "zh": "简答题",   "en": "Short answer",    "minutes": null, "share": 0.35},
    {"code": "ER",  "letter": "E", "zh": "论述题",   "en": "Extended answer", "minutes": null, "share": 0.40}
  ],
  "paper_minutes": [10, 180],
  "topics": [{"code": "EQ", "file": "01_Equilibrium", "zh": "化学平衡", "en": "Chemical equilibrium"}],
  "key_style": "description-marks",
  "checker": "chem",
  "sketch_words": ["draw the structural formula", "complete the diagram", "sketch"],
  "sheets": ["DataBooklet"],
  "files": {"catalogue.json": "sha256:…", "…": "…"}
}
```

Maths packs say `"sections": [{"code": "CalcFree", "letter": "F", "zh": "计算器禁用", "en": "Calculator-free",
"minutes": [5, 50]}, {"code": "CalcAssumed", "letter": "A", …, "minutes": [10, 100]}]`, `"key_style": "ticks"`,
`"checker": "sympy"`, `"sheets": ["FormulaSheet"]`.

Field rules:
- `order`: optional integer for stable subject ordering (the bundled maths packs use 0, 1, 2).
- `papers`: `{years: [...], excluded: {"2019": "why"}}` — the years covered and the reason for every year or paper left out
  (MAA 2019: keys unobtainable). Shown to people, never used to skip files (that is `sources.tsv` `need`).
- `quality`: written by export — `ready` when `pack_status.py` passes, `draft` for `--draft` exports.
- `sections[].short`: compact label (maths CF/CA); defaults to `code`. `recognise` lists section title words used to distinguish separate source files. `minutes: null` means use whole-paper `paper_minutes`; advisory per-section time belongs in `suggested_minutes`.
- Sections are subject metadata, never a framework-wide CA/CF enum. Use stable `code`/`letter` identifiers and localized display names. Maths keeps CF/CA; a shared science paper can display Section One/Two/Three with its question-type name. Verify each subject's official structure before creating its profile.
- `paper_layout`: `separate-sections` (maths) or `shared` (one exam/key containing multiple sections, Chemistry). This describes source files, not the number of sections or their timers.
- `sections[].suggested_minutes`: optional advisory working time within a shared paper. It is separate from `minutes` (reading/working times of an independent paper). Chemistry uses whole-paper `paper_minutes`; do not invent separate reading periods for MC/SA/ER.
- `sections[].share`: score weight, independent of raw marks. Yearly question counts and raw section totals come from the validated papers, not immutable pack constants. Calculate weighted scores per section before summing.
- `scoring`: `{mode: "section-weighted", valid_from: 2024, valid_to: 2025, source: "https://…"}`.
  `raw` uses earned/possible across the supplied questions. Weighted mode requires all positive section shares
  to sum to 1; complete-paper score is `100 * sum(share * earned / possible)`.
  For partial coverage, `paper_percent` is null; `weighted_contribution` is the known contribution and
  `practice_percent` renormalizes only the included section shares. Missing sections are never assigned zero.
  Caller supplies raw maxima for the exact paper/selection, never median targets. An explicit year outside
  the verified range is refused. Bundled maths has verified CF/CA 35%/65% for 2024–2025; older years are not
  certified by this metadata. This is an examination percentage, not a scaled ATAR or school course score.
- `sketch_mode`: `legacy-maths` uses the existing built-in drawing detector; `words` treats `sketch_words`
  as literal phrases. Imported packs cannot inject arbitrary executable expressions or drawing regexes.
- Chemistry stage-0 evidence is in `CHE/README.md`. Its MC key can accept alternative letters; written rubrics can award a capped number of marks from alternatives. A handler must preserve these semantics rather than counting every alternative as an additional mark. Shared question stimuli must survive segmentation.
- `subject`: 2–4 capital letters, unique; becomes the folder name and the id prefix `<S>-<year><letter>-Q<n>`.
- `sections[].letter` is what `parttags.txt` uses (`2024A 9 …`); `code` is the file-name section
  (`2024_<S>_Exam_<code>.pdf`). One paper with several sections: the exam and key are one file each
  (`<year>_<S>_Exam.pdf`), and segmentation assigns each question its section by the section headings.
- `key_style` and `checker` name built-in handlers (`ticks`, `description-marks`, `mc-grid`; `sympy`, `chem`,
  `none`); packs never carry code — the app refuses a pack whose handler it does not have, saying which
  WTF version adds it.
- `files` hashes every other file in the zip; the importer checks them.
- Import accepts only the listed data paths, rejects traversal, Windows path aliases, links, duplicate names,
  unlisted files, unknown handlers and bad hashes. Limits: 2,000 entries, 64 MiB per file, 256 MiB total.
  Installation registers `pack.json` last and rolls back overwritten files on failure; no database is built
  until the normal wizard completes.

## Import (one click: 题库 → 管理科目 → 导入学科包…)

1. Read `pack.json`; refuse with a plain message on a newer `wtf_pack`, a missing handler, or a bad hash.
2. If the subject exists, show old → new version and what changes (patterns, tags counts); replace on yes.
3. Copy files to their places under the data root (`<S>/methods…`, `tools/catalogue_<S>.json`, `tools/(part)tags_<S>.txt`,
   `skills/wace-<s>-questions/`, `cheatsheet/`), and the subject's `sources.tsv` to `<S>/sources.tsv`.
4. Register the subject: an installed pack's `pack.json` stays at `<S>/pack.json`; the subject list, topics,
   sections, recognition words and generator course name are read from these files instead of Python dicts.
5. Tick the subject in the wizard and continue there (download / import papers → `build_all.run([S])` →
   `blueprint.py`). No partial bank: the same "不配齐不建库" rule.

## Distribution

- **Online index**: `packs.json` in the repo lists every published pack `{subject, version, requires_wtf, url, sha256, size}`; `url` points at a GitHub Release asset (same channel as the app updater). 管理科目 shows the list (installed /
  update available / not installed); ticking one downloads, checks the hash, installs, then the wizard fetches papers and builds.
- **Pack updates** are independent of app releases: a newer pack version in the index shows 「数据包有更新」.
- **Local file**: 管理科目 → 导入学科包… accepts any `.wtfpack` (USB, WeChat, Drive, a teacher's own pack); a pack whose
  hash is not in the official index gets a one-line 「非官方来源」 confirmation. Safe because packs are data only.
- **Bundled**: the installer ships the MAM/MAS/MAA packs so the first run works offline; new subjects come from the index.
- Packs contain no SCSA material, so they can be public.

## Export (developer side, end of this workflow)

`py tools/pack.py export <S> [--out dist/]` — collects the files above, writes hashes, refuses if
`scripts/pack_status.py <S>` is not all green or if anything SCSA-derived would be included
(`questions.json`, `wace.db`, `papers/`, topic PDFs, `evidence/`).

## What the app reads from packs (implemented in v2.0: `tools/subjects.py` + `tools/handlers.py`)

| Formerly hard-coded | From pack.json |
|---|---|
| `store.SUBJECT_NAMES`, `ui_setup.SUBJECTS` | `name` |
| `build_docs.TOPICS` | `topics` |
| `paperid.identify` course titles, kinds | `recognise` |
| `generator.SUBJECT` | `course` |
| `CalcFree/CalcAssumed`, `TIMES`, `SEC_NAME`, CF/CA labels in ~15 plugins | `sections`, `paper_minutes` |
| `build_db.SECTION`, `parttags` letters | `sections[].letter` |
| `markpoints.points` | `key_style` |
| SymPy check in the generator | `checker` |
| `partmarks.SKETCH` words | `sketch_words` |
| formula sheet viewer (`ui_formula`) | `sheets` |
