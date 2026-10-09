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

## Quick start (Windows)

```bat
py -3 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python tools\fetch.py
.venv\Scripts\python tools\build_all.py
app\WACE学习系统.bat
```

`fetch.py` downloads every missing paper. SCSA's site uses bot protection, so some direct downloads may be refused; the script then prints the URLs — open them in a browser, save the PDFs into one folder, and run `tools\fetch.py --from <that folder>`. `build_all.py` then produces `questions.json`, topic PDFs, question banks and `wace.db` (≈ 1 minute). Other platforms: the Python code is portable; the PDF renderers expect Microsoft YaHei (`msyh.ttc`) for CJK text.

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
  fetch.py         sources.tsv -> */papers
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

  The program checks part labels and mark counts between steps; any failure regenerates with the reason (2 retries by default). Nothing answer-like is shown until all steps pass; 「查看验证记录」 shows every raw reply.
- **Settings** (设置 → 模型与 API key): Anthropic format (`/v1/messages`) or OpenAI format (`/chat/completions`) with your own base URL, model and key — any compatible service works. Keys are stored only in `%APPDATA%\wace-maths\config.json` (empty → `ANTHROPIC_API_KEY` / `OPENAI_API_KEY`). `mock` is an offline provider for trying the pipeline.
- **Architecture** (microkernel): `kernel.py` = service registry + events + plugin loader with no domain code; `main.py` = thin glue; `plugins.txt` lists the plugins; each `plugins/*.py` does one job (store, render, llm + one file per provider, generator, ui_shell / tree / pattern / question / generate / settings).
- **Tests**: `app\tests\test_providers.py` (both adapters against a local fake server), `app\tests\smoke_gui.py <dir>` (drives the window with the mock provider and saves screenshots).

Limits: the checker is itself a model (no symbolic re-computation yet); Tk can't render LaTeX, so generated maths is plain Unicode.

## Licence

Code: MIT (`LICENSE`). Notes, tags, cheat sheets and skills: CC BY-NC-SA 4.0. SCSA material: see above.
