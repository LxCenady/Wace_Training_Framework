# WTF — WACE Training Framework

> *Yes, the acronym is intentional. No, we will not be taking questions about it. Mostly because the app will generate them for you.*

WTF is a serious, rigorously engineered study system for the Western Australian ATAR courses **Mathematics Methods (MAM)** and **Mathematics Specialist (MAS)**, built on the 2016–2025 SCSA past exams. It exists because the average student's revision strategy — "open a past paper, feel bad, close the past paper" — has a measured completion rate of approximately zero.

What it actually does, stated with a straight face:

- every past question is split by **topic**, and every **sub-question** is tagged with the specific **题型 (question pattern)** it uses. Per part, not per question, because examiners enjoy putting three topics into one question and calling it "(c)";
- every ratified marking key is split into **one row per mark**, so you can see exactly which tick you donated to the examiner;
- hand-written, independently reviewed **solving-method notes** for every pattern (Chinese with English terms) and 3-page **cheat sheets**, for those who believe 3 pages is "light reading";
- a desktop **GUI** (knowledge tree → pattern → past questions, marking key hidden until you are brave enough) that can ask an LLM of your choice to **write a similar question, solve it independently, check it, and split the answer into mark points before showing you anything**. The AI marks its own homework, then a different AI marks that, then SymPy marks both. Trust issues are a feature;
- Claude Code **skills** for generating topic quizzes, for when one AI is not enough.

> 中文简介：WACE 数学方法 / 专业数学刷题系统，名字缩写纯属巧合（并不是）。真题按知识点与小问题型标注，评分标准拆到每一分，每个题型都有解题思路讲义。GUI 里按知识图谱选题型看真题，或者让你自己接入的 AI（OpenAI / Anthropic 格式）出相似题：出题、独立解题、独立核对、SymPy 复算、拆成得分点，全部通过才给答案。AI 不被信任，这是设计。

## Copyright — the exams are not in this repo (this part is not a joke)

The past exams, marking keys and examination reports are © School Curriculum and Standards Authority (SCSA), licensed only for non-commercial copying *within educational institutions*. They are therefore **not redistributed** here, and neither is anything containing their text or images (`questions.json`, topic PDFs, question banks, `wace.db`). You download them yourself from SCSA and build everything locally — `sources.tsv` lists the official URL of every file (2016–2019 via the Wayback Machine).

Everything else (code, tags, method notes, cheat sheets, skills) is original work in this repo.

## Quick start for students (Windows, nothing to install, allegedly)

1. Download **`WTF-Setup-vX.Y.Z.exe`** from the latest [release](../../releases) and double-click it. It installs for you only (no administrator rights, default `%LOCALAPPDATA%\Programs\WTF`), adds desktop and Start-menu shortcuts and starts the app. Running a newer setup over an old install upgrades it and keeps your papers, AI questions and mistakes, because deleting a student's 错题本 is how wars start. (Allergic to installers? `WTF-Windows-vX.Y.Z.zip` is the same app — extract anywhere, a USB stick works.)
   Windows SmartScreen will warn you because the app is not code-signed. Code signing costs money; this README is free. *More info → Run anyway.*
2. The first run opens the **import wizard**, which starts working before you have finished reading it:
   - ① the 2016–2019 papers download by themselves from the Wayback Machine, three at a time, with an ETA. The Internet Archive is a national treasure running on what appears to be a single hamster; please be patient with the hamster;
   - ② 2020–2025: click 「打开下一批」 to open 6 official links at a time in your browser and save the PDFs (Ctrl+S in the PDF viewer) into your Downloads folder. File names do not matter — the wizard watches the folder and recognises each paper from its first page. Name them `asdf (3).pdf` if you must; we have seen worse;
   - ③ once the last paper arrives, the bank is built (~1 min) and the app restarts into the full interface. You did not have to touch a terminal. You're welcome.

   Downloads retry dropped connections, timeouts and "too many requests" with polite, growing pauses, and failed files get a second round; update downloads resume where they stopped. Sample papers are skipped because nobody has ever needed them. The window sizes itself to your screen and is DPI-aware, so it is sharp at 125–200 % scaling instead of looking like it was rendered on a potato.
