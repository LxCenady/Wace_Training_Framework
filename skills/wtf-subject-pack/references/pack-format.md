# The subject pack file (`.wtfpack`) — protocol v1 (draft)

The end product of this workflow is **one file** that WTF imports in one click to become a subject:
`<S>-<version>.wtfpack`, a zip with `pack.json` at its root. The pack carries everything hand-made
(catalogue, tags, notes, cheat sheets, skill, subject profile) and only *references* the papers: SCSA papers
and anything cut from them are never inside a pack, so a pack can be shared and committed. On import WTF
reads the manifest, fetches the papers listed (the wizard's usual download / save-in-browser flow), and runs
`build_all` for that subject.

Packs are WTF's main mods: a subject is added by publishing a pack, never by editing the framework. Packs are **data only** — no code. Behaviour a subject needs (a key parser, an answer checker) is a built-in handler of WTF that the pack names; a new kind of handler is the one case that needs a WTF release, and `requires_wtf` says which.

Status: protocol designed 2026-10; importer/exporter not implemented yet. When implementing, also export
MAM/MAS/MAA as packs and rebuild from them — byte-identical `wace.db` rows prove the protocol is complete.

## Layout

```
pack.json                      the index (below)
sources.tsv                    this subject's manifest lines, same format as the repo's sources.tsv
catalogue.json                 pattern catalogue (tools/catalogue_<S>.json)
tags.txt  parttags.txt         tools/tags_<S>.txt, tools/parttags_<S>.txt
methods/NN_Topic_解题思路.md    notes, zh   (+ 审校记录.md; PDFs optional — the importer can render)
methods_en/NN_Topic_Methods.md notes, en
cheatsheet/<S>_CheatSheet.md, <S>_CheatSheet_EN.md (+ PDFs optional)
skill/SKILL.md, skill/topics/*.md   → skills/wace-<s>-questions/ (blueprint block is regenerated after build)
```

## pack.json

```json
{
  "wtf_pack": 1,
  "subject": "CHE",
  "version": "2026.11.0",
  "name": {"zh": "Chemistry 化学", "en": "Chemistry ATAR"},
  "course": "Chemistry ATAR (Units 3-4)",
  "requires_wtf": ">=1.8.0",
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
- `subject`: 2–4 capital letters, unique; becomes the folder name and the id prefix `<S>-<year><letter>-Q<n>`.
- `sections[].letter` is what `parttags.txt` uses (`2024A 9 …`); `code` is the file-name section
  (`2024_<S>_Exam_<code>.pdf`). One paper with several sections: the exam and key are one file each
  (`<year>_<S>_Exam.pdf`), and segmentation assigns each question its section by the section headings.
- `key_style` and `checker` name built-in handlers (`ticks`, `description-marks`, `mc-grid`; `sympy`, `chem`,
  `none`); packs never carry code — the app refuses a pack whose handler it does not have, saying which
  WTF version adds it.
- `files` hashes every other file in the zip; the importer checks them.

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

## What the app must read from packs instead of code (implementation list)

| Today (hard-coded) | From pack.json |
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
