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

<!-- blueprint:start (generated by tools/blueprint.py from wace.db — do not edit by hand) -->
## Paper blueprint (from the 2016–2025 papers)

Use this when writing a set or a mock paper: **randomise** (vary question count, marks per question, which patterns appear, and order within the difficulty ramp — never the same paper twice), but keep the **topic mark distribution** close to the real one below, and make the stated share of questions **cross-topic** (two topics in one question), using only pairings that real papers use.

### Calculator-free

- Questions per paper (2020–2025): 5–7; marks per question: 3–14 (median 7).
- Share of marks by topic: Integration & applications 27%, Differentiation & applications 25%, Continuous random variables & normal 18%, Exponential & logarithmic functions 17%, Discrete random variables & binomial 7%, Rectilinear motion (kinematics) 5%, Sample proportions & confidence intervals 1%.
- Cross-topic questions: 36% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Integration & applications** — 66% of its questions are cross-topic; pairs with Differentiation & applications 74%, Exponential & logarithmic functions 26%, Continuous random variables & normal 11%, Rectilinear motion (kinematics) 5%.
  - **Differentiation & applications** — 62% of its questions are cross-topic; pairs with Integration & applications 88%, Exponential & logarithmic functions 25%, Continuous random variables & normal 6%.
  - **Discrete random variables & binomial** — 50% of its questions are cross-topic; pairs with Continuous random variables & normal 100%.
  - **Exponential & logarithmic functions** — 44% of its questions are cross-topic; pairs with Integration & applications 71%, Differentiation & applications 57%.
  - **Continuous random variables & normal** — 43% of its questions are cross-topic; pairs with Discrete random variables & binomial 67%, Integration & applications 33%, Differentiation & applications 17%.
  - **Rectilinear motion (kinematics)** — 33% of its questions are cross-topic; pairs with Integration & applications 100%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Sample proportions & confidence intervals: `MAM.CI.4` 3 (max 3)
  - Continuous random variables & normal: `MAM.CRV.1` 3–7 (max 7), `MAM.CRV.2` 5–6 (max 7), `MAM.CRV.3` 5–10 (max 10), `MAM.CRV.4` 2–3 (max 3), `MAM.CRV.6` 2–6 (max 6), `MAM.CRV.7` 2 (max 2)
  - Differentiation & applications: `MAM.D.1` 2–3 (max 4), `MAM.D.2` 2–5 (max 5), `MAM.D.3` 3 (max 4), `MAM.D.4` 3–10 (max 10), `MAM.D.5` 3–5 (max 5), `MAM.D.6` 5–7 (max 7), `MAM.D.7` 2–3 (max 3), `MAM.D.8` 2 (max 2), `MAM.D.10` 1–3 (max 3)
  - Discrete random variables & binomial: `MAM.DRV.1` 2–6 (max 6), `MAM.DRV.2` 2–3 (max 3), `MAM.DRV.4` 3–5 (max 5)
  - Integration & applications: `MAM.I.1` 3–5 (max 7), `MAM.I.2` 3 (max 4), `MAM.I.3` 1–4 (max 6), `MAM.I.4` 2–4 (max 6), `MAM.I.5` 2–7 (max 8), `MAM.I.6` 1–2 (max 2), `MAM.I.7` 4–8 (max 8)
  - Exponential & logarithmic functions: `MAM.L.1` 4–6 (max 9), `MAM.L.2` 2–4 (max 5), `MAM.L.3` 5–7 (max 7), `MAM.L.5` 8 (max 8), `MAM.L.7` 1–3 (max 3)
  - Rectilinear motion (kinematics): `MAM.M.1` 4–6 (max 6), `MAM.M.3` 3 (max 3), `MAM.M.4` 6 (max 6), `MAM.M.6` 6 (max 6)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `MAM.CRV.1` 100%, `MAM.CRV.4` 100%, `MAM.D.5` 100%, `MAM.D.6` 100%, `MAM.D.8` 100%, `MAM.DRV.2` 100%, `MAM.I.3` 100%, `MAM.I.7` 100%, `MAM.DRV.4` 80%, `MAM.D.7` 75%, `MAM.L.3` 75%, `MAM.D.10` 67%, `MAM.D.2` 67%, `MAM.DRV.1` 67%, `MAM.CRV.2` 60%, `MAM.CRV.3` 60%, `MAM.I.5` 57%, `MAM.CRV.6` 50%, `MAM.D.4` 50%, `MAM.I.4` 50%, `MAM.I.6` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `MAM.D.5` 67%, `MAM.CRV.3` 40%, `MAM.D.4` 25%, `MAM.L.3` 25%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Differentiation & applications + Integration & applications: `MAM.D.1` Direct differentiation (combining rules) + `MAM.I.2` "Hence" — using the derivative just found to integrate (5); `MAM.D.1` Direct differentiation (combining rules) + `MAM.I.1` Basic indefinite integrals and finding f from f′ (5); `MAM.D.3` "rate of change of f′(x)", "explain the meaning of f″" + `MAM.I.1` Basic indefinite integrals and finding f from f′ (4); `MAM.D.10` Interpretation and description (1–3 marks every year) + `MAM.I.1` Basic indefinite integrals and finding f from f′ (1)
  - Integration & applications + Exponential & logarithmic functions: `MAM.I.5` Area under a curve / between curves + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (3); `MAM.I.5` Area under a curve / between curves + `MAM.L.2` Solving Exponential / Logarithmic Equations (CF exact values) (1); `MAM.I.6` Definite integral equations with unknown parameters + `MAM.L.2` Solving Exponential / Logarithmic Equations (CF exact values) (1); `MAM.I.6` Definite integral equations with unknown parameters + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (1)
  - Continuous random variables & normal + Discrete random variables & binomial: `MAM.CRV.3` Uniform distribution + `MAM.DRV.4` Bernoulli and binomial distributions (2); `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations + `MAM.DRV.4` Bernoulli and binomial distributions (1); `MAM.CRV.1` Relative frequency histogram → probability (CF) + `MAM.DRV.2` Expected value, variance and linear transformations (1); `MAM.CRV.2` Basic pdf operations + `MAM.DRV.4` Bernoulli and binomial distributions (1)
  - Differentiation & applications + Exponential & logarithmic functions: `MAM.D.1` Direct differentiation (combining rules) + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (1); `MAM.D.4` Full function analysis (stationary points + nature + inflection points + graph sketching) + `MAM.L.2` Solving Exponential / Logarithmic Equations (CF exact values) (1); `MAM.D.7` Increments formula δy ≈ (dy/dx)·δx + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (1); `MAM.D.1` Direct differentiation (combining rules) + `MAM.L.1` Expressing Logarithms Using Given Letters (CF) (1)
  - Continuous random variables & normal + Integration & applications: `MAM.CRV.2` Basic pdf operations + `MAM.I.2` "Hence" — using the derivative just found to integrate (2)
  - Integration & applications + Rectilinear motion (kinematics): `MAM.I.4` FTC and functions defined by integrals + `MAM.M.1` Given x(t), find v, a and what they mean (1)
  - Continuous random variables & normal + Differentiation & applications: `MAM.CRV.2` Basic pdf operations + `MAM.D.1` Direct differentiation (combining rules) (1)

### Calculator-assumed

- Questions per paper (2020–2025): 9–10; marks per question: 4–21 (median 10).
- Share of marks by topic: Sample proportions & confidence intervals 25%, Exponential & logarithmic functions 17%, Differentiation & applications 16%, Discrete random variables & binomial 16%, Continuous random variables & normal 13%, Rectilinear motion (kinematics) 8%, Integration & applications 6%.
- Cross-topic questions: 36% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Integration & applications** — 77% of its questions are cross-topic; pairs with Differentiation & applications 90%, Exponential & logarithmic functions 20%, Continuous random variables & normal 20%.
  - **Continuous random variables & normal** — 63% of its questions are cross-topic; pairs with Discrete random variables & binomial 58%, Sample proportions & confidence intervals 33%, Integration & applications 17%, Differentiation & applications 8%, Exponential & logarithmic functions 8%.
  - **Discrete random variables & binomial** — 62% of its questions are cross-topic; pairs with Sample proportions & confidence intervals 67%, Continuous random variables & normal 47%.
  - **Differentiation & applications** — 61% of its questions are cross-topic; pairs with Integration & applications 53%, Exponential & logarithmic functions 53%, Sample proportions & confidence intervals 6%, Rectilinear motion (kinematics) 6%, Continuous random variables & normal 6%.
  - **Sample proportions & confidence intervals** — 48% of its questions are cross-topic; pairs with Discrete random variables & binomial 77%, Continuous random variables & normal 31%, Differentiation & applications 8%.
  - **Exponential & logarithmic functions** — 42% of its questions are cross-topic; pairs with Differentiation & applications 82%, Integration & applications 18%, Rectilinear motion (kinematics) 18%, Continuous random variables & normal 9%.
  - **Rectilinear motion (kinematics)** — 20% of its questions are cross-topic; pairs with Exponential & logarithmic functions 100%, Differentiation & applications 50%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Sample proportions & confidence intervals: `MAM.CI.1` 3–6 (max 6), `MAM.CI.2` 2–4 (max 6), `MAM.CI.3` 2 (max 4), `MAM.CI.4` 2–5 (max 9), `MAM.CI.5` 2–4 (max 4), `MAM.CI.6` 4 (max 4), `MAM.CI.7` 2–6 (max 6)
  - Continuous random variables & normal: `MAM.CRV.1` 2 (max 2), `MAM.CRV.2` 3–7 (max 9), `MAM.CRV.3` 3–9 (max 9), `MAM.CRV.4` 2–7 (max 10), `MAM.CRV.5` 3–5 (max 5), `MAM.CRV.7` 2 (max 2)
  - Differentiation & applications: `MAM.D.1` 2 (max 4), `MAM.D.4` 3–7 (max 13), `MAM.D.5` 5 (max 5), `MAM.D.6` 3–6 (max 10), `MAM.D.7` 3 (max 3), `MAM.D.8` 2–6 (max 6), `MAM.D.9` 4–5 (max 5), `MAM.D.10` 1–4 (max 4)
  - Discrete random variables & binomial: `MAM.DRV.1` 2–4 (max 5), `MAM.DRV.2` 2–7 (max 8), `MAM.DRV.3` 2–6 (max 9), `MAM.DRV.4` 3–6 (max 9), `MAM.DRV.5` 2–3 (max 3), `MAM.DRV.6` 2–4 (max 4)
  - Integration & applications: `MAM.I.1` 4 (max 4), `MAM.I.4` 2–4 (max 4), `MAM.I.5` 4–5 (max 6), `MAM.I.6` 3 (max 3), `MAM.I.8` 4–5 (max 8)
  - Exponential & logarithmic functions: `MAM.L.1` 2–3 (max 3), `MAM.L.2` 2–3 (max 3), `MAM.L.3` 2–6 (max 6), `MAM.L.4` 6–8 (max 10), `MAM.L.5` 7–10 (max 11), `MAM.L.6` 2–3 (max 3), `MAM.L.7` 1–2 (max 5)
  - Rectilinear motion (kinematics): `MAM.M.1` 2 (max 5), `MAM.M.2` 3–5 (max 6), `MAM.M.3` 2–5 (max 5), `MAM.M.4` 2–3 (max 4), `MAM.M.5` 2–4 (max 4), `MAM.M.6` 2–4 (max 4)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `MAM.D.4` 100%, `MAM.D.9` 100%, `MAM.I.8` 100%, `MAM.L.1` 100%, `MAM.L.2` 100%, `MAM.D.6` 80%, `MAM.I.5` 80%, `MAM.L.7` 80%, `MAM.CRV.7` 75%, `MAM.CRV.2` 71%, `MAM.CRV.3` 67%, `MAM.D.10` 67%, `MAM.L.3` 67%, `MAM.L.5` 60%, `MAM.CI.7` 50%, `MAM.D.5` 50%, `MAM.D.8` 50%, `MAM.DRV.6` 50%, `MAM.L.6` 50%, `MAM.M.5` 50%, `MAM.M.6` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `MAM.D.4` 71%, `MAM.L.3` 67%, `MAM.M.6` 50%, `MAM.L.5` 40%, `MAM.D.10` 33%, `MAM.D.9` 33%, `MAM.M.1` 20%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Sample proportions & confidence intervals + Discrete random variables & binomial: `MAM.CI.3` Use a confidence interval to test a claim + `MAM.DRV.4` Bernoulli and binomial distributions (8); `MAM.CI.2` Calculate a confidence interval and margin of error + `MAM.DRV.4` Bernoulli and binomial distributions (7); `MAM.CI.1` Write down the distribution of p̂ and find a probability + `MAM.DRV.4` Bernoulli and binomial distributions (3); `MAM.CI.5` Factors affecting interval width + `MAM.DRV.4` Bernoulli and binomial distributions (3)
  - Differentiation & applications + Exponential & logarithmic functions: `MAM.D.1` Direct differentiation (combining rules) + `MAM.L.4` Exponential Growth/Decay Models (3); `MAM.D.4` Full function analysis (stationary points + nature + inflection points + graph sketching) + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (2); `MAM.D.4` Full function analysis (stationary points + nature + inflection points + graph sketching) + `MAM.L.6` Logarithmic models + differentiation + drawing a conclusion (2); `MAM.D.1` Direct differentiation (combining rules) + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (1)
  - Differentiation & applications + Integration & applications: `MAM.D.7` Increments formula δy ≈ (dy/dx)·δx + `MAM.I.4` FTC and functions defined by integrals (2); `MAM.D.6` Optimisation (optimisation) + `MAM.I.5` Area under a curve / between curves (2); `MAM.D.1` Direct differentiation (combining rules) + `MAM.I.5` Area under a curve / between curves (1); `MAM.D.4` Full function analysis (stationary points + nature + inflection points + graph sketching) + `MAM.I.5` Area under a curve / between curves (1)
  - Continuous random variables & normal + Discrete random variables & binomial: `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations + `MAM.DRV.5` Combined with the normal distribution ("at least k out of n items …") (4); `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations + `MAM.DRV.1` Completing a distribution table / finding unknown probabilities (2); `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations + `MAM.DRV.2` Expected value, variance and linear transformations (2); `MAM.CRV.3` Uniform distribution + `MAM.DRV.4` Bernoulli and binomial distributions (1)
  - Sample proportions & confidence intervals + Continuous random variables & normal: `MAM.CI.1` Write down the distribution of p̂ and find a probability + `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations (2); `MAM.CI.2` Calculate a confidence interval and margin of error + `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations (1); `MAM.CI.3` Use a confidence interval to test a claim + `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations (1); `MAM.CI.4` Sample size / reversing from an interval + `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations (1)
  - Integration & applications + Exponential & logarithmic functions: `MAM.I.5` Area under a curve / between curves + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (2)
  - Exponential & logarithmic functions + Rectilinear motion (kinematics): `MAM.L.2` Solving Exponential / Logarithmic Equations (CF exact values) + `MAM.M.5` Maximum velocity / zero acceleration (1); `MAM.L.4` Exponential Growth/Decay Models + `MAM.M.1` Given x(t), find v, a and what they mean (1); `MAM.L.4` Exponential Growth/Decay Models + `MAM.M.3` When it is at rest / changes direction / returns to the starting point (1)
  - Continuous random variables & normal + Integration & applications: `MAM.CRV.2` Basic pdf operations + `MAM.I.8` Integration applications in context (cross-sectional area, volume, total change) (1); `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations + `MAM.I.8` Integration applications in context (cross-sectional area, volume, total change) (1)
  - Sample proportions & confidence intervals + Differentiation & applications: `MAM.CI.4` Sample size / reversing from an interval + `MAM.D.6` Optimisation (optimisation) (1)
  - Differentiation & applications + Rectilinear motion (kinematics): `MAM.D.4` Full function analysis (stationary points + nature + inflection points + graph sketching) + `MAM.M.5` Maximum velocity / zero acceleration (1)
  - Continuous random variables & normal + Differentiation & applications: `MAM.CRV.4` Normal distribution — forward probability and inverse quantile calculations + `MAM.D.7` Increments formula δy ≈ (dy/dx)·δx (1)
  - Continuous random variables & normal + Exponential & logarithmic functions: `MAM.CRV.2` Basic pdf operations + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (1); `MAM.CRV.7` Determining whether a model is appropriate (explanation question) + `MAM.L.7` Calculus of eˣ / ln x (cross-reference) (1)

<!-- blueprint:end -->