3. For AI questions and explanations, add your own API key in 设置 (default: DeepSeek). Browsing past questions, marking keys and notes needs no key, no account and no subscription. We checked: still no subscription.

Your AI questions and 错题本 live in `generated.db` next to `WTF.exe`. Teachers can prepare a copy without the GUI — i.e. without having to look at it:
`WTF.exe --import <folder of PDFs> --build` (log in `WTF.log`).

## Features at a glance

| Feature | Where | What it does |
|---|---|---|
| Knowledge tree | left pane | subject → topic → 题型 (pattern) → every past question that uses it, plus your ★ AI questions |
| Pattern notes | click a pattern | how to recognise it, the steps, where the marks are, examiners' warnings, and how many marks it usually carries per section |
| Past questions | click a question | the original exam crop; 「显示评分标准」 reveals the official key, split one row per mark |
| AI similar questions | select pattern(s) → 「AI 生成相似题」 | new question, independently solved, cross-checked, SymPy-verified, split into mark points — answers stay hidden until you ask |
| Unit questions | select a unit title → 「AI 生成相似题」 | questions on a whole unit, each built on a real question's shape: patterns, marks and cross-unit pairings follow the unit's real statistics (shown on the unit's page) |
| Batch generation | 难度 + 数量 under the tree | up to 20 questions at a time, 基础 / 标准 / 拔高 |
| Past question search | 「真题搜索」 next to 「AI 生成相似题」, or Ctrl+F | find past questions by any mix of patterns and units (all-of / any-of), cross-unit only, with a drawing part or a figure, by year, marks and words; see which patterns and units appear together; export the results as PDF |
| 我的 AI 题库 | Ctrl+B | every AI question, arranged like the knowledge tree (subject → unit → pattern), searchable, exportable |
| Self-marking | right-click a part → 「此题扣分」 | tick the mark points you lost; they go to the 错题本 |
| 错题本 | Ctrl+E | mistakes grouped by pattern, weakest first; 一键讲解, 错题加强题, spaced review |
| Mock exam | Ctrl+M | real past paper or AI-assembled paper, WACE timing, auto-submit, marking, history |
| 掌握度地图 | Ctrl+G | one tile per pattern, coloured by your score rate |
| Formula sheet | right pane (F2) | the official sheet for the subject you are viewing, resizable |
| PDF export | 我的 AI 题库 / a finished batch / 真题搜索 / mock exam | question paper (one question per page, rest is working space) + answer paper with ☐ mark boxes |
| English UI | 设置 → 界面语言 | the whole interface, notes and explanations in English |
| Updates | 帮助 → 检查更新 | download, verify and install new releases without losing your data |

## How to use it

**1. Learn a pattern.** Expand a topic in the tree and click a 题型. Read the method notes; the grey line under the title says how many marks it usually carries in calculator-free and calculator-assumed papers. Expand the pattern to see every past question on it — the list shows which parts use it.

**2. Do past questions, then mark yourself.** Click a question, do it on paper (formula sheet on the right, F2 to hide it), then press 「显示评分标准」. For every part you dropped marks on, right-click the part (or a mark point) → 「此题扣分」, tick the points you missed and add a note in your own words. That is the whole bookkeeping; the app does the rest.

**3. Get new questions when the past ones run out.** Select a **unit title** to practise the whole unit the way the exam tests it, or one pattern, or Ctrl-click several patterns to combine them; choose 卷型 (CF/CA/任意), 总分 (0 = let the real papers decide), 难度 and 数量; press 「AI 生成相似题」. A unit's page lists what unit questions are built from: its real questions per section, how often they cross into other units and with which, and each pattern's share of the unit's marks, usual marks and how often it comes with a figure or a drawing part. Each question appears under ★ in the tree and in 我的 AI 题库 once it has passed every check. Answers are hidden: do it first, then reveal and self-mark exactly as with past questions.

**4. Close the loop in the 错题本 (Ctrl+E).** Weakest patterns come first. Select a mistake and press 「一键讲解所选错题」 for a full explanation of each mark you lost; 「生成错题加强题」 writes new questions that require exactly the steps you got wrong (with nothing selected, it targets your weakest pattern). Mistakes come back for review after 1, 3, 7, 14 and 30 days: tick 「只看今日待复习」, right-click a mistake → 「复习：做一道同题型新题」, then mark it 「复习通过」 or 「又错了」.

**5. Sit a mock exam (Ctrl+M).** Choose subject, section and a real year or 「AI 组卷」. AI papers are assembled while you watch (each question's patterns and marks are listed); start when ready. Reading time and working time follow WACE (CF 5 + 50 min, CA 10 + 100 min) and the paper submits itself at the end. Then open each question, reveal the key, right-click to deduct, and the score updates. Every attempt is kept in the history.

**6. Print.** In 我的 AI 题库, select questions (or whole groups, or a search) → 导出练习卷 PDF; mock exams have their own export. You get a question paper with one question per page and an answer paper where no question is split across pages, each mark point with a ☐ to tick.

**6½. Search the past papers (Ctrl+F).** Select patterns or a unit in the tree and press 「真题搜索」: every past question that contains all of them (or any of them), with each pattern's marks, whether it crosses units and whether it has a drawing part. Under the list: the patterns and units that most often come together with your choice — the cross-pattern index. Tick 「只看跨单元」 to see only cross-unit questions. 「导出 PDF」 exports the selected results (or all of them): the questions cut from the original papers as vectors, one per page, and their marking keys.

**7. Watch the map (Ctrl+G).** Each tile is a pattern; colour is your score rate, grey means not attempted, the number is how many marks it carried across past papers. Big number + red tile = where your next hour goes. Right-click a tile to practise it.

**Shortcuts:** Ctrl+F 真题搜索 · Ctrl+B 我的 AI 题库 · Ctrl+E 错题本 · Ctrl+M 模拟考试 · Ctrl+G 掌握度地图 · F2 formula sheet · Ctrl-click patterns to combine · double-click to open · right-click a part to deduct marks.

> **中文使用说明**
> 1. **学题型**：左侧知识图谱点开知识点 → 点题型，看解题思路；标题下灰字是这个题型在 CF / CA 卷里一般占几分。展开题型可以看到所有用到它的真题。
> 2. **刷真题 + 自批**：点真题，在纸上做完再点「显示评分标准」。哪一小问扣分了就右键 →「此题扣分」，勾掉丢的得分点、写一句备注，自动进错题本。
> 3. **AI 出题**：选**单元标题**按该单元真题的题型分布、分值和跨单元搭配出题（单元页面会列出这些统计）；或选一个题型（Ctrl+点击可多选组合），设卷型、总分（0 = 按真题自动）、难度、数量，点「AI 生成相似题」。通过全部校验才入库，答案默认隐藏。
> 4. **错题闭环**（Ctrl+E）：薄弱题型排前面；「一键讲解所选错题」逐分讲清楚丢在哪；「生成错题加强题」专练丢分步骤；按 1/3/7/14/30 天间隔复习（勾「只看今日待复习」，右键错题做复习题）。
> 5. **模拟考**（Ctrl+M）：真题年份或 AI 组卷，WACE 计时、到点自动交卷，交卷后右键扣分出成绩，历史全部保留。
> 6. **打印**：我的 AI 题库（Ctrl+B）里选题 →「导出练习卷 PDF」：试卷每题一页，答案卷不跨页、每个得分点带 ☐。
> 6½. **真题搜索**（Ctrl+F，在「AI 生成相似题」旁边）：在左侧选题型或单元，查同时包含（或包含任一）的所有真题，可只看跨单元、含作图小问、有配图；列表下方是常一起出现的题型和单元（跨题型索引）；「导出 PDF」把结果从原卷矢量裁切成试题 + 评分标准。批量 AI 出题完成后也可「导出本批 PDF」。
> 7. **掌握度地图**（Ctrl+G）：颜色是得分率，数字是该题型历年总分值。分值大又发红的，就是下一小时该去的地方。

## Quick start for developers

```bat
py -3 -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python tools\fetch.py
.venv\Scripts\python tools\build_all.py
app\WACE学习系统.bat
```

`fetch.py` downloads every missing paper. SCSA's site has bot protection, and to SCSA your script is a bot (it is), so some direct downloads will be refused; the script then prints the URLs — open them in a browser like a human, save the PDFs into one folder, and run `tools\fetch.py --from <that folder>`. `build_all.py` then produces `questions.json`, topic PDFs, question banks and `wace.db` (≈ 1 minute, or one coffee if you sip fast). Other platforms: the Python code is portable; the PDF renderers expect Microsoft YaHei (`msyh.ttc`) for CJK text. Linux users already know how to fix that, and will tell you.

## English edition

- **App**: 设置 (Settings) → 模型与 API key → 界面语言 / Language → English, then restart (the first-run wizard has the same switch). Pattern names, method notes and AI explanations switch to English too.
- **Notes**: `MAM/methods_en/`, `MAS/methods_en/` (method notes + review logs, md + pdf) and `cheatsheet/*_CheatSheet_EN.*`.
- **How it is made**: `tools/translate.py docs` translates the Chinese notes chunk by chunk with the configured model (DeepSeek by default — outsourcing, essentially) and caches every chunk; `tools/translate.py ui` builds `app/i18n/en.json` from the Chinese fragments in the code plus any fragment the running app reported missing. The interface code stays single-language: the `i18n` plugin translates text at the exact moment it reaches Tk, which is either elegant or unhinged depending on who you ask. Glossary: 题型 = pattern, 知识点 = topic, 错题本 = mistake book, 得分点 = mark points, 评分标准 = marking key.
- `app/tests/smoke_en.py` opens every main view in English and lists any Chinese still on screen (currently none; it was very thorough about this).

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
  package_win.py   Windows release: PyInstaller app -> dist/WTF-Windows-<ver>.zip + WTF-Setup-<ver>.exe
  installer.py     the setup exe: per-user install, shortcuts, upgrades keep user data
  build_all.py     runs the steps below in order
  segment.py       papers -> questions.json (page regions of every question in exam + key)
  build_docs.py    questions.json + tags_*.txt -> topic PDFs (exam crop + key crop) and .md indexes
  build_bank.py    question-only banks per topic, newest first
  markpoints.py    marking-key text -> one row per mark (tick lines under "Specific behaviours")
  build_db.py      everything -> wace.db; prints any tag / key inconsistency
  blueprint.py     real paper statistics -> mark distribution + cross-topic pairings for skills and mock exams
  tags_*.txt       topic tags per question
  parttags_*.txt   per-sub-question pattern tags, e.g. `2024A 12 a=D6 b=D6 c=D6`
                   (code = topic letter(s) + 题型 number in methods/; a question's patterns = union of its parts)
  audit*.py, evidence.py, render_*.py, translate.py   checks, evidence packs for the notes, md -> pdf, translation
app/             GUI (below)
```

`wace.db` (SQLite) tables: `topics`, `patterns` (title + method text), `questions` (crop regions, stem, `points_ok`), `parts` (marks of every part as printed on the paper — `tools/partmarks.py` reads the "(n marks)" after each (a)/(b)(i), and they agree with the marking key's tick count on every question where that count is clean), `part_patterns`, `points` (one row per mark), `questions.figure` / `parts.sketch` (whether the question shows a graph or diagram, and whether the part asks the student to sketch, draw, plot, shade or mark on it — read from the stems and the exam crops), and the view `pattern_marks` (every real question × pattern × topic × section → the marks that pattern carried in it), which feeds the mock-exam blueprint, the skills and the "marks" line on each pattern page. For 16 of 367 questions the key's ticks do not split cleanly (`points_ok = 0`) — the marking key, too, has its moods — and the GUI then shows the original key crop as the authority. AI-generated questions go to a separate `generated.db`, so rebuilding never deletes them.

## How it works (`app/`)

- **Knowledge tree**: subject → topic → pattern → past questions (showing which parts hit that pattern) and ★ AI questions. Select a pattern for its method notes; select a question for the exam crop, then 「显示评分标准」 for the per-mark points and the official key crop. Peeking early is between you and your conscience.
- **AI questions**: select one or more patterns (Ctrl-click to combine), choose section and marks, press 「AI 生成相似题」. Each step is a separate model call with no shared context, so no model can copy another model's homework:
  1. *setter* — sees the skill, the pattern notes and real past questions; writes the question and intended answers;
  2. *solver* — sees only the question;
  3. *checker* — compares setter and solver part by part, re-derives any disagreement, checks the question is well-posed;
  4. *examiner* — splits the verified solution into exactly one behaviour per mark.

  Between checker and examiner, **SymPy recomputes** every numeric part from a solver-written expression (e.g. `solve(diff(pi*r**2 + 16*pi/r, r), r)`, `P(Normal('X', 32, 4) > 40)`) and compares it with both models' answers; a disagreement sends the question back. The expression is whitelisted (numbers, arithmetic, known maths functions — no attributes, imports or dunders) and runs in a separate, time-limited process; parts it cannot evaluate are shown as unchecked, never as wrong. SymPy has no opinions, which is exactly why it is here.
  The program checks part labels and mark counts between steps; any failure regenerates with the reason (2 retries by default). Nothing answer-like is shown until all steps pass; 「查看验证记录」 shows every raw reply, for the forensically inclined.
- **Batch generation**: choose 难度 (基础 / 标准 / 拔高 — calibrated in the prompt against the opening parts, the median past question, and the final parts of the hardest recent questions) and 数量 (1–20). Questions run 4 at a time (`parallel` in the config), each through the full four-step check; a failure only drops that question. The setter is shown the openings of the latest AI questions on the same patterns and told not to reuse their context, function or numbers — otherwise every question would be about a farmer and his fence.
- **Unit questions**: select a unit title instead of a pattern. Each question takes the shape of a real question led by that unit — its patterns and the marks each carried — varied the same way as mock-paper questions (same-unit swaps, ±1 mark). Real shapes are drawn without replacement, so a batch does not repeat itself and still matches the unit: over 2,000 simulated questions per unit, the cross-unit rate is within 2 points of the real one for all 14 units and each pattern's share of the unit's marks within 3.4 %. With section 任意, CF and CA come as often as the unit's real questions sit in each.
- **我的 AI 题库** (menu 题库, the button under the tree, or Ctrl+B): every generated question, arranged like the knowledge tree — subject → unit → pattern → questions, only where there are questions, with counts and the difficulty mix. A question sits once, under its lead pattern; its other patterns have their own column. Searching expands what matches; sort by any column; double-click to open (answers still hidden); selecting a subject, unit or pattern exports everything under it.
- **Formula sheet** pinned on the right (newest official sheet; follows the subject you are viewing; drag its edge to resize, re-rendered sharp at any width; F2 hides it, for those who have memorised it, or claim to have).
- **Self-marking (自批卷)**: every part of an AI answer and of a past question's key is labelled with its topic + 题型. Right-click a part → 「此题扣分」, tick the mark points you missed, add a note → it goes into **我的错题本** (Ctrl+E), grouped by pattern, weakest first. Honesty is not enforced, merely encouraged.
- **错题加强题**: from the 错题本, generate targeted questions for the selected (or weakest) pattern; the setter is told exactly which mark points you lost, so the new question requires those exact steps. It remembers. It is patient.
- **一键讲解**: one click explains a recorded mistake — what the part tests, why each missed mark was lost (using your note), the full correct working with every mark shown, and habits to avoid it next time. Cached; 「重新讲解」 asks again if the first explanation did not land.
- **导出练习卷 PDF** (我的 AI 题库): selected questions, whole groups or the current search → a question paper with suggested time, one question per page and the rest of the page (plus a blank page if that is not enough, ~3 lines per mark) as working space, and an answer paper whose mark points have ☐ boxes for marking on actual paper, the ancient medium. Answers share pages, but a question that does not fit moves whole to the next page — nothing is cut in half unless it is longer than a page.
- **模拟考试** (Ctrl+M): a real past paper or an AI-assembled one. Every AI question is built on the shape of a real question — which patterns it combined and how many marks each carried — then reshuffled: patterns swapped for same-topic ones that have carried that many marks, marks nudged by one inside what real papers show. Topic shares, question counts and cross-topic pairings land within a few percent of the real papers, no two mock papers are alike, and none of them are kind. (Earlier versions once offered a 12-mark calculator-free definite integral. That examiner has been let go.) WACE timing (CF 5 + 50 min, CA 10 + 100 min) with auto-submit, a live progress display while the paper is being assembled, and export to PDF; then mark each question with right-click and watch the score update in real time; history of all attempts, kept forever.
- **掌握度地图** (Ctrl+G): one tile per pattern — colour = your score rate on it (grey = not attempted, i.e. avoided), number = marks it carried across past papers; click for the notes, right-click to practise it.
- **间隔复习**: every mistake comes back after 1, 3, 7, 14 and 30 days (Leitner boxes), like a sequel nobody asked for. The 错题本 shows what is due today, and a review can generate a fresh question aimed at the points you missed.
- **Settings** (设置 → 模型与 API key): Anthropic format (`/v1/messages`) or OpenAI format (`/chat/completions`) with your own base URL, model and key — any compatible service works. **Default: DeepSeek** (`https://api.deepseek.com`, `deepseek-flash`, thinking mode at `reasoning_effort: max`, because "min" felt disrespectful to the exam); the per-provider 额外参数 JSON is merged into every request body. Keys are stored only in `%APPDATA%\wace-maths\config.json` (empty → `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`). An empty balance (HTTP 402) or a bad key stops the batch with a readable message instead of failing 20 questions one by one. `mock` is an offline provider for trying the pipeline without paying anyone.
- **Architecture** (microkernel): `kernel.py` = service registry + events + plugin loader with no domain code whatsoever; `main.py` = thin glue; `plugins.txt` lists the plugins; each `plugins/*.py` does one job (store, render, llm + one file per provider, generator, symcheck, mathtext, figure, updater, and one file per view). Plugins mostly talk through the kernel's services and events rather than poking each other directly, which is the closest software gets to a healthy relationship.
- **Tests**: `app\tests\test_providers.py` (both adapters against a local fake server), `app\tests\smoke_gui.py <dir>` (drives the window with the mock provider and saves screenshots), `smoke_en.py`, `smoke_setup.py` (the wizard, offline). Tests use their own config file and never touch yours.

**Maths and figures.** Generated questions, keys, solutions and explanations are written in LaTeX (`$…$`, `$$…$$`; money as `\$5`) and rendered with [ziamath](https://ziamath.readthedocs.io/) — pure Python, no TeX install, no 4 GB download — as images in the app and as vectors in exported PDFs. LaTeX that a model wrote with single backslashes inside JSON (`\frac` silently becoming a form feed, `\int` making the JSON invalid) is repaired before use; models do this a lot and never apologise. When a question needs a drawing — a graph to read from, a shape, an Argand diagram, a histogram — the setter gives a **figure spec as data, not code** (curves, shaded regions, implicit curves, points, segments, polygons, circles, vectors, labels, bars; expressions through the same whitelist as the SymPy check), drawn with [ziaplot](https://pypi.org/project/ziaplot/). The solver and checker read the spec, so a figure question is still solved independently; a spec that cannot be drawn sends the question back. Figures and drawing parts come at the real papers' rates: every pattern knows how often its real questions show a figure and how often they make the student draw (slope-field questions: always a figure, half the time "draw the solution curve"; graph transformations: a sketch about 70 % of the time), each new question rolls against those odds, and a question that rolled a figure or a drawing part and came back without one is sent back. Drawing parts give the student blank, scaled axes (or the slope field, the Argand diagram) and carry the completed drawing in the marking key. Slope fields are a figure element of their own (`{"slope": "dy/dx", "step": 0.5}`), vertical where the gradient is undefined, as on the real papers.

**Updates.** At start-up (at most once a day; switch off in Settings) and from 帮助 → 检查更新, the app asks GitHub for the latest release. The packaged app can then download it (resuming if the connection drops), verify its SHA-256 (published by GitHub) and that it contains `WTF.exe`, and — after it exits — copy the new files over its folder without touching the student's papers, `generated.db` or `WTF.log`; it restarts and rebuilds the question bank by itself (≈1 min). Source checkouts are only told about the new release (you have `git pull`; use it). The version lives in `app/version.txt`.

`WTF.exe --selftest` (or `python app/main.py --selftest`) checks LaTeX, figures, the SymPy check and the question bank, and writes the result to `WTF.log`. If something crashes, it is in `WTF.log` too. Fittingly named.

**Known limits** (stated plainly, as is tradition): parts whose answer is not a number or expression (inequalities, loci, explanations) are verified by the models only; some solver expressions merely restate the answer, which makes their SymPy check weak; and no part of this software will sit the exam for you. We looked into it.

## Licence

Code: MIT (`LICENSE`). Notes, tags, cheat sheets and skills: CC BY-NC-SA 4.0. SCSA material: © SCSA, not included, see above.
