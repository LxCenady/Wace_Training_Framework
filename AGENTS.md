# AGENTS.md — handover for coding agents (Codex, Claude Code, …)

Read this first. It is the state of the project as of 2026-10-12 and the rules the owner works by.
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

**In progress — MAA wrap-up** (uncommitted when this was written):
- tags: three independent reviews + arbitration changed 41 part tags; `tools/parttags_MAA.txt` re-exported
  (`labels.json` → tags is a one-off script; the audit `tools/audit_maa.py --labels evidence/maa/labels.json` is 0 errors;
  its "missing 1 / invalid 1" is 2019, excluded on purpose). Review files: `evidence/maa/tag_review/` (local).
- notes: the 真题 / Past questions lines are regenerated from the tags; a sub-agent is updating the rest of the text
  (resolved labelling remarks, examples now under another pattern, header counts) and appending to 审校记录.md.
- still to do: re-render the notes PDFs (`tools/render_methods.py MAA`), rebuild wace.db, run `tools/blueprint.py`
  (fills the empty blueprint block of `skills/wace-maa-questions/SKILL.md` — that skill was edited to read wace.db,
  not evidence/), commit tags + notes + PDFs + skill.
- 2017 CA Q8: the key's 98 974 is an end-of-period perpetuity while the stem says payments at the start of the year —
  a known inconsistency in the official key, noted in the notes; not a tag issue.

Next planned work: subject packs (`.wtfpack`, `pack.json` index) as WTF's main mods — data only (no code), distributed
via a `packs.json` index of GitHub release assets + local-file import, maths packs bundled in the installer. First a
one-time generalisation so subject names, sections (CalcFree/CalcAssumed is hard-coded in ~15 plugins), key style,
answer checker and sketch words come from packs (`skills/wtf-subject-pack/references/pack-format.md`,
`subject-profiles.md`); verify by rebuilding MAM/MAS/MAA from their packs with 0 differing rows; then Chemistry
(one paper with MC / short / extended sections, description-marks keys, data booklet, no SymPy).
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
5. `ui_setup.SUBJECTS` duplicates `store.SUBJECT_NAMES` — merge when subjects move into packs.
6. rclone's shared Google client_id is retired during 2026 (affects the owner's Drive sync, not the app).
