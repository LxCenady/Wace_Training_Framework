# AGENTS.md — handover for coding agents (Codex, Claude Code, …)

Read this first. It is the state of the project as of 2026-10-11 and the rules the owner works by.
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
- Copyright: SCSA papers, keys and anything containing their text (`questions.json`, topic PDFs, `wace.db`, question
  banks) are **never committed or redistributed**. `.gitignore` already covers them.

## What this is

WTF (WACE Training Framework): a desktop study system for WA ATAR Mathematics Methods (MAM) and Specialist (MAS),
built on the 2016–2025 SCSA past exams. Public repo `LxCenady/Wace_Training_Framework`, releases for Windows
(Setup.exe + portable zip) and macOS (two .dmg, built by GitHub Actions). Current version: `app/version.txt` (1.7.0).
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
                          ui_formula, updater, ui_settings, ui_setup (wizard)
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
MAM/ MAS/ methods/ methods_en/   method notes (Chinese + English), cheatsheet/, skills/ (Claude Code skills)
.github/workflows/build-mac.yml  Mac build on release (and on pushes to branch `mac`)
```

Data the app builds locally (not in git): `*/papers/*.pdf`, `questions.json`, `wace.db`, `generated.db` (the user's
AI questions, mistakes, attempts, exams, 工作区), `WTF.log`.

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
..\.venv\Scripts\python tests\smoke_setup.py <empty temp dir> E:\WACE_Maths
```

Run all four before committing UI or pipeline changes. The smoke tests drive the real window; their screenshots
use PowerShell and come out white when the screen is locked or covered (the assertions still run).

Release (only when the owner says so): bump `app/version.txt`, commit, `tools/package_win.py` (makes the zip,
`WTF-Setup-v<ver>.exe` and a fixed-name `WTF-Setup.exe`), check the packaged exe (`--import <pdfs> --build`, then
`--selftest`), `git push`, `gh release create v<ver> <the three files> --notes-file …`. Publishing the release
triggers the Mac workflow, which attaches `WTF-macOS-arm64*.dmg` and `WTF-macOS-x86_64*.dmg`. README links to
`releases/latest/download/<fixed name>` — keep those names.

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

## State and open items (2026-10-11)

Unpushed local commits since v1.7.0: 设置 → 导出文件夹; 常一起考的题型 panel; 工作区 (drag-and-drop basket,
合并导出, 出卷模式); rotated/trimmed setter examples; this file. The owner may want them released as v1.8.0.

Open items, roughly by value:
0. **Hard-coded paper totals disagree with the live ones**: `app/plugins/ui_exam.py` `BLUEPRINT` (MAM CF 52 / CA 98,
   MAS 48 / 89) drives AI mock papers, while 工作区 出卷模式 uses `store.paper_totals` (median since 2020: MAM 51 / 100,
   MAS 48 / 89). Make ui_exam use `store.paper_totals` and delete the constant (keep the question-count part only if
   still needed, or derive it too). Everything else statistical is computed from wace.db at run time; the skills'
   "Paper blueprint" block is a snapshot regenerated by `tools/blueprint.py`.
1. **Mac version untested by a person** — a classmate is trying v1.7.0; expect screenshots (fonts, right-click,
   ⌘ shortcuts, wizard, PDF fonts). Fixes go in `app/plat.py` first.
2. English wizard banner is assembled from fragments and reads awkwardly ("Still missing 63 ."): rewrite those
   lines as whole sentences.
3. Example rotation helps context variety, but the setter still drifts to classic models (open-top tank etc.). A fair
   evaluation needs ≥20 questions per arm; consider listing recent contexts to avoid.
4. A "my own papers" data source (school trial papers the student has; not scraped): import + AI-drafted tags +
   human confirmation, kept out of the blueprint statistics. Discussed, not started.
5. rclone's shared Google client_id is retired during 2026 (affects the owner's Drive sync, not the app).
