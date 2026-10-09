---
name: wace-mam-questions
description: Generate original WACE Mathematics Methods ATAR (MAM, Units 3–4) exam-style questions with SCSA-style marking keys, by topic (differentiation, integration, rectilinear motion, exp/log, discrete RV/binomial, continuous RV/normal, sample proportions/CI), calibrated against every 2016–2025 past paper. Use when the user asks for Methods / MAM / 数学方法 practice questions, 出题, a topic quiz, or a mock section.
---

# WACE Mathematics Methods — topic question generator

## Locating `<ROOT>` (live path — never hard-code)

All paths below are relative to `<ROOT>`, the data folder that contains `MAM/`, `MAS/`, `tools/` and `wace.db`. Resolve it once per session, in this order:

1. Environment variable `WACE_MATHS_ROOT`, if set and it contains `MAM/`.
2. Walk up from this SKILL.md's real location: the first ancestor folder containing both `MAM/` and `MAS/` (the canonical copy lives at `<ROOT>/skills/<skill>/SKILL.md`, so normally two levels up).
3. Fallback `E:\WACE_Maths`. If none exists, ask the user where the folder is.

Python: `<ROOT>\.venv\Scripts\python.exe` if present, otherwise any Python 3 with sympy/scipy.

Indexed database `<ROOT>\wace.db` (SQLite, built by `tools/build_db.py`): every past question is tagged per sub-question with pattern codes like `MAM.D.6` (= topic code + 题型 number in the methods notes). Useful queries:
- similar past questions: `SELECT DISTINCT qid FROM part_patterns WHERE pattern='<code>'`
- the pattern's method text: `SELECT title, method FROM patterns WHERE code='<code>'`
- one-row-per-mark marking scheme: `SELECT label, text FROM points WHERE qid='<qid>' ORDER BY ord` (trust it only when `questions.points_ok=1`; otherwise read the key PDF crop).

Past-paper corpus (2016–2025, 174 questions, 1500 marks), split by topic, lives on disk:

- Topic guides (syllabus + what SCSA actually asks): `topics/<NN_Topic>.md` next to this file — read the one for the requested topic first.
- Question bank (stem text of every past question in that topic, with page refs): `<ROOT>\MAM\topics\<NN_Topic>.md`
- Same questions as PDF (original exam crop + ratified marking key crop, vector quality): `<ROOT>\MAM\topics\<NN_Topic>.pdf`
- Solving-method notes (题型 patterns, step-by-step method, where each mark is awarded, examiners' report warnings; Chinese with English terms): `<ROOT>\MAM\methods\<NN_Topic>_解题思路.md`
- Full original papers, keys, exam reports, formula sheets: `<ROOT>\MAM\papers\` (citations like "2016S F4" = 2016 official sample exam; those are only in papers/, not in the topic files)

| code | topic file | 中文 | share of marks (primary) | calc-free / calc-assumed questions |
|---|---|---|---|---|
| D | 01_Differentiation | 微分及其应用 | 23% | 22 / 21 |
| I | 02_Integration | 积分及其应用 | 12% | 16 / 7 |
| M | 03_Rectilinear_Motion | 直线运动 | 7% | 3 / 9 |
| L | 04_Exp_Log | 指数与对数函数 | 15% | 10 / 17 |
| DRV | 05_Discrete_RV | 离散随机变量与二项分布 | 11% | 4 / 14 |
| CRV | 06_Continuous_RV_Normal | 连续随机变量与正态分布 | 19% | 13 / 17 |
| CI | 07_Sample_Proportions_CI | 样本比例与置信区间 | 14% | 2 / 19 |

## Workflow

1. **Pin down the request.** Topic(s), number of questions, difficulty (基础 / 中等 / 压轴 ≈ early-section / mid / last-question level), section (calculator-free or calculator-assumed; default: whichever the topic guide says is typical), language of the question (default English, exactly like the real paper; give explanations in Chinese if the user writes Chinese). Don't ask if sensible defaults exist — state the defaults you used.
2. **Calibrate.** Read `topics/<topic>.md` and the matching `methods\<NN_Topic>_解题思路.md` (pick which 题型 pattern(s) each new question tests; the marking key must award marks where that pattern's 得分点 says). Then grep the bank file for 2–4 past questions closest to what you will write (same sub-skill, same section). For a hard/long question, open the matching PDF pages with Read (`pages` param) to see the real marking key granularity.
3. **Write original questions.** New context, new numbers, new structure — never copy or lightly reword a past question. Keep the SCSA voice: "Determine…", "Show that…", "Hence…", "Justify your answer.", "correct to 0.01", contexts drawn from WA life. Number parts (a), (b)(i)… with marks per part; header `Question N (x marks)`.
   - Calculator-free: numbers must give exact, tidy answers (ln 2, e³, π/6, fractions); no normal/binomial probabilities that need a calculator.
   - Calculator-assumed: realistic data, answers "correct to 2 d.p." etc., CAS-style steps acceptable but working must be stated.
4. **Write the marking key** in SCSA format for every part:
   ```
   Solution
   <full worked solution>
   Specific behaviours
   ✓ <one observable action per mark>
   ```
   Number of ✓ = marks for that part; part marks sum to the question total. Mark the "show that" steps, justification, units and rounding the way the real keys do (see guide).
5. **Verify before showing.** Solve every part independently with `<ROOT>\.venv\Scripts\python.exe` (sympy for calculus/algebra, scipy.stats for normal/binomial). Fix any mismatch. Check calculator-free answers really are exact and calculable by hand. Report that verification ran.
6. **Output.** Questions first, then a separator, then the marking key (so the user can attempt first). Use LaTeX (`$...$`). After the key, one line per question: "最接近的真题: 2022 Calculator-assumed Q12 (PDF p.x)" so the user can compare. If the user wants a file, save to `<ROOT>\generated\MAM\<topic>_<YYYYMMDD>.md`.

## Mock section mode

If asked for a 模拟卷 / mock: calculator-free ≈ 50 marks / 50 min, 6–8 questions; calculator-assumed ≈ 100 marks / 100 min, 9–11 questions. Weight topics by the share column above, mix multi-topic questions (real papers often join e.g. calculus + log, or binomial + normal), order questions roughly easy → hard.

## Conventions every key must follow

- One mark = one ✓ behaviour; partial credit is per behaviour, never "award 2 if…".
- Rounding/units: penalise only where the question demands it ("correct to …", "in context").
- Probability answers: state the distribution with parameters when the question says "State the distribution" (e.g. X ~ Bin(20, 0.35)).
- Confidence intervals: use z = 1.645 / 1.960 / 2.576 for 90/95/99%. Minimum sample size: always p̂ = 0.5 unless told to use a given p̂. Decisions from a CI must state whether the claimed value lies inside; "does it prove…" ⇒ No.
- Optimisation using calculus: the key awards a mark for verifying max/min (second derivative or sign test) unless the question says "You do not need to verify".
- Use the formula sheet conventions (`<ROOT>\MAM\papers\2022_MAM_FormulaSheet.pdf`): increments formula δy ≈ (dy/dx)δx, Var(aX+b) = a²Var(X), p̂ ~ N(p, p(1−p)/n).

## Explain mode

If the user asks how to solve a type of question (怎么做 / 解题思路 / 讲一下) rather than for new questions: answer from the methods note for that topic — identify the pattern, give the steps and the mark-earning lines, cite 1–2 past questions with their PDF pages — then offer a fresh practice question of that pattern.
