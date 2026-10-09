# WTF — WACE Training Framework

A study system for the Western Australian ATAR courses **Mathematics Methods (MAM)** and **Mathematics Specialist (MAS)**, built on the 2016–2025 SCSA past exams:

- every past question split by **topic**, and every **sub-question** tagged with the specific **题型 (question pattern)** it uses (questions combine several patterns, so tags are per part);
- every ratified marking key split into **one row per mark**;
- hand-written, independently reviewed **solving-method notes** per pattern (Chinese with English terms) and 3-page **cheat sheets**;
- a desktop **GUI** (knowledge tree → pattern → past questions, marking key revealed on demand) that can ask an LLM of your choice to **write a similar question, solve it independently, verify it, and split the answer into mark points before showing anything**;
- Claude Code **skills** for generating topic quizzes.

> 中文简介：WACE 数学方法 / 专业数学的刷题系统。真题按知识点与小问题型标注、评分标准拆到每一分、每个题型有解题思路讲义；GUI 里按知识图谱选题型看真题，或让你自己接入的 AI（OpenAI / Anthropic 格式）出相似题——出题、独立解题、独立核对、拆成得分点都通过后才给答案。

## Copyright — the exams are not in this repo

The past exams, marking keys and examination reports are © School Curriculum and Standards Authority (SCSA), licensed only for non-commercial copying *within educational institutions*. They are therefore **not redistributed** here, and neither is anything containing their text or images (`questions.json`, topic PDFs, question banks, `wace.db`). You download them yourself from SCSA and build everything locally — `sources.tsv` lists the official URL of every file (2016–2019 via the Wayback Machine).

Everything else (code, tags, method notes, cheat sheets, skills) is original work in this repo.

## Quick start for students (Windows, nothing to install)

1. Download `WTF-Windows-vX.Y.Z.zip` from the latest [release](../../releases) and extract it anywhere (a USB stick works).
2. Double-click `WTF.exe`. The first run opens the **import wizard**:
   - ① 2016–2019 papers download automatically from the Wayback Machine;
   - ② 2020–2025: click 「打开下一批」 to open 6 official links at a time in your browser and save the PDFs (Ctrl+S in the PDF viewer) into your Downloads folder — any file names: the wizard watches the folder and recognises each paper from its first page;
   - ③ 「建立题库并启动」 builds the question bank (~1 min) and restarts into the full app.
3. For AI questions and explanations, add your own API key in 设置 (default: DeepSeek). Browsing past questions, marking keys and notes needs no key.

Your AI questions and 错题本 live in `generated.db` next to `WTF.exe`. Teachers can prepare a copy without the GUI:
`WTF.exe --import <folder of PDFs> --build` (log in `WTF.log`).

## Quick start for developers

```bat
py -3 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python tools\fetch.py
.venv\Scripts\python tools\build_all.py
app\WACE学习系统.bat
```

`fetch.py` downloads every missing paper. SCSA's site uses bot protection, so some direct downloads may be refused; the script then prints the URLs — open them in a browser, save the PDFs into one folder, and run `tools\fetch.py --from <that folder>`. `build_all.py` then produces `questions.json`, topic PDFs, question banks and `wace.db` (≈ 1 minute). Other platforms: the Python code is portable; the PDF renderers expect Microsoft YaHei (`msyh.ttc`) for CJK text.

## English edition

- **App**: 设置 (Settings) → 模型与 API key → 界面语言 / Language → English, then restart (the first-run wizard has the same switch). Pattern names, method notes and AI explanations switch to English too.
- **Notes**: `MAM/methods_en/`, `MAS/methods_en/` (methods notes + review logs, md + pdf) and `cheatsheet/*_CheatSheet_EN.*`.
- **How it is made**: `tools/translate.py docs` translates the Chinese notes chunk by chunk with the configured model (DeepSeek by default) and caches every chunk; `tools/translate.py ui` builds `app/i18n/en.json` from the Chinese fragments in the code plus any fragment the running app reported missing. The interface code stays single-language: the `i18n` plugin translates text where it reaches Tk. Glossary: 题型 = pattern, 知识点 = topic, 错题本 = mistake book, 得分点 = mark points, 评分标准 = marking key.
- `app/tests/smoke_en.py` opens every main view in English and lists any Chinese still on screen (currently none).

