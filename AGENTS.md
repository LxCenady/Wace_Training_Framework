# AGENTS.md — handover for coding agents (Codex, Claude Code, …)

Read this first — then go to **NEXT TASK: subject packs**. It is the state of the project as of 2026-10-12 and the rules the owner works by.
Machine-specific details (paths on the owner's PC, the Google Drive sync, their settings) are in
`HANDOFF.local.md` (not in git) — read it too if it exists.

## The owner and how to work with them

- The owner is a WACE student. **Reply in Chinese** (every user-facing message, including progress notes).
- **KISS + UNIX philosophy**: one module, one job; the kernel stays tiny; features are plugins; `main.py` is thin glue.
- **Do not push or release unless asked** ("发布" / "发" / "push" means go). Commit locally freely, with clear messages.
- **Measure, don't assert.** Claims about question quality, distributions, etc. are backed by numbers from the data
  (the owner caught a 12-mark calculator-free definite integral once; the fix came from data, not prompts).
- Be honest about what was not tested (e.g. the Mac GUI has never been run on a real Mac).
- Tests must **never touch the owner's settings or data**: every test redirects `plugins.config.PATH` to a temp file
  and uses an in-memory `generated.db`.
- The owner prefers fixed, foolproof behaviour over clever options ("写死", "不配齐不建库").
- Work that needs no judgment (evidence packs, first-pass labelling, note drafts, reviews, translation checks) goes to
  cheaper sub-agents (Claude: `model: haiku`); keep catalogues, review samples, arbitration and code for yourself, and
  spot-check every sub-agent claim against the papers before passing it on.
- Downloading anything needs the owner's say-so.
- Copyright: SCSA papers, keys and anything containing their text (`questions.json`, topic PDFs, `wace.db`, question
  banks) are **never committed or redistributed**. `.gitignore` already covers them.

## What this is

WTF (WACE Training Framework): a desktop study system for WA ATAR Mathematics Methods (MAM), Specialist (MAS) and
Applications (MAA, since 2026-10),
built on the 2016–2025 SCSA past exams. Public repo `LxCenady/Wace_Training_Framework`, releases for Windows
(Setup.exe + portable zip) and macOS (two .dmg, built by GitHub Actions). Current version: `app/version.txt` (1.8.0).
README.md describes every feature for users (deadpan-humorous tone on purpose; keep the copyright part serious).

## Layout

```
app/                      the GUI (Python 3.12 + Tk), run: .venv\Scripts\python app\main.py
  kernel.py               service registry + events + plugin loader (no domain code)
  main.py                 thin glue: data root, plugin list; flags --selftest, --import DIR, --build, --symcheck
  plat.py                 every Windows/macOS difference (fonts, data root, open file, right click, ⌘ shortcuts)
  plugins.txt             plugins loaded in order (setup.txt = first-run wizard set, used when wace.db is missing)
  plugins/*.py            one job each: config, i18n, store, render, llm(+openai/anthropic/mock), symcheck, mathtext,
                          figure, generator, ui_shell, ui_tree, ui_pattern, ui_question, ui_generate, ui_mybank,
                          ui_search, ui_workspace, ui_mistakes, ui_explain, ui_exam, ui_mastery, export_pdf,
                          ui_formula, updater, ui_settings, ui_setup (wizard; also 管理科目 via --setup), ui_subjects
                          external_pdf, external_store, external_tagger, ui_external*: independent external library
  i18n/en.json            English UI: CJK fragments -> English (built by tools/translate.py ui)
  tests/                  test_providers.py, smoke_gui.py <dir>, smoke_en.py <dir>, smoke_setup.py <dir> <repo>
tools/                    data pipeline (also bundled into the packaged app)
  fetch.py paperid.py     download / recognise SCSA papers (2016–19 from the Wayback Machine; 2020–25 by browser)
  segment.py              papers -> questions.json (crop regions, stem text)
  partmarks.py            stem text -> marks per part as printed, part texts, drawing parts, figures, preamble
  markpoints.py           marking key -> one row per mark
  build_db.py             everything -> wace.db (tables: topics, patterns, questions, parts, part_patterns, points;
                          view pattern_marks)
  build_docs.py build_bank.py build_all.py
  blueprint.py            real-paper statistics: mock-paper plans (plan), unit questions (unit_plan),
                          per-pattern marks / figure / drawing rates; also writes the skills' blueprint block
  tags_*.txt parttags_*.txt   the hand-made labels (the most valuable data in the repo)
  package_win.py package_mac.py installer.py translate.py render_*.py audit*.py
MAM/ MAS/ MAA/ methods/ methods_en/   method notes (Chinese + English), cheatsheet/, skills/ (Claude Code skills;
                          skills/wtf-subject-pack = how to add a subject, incl. the .wtfpack protocol draft)
.github/workflows/build-mac.yml  Mac build on release (and on pushes to branch `mac`)
```

Data the app builds locally (not in git): `*/papers/*.pdf`, `questions.json`, `wace.db`, `generated.db` (the user's
AI questions, mistakes, attempts, exams, 工作区), `WTF.log`.
External imports live separately in `external.db` and `external/` (both ignored and never redistributed).
The external plugins expose services through the kernel; they never add questions to `store.past_index`,
the SCSA knowledge tree, blueprint, exam weights or paper totals. `skills/wace-external-tagging/SKILL.md`
is the shared runtime instruction for UI and `tools/tag_external.py` API tagging; labels remain human-review drafts.

## Architecture rules

- Plugins talk through `k.provide(name, fn)` / `k.get(name, default)` and `k.on(event)` / `k.emit(event)`.
  A plugin that needs another's widget asks for a service (e.g. `ui.tree.actions`, `tree.widget`, `ui.middle`,
  `workspace.source`, `export.target`) instead of importing it.
