# WTF — WACE Training Framework

> *Yes, the acronym is intentional. No, we will not be taking questions about it. Mostly because the app will generate them for you.*

## ⬇ Download

| | |
|---|---|
| **Windows** | [**WTF-Setup.exe**](https://github.com/LxCenady/Wace_Training_Framework/releases/latest/download/WTF-Setup.exe) — double-click it. That is the whole installation. |
| **Mac, Apple silicon** (M1–M4) | [**WTF-macOS-arm64.dmg**](https://github.com/LxCenady/Wace_Training_Framework/releases/latest/download/WTF-macOS-arm64.dmg) |
| **Mac, Intel** | [**WTF-macOS-x86_64.dmg**](https://github.com/LxCenady/Wace_Training_Framework/releases/latest/download/WTF-macOS-x86_64.dmg) |

On a Mac: open the .dmg and drag WTF onto Applications. The app is not signed by Apple (that costs a yearly fee; this README remains free), so the first time **right-click WTF in Applications → Open → Open**. Not sure which Mac you have? Apple menu → About This Mac: "Apple M…" means Apple silicon, "Intel" means Intel. Your data lives in `~/Library/Application Support/WTF`.
The Mac version is new: if something looks off, a screenshot in an [issue](https://github.com/LxCenady/Wace_Training_Framework/issues) is the fastest fix.

(Other files and release notes: [latest release](https://github.com/LxCenady/Wace_Training_Framework/releases/latest).)

> **Teachers and students: please do not attempt to run WTF by reading the code.** It does not run that way. We have checked, at length. Download the installer above and let the computer do the reading.
>
> **老师、同学们：请不要试图通过阅读代码来运行 WTF。** 读代码它是不会跑起来的，我们认真试过了。点上面的链接下载安装包，双击即可（Mac：打开 dmg，把 WTF 拖进「应用程序」，第一次在「应用程序」里右键 WTF →「打开」）。

**Only here for the notes?** Read the PDFs, not the `.md` files — GitHub's Markdown preview and maths are not on speaking terms:
method notes [MAM](MAM/methods) · [MAS](MAS/methods) · [MAA](MAA/methods) · [Chemistry](CHE/methods) · [Physics](PHY/methods) · [Accounting and Finance](ACF/methods) (English: [MAM](MAM/methods_en) · [MAS](MAS/methods_en) · [MAA](MAA/methods_en) · [Chemistry](CHE/methods_en) · [Physics](PHY/methods_en) · [Accounting and Finance](ACF/methods_en)), cheat sheets [MAM](cheatsheet/MAM_CheatSheet.pdf) · [MAS](cheatsheet/MAS_CheatSheet.pdf) · [MAA](cheatsheet/MAA_CheatSheet.pdf) · [Chemistry](cheatsheet/CHE_CheatSheet.pdf) · [Accounting and Finance](cheatsheet/ACF_CheatSheet.pdf) (English: [MAM](cheatsheet/MAM_CheatSheet_EN.pdf) · [MAS](cheatsheet/MAS_CheatSheet_EN.pdf) · [MAA](cheatsheet/MAA_CheatSheet_EN.pdf) · [Chemistry](cheatsheet/CHE_CheatSheet_EN.pdf) · [Accounting and Finance](cheatsheet/ACF_CheatSheet_EN.pdf)).
The past papers themselves are not here (see *Copyright* below): the app fetches them for you on its first run, which is why there is no question bank in this repository and never will be.

WTF is a desktop study framework that reverse-engineers past exams. It reads each past paper and its marking key **mark by mark**, tags every awarded mark with the question pattern and the knowledge it rewards, and turns the result into a searchable bank with method notes, statistics, AI practice questions and mock papers. The framework does not know any course. Courses arrive as **subject packs**: data-only `.wtfpack` files anyone can download, import or build. The first packs are Western Australian ATAR courses built on SCSA past exams. It exists because the average student's revision strategy — "open a past paper, feel bad, close the past paper" — has a measured completion rate of approximately zero.

## Subject packs — download, import, or build your own

| Course | Pack | Past papers | Questions | Classified by |
|---|---|---|---:|---|
| Mathematics Methods (MAM) | built in | 2016–2025 | 174 | 51 patterns |
| Mathematics Specialist (MAS) | built in | 2016–2025 | 193 | 45 patterns |
| Mathematics Applications (MAA) | built in | 2016–2025 | 138 | 67 patterns |
| Chemistry (CHE) | built in · [**CHE-2026.10.1.wtfpack**](https://github.com/LxCenady/Wace_Training_Framework/raw/main/packs/CHE-2026.10.1.wtfpack) | 2016–2025 | 400 | 64 patterns |
| Physics (PHY) | built in · [**PHY-2026.10.1.wtfpack**](https://github.com/LxCenady/Wace_Training_Framework/raw/main/packs/PHY-2026.10.1.wtfpack) | 2016–2025 | 203 | 79 syllabus content nodes × 11 award skills |
| Accounting and Finance (ACF) | built in · [**ACF-2026.10.1.wtfpack**](https://github.com/LxCenady/Wace_Training_Framework/raw/main/packs/ACF-2026.10.1.wtfpack) | 2020–2025 | 135 | 114 patterns, 283 knowledge atoms |

**Importing a pack:** 题库 → 管理科目 → 导入学科包… (Subjects → Manage subjects → Import subject pack) → choose the `.wtfpack`. WTF checks the format, the minimum framework version, the handlers it needs, safe file paths and every payload hash. Then the paper wizard asks you for that course's original PDFs, recognises each one from its first page, checks it against the pack's SHA-256 manifest and builds the bank on your computer. The same packs are also on every [release](https://github.com/LxCenady/Wace_Training_Framework/releases/latest) and in [`packs/`](packs). Physics and Chemistry need WTF 2.0.2 or newer; Accounting and Finance needs 2.0.4.

**What a pack carries:** the course profile (sections, timing, weights, reference sheets, which built-in marking parser to use), the pattern and knowledge catalogue, a code for every awarded mark of every past question, the shapes of keys the parser cannot divide by itself, bilingual method notes, a cheat sheet, a question-generation skill and the source manifest (official URLs, Wayback captures, SHA-256). **What a pack never carries:** exam papers, marking keys, examiners' reports or any text cut from them. The pack is a recipe; your own copies of the papers are the ingredients. That is how a pack can be shared freely without sharing anything that is not ours. The format is documented in [pack-format.md](skills/wtf-subject-pack/references/pack-format.md).

**Building a pack for another course** — the protocol is general; the only course-specific input is the papers:

- **WTF Compiler** (in the app, free): bring the exam PDFs, marking keys and a syllabus, connect your own AI agent through **MCP**, and the Compiler walks it through parsing, a pattern catalogue, per-mark codes, notes, review, validation, build and export, checking every stage's JSON before accepting it. PDFs stay on your computer and are rebound by SHA-256. Essay levels, alternatives and follow-through remain scoring structures rather than invented one-mark rows. Your agent does the thinking; the Compiler checks whether the thinking arrived in valid JSON. [Workflow and protocol](docs/compiler.md).
- **The pack flow** used for the packs above ([skills/wtf-subject-pack](skills/wtf-subject-pack/SKILL.md)): pair papers with keys, cut questions and marks, label every awarded mark bottom-up, cluster the labels into a catalogue that a person approves, assign every mark, then run a blind second assignment on a sample, which must agree on at least 90% of patterns before notes, a cheat sheet and a skill are written and the pack is exported. The Physics, Chemistry and Accounting packs record their review numbers in their notes.

A course whose marking keys use a layout WTF has no parser for still needs framework work: packs cannot ship executable code. JSON has many talents. Inventing a parser is not one of them.

What it actually does, stated with a straight face:

- every past question is split by **topic**, and every **sub-question** is tagged with the specific **题型 (question pattern)** it uses. Per part, not per question, because examiners enjoy putting three topics into one question and calling it "(c)";
- marking keys are split into **one row per mark** where their structure reconciles with the printed marks; otherwise the original key crop stays visible, because inventing a missing mark is the examiner's job;
- hand-written, independently reviewed **solving-method notes** for every pattern (Chinese with English terms) and 3-page **cheat sheets**, for those who believe 3 pages is "light reading";
- a desktop **GUI** (knowledge tree → pattern → past questions, marking key hidden until you are brave enough) that can ask an LLM of your choice to **write a similar question, solve it independently, check it, and split the answer into mark points before showing you anything**. Maths packs also request SymPy recomputation; Chemistry currently relies on the model checks and structural validation, without a dedicated chemical verifier. Trust issues are a feature. A universal correctness certificate is not;
- Claude Code **skills** for generating topic quizzes, for when one AI is not enough.

> 中文简介：WTF 是一个把历年真题「逆向工程」的学习框架：逐个评分点读懂真卷和评分标准，把每一分标上题型和知识点，变成可检索的题库、讲义、统计、AI 练习题和模拟卷。名字缩写纯属巧合（并不是）。框架本身不认识任何课程，课程以**学科包**（只含数据的 `.wtfpack`）的形式提供，可以自由下载、导入，也可以自己制作。目前有数学方法、专业数学、数学应用、化学、物理、会计与金融六个 WACE 学科包；化学、物理、会计的包可单独下载（见上表），在「题库 → 管理科目 → 导入学科包」导入，再按提示提供本机原卷即可建库。学科包只带「配方」（课程结构、目录、逐分代码、讲义、出题 skill、真题来源和 SHA-256），绝不包含试卷、评分标准或其中的文字。要给别的课程做包：在应用里用 WTF Compiler，通过 MCP 接入你自己的 AI 代理；或者按 `skills/wtf-subject-pack` 的流程制作。AI 经出题、独立解题、核对和得分点整理；数学额外做 SymPy 复算。AI 不被信任，这是设计；不代表它终于值得信任了。

## Subject packs — the syllabus has moved out of the engine

There are two kinds of plugin, and only one of them gets to run Python:

| Layer | Contains | Responsibility |
|---|---|---|
| **Framework and feature plugins** | `app/kernel.py`, `app/plugins/*.py`, the shared tools in `tools/` | UI, databases, PDF rendering, AI providers, generation, marking, search, exports and updates |
| **Subject packs** | a data-only `.wtfpack` archive | course profile, sections and timing, scoring metadata, topics/pattern tags, bilingual notes, cheat sheets, question-generation skill and paper-source manifest |
| **Your local data** | downloaded PDFs, derived crops/indexes, `wace.db`, `generated.db`, `external.db` | the papers you fetched, the bank you built, and the mistakes you personally contributed |

The tiny kernel supplies services and events. Feature plugins register services with `provide/get` and communicate through `on/emit`; `main.py` wires them together. Subject packs do not join that Python plugin loader. They are read by the subject registry, which tells the same tools how to handle each course. A timetable should not require a software fork. It already requires enough stationery.

Each installed subject has `<S>/pack.json` and `<S>/sources.tsv`. The profile defines names, topics, section codes, paper layout, timers, weights, reference sheets and which **built-in** marking parser/checker to use. Maths uses separate CF/CA papers; Chemistry uses one paper with MC/SA/ER sections. Raw marks and section weights are separate metadata: 100 raw marks and 100% are not synonyms, however reassuring the number looks.

The source manifest records official URLs, download method, exact Wayback capture where applicable, SHA-256, size/page count and whether a file is required. The app checks the saved PDFs against that manifest before using the pack's crop locations. A PDF with the right title and the wrong pages is still the wrong PDF. It has simply dressed well.

**Installing a pack:** 题库 → 管理科目 → 导入学科包… → choose a local `.wtfpack`. WTF checks its format, minimum framework version, supported handlers, safe file paths and payload hashes, installs the data, then opens the paper-import wizard. All required files for the selected subjects must be present before it builds the bank. Pack installation does not conjure copyrighted papers out of a ZIP.

```text
subject pack: profile + notes + tags + source manifest
                         ↓
download/import matching original PDFs on your computer
                         ↓
recognise → segment → read marks + apply tags → build wace.db
                         ↓
the same UI, search, practice, AI workflow and PDF export
```

**Current boundary:** packs are downloaded as files and imported locally; there is no in-app online catalogue or one-click online installation yet. Adding a course that uses supported layouts and handlers is data work. A new parser or independent verifier is framework work, registered centrally; packs cannot ship executable code. The built-in subjects use this same mechanism. There is no secret seventh subject hidden in `main.py`, waiting for its own `if` statement.

A catalogue can also flag patterns: `examined: false` (current syllabus content without a past question yet), `historical_only` (content removed from the current syllabus: kept for history, never drawn into AI papers) and `diagnostic: false` (a record that shows no knowledge, such as a cancelled question: also left out of mastery). The flags live in the database table `pattern_flags`; asking for a historical pattern by name still works.

> 中文架构说明：框架的功能插件是 Python 代码，由微内核加载；学科包是数据，由注册表读取。两者共用界面与建库流程，但学科包不能带可执行代码，也不包含 SCSA 原卷或衍生题库。新增学科若能复用已有卷型和处理器，制作包即可；新的评分格式或验算能力仍需扩展框架。现在学科包以文件形式下载、本地导入，应用内还没有在线包商店。目录可以标记题型：现行未考、已删除的历史内容（AI 组卷不抽）、无诊断意义的记录（如取消题，也不计入掌握度）。外源卷库继续独立存放，不混入 SCSA 真题统计。

## Copyright — the exams are not in this repo (this part is not a joke)

The past exams, marking keys and examination reports are © School Curriculum and Standards Authority (SCSA), licensed only for non-commercial copying *within educational institutions*. They are therefore **not redistributed** here or inside subject packs, and neither is anything containing their text or images (`questions.json`, topic PDFs, question banks, `wace.db`). You download them yourself from SCSA and build everything locally — each subject's `<S>/sources.tsv` lists its official sources and file checksums (2016–2019 via the Wayback Machine).

Everything else (code, tags, method notes, cheat sheets, skills) is original work in this repo.

## Quick start for students (Windows or Mac, nothing to install, allegedly)

On a Mac, step 1 is the .dmg above (drag to Applications, right-click → Open the first time); the rest is the same, with ⌘ where Windows says Ctrl, and a two-finger click (or Control-click) for right-click.

1. Download **[WTF-Setup.exe](https://github.com/LxCenady/Wace_Training_Framework/releases/latest/download/WTF-Setup.exe)** (always the newest version) and double-click it. It installs for you only (no administrator rights, default `%LOCALAPPDATA%\Programs\WTF`), adds desktop and Start-menu shortcuts and starts the app. Running a newer setup over an old install upgrades it and keeps your papers, AI questions and mistakes, because deleting a student's 错题本 is how wars start. (Allergic to installers? `WTF-Windows-vX.Y.Z.zip` is the same app — extract anywhere, a USB stick works.)
   Windows SmartScreen will warn you because the app is not code-signed. Code signing costs money; this README is free. *More info → Run anyway.*
2. The first run opens the **import wizard**. Tick the subjects you actually take (MAM, MAS, MAA, CHE, PHY, ACF — the wizard knows which packs are installed, not why you chose them); only their papers are fetched. Then it starts working before you have finished reading this:
   - ① the 2016–2019 papers download by themselves from the Wayback Machine, three at a time, with an ETA. The Internet Archive is a national treasure running on what appears to be a single hamster; please be patient with the hamster;
   - ② 2020–2025: click 「打开下一批」 to open 6 official links at a time in your browser, press Ctrl+S on each PDF and just click Save — the browser's default, the Downloads folder, is the only place the wizard looks. Then click 「我存好了，检查下载文件夹」. File names do not matter: each paper is recognised from its first page. Name them `asdf (3).pdf` if you must; we have seen worse;
   - ③ the bank is built only when **every required file** is in — then by itself — and the app restarts into the full interface. Sample papers and examination reports are optional and do not block it. There is no half-built bank to wonder about. A banner at the top always says what to do next, in case reading this README did not go well either.

   Downloads retry dropped connections, timeouts and "too many requests" with polite, growing pauses, and failed files get a second round; update downloads resume where they stopped. Wrong-version PDFs are rejected rather than silently giving every question a new haircut. The window sizes itself to your screen and is DPI-aware, so it is sharp at 125–200 % scaling instead of looking like it was rendered on a potato.
3. For AI questions and explanations, add your own API key in 设置 (default: DeepSeek). Browsing past questions, marking keys and notes needs no key, no account and no subscription. We checked: still no subscription.

Your AI questions and 错题本 live in `generated.db` in the app's data folder: next to `WTF.exe` on Windows, or `~/Library/Application Support/WTF` on Mac. Teachers can prepare a copy without the GUI — i.e. without having to look at it:
`WTF.exe --import <folder of PDFs> --build` (log in `WTF.log`).

## Features at a glance

| Feature | Where | What it does |
|---|---|---|
| Knowledge tree | left pane | subject → topic → 题型 (pattern) → every past question that uses it, plus your ★ AI questions; select one pattern and the patterns that most often share its past questions light up (↔ 2/12 道 · 17 %) |
| Pattern notes | click a pattern | how to recognise it, the steps, where the marks are, examiners' warnings, and how many marks it usually carries per section |
| Past questions | click a question | the original exam crop; 「显示评分标准」 reveals the official key, split one row per mark |
| AI similar questions | select pattern(s) → 「AI 生成相似题」 | new question, independently solved, cross-checked, split into mark points; maths additionally uses SymPy — answers stay hidden until you ask |
| Unit questions | select a unit title → 「AI 生成相似题」 | questions on a whole unit, each built on a real question's shape: patterns, marks and cross-unit pairings follow the unit's real statistics (shown on the unit's page) |
| Batch generation | 难度 + 数量 under the tree | up to 20 questions at a time, 基础 / 标准 / 拔高 |
| Past question search | 「真题搜索」 next to 「AI 生成相似题」, or Ctrl+F | find past questions by any mix of patterns and units (all-of / any-of), cross-unit only, with a drawing part or a figure, by year, marks and words; see which patterns and units appear together; export the results as PDF |
| 我的 AI 题库 | Ctrl+B | every AI question, arranged like the knowledge tree (subject → unit → pattern), searchable, exportable |
| Self-marking | right-click a part → 「此题扣分」 | tick the mark points you lost; they go to the 错题本 |
| 错题本 | Ctrl+E | mistakes grouped by pattern, weakest first; 一键讲解, 错题加强题, spaced review |
| Mock exam | Ctrl+M | real past paper or AI-assembled paper, WACE timing, auto-submit, marking, history |
| 掌握度地图 | Ctrl+G | one tile per pattern, coloured by your score rate |
| Reference sheets | right pane (F2) | choose subject and year; maths formula sheets or Chemistry data booklets, follows the question you are viewing, resizable |
| PDF export | 我的 AI 题库 / a finished batch / 真题搜索 / mock exam | question paper (one question per page, rest is working space) + answer paper with ☐ mark boxes |
| Subject packs | 题库 → 管理科目 → 导入学科包… | import a local data-only `.wtfpack`, validate its profile and files, then fetch its required papers and build locally; no executable code or SCSA originals in the pack |
| 管理科目 | 题库 → 管理科目 | add or drop subjects later: tick a subject, fetch its papers, rebuild — your AI questions and 错题本 stay |
| English UI | 设置 → 界面语言 | the whole interface, notes and explanations in English |
| Updates | 帮助 → 检查更新 | download, verify and install new releases without losing your data |

## How to use it

**1. Learn a pattern.** Choose a subject in the tree's drop-down, expand a topic and click a 题型. Read the method notes; the grey line under the title says how many marks it usually carries in that subject's sections. Expand the pattern to see every past question on it — the list shows which parts use it. The patterns that most often appear in the same past questions light up in the tree, with how many of this pattern's questions also use them (only pairs seen at least twice; a unit holding one is opened). Ctrl-click them to combine for an AI question, or press 「真题搜索」 to see those questions.

**2. Do past questions, then mark yourself.** Click a question, do it on paper (formula sheet on the right, F2 to hide it), then press 「显示评分标准」. For every part you dropped marks on, right-click the part (or a mark point) → 「此题扣分」, tick the points you missed and add a note in your own words. That is the whole bookkeeping; the app does the rest.

**3. Get new questions when the past ones run out.** Select a **unit title** to practise the whole unit the way the exam tests it, or one pattern, or Ctrl-click several patterns to combine them; choose 卷型 (sections of the selected subject, or 任意), 总分 (0 = let the real papers decide), 难度 and 数量; press 「AI 生成相似题」. A unit's page lists what unit questions are built from: its real questions per section, how often they cross into other units and with which, and each pattern's share of the unit's marks, usual marks and how often it comes with a figure or a drawing part. Each question appears under ★ in the tree and in 我的 AI 题库 once it has passed every check. Answers are hidden: do it first, then reveal and self-mark exactly as with past questions.

**4. Close the loop in the 错题本 (Ctrl+E).** Weakest patterns come first. Select a mistake and press 「一键讲解所选错题」 for a full explanation of each mark you lost; 「生成错题加强题」 writes new questions that require exactly the steps you got wrong (with nothing selected, it targets your weakest pattern). Mistakes come back for review after 1, 3, 7, 14 and 30 days: tick 「只看今日待复习」, right-click a mistake → 「复习：做一道同题型新题」, then mark it 「复习通过」 or 「又错了」.

**5. Sit a mock exam (Ctrl+M).** Choose subject, section and a real year or 「AI 组卷」. AI papers are assembled while you watch (each question's patterns and marks are listed); start when ready. Reading and working time come from the subject profile (maths CF 5 + 50 min, CA 10 + 100 min; Chemistry section practice uses its suggested working time) and the paper submits itself at the end. Then open each question, reveal the key, right-click to deduct, and the score updates. Every attempt is kept in the history.

**6. Print.** In 我的 AI 题库, select questions (or whole groups, or a search) → 导出练习卷 PDF; mock exams have their own export. You get a question paper with one question per page and an answer paper where no question is split across pages, each mark point with a ☐ to tick.

**6½. Search the past papers (Ctrl+F).** Select patterns or a unit in the tree and press 「真题搜索」: every past question that contains all of them (or any of them), with each pattern's marks, whether it crosses units and whether it has a drawing part. Under the list: the patterns and units that most often come together with your choice — the cross-pattern index. Tick 「只看跨单元」 to see only cross-unit questions. 「导出 PDF」 exports the selected results (or all of them): the questions cut from the original papers as vectors, one per page, and their marking keys.

**7. Watch the map (Ctrl+G).** Each tile is a pattern; colour is your score rate, grey means not attempted, the number is how many marks it carried across past papers. Big number + red tile = where your next hour goes. Right-click a tile to practise it.

**Shortcuts:** Ctrl+F 真题搜索 · Ctrl+B 我的 AI 题库 · Ctrl+E 错题本 · Ctrl+M 模拟考试 · Ctrl+G 掌握度地图 · F2 formula sheet · Ctrl-click patterns to combine · double-click to open · right-click a part to deduct marks.

> **中文使用说明**
> 1. **学题型**：左侧下拉选择学科，点开知识点 → 点题型，看解题思路；标题下灰字是这个题型在该学科各分区一般占几分。数学是 CF / CA，化学是 MC / SA / ER。展开题型可以看到所有用到它的真题。选中一个题型时，跟它在同一道真题里出现最多的题型会在图谱上高亮（↔ 共现道数 / 本题型道数 · 比例），Ctrl+点击即可组合出题。
> 2. **刷真题 + 自批**：点真题，在纸上做完再点「显示评分标准」。哪一小问扣分了就右键 →「此题扣分」，勾掉丢的得分点、写一句备注，自动进错题本。
> 3. **AI 出题**：选**单元标题**按该单元真题的题型分布、分值和跨单元搭配出题（单元页面会列出这些统计）；或选一个题型（Ctrl+点击可多选组合），设卷型、总分（0 = 按真题自动）、难度、数量，点「AI 生成相似题」。通过全部校验才入库，答案默认隐藏。
> 4. **错题闭环**（Ctrl+E）：薄弱题型排前面；「一键讲解所选错题」逐分讲清楚丢在哪；「生成错题加强题」专练丢分步骤；按 1/3/7/14/30 天间隔复习（勾「只看今日待复习」，右键错题做复习题）。
> 5. **模拟考**（Ctrl+M）：真题年份或 AI 组卷，WACE 计时、到点自动交卷，交卷后右键扣分出成绩，历史全部保留。
> 6. **打印**：我的 AI 题库（Ctrl+B）里选题 →「导出练习卷 PDF」：试卷每题一页，答案卷不跨页、每个得分点带 ☐。
> 6½. **真题搜索**（Ctrl+F，在「AI 生成相似题」旁边）：在左侧选题型或单元，查同时包含（或包含任一）的所有真题，可只看跨单元、含作图小问、有配图；列表下方是常一起出现的题型和单元（跨题型索引）；「导出 PDF」把结果从原卷矢量裁切成试题 + 评分标准。批量 AI 出题完成后也可「导出本批 PDF」。
> 7. **掌握度地图**（Ctrl+G）：颜色是得分率，数字是该题型历年总分值。分值大又发红的，就是下一小时该去的地方。

## External papers — kept separate from SCSA past questions

Open **外源卷库 / External library** in the menu and import a PDF question paper together with its answer PDF.
Enter the paper name, school or other source, subject and section. Originals are copied into
`external/`; crops, marks, text and tags live in a separate `external.db`. External questions are searched only
in this library and never affect the SCSA knowledge tree, past-question search, paper totals or blueprint.

Recognised `Question N` / `QN` headings produce unconfirmed crop drafts. Rotated or unrecognised layouts
use manual cropping. Open a question and choose
**编辑切块与标注** to inspect or redraw question/answer rectangles, add cross-page regions, set marks, and select
multiple patterns. Unrecognised or scanned papers can be split manually with **新增题目或小问切块**; enter text
manually for keyword search and AI tagging. OCR is not included. You can also isolate subquestions such as
`Q1(a)` for their own tags. Answers remain hidden until you choose to reveal them.

**AI 标注选中项** calls the provider, model and API key in your Settings. It reads both question and answer text,
uses the current subject's pattern definitions and [external tagging skill](skills/wace-external-tagging/SKILL.md),
and saves proposed tags with reasons for human review. It does not overwrite confirmed tags. Check crops,
marks and tags before ticking the confirmation box. No API call is made just by importing or searching.

For a batch of unconfirmed questions in one imported paper:

```bat
.venv\Scripts\python tools\tag_external.py --list
.venv\Scripts\python tools\tag_external.py --paper <ID>
```

> 中文：外源试卷与答案成对导入、单独切块和标注；在「外源卷库」中独立检索，绝不混入 SCSA 真卷统计。
> AI 标注使用你设置中的 API 和模型，题目与答案文字会发送给该服务商；结果是待人工确认的草稿。
> 扫描件需要手动框选、补充文字，本版本不含 OCR。备份时同时保存 `external.db` 和 `external/`。
> 外源原件、数据库和提取内容均留在本机，不进入 Git 或发行包。

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
- **Notes**: `<S>/methods_en/` for every subject (method notes + review logs, md + pdf) and `cheatsheet/*_CheatSheet_EN.*`.
- **How it is made**: `tools/translate.py docs <S>` translates one subject's Chinese notes chunk by chunk with the configured model (DeepSeek by default — outsourcing, essentially); choose the subject deliberately, because rebuilding every translation can overwrite hand edits. `tools/translate.py ui` builds `app/i18n/en.json` from the Chinese fragments in the code plus any fragment the running app reported missing. The interface code stays single-language: the `i18n` plugin translates text at the exact moment it reaches Tk, which is either elegant or unhinged depending on who you ask. Glossary: 题型 = pattern, 知识点 = topic, 错题本 = mistake book, 得分点 = mark points, 评分标准 = marking key.
- `app/tests/smoke_en.py` opens every main view in English and lists any Chinese still on screen (currently none; it was very thorough about this).

## Layout

```
MAM/ MAS/ MAA/ CHE/ PHY/ ACF/             installed subject data
  pack.json      course profile: topics, sections, layout, timing, weights, built-in handlers and sheets
  sources.tsv    paper URLs + download method + archive capture + hashes + required/optional status
  methods/       NN_Topic_解题思路.md/.pdf   题型 patterns: how to recognise, steps, where the marks are,
                                             examiners'-report warnings, cited past questions; 审校记录 = review log
  methods_en/    English editions
  papers/ topics/ 题库/ questions.json      (built locally, not in git)
cheatsheet/      per-subject cheat sheets (md + pdf)
skills/          wace-<s>-questions: question-generation instructions, one per subject
                 wtf-subject-pack: authoring and reviewing a subject pack (the pack flow)
                 wtf-compiler: the agent side of the WTF Compiler (MCP)
packs/           downloadable subject packs (.wtfpack)
docs/            compiler.md (Compiler workflow and protocol), account_api.md
                 (paths resolve live: $WACE_MATHS_ROOT, else the folder above skills/)
tools/
  subjects.py      validates and reads installed profiles; the shared subject registry
  handlers.py      built-in marking parsers/checkers selected by profile (no pack-supplied code)
  pack.py          export / inspect / import data-only .wtfpack archives
  scoring.py       raw marks and section-weighted score summaries
  rubric.py        structured-award scoring algebra and overlapping atomic coverage (not the live bank format)
  fetch.py         <S>/sources.tsv -> */papers; recognise saved PDFs and verify source hashes
  package_win.py   Windows release: PyInstaller app -> dist/WTF-Windows-<ver>.zip + WTF-Setup-<ver>.exe
  installer.py     the setup exe: per-user install, shortcuts, upgrades keep user data
  build_all.py     runs the steps below in order
  segment.py       papers -> questions.json (page regions of every question in exam + key)
  segment_mc.py    multiple-choice regions and accepted answers for a shared paper
  build_docs.py    questions.json + tags_*.txt -> topic PDFs (exam crop + key crop) and .md indexes
  build_bank.py    question-only banks per topic, newest first
  markpoints.py    built-in ticks and Description/Marks key parsers; inconsistent keys keep image fallback
  build_db.py      everything -> wace.db; prints any tag / key inconsistency
  blueprint.py     real paper statistics -> mark distribution + cross-topic pairings for skills and mock exams
  tags_*.txt       topic tags per question
  parttags_*.txt   per-sub-question pattern tags, e.g. `2024A 12 a=D6 b=D6 c=D6`
                   (code = topic letter(s) + 题型 number in methods/; a question's patterns = union of its parts)
  audit*.py, evidence.py, render_*.py, translate.py   checks, evidence packs for the notes, md -> pdf, translation
app/             GUI (below)
```

`wace.db` (SQLite) is the locally built SCSA index: `topics`, `patterns` (notes), `questions` (source crops, stem, `points_ok`), `parts` (printed marks and drawing flags), `part_patterns` and `points`. The `pattern_marks` view feeds practice statistics and blueprints; currently a part tagged with several patterns shares its marks evenly between them. That is a statistical allocation, not a proof of which knowledge atom earned each mark. The structured scoring-tree/atomic-coverage module is a separate foundation and is not yet the bank's storage or self-marking model. If a key does not reconcile (`points_ok = 0`), the GUI shows the official crop rather than pretending the parser won. AI questions, attempts and mistakes live in `generated.db`; external imports live in `external.db` and `external/`, outside the SCSA index and its statistics. Rebuilding the past bank does not turn your mistakes into somebody else's problem.

## How it works (`app/`)

- **Knowledge tree**: subject → topic → pattern → past questions (showing which parts hit that pattern) and ★ AI questions. Select a pattern for its method notes; select a question for the exam crop, then 「显示评分标准」 for the per-mark points and the official key crop. Peeking early is between you and your conscience.
- **AI questions**: select one or more patterns (Ctrl-click to combine), choose section and marks, press 「AI 生成相似题」. Each step is a separate model call with no shared context, so no model can copy another model's homework:
  1. *setter* — sees the skill, the pattern notes and real past questions; writes the question and intended answers;
  2. *solver* — sees only the question;
  3. *checker* — compares setter and solver part by part, re-derives any disagreement, checks the question is well-posed;
  4. *examiner* — splits the verified solution into exactly one behaviour per mark.

  For packs with `checker: sympy` (the three maths courses), **SymPy recomputes** numeric parts with supported solver-written expressions (e.g. `solve(diff(pi*r**2 + 16*pi/r, r), r)`, `P(Normal('X', 32, 4) > 40)`) and compares them with both models' answers; a disagreement sends the question back. The expression is whitelisted (numbers, arithmetic, known maths functions — no attributes, imports or dunders) and runs in a separate, time-limited process; parts it cannot evaluate are shown as unchecked, never as wrong. Chemistry currently uses `checker: none`, which skips this independent computation, not the solver/checker model calls. SymPy has no opinions. It also has no Chemistry ATAR qualification.
  The program checks part labels and mark counts between steps; any failure regenerates with the reason (2 retries by default). Nothing answer-like is shown until all steps pass; 「查看验证记录」 shows every raw reply, for the forensically inclined.
- **Batch generation**: choose 难度 (基础 / 标准 / 拔高 — calibrated in the prompt against the opening parts, the median past question, and the final parts of the hardest recent questions) and 数量 (1–20). Questions run 4 at a time (`parallel` in the config), each through the full four-step check; a failure only drops that question. The setter is shown the openings of the latest AI questions on the same patterns and told not to reuse their context, function or numbers — otherwise every question would be about a farmer and his fence.
- **Unit questions**: select a unit title instead of a pattern. Each question takes the shape of a real question led by that unit — its patterns and the marks each carried — varied the same way as mock-paper questions (same-unit swaps, ±1 mark). Real shapes are drawn without replacement, so a batch does not repeat itself and still matches the unit: over 2,000 simulated questions per unit, the cross-unit rate is within 2 points of the real one for all 14 units and each pattern's share of the unit's marks within 3.4 %. Those figures describe the earlier two-maths-course evaluation, not a fresh four-subject benchmark. With section 任意, sections are sampled from the selected unit's real questions.
- **我的 AI 题库** (menu 题库, the button under the tree, or Ctrl+B): every generated question, arranged like the knowledge tree — subject → unit → pattern → questions, only where there are questions, with counts and the difficulty mix. A question sits once, under its lead pattern; its other patterns have their own column. Searching expands what matches; sort by any column; double-click to open (answers still hidden); selecting a subject, unit or pattern exports everything under it.
- **Reference sheets** pinned on the right (subject/year drop-downs; follows the question's year; formula sheets for maths, data booklets for Chemistry; drag its edge to resize, re-rendered sharp at any width; F2 hides it, for those who have memorised it, or claim to have).
- **Self-marking (自批卷)**: every part of an AI answer and of a past question's key is labelled with its topic + 题型. Right-click a part → 「此题扣分」, tick the mark points you missed, add a note → it goes into **我的错题本** (Ctrl+E), grouped by pattern, weakest first. Honesty is not enforced, merely encouraged.
- **错题加强题**: from the 错题本, generate targeted questions for the selected (or weakest) pattern; the setter is told exactly which mark points you lost, so the new question requires those exact steps. It remembers. It is patient.
- **一键讲解**: one click explains a recorded mistake — what the part tests, why each missed mark was lost (using your note), the full correct working with every mark shown, and habits to avoid it next time. Cached; 「重新讲解」 asks again if the first explanation did not land.
- **导出练习卷 PDF** (我的 AI 题库): selected questions, whole groups or the current search → a question paper with suggested time, one question per page and the rest of the page (plus a blank page if that is not enough, ~3 lines per mark) as working space, and an answer paper whose mark points have ☐ boxes for marking on actual paper, the ancient medium. Answers share pages, but a question that does not fit moves whole to the next page — nothing is cut in half unless it is longer than a page.
- **模拟考试** (Ctrl+M): a real past paper or an AI-assembled one. Every AI question is built on the shape of a real question — which patterns it combined and how many marks each carried — then reshuffled: patterns swapped for same-topic ones that have carried that many marks, marks nudged by one inside what real papers show. Topic shares, question counts and cross-topic pairings land within a few percent of the real papers, no two mock papers are alike, and none of them are kind. (Earlier versions once offered a 12-mark calculator-free definite integral. That examiner has been let go.) Profile-defined timing (maths CF 5 + 50 min, CA 10 + 100 min; Chemistry section practice uses its suggested working time) with auto-submit, a live progress display while the paper is being assembled, and export to PDF; then mark each question with right-click and watch the score update in real time; history of all attempts, kept forever.
- **掌握度地图** (Ctrl+G): one tile per pattern — colour = your score rate on it (grey = not attempted, i.e. avoided), number = marks it carried across past papers; click for the notes, right-click to practise it.
- **间隔复习**: every mistake comes back after 1, 3, 7, 14 and 30 days (Leitner boxes), like a sequel nobody asked for. The 错题本 shows what is due today, and a review can generate a fresh question aimed at the points you missed.
- **Settings** (设置 → 模型与 API key): Anthropic format (`/v1/messages`) or OpenAI format (`/chat/completions`) with your own base URL, model and key — any compatible service works. **Default: DeepSeek** (`https://api.deepseek.com`, `deepseek-flash`, thinking mode at `reasoning_effort: high` — we measured `max`: it thought 40% more expensively and twice as slowly to pass the same checks, so it was demoted); the per-provider 额外参数 JSON is merged into every request body. Keys are stored only in `%APPDATA%\wace-maths\config.json` (empty → `DEEPSEEK_API_KEY` / `OPENAI_API_KEY` / `ANTHROPIC_API_KEY`). An empty balance (HTTP 402) or a bad key stops the batch with a readable message instead of failing 20 questions one by one. `mock` is an offline provider for trying the pipeline without paying anyone.
- **Architecture** (microkernel): `kernel.py` = service registry + events + plugin loader with no domain code whatsoever; `main.py` = thin glue; `plugins.txt` lists the plugins; each `plugins/*.py` does one job (store, render, llm + one file per provider, generator, symcheck, mathtext, figure, updater, and one file per view). Plugins mostly talk through the kernel's services and events rather than poking each other directly, which is the closest software gets to a healthy relationship.
- **Tests**: `app\tests\test_providers.py` (both adapters against a local fake server), `app\tests\smoke_gui.py <dir>` (drives the window with the mock provider and saves screenshots), `smoke_en.py`, `smoke_setup.py` (the wizard, offline). Tests use their own config file and never touch yours.

**Maths and figures.** Generated questions, keys, solutions and explanations are written in LaTeX (`$…$`, `$$…$$`; money as `\$5`) and rendered with [ziamath](https://ziamath.readthedocs.io/) — pure Python, no TeX install, no 4 GB download — as images in the app and as vectors in exported PDFs. LaTeX that a model wrote with single backslashes inside JSON (`\frac` silently becoming a form feed, `\int` making the JSON invalid) is repaired before use; models do this a lot and never apologise. When a question needs a drawing — a graph to read from, a shape, an Argand diagram, a histogram — the setter gives a **figure spec as data, not code** (curves, shaded regions, implicit curves, points, segments, polygons, circles, vectors, labels, bars; expressions through the same whitelist as the SymPy check), drawn with [ziaplot](https://pypi.org/project/ziaplot/). The solver and checker read the spec, so a figure question is still solved independently; a spec that cannot be drawn sends the question back. Figures and drawing parts come at the real papers' rates: every pattern knows how often its real questions show a figure and how often they make the student draw (slope-field questions: always a figure, half the time "draw the solution curve"; graph transformations: a sketch about 70 % of the time), each new question rolls against those odds, and a question that rolled a figure or a drawing part and came back without one is sent back. Drawing parts give the student blank, scaled axes (or the slope field, the Argand diagram) and carry the completed drawing in the marking key. Slope fields are a figure element of their own (`{"slope": "dy/dx", "step": 0.5}`), vertical where the gradient is undefined, as on the real papers.

**Updates.** At start-up (at most once a day; switch off in Settings) and from 帮助 → 检查更新, the app asks GitHub for the latest release. The packaged app can then download it (resuming if the connection drops), verify its SHA-256 (published by GitHub) and that it contains `WTF.exe`, and — after it exits — copy the new files over its folder without touching the student's papers, `generated.db` or `WTF.log`; it restarts and rebuilds the question bank by itself (≈1 min). Source checkouts are only told about the new release (you have `git pull`; use it). The version lives in `app/version.txt`.

`WTF.exe --selftest` (or `python app/main.py --selftest`) checks LaTeX, figures, the SymPy check and the question bank, and writes the result to `WTF.log`. If something crashes, it is in `WTF.log` too. Fittingly named.

**Known limits** (stated plainly, as is tradition): parts whose answer is not a number or expression (inequalities, loci, explanations) are verified by the models only; some solver expressions merely restate the answer, which makes their SymPy check weak; and no part of this software will sit the exam for you. We looked into it.

## Licence

Code: MIT (`LICENSE`). Notes, tags, cheat sheets and skills: CC BY-NC-SA 4.0. SCSA material: © SCSA, not included, see above.