## Layout

```
MAM/ MAS/
  methods/       NN_Topic_解题思路.md/.pdf   题型 patterns: how to recognise, steps, where the marks are,
                                             examiners'-report warnings, cited past questions; 审校记录 = review log
  papers/ topics/ 题库/ questions.json      (built locally, not in git)
cheatsheet/      MAM / MAS cheat sheets (md + pdf, 3 pages each)
skills/          wace-mam-questions, wace-mas-questions (Claude Code skills; paths resolve live:
                 $WACE_MATHS_ROOT, else the folder above skills/)
tools/
  fetch.py         sources.tsv -> */papers; import any-named PDFs (paperid.py recognises a paper from its first page)
  package_win.py   portable Windows release: PyInstaller exe + data files -> dist/WTF-Windows-<ver>.zip
  build_all.py     runs the steps below in order
  segment.py       papers -> questions.json (page regions of every question in exam + key)
  build_docs.py    questions.json + tags_*.txt -> topic PDFs (exam crop + key crop) and .md indexes
  build_bank.py    question-only banks per topic, newest first
  markpoints.py    marking-key text -> one row per mark (tick lines under "Specific behaviours")
  build_db.py      everything -> wace.db; prints any tag / key inconsistency
  tags_*.txt       topic tags per question
  parttags_*.txt   per-sub-question pattern tags, e.g. `2024A 12 a=D6 b=D6 c=D6`
                   (code = topic letter(s) + 题型 number in methods/; a question's patterns = union of its parts)
  audit*.py, evidence.py, render_*.py   checks, evidence packs for the notes, md -> pdf
app/             GUI (below)
```

`wace.db` (SQLite) tables: `topics`, `patterns` (title + method text), `questions` (crop regions, stem, `points_ok`), `parts`, `part_patterns`, `points` (one row per mark). For 16 of 367 questions the key's ticks don't split cleanly (`points_ok = 0`); the GUI then shows the original key crop as the authority. AI-generated questions go to a separate `generated.db`, so rebuilding never deletes them.

## GUI (`app/`)

- **Knowledge tree**: subject → topic → pattern → past questions (showing which parts hit that pattern) and ★ AI questions. Select a pattern for its method notes; select a question for the exam crop, then 「显示评分标准」 for the per-mark points and the official key crop.
- **AI questions**: select one or more patterns (Ctrl-click to combine), choose section and marks, press 「AI 生成相似题」. Each step is a separate model call with no shared context:
  1. *setter* — sees the skill, the pattern notes and real past questions; writes the question and intended answers;
  2. *solver* — sees only the question;
  3. *checker* — compares setter and solver part by part, re-derives any disagreement, checks the question is well-posed;
  4. *examiner* — splits the verified solution into exactly one behaviour per mark.

  Between checker and examiner, **SymPy recomputes** every numeric part from a solver-written expression (e.g. `solve(diff(pi*r**2 + 16*pi/r, r), r)`, `P(Normal('X', 32, 4) > 40)`) and compares it with both models' answers; a disagreement sends the question back. The expression is whitelisted (numbers, arithmetic, known maths functions — no attributes, imports or dunders) and runs in a separate, time-limited process; parts it cannot evaluate are shown as unchecked, never as wrong.
  The program checks part labels and mark counts between steps; any failure regenerates with the reason (2 retries by default). Nothing answer-like is shown until all steps pass; 「查看验证记录」 shows every raw reply.