- Anything OS-specific goes in `app/plat.py`.
- UI text is Chinese in the code; English comes from `i18n` at the Tk boundary. After adding UI text run
  `tools/translate.py ui` (uses the configured LLM, DeepSeek by default) and **check the new entries**: the machine
  translation often says "past papers" where 真题 means "past questions" — fix by editing `app/i18n/en.json`
  (existing entries are never overwritten by later runs). `smoke_en.py` must report 0 CJK runs.
- Question generation (`plugins/generator.py`): setter -> independent solver -> checker -> SymPy recompute ->
  examiner (one mark point per mark). Marks per pattern come from real question shapes (`blueprint`); figures and
  drawing parts are required at the real papers' rates; examples are rotated (`pick_examples`) and trimmed
  (`example_text`).

## Run, test, build

```bat
.venv\Scripts\python app\main.py                      :: run (source)
.venv\Scripts\python tools\build_all.py               :: rebuild wace.db etc. (close the app first: it locks wace.db)
.venv\Scripts\python app\main.py --selftest            :: LaTeX, figures, SymPy, bank -> WTF.log
cd app
..\.venv\Scripts\python tests\test_providers.py
..\.venv\Scripts\python tests\smoke_gui.py  <empty temp dir>
..\.venv\Scripts\python tests\smoke_en.py   <empty temp dir>
..\.venv\Scripts\python tests\smoke_setup.py <temp dir> E:\WACE_Maths   :: fresh install, all three subjects ticked
..\.venv\Scripts\python tests\test_external.py
..\.venv\Scripts\python tests\smoke_external.py <empty temp dir> en
```

Run all of them before committing UI or pipeline changes. `smoke_gui` / `smoke_en` need the directory to **exist** (create it;
a deleted one fails with "cannot open file … smoke_past.pdf" / a PowerShell screenshot error, not an app bug).
After any pipeline or tag change, build into a temp file (`build_db.build(<tmp>)`) and compare with the current
wace.db per subject: subjects you did not touch must have **0 differing rows** in questions, parts, part_patterns, points. The smoke tests drive the real window; their screenshots
use PowerShell and come out white when the screen is locked or covered (the assertions still run).
The four original tests use `tests.safe_runtime.isolate()` before loading plugins: settings get a fresh temporary
path, generated/external SQLite connections are in memory from their first open, and the owner's wace.db is
read-only. Synthetic external tests use their own temporary PDFs and a local fake API, never real user papers.

Release (only when the owner says so): bump `app/version.txt`, commit, `tools/package_win.py` (makes the zip,
`WTF-Setup-v<ver>.exe` and a fixed-name `WTF-Setup.exe`), check the packaged exe (`--import <pdfs> --build`, then
`--selftest`), `git push`, `gh release create v<ver> <the three files> --notes-file …`. Publishing the release
triggers the Mac workflow, which attaches `WTF-macOS-arm64*.dmg` and `WTF-macOS-x86_64*.dmg`. README links to
`releases/latest/download/<fixed name>` — keep those names.

## NEXT TASK: subject packs (handed to the next agent on 2026-10-12)

Goal (owner's words: 学科包就是主要的模组/插件，不用动框架了): a subject is added by publishing a **subject pack**,
never by editing the framework. A pack is a `.wtfpack` zip with a `pack.json` index; it carries only hand-made data
(catalogue, tags, notes, cheat sheets, question skill, subject profile) and the URLs of the papers, **never SCSA
material and never code**. WTF imports it in one click, fetches the listed papers (same wizard flow, same
不配齐不建库 rule) and builds the subject. Full protocol: `skills/wtf-subject-pack/references/pack-format.md`; where
the code assumes maths: `skills/wtf-subject-pack/references/subject-profiles.md`. Read both first.

Do it in phases, one commit (or a few) per phase, **never push**, and after every phase prove non-regression:
build into a temp file and compare with the current `wace.db` — MAM, MAS and MAA must have **0 differing rows** in
questions, parts, part_patterns, points, patterns (script pattern: `build_db.build(<tmp>)`, then compare
`SELECT … WHERE subject=?` row sets) — and run every test in "Run, test, build". Keep the owner's rules: KISS, one
module one job, main.py thin glue, Chinese UI text + `tools/translate.py ui` for new strings (check 真题 = past questions).

**Phase 1 — subject registry, no behaviour change.**
- Write `MAM/pack.json`, `MAS/pack.json`, `MAA/pack.json` (committed; schema in pack-format.md): names, course,
  topics (from `build_docs.TOPICS`), sections `[{code: CalcFree, letter: F, zh, en, minutes: [5, 50]}, {code: CalcAssumed,
  letter: A, …, minutes: [10, 100]}]`, recognise words (from `paperid.identify`), `key_style: ticks`, `checker: sympy`,
  `sketch_words` (from `partmarks.SKETCH`), `sheets: [FormulaSheet]`.
- New `tools/subjects.py` (one job: read every `<ROOT>/<S>/pack.json`; tools/ is already on sys.path in the app):
  `names()`, `info(S)`, `topics(S)`, `sections(S)`, `section_letter(S, code)`, … Validate with plain checks, fail loudly.
- Replace the literals with it: `store.SUBJECT_NAMES` and `ui_setup.SUBJECTS` (merge the duplicate), `generator.SUBJECT`,
  `build_docs.TOPICS` (may stay as a dict built from the registry so callers keep working), `paperid` course titles,
  `build_db.SECTION`, `fetch.subjects()`.
- Done when: 0 differing rows, all tests pass, `grep '"MAM"'` in app/ and tools/ only finds tests and pack files.

**Phase 2 — sections from the pack.** `CalcFree/CalcAssumed`, CF/CA labels and the 50/100-minute timers are hard-coded
in ~15 places (list in subject-profiles.md: store, export_pdf, external_store, generator, llm_mock, ui_exam, ui_explain,
ui_external, ui_generate, ui_mybank, ui_pattern, ui_question, ui_search, ui_tree, ui_workspace (出卷模式 meters),
segment, paperid, audit_totals, blueprint). Read them from `subjects.sections(S)`. Maths output must look identical:
compare smoke_gui / smoke_en screenshots before and after. Keep it boring: a section is `{code, letter, zh, en, minutes}`.

**Phase 3 — handlers named by the pack.** `markpoints.points` behind a tiny registry `{"ticks": points}`; the
generator's SymPy step runs only when `checker == "sympy"`; `partmarks.is_sketch` uses the pack's `sketch_words`;
`ui_formula` shows the pack's `sheets`. No new handlers yet (Chemistry's `description-marks` key parser and `chem`
checker come with Chemistry). A pack naming an unknown handler is refused with a plain message.