- **Batch generation**: choose 难度 (基础 / 标准 / 拔高 — calibrated in the prompt against the opening parts, the median past question, and the final parts of the hardest recent questions) and 数量 (1–20). Questions run 4 at a time (`parallel` in the config), each through the full four-step check; a failure only drops that question. The setter is shown the openings of the latest AI questions on the same patterns and told not to reuse their context, function or numbers.
- **我的 AI 题库** (menu 题库, the button under the tree, or Ctrl+B): every generated question; questions with identical pattern tags fold into one group (count + difficulty mix), searching expands matching groups, sort by any column, double-click to open (answers still hidden until clicked).
- **Formula sheet** pinned on the right (newest official sheet; follows the subject you are viewing; drag its edge to resize, re-rendered sharp at any width; F2 hides it).
- **Self-marking (自批卷)**: every part of an AI answer and of a past question's key is labelled with its topic + 题型. Right-click a part → 「此题扣分」, tick the mark points you missed, add a note → it goes into **我的错题本** (Ctrl+E), grouped by pattern, weakest first.
- **错题加强题**: from the 错题本, generate targeted questions for the selected (or weakest) pattern; the setter is told exactly which mark points you lost, so the new question requires those steps.
- **一键讲解**: one click explains a recorded mistake in Chinese — what the part tests, why each missed mark was lost (using your note), the full correct working with every mark shown, and habits to avoid it next time. Cached; 「重新讲解」 asks again.
- **导出练习卷 PDF** (我的 AI 题库): selected questions, whole groups or the current search → a question paper with working space and suggested time, plus an answer paper whose mark points have ☐ boxes for marking on paper.
- **模拟考试** (Ctrl+M): a real past paper or an AI-assembled one (patterns drawn by the marks they carried in past papers, median total and length, difficulty rising), WACE timing (CF 5 + 50 min, CA 10 + 100 min) with auto-submit; then mark each question with right-click and the score updates; history of all attempts.
- **掌握度地图** (Ctrl+G): one tile per pattern — colour = your score rate on it (grey = not attempted), number = marks it carried across past papers; click for the notes, right-click to practise it.
- **间隔复习**: every mistake is reviewed after 1, 3, 7, 14, 30 days (Leitner boxes); the 错题本 shows what is due today, and a review can generate a fresh question aimed at the points you missed.
- **Settings** (设置 → 模型与 API key): Anthropic format (`/v1/messages`) or OpenAI format (`/chat/completions`) with your own base URL, model and key — any compatible service works. **Default: DeepSeek** (`https://api.deepseek.com`, `deepseek-flash`, thinking mode at `reasoning_effort: max`); the per-provider 额外参数 JSON is merged into every request body. Keys are stored only in `%APPDATA%\wace-maths\config.json` (empty → `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`). `mock` is an offline provider for trying the pipeline.
- **Architecture** (microkernel): `kernel.py` = service registry + events + plugin loader with no domain code; `main.py` = thin glue; `plugins.txt` lists the plugins; each `plugins/*.py` does one job (store, render, llm + one file per provider, generator, ui_shell / tree / pattern / question / generate / settings).
- **Tests**: `app\tests\test_providers.py` (both adapters against a local fake server), `app\tests\smoke_gui.py <dir>` (drives the window with the mock provider and saves screenshots).

**Maths and figures.** Generated questions, keys, solutions and explanations are written in LaTeX (`$…$`, `$$…$$`; money as `\$5`) and rendered with [ziamath](https://ziamath.readthedocs.io/) — pure Python, no TeX install — as images in the app and as vectors in exported PDFs. LaTeX that a model wrote with single backslashes inside JSON (`\frac` silently becoming a form feed, `\int` making the JSON invalid) is repaired before use. When a question needs a drawing — a graph to read from, a shape, an Argand diagram, a histogram — the setter gives a **figure spec as data, not code** (curves, shaded regions, implicit curves, points, segments, polygons, circles, vectors, labels, bars; expressions through the same whitelist as the SymPy check), drawn with [ziaplot](https://pypi.org/project/ziaplot/). The solver and checker read the spec, so a figure question is still solved independently; a spec that cannot be drawn sends the question back. Sketch parts can carry the expected graph in the marking key.

`WTF.exe --selftest` (or `python app/main.py --selftest`) checks LaTeX, figures, the SymPy check and the question bank, and writes the result to `WTF.log`.

Limits: parts whose answer is not a number or expression (inequalities, loci, explanations) are verified by the models only; some solver expressions merely restate the answer, which makes their SymPy check weak.

## Licence

Code: MIT (`LICENSE`). Notes, tags, cheat sheets and skills: CC BY-NC-SA 4.0. SCSA material: see above.