**Phase 4 — export and import.**
- `tools/pack.py export <S> [--out dist/]`: zip `pack.json`, the subject's `sources.tsv` lines, catalogue (if any),
  tags, parttags, `methods/`, `methods_en/`, cheat sheets, `skills/wace-<s>-questions/`; write sha256 of every file into
  `pack.json["files"]`; **refuse** if anything SCSA-derived would go in (`questions.json`, `papers/`, `topics/`, `题库/`,
  `wace.db`, `evidence/`). Refuse unless `skills/wtf-subject-pack/scripts/pack_status.py <S>` passes (except pack.json).
- `tools/pack.py import <file>` (+ the same function for the GUI): check `wtf_pack` version, handlers, hashes; copy into
  place; subject sources go to `<S>/sources.tsv` and `fetch.sources()` reads those too.
- GUI: 题库 → 管理科目 → 「导入学科包…」 (file dialog) → the wizard with that subject ticked.
- Acceptance: on an empty data root, import the three exported maths packs, let the wizard fetch (smoke_setup-style,
  offline with local PDFs) and build: 0 differing rows against the current wace.db. Add this as a test.

**Phase 5 — distribution.** `packs.json` in the repo lists published packs `{subject, version, requires_wtf, url,
sha256, size}`, `url` = a GitHub release asset. 管理科目 lists them (installed / update available / not installed);
installing = download + hash check + import. A pack not in the official index asks one 「非官方来源」 confirmation.
`tools/package_win.py` / the Mac build bundle the three maths packs so the first run works offline. Downloads need the
owner's go-ahead; publishing release assets only when the owner says 发布.

**Then Chemistry** starts at stage 0 of `skills/wtf-subject-pack/SKILL.md` *with the owner* (paper structure, key
style, data booklet, answer checks — the Chemistry column in subject-profiles.md is an unverified first draft).

Not part of this task: changing tags or notes, the MAS points_ok gap (180/193), catalogues for MAM/MAS.

## Adding a subject

Follow `skills/wtf-subject-pack/SKILL.md` (stages 0–12, delegation templates, the `.wtfpack` protocol draft).
`python skills/wtf-subject-pack/scripts/pack_status.py <SUBJ>` prints a parity checklist (MAA 25/28, MAM 24/26, MAS 23/26
on 2026-10-12; the missing items are `pack.json` everywhere, catalogue files for MAM/MAS, MAS points_ok 180/193).
MAA tag conventions decided in the 2026-10-12 arbitration (keep them for new labels): tag the pattern(s) whose marks
the key awards; FIN10 only when the key gives a mark for the rate conversion itself; nominal rate = FIN10, effective
rate = FIN2; FIN1 has no periodic payments (loan with repayments FIN4, annuity FIN7/FIN8); shortest Hamiltonian
path/cycle = GRF6 + GRF4, GRF9 only when vertices may repeat; NDM7 only when the key marks float.

## Pitfalls that already cost time

- **Shell heredocs eat backslashes** (`"\\n"` becomes a real newline, `"\\0"` a NUL byte). Edit Python files with an
  editor tool or a script file, not with `python - <<EOF` containing backslashes.
- `git ls-files` quotes non-ASCII names on other machines: use `git ls-files -z` (done in package_win and tests).
- `event_generate` mouse events all have time 0, so two presses read as a double-click: pass `time=` in tests.
- Key events only reach the focused widget; a binding that returns "break" on ButtonPress skips the class binding,
  so set the focus yourself (see `ui_workspace.source`).
- `winfo_containing` depends on the OS window stacking; use geometry for drop targets.
- The running app holds `wace.db` open: rebuilding fails with WinError 32 — ask the owner to close WTF.
- The 2025 MAM calculator-free paper really is 47 marks (not a data error).
- Download errors on Macs / school networks: HTTPS uses the OS certificate store (`plat.use_system_certificates`,
  truststore; `--selftest` checks it). Never turn certificate verification off.
- `ui_setup.restart(args)` takes arguments: test doubles must accept them (a lambda without parameters made
  smoke_setup report "build did not finish" because the TypeError was swallowed by Tk).

## State and open items (2026-10-12)

Last release: v1.8.0. Unpushed local commits since then (newest first): docs; optional subjects (wizard checkboxes,
题库 → 管理科目 via `--setup`, `ui_subjects`); MAA cheat sheets; 2020/21 MAA formula sheets via Wayback;
wtf-subject-pack skill (2 commits); build_all builds every subject; MAA joins the bank; MAA notes; MAA tooling
(Codex); partmarks (h)/(i) fix; Mac certificate fix (truststore). All tests passed on 2026-10-12. The owner decides
when to release.

**MAA is at parity** (`pack_status.py MAA`: 27/28, only `pack.json` missing): 138 questions, 698 tagged parts, 67 patterns,
points_ok 134/138 (2021 CA Q9 shows its key as an image on purpose). Tags were reviewed by three independent passes +
arbitration on 2026-10-12 (41 parts changed; files in `evidence/maa/tag_review/`, local); notes, stars and counts
follow the tags; MAM/MAS rows unchanged. 2017 CA Q8: the official key's 98 974 is an end-of-period perpetuity while the
stem says start of year — a known key inconsistency, noted in the notes, not a tag issue.

Subject packs in progress (2026-10-11): Phase 1 migrates the three maths names, courses, topics, recognition
titles and section letters to `<S>/pack.json`, read by `tools/subjects.py`; packaging includes the registry.
The registry accepts shared-paper sections with `minutes: null` and whole-paper `paper_minutes`.
Temporary rebuild compared 8,740 rows across questions, parts, part_patterns, points and patterns: 0 differences
for MAM/MAS/MAA. Section selectors, timer consumers, handlers and pack import/export still need Phases 2–5.
All six app checks passed; both English smoke checks reported 0 CJK runs. Two registry tests passed;
protected config/generated/wace/external files remained unchanged by SHA-256. Evidence: `evidence/packs/` (ignored).
The owner confirmed sections must be metadata: maths CF/CA, science Section One/Two/Three; verify science
profiles against official papers. Chemistry stage-0 findings are in `CHE/README.md`; no chemistry pack installed.

Open items, roughly by value:
0. **Completed locally**: AI mock papers and 工作区 now both use `store.paper_totals` (MAM 51 / 100,
   MAS 48 / 89 in the current data); `BLUEPRINT` was deleted. Everything statistical is computed from wace.db
   at run time; the skills' "Paper blueprint" block is a snapshot regenerated by `tools/blueprint.py`.
1. **Mac**: a classmate's v1.7.0 hit CERTIFICATE_VERIFY_FAILED / Errno 61 on downloads; fixed locally with truststore
   (unreleased, not yet confirmed on a real Mac). Fonts, right-click, ⌘ shortcuts, wizard and PDF fonts still need a
   person's screenshots. Fixes go in `app/plat.py` first.
2. **Completed locally**: English notes and UI dictionary retranslated; wizard status messages now use whole
   Chinese source sentences, with reviewed English fragments. Continue checking runtime English with smoke_en.
3. Example rotation helps context variety, but the setter still drifts to classic models (open-top tank etc.). A fair
   evaluation needs ≥20 questions per arm; consider listing recent contexts to avoid.
4. **Implemented locally**: external paper/answer pairs, draft heading-based crops, manual rectangles (including
   scans/rotated pages), pattern tags, API proposals + human confirmation, and separate external search.
   OCR is not included; scan text can be entered manually. Real external-school-paper tagging and Mac GUI
   have not been tested; synthetic PDF/database tests and local fake API cover the mechanics.
5. Subject names in setup/store now come from the same pack registry; no duplicate literal list.
6. rclone's shared Google client_id is retired during 2026 (affects the owner's Drive sync, not the app).
