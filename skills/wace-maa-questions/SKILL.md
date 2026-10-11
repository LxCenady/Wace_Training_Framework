---
name: wace-maa-questions
description: Generate original WACE Mathematics Applications ATAR (MAA, Units 3–4) exam-style questions with SCSA-style marking keys, by topic (bivariate data, sequences growth & decay, graphs & networks, time series, loans/investments/annuities, network & decision mathematics), calibrated against the 2016–2025 papers. Use when the user asks for Applications / MAA / 数学应用 practice questions, 出题, a topic quiz, or a mock section.
---

# WACE Mathematics Applications — topic question generator

## Locating `<ROOT>` (live path — never hard-code)

All paths below are relative to `<ROOT>`, the data folder that contains `MAA/`, `MAM/`, `MAS/` and `tools/`. Resolve it once per session, in this order:

1. Environment variable `WACE_MATHS_ROOT`, if set and it contains `MAA/`.
2. Walk up from this SKILL.md's real location: the first ancestor folder containing both `MAA/` and `MAM/` (the canonical copy lives at `<ROOT>/skills/wace-maa-questions/SKILL.md`, so normally two levels up).
3. Fallback `E:\WACE_Maths`. If none exists, ask the user where the folder is.

Python: `<ROOT>\.venv\Scripts\python.exe` if present, otherwise any Python 3. The checks in step 5 need only the standard library (`itertools`, `fractions`); sympy or numpy are optional.

Indexed database `<ROOT>\wace.db` (SQLite, built by `tools/build_db.py`): every past question is tagged per sub-question with pattern codes like `MAA.FIN.4` (= topic code + 题型 number in the methods notes; `FIN4` in the catalogue and tag files). Useful queries:
- similar past questions: `SELECT DISTINCT qid FROM part_patterns WHERE pattern='<code>'`
- the pattern's method text: `SELECT title, method FROM patterns WHERE code='<code>'`
- marks a pattern carried in real questions: `SELECT qid, marks FROM pattern_marks WHERE pattern='<code>'`
- one-row-per-mark marking scheme: `SELECT label, text FROM points WHERE qid='<qid>' ORDER BY ord` (trust it only when `questions.points_ok=1`; otherwise read the key PDF crop).

Pattern definitions (67 patterns, names, syllabus references, boundaries between neighbours): `<ROOT>\tools\catalogue_MAA.json`; per-part tags: `<ROOT>\tools\parttags_MAA.txt`. Example codes: `FIN4` = reducing-balance loan recurrence; `TSI4` = seasonal indices by the average percentage method.

Past-paper corpus, 2016–2025 (no 2019 marking key), 138 questions, 1350 part marks:

- Topic guides (patterns, typical marks, what SCSA asks): `topics/<NN_Topic>.md` next to this file. Read the one for the requested topic first.
- Question bank (stems with page refs): `<ROOT>\MAA\topics\<NN_Topic>.md`.
- Same questions as PDF (exam crop plus marking-key crop): `<ROOT>\MAA\topics\<NN_Topic>.pdf`.
- Solving-method notes, Chinese: `<ROOT>\MAA\methods\<NN_Topic>_解题思路.md`. English mirror: `<ROOT>\MAA\methods_en\<NN_Topic>_Methods.md`.
- Full papers, keys, examiners' reports, formula sheets: `<ROOT>\MAA\papers\`. Citations such as "2016 CA Q12" mean the 2016 Calculator-assumed paper, question 12; "CF" means Calculator-free. These are cited only from `papers/` and the bank.

| code | topic file | 中文 | share of marks | CF / CA questions |
|---|---|---|---|---|
| BIV | 01_Bivariate_Data | 双变量数据分析 (Unit 3.1) | 22% | 12 / 14 |
| SEQ | 02_Sequences | 数列增长与衰减 (Unit 3.2) | 14% | 9 / 14 |
| GRF | 03_Graphs_Networks | 图与网络 (Unit 3.3) | 12% | 17 / 6 |
| TSI | 04_Time_Series | 时间序列分析 (Unit 4.1) | 9% | 1 / 9 |
| FIN | 05_Loans_Annuities | 贷款、投资与年金 (Unit 4.2) | 19% | 1 / 24 |
| NDM | 06_Network_Decisions | 网络与决策数学 (Unit 4.3) | 23% | 20 / 17 |

Shares are of the 2016–2025 tagged part marks. Question counts are per topic; a question can carry two topics, but only 6 of 138 do.

## Paper format (what the real papers look like)

- **Section One: Calculator-free.** 5–7 questions, 50 working minutes, about 50 marks (weighted 35%). A formula sheet is provided.
- **Section Two: Calculator-assumed.** 8–10 questions, 100 working minutes, about 100 marks (weighted 65%). Scientific, graphic and CAS calculators are permitted.
- Each question has a header `Question N (x marks)`. Question totals run from 3 to 19 marks; calculator-assumed questions are longer.
- Calculator-free papers are mostly networks (GRF, NDM), two-way tables (BIV), and exact-arithmetic sequences (SEQ). Calculator-assumed papers are mostly finance (FIN), time series (TSI), regression and growth models (BIV, SEQ).
- Calculator-assumed papers dominate by marks (about two-thirds of all marks). Calculator-free papers are still a third of the marks, so generate both.

## Workflow

1. **Pin down the request.** Topic(s), number of questions, section (default: where the table above says the topic usually sits; BIV can go either way, SEQ is calculator-free for arithmetic and calculator-assumed for geometric growth, GRF and NDM are mostly calculator-free, FIN and TSI are calculator-assumed), difficulty (基础 / 中等 / 压轴 ≈ early / mid / last-question level), language (default English, like the real paper; explanations in Chinese if the user writes Chinese). State the defaults you used rather than asking.
2. **Calibrate.** Read `topics/<topic>.md` and the matching Chinese method note `MAA\methods\<NN_Topic>_解题思路.md` (or its English mirror). Pick which pattern(s) each new question tests. The marking key must award marks where that pattern's steps and mark points say. Then grep the bank `MAA\topics\<NN_Topic>.md` for 2–4 past questions nearest to what you will write (same pattern, same section). For a long question, open the matching PDF pages with Read to see how the key splits its marks.
3. **Write original questions.** New context, new numbers, new structure. Never copy or lightly reword a past question. Use the SCSA voice: "Determine…", "Complete the table…", "Draw…", "Explain…", "Comment on…", "Justify your answer", "correct to 2 decimal places". Keep the contexts Australian and everyday (sport participation survey, canteen sales, bus timetable, sprinkler pipes, car depreciation, retirement savings, pop-up shop, fuel use), and give each one new numbers. Number parts (a), (b)(i) and so on, with marks per part. Header: `Question N (x marks)`.
   - Calculator-free: small graphs (up to about 8 vertices), assignment matrices up to 4 × 4, exact fractions or whole numbers, no logarithms or non-integer powers, tables of at most about five values. Keep every answer hand-computable.
   - Calculator-assumed: realistic data (8–15 points for regression, 8–28 quarters or weeks for time series), money to the cent, stated rounding ("correct to 2 decimal places", "to the nearest dollar"), and the financial parameters written out (N, I, PV, PMT, FV, P/Y, C/Y, timing).
   - Do not mix two topics in one question unless the pairing is one the real papers use: GRF with NDM (5 of 6 cross-topic questions), or FIN with SEQ (1).
4. **Write the marking key** in SCSA format for every part:
   ```
   Solution
   <full worked solution>
   Specific behaviours
   ✓ <one observable action per mark>
   ```
   The number of ✓ equals the part's marks, and the part marks sum to the question total. Mark the working, the setup, the in-context conclusion and units the way the real keys do (see the conventions below).
5. **Verify before showing.** Solve every part independently. Use closed forms for finance and time series (write the arithmetic out in a short script). For networks, use brute force: enumerate all paths; all spanning trees for graphs with up to about 8 edges; all S–T cuts; all permutations for assignments up to 6 × 6; compare the Hungarian answer with the brute-force minimum. For regression, compute the slope, intercept, r and residuals directly. Fix any mismatch. Confirm that calculator-free answers are exact and hand-computable. Report that verification ran.
6. **Output.** Questions first, then a separator, then the marking key, so the user can attempt first. Use LaTeX (`$...$`) for maths and tables for matrices and networks (a text edge list is fine if a drawing is not possible; say that a diagram is needed). After the key, one line per question: "最接近的真题: 2018 CA Q14 (bank PDF p.x)" so the user can compare. If the user wants a file, save to `<ROOT>\generated\MAA\<topic>_<YYYYMMDD>.md`.

## Mock section mode

If asked for a 模拟卷 or mock: Section One ≈ 50 marks / 50 min, 5–7 questions (GRF, NDM, BIV, SEQ dominate; keep to exact arithmetic). Section Two ≈ 100 marks / 100 min, 8–10 questions (FIN, TSI, BIV, SEQ, NDM). Weight topics by the share column. Order the questions from easier to harder within each section, and leave the longest finance and time-series questions for the second half. Keep questions single-topic.

## Conventions every key must follow

- One mark = one ✓ behaviour. Partial credit is per behaviour, never "award 2 if…".
- Working: two-mark questions and longer must show working. Calculator answers need the inputs written: for a financial solver, state N, I, PV, PMT, FV, P/Y and C/Y, and the sign convention. A correct answer with no working can earn no marks.
- Explanations and conclusions are "in context": name the variables, the direction of change, the units, and say "on average" or "predicted" for regression-based statements. Generic "it is an association" statements earn nothing.
- Regression: write the equation with the variable names the stem uses. Draw the line with a ruler, and state the two points used. The sign of r follows the sign of the slope. Give r² as a percentage when the question asks for "the proportion".
- Prediction: a value outside the range of the data is extrapolation and is unreliable. Judge whether the prediction is reliable from both the range of x and the strength of r.
- Association and causation: a strong correlation alone does not prove causation. A good answer names a specific confounding factor or a reverse direction.
- Percentage tables: take percentages within the groups of the explanatory variable (row percentages if it is in the rows, column percentages if in the columns).
- Money to the cent. Discrete counts (periods, people, fish) are rounded in the direction the context needs. The number of payments needed to clear a loan is rounded up to the next whole period.
- Networks: arrows on directed networks, including dummy activities. Route answers list the vertices in order, and the total is the sum of the edge weights. Max flow: list each path with its flow and add them up. Cut capacity counts only arcs going from the source side to the sink side. Euler's formula check writes v, e and f first, then substitutes. Eulerian status is decided by counting odd vertices. Hamiltonian routes repeat no vertex. Critical activities have float 0. Latest starting time is the minimum over the successors.
- Hungarian algorithm: state the number of lines that cover the zeros at each stage. The total cost or output uses the original matrix values, not the reduced ones. For a maximisation problem, subtract each entry from a constant before starting.
- Time series: index the time periods the way the question does, and check the cycle length (quarters, 5-, 6-, 7-day weeks). Seasonal indices are decimals in calculations, normalised to average 1 (or 100%). Deseasonalise by dividing; restore by multiplying.

## Explain mode

If the user asks how to solve a type of question (怎么做 / 解题思路 / 讲一下) rather than for new questions: answer from the topic guide and the matching method note. Identify the pattern code, give the steps and the mark-earning lines, and cite 1–2 past questions with their bank PDF pages. Then offer a fresh practice question of that pattern.

## Known caveats (keep generated keys honest)

- 2017 CA Q8 (loan): the stem says payments are at the start of the year, but the key solves with end-of-period payments. When you write a question with a payment-timing choice, state the timing explicitly and solve with that timing.
- 2017 CA Q15(b)(vi) (time series): the key calls a forecast one cycle beyond the data "reliable". The default rule is that a forecast beyond the last observed period is extrapolation. Use the exception only if the question asks for it.
- GRF9 and GRF6: two keys (2020 CA Q13(a), 2022 CA Q10(b)(ii)) tag a visit-every-vertex route with no revisits. Treat any route that repeats no vertex as a Hamiltonian-type route, and keep the GRF9 "may revisit" wording only when the stem allows repeats.
- 2018 CA Q9(b) (sequences): the key's written answer does not match its own table value (47.249 rounds to 47). Avoid rounding edge cases like this, or state the rounding rule explicitly.
- Catalogue status `related` (BIV12–BIV14, SEQ9, GRF7, GRF9, FIN10, NDM11, NDM13–NDM15): the syllabus link is indirect. Use these operations only as one component of a larger question, not as the whole question.

<!-- blueprint:start (generated by tools/blueprint.py from wace.db — do not edit by hand) -->
## Paper blueprint (from the 2016–2025 papers)

Use this when writing a set or a mock paper: **randomise** (vary question count, marks per question, which patterns appear, and order within the difficulty ramp — never the same paper twice), but keep the **topic mark distribution** close to the real one below, and make the stated share of questions **cross-topic** (two topics in one question), using only pairings that real papers use.

### Calculator-free

- Questions per paper (2020–2025): 5–7; marks per question: 3–13 (median 9).
- Share of marks by topic: Networks and decision mathematics 31%, Graphs and networks 26%, Bivariate data analysis 23%, Growth and decay in sequences 16%, Time series analysis 3%, Loans, investments and annuities 1%.
- Cross-topic questions: 7% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Graphs and networks** — 24% of its questions are cross-topic; pairs with Networks and decision mathematics 100%.
  - **Networks and decision mathematics** — 20% of its questions are cross-topic; pairs with Graphs and networks 100%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Bivariate data analysis: `MAA.BIV.1` 5–7 (max 7), `MAA.BIV.2` 1–2 (max 5), `MAA.BIV.3` 2 (max 2), `MAA.BIV.4` 1–2 (max 2), `MAA.BIV.5` 2 (max 2), `MAA.BIV.6` 2 (max 2), `MAA.BIV.7` 1–2 (max 2), `MAA.BIV.8` 3–4 (max 4), `MAA.BIV.9` 1–2 (max 2), `MAA.BIV.10` 2 (max 2), `MAA.BIV.11` 1 (max 3), `MAA.BIV.14` 2 (max 2), `MAA.BIV.15` 1–2 (max 2), `MAA.BIV.16` 2 (max 2)
  - Loans, investments and annuities: `MAA.FIN.2` 2 (max 2), `MAA.FIN.3` 3 (max 3)
  - Graphs and networks: `MAA.GRF.1` 2–4 (max 4), `MAA.GRF.2` 2–5 (max 7), `MAA.GRF.3` 2–4 (max 7), `MAA.GRF.4` 3–4 (max 4), `MAA.GRF.5` 1–2 (max 4), `MAA.GRF.6` 1–2 (max 3), `MAA.GRF.7` 3 (max 3), `MAA.GRF.8` 1–2 (max 2), `MAA.GRF.9` 3 (max 3)
  - Networks and decision mathematics: `MAA.NDM.1` 3–4 (max 5), `MAA.NDM.2` 2 (max 2), `MAA.NDM.3` 3–4 (max 5), `MAA.NDM.4` 1 (max 1), `MAA.NDM.5` 1–2 (max 2), `MAA.NDM.6` 4–5 (max 5), `MAA.NDM.7` 1–4 (max 4), `MAA.NDM.8` 3 (max 3), `MAA.NDM.9` 2 (max 4), `MAA.NDM.10` 6–7 (max 8), `MAA.NDM.11` 2 (max 2), `MAA.NDM.12` 2 (max 2), `MAA.NDM.13` 2 (max 2), `MAA.NDM.15` 2 (max 2)
  - Growth and decay in sequences: `MAA.SEQ.1` 2 (max 2), `MAA.SEQ.2` 4–7 (max 9), `MAA.SEQ.3` 1 (max 1), `MAA.SEQ.4` 3–4 (max 4), `MAA.SEQ.5` 2–3 (max 3), `MAA.SEQ.6` 2 (max 2), `MAA.SEQ.7` 2 (max 2)
  - Time series analysis: `MAA.TSI.3` 2 (max 2), `MAA.TSI.4` 3 (max 3), `MAA.TSI.5` 3 (max 3), `MAA.TSI.6` 1 (max 1), `MAA.TSI.7` 3 (max 3)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `MAA.BIV.14` 100%, `MAA.BIV.15` 100%, `MAA.BIV.16` 100%, `MAA.BIV.4` 100%, `MAA.NDM.1` 100%, `MAA.NDM.10` 100%, `MAA.NDM.2` 100%, `MAA.NDM.5` 100%, `MAA.NDM.6` 100%, `MAA.NDM.7` 100%, `MAA.NDM.9` 100%, `MAA.GRF.5` 91%, `MAA.GRF.1` 89%, `MAA.GRF.3` 88%, `MAA.GRF.2` 80%, `MAA.GRF.4` 75%, `MAA.BIV.11` 67%, `MAA.BIV.8` 67%, `MAA.GRF.6` 67%, `MAA.GRF.8` 67%, `MAA.SEQ.5` 67%, `MAA.BIV.1` 62%, `MAA.BIV.2` 62%, `MAA.NDM.3` 60%, `MAA.BIV.3` 50%, `MAA.BIV.7` 50%, `MAA.BIV.9` 50%, `MAA.GRF.7` 50%, `MAA.SEQ.3` 50%, `MAA.SEQ.4` 50%, `MAA.SEQ.7` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `MAA.BIV.15` 100%, `MAA.NDM.9` 67%, `MAA.NDM.1` 60%, `MAA.BIV.14` 50%, `MAA.BIV.16` 50%, `MAA.BIV.3` 50%, `MAA.GRF.7` 50%, `MAA.NDM.3` 40%, `MAA.NDM.10` 25%, `MAA.NDM.2` 25%, `MAA.GRF.1` 22%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Graphs and networks + Networks and decision mathematics: `MAA.GRF.2` Adjacency matrices and multistage counts + `MAA.NDM.1` Spanning trees and minimum spanning trees (1); `MAA.GRF.2` Adjacency matrices and multistage counts + `MAA.NDM.2` Minimum connector problem (1); `MAA.GRF.9` Shortest journey visiting every vertex + `MAA.NDM.1` Spanning trees and minimum spanning trees (1); `MAA.GRF.1` Graph types, degrees and construction + `MAA.NDM.10` Optimal assignment and Hungarian algorithm (1)

### Calculator-assumed

- Questions per paper (2020–2025): 8–10; marks per question: 6–19 (median 11).
- Share of marks by topic: Loans, investments and annuities 29%, Bivariate data analysis 21%, Networks and decision mathematics 19%, Growth and decay in sequences 13%, Time series analysis 13%, Graphs and networks 5%.
- Cross-topic questions: 2% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Graphs and networks** — 17% of its questions are cross-topic; pairs with Networks and decision mathematics 100%.
  - **Growth and decay in sequences** — 7% of its questions are cross-topic; pairs with Loans, investments and annuities 100%.
  - **Networks and decision mathematics** — 6% of its questions are cross-topic; pairs with Graphs and networks 100%.
  - **Loans, investments and annuities** — 4% of its questions are cross-topic; pairs with Growth and decay in sequences 100%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Bivariate data analysis: `MAA.BIV.1` 2 (max 2), `MAA.BIV.2` 1 (max 1), `MAA.BIV.3` 1–3 (max 4), `MAA.BIV.4` 2–3 (max 5), `MAA.BIV.5` 1–2 (max 4), `MAA.BIV.6` 2 (max 3), `MAA.BIV.7` 1–2 (max 2), `MAA.BIV.8` 2–3 (max 3), `MAA.BIV.9` 1–2 (max 3), `MAA.BIV.10` 3 (max 3), `MAA.BIV.11` 1 (max 1), `MAA.BIV.12` 5–6 (max 6), `MAA.BIV.13` 2 (max 2), `MAA.BIV.14` 1–2 (max 3), `MAA.BIV.15` 1–2 (max 2), `MAA.BIV.16` 1–2 (max 2)
  - Loans, investments and annuities: `MAA.FIN.1` 2–4 (max 4), `MAA.FIN.2` 2–3 (max 4), `MAA.FIN.3` 2–3 (max 3), `MAA.FIN.4` 3–6 (max 8), `MAA.FIN.5` 1–3 (max 5), `MAA.FIN.6` 3–5 (max 6), `MAA.FIN.7` 3–6 (max 8), `MAA.FIN.8` 3–4 (max 8), `MAA.FIN.9` 2–3 (max 3), `MAA.FIN.10` 1–2 (max 3)
  - Graphs and networks: `MAA.GRF.2` 3 (max 3), `MAA.GRF.3` 2–4 (max 4), `MAA.GRF.4` 3–8 (max 8), `MAA.GRF.5` 1–2 (max 2), `MAA.GRF.6` 2–4 (max 4), `MAA.GRF.7` 5 (max 5), `MAA.GRF.8` 1 (max 1)
  - Networks and decision mathematics: `MAA.NDM.1` 5–6 (max 6), `MAA.NDM.2` 2–3 (max 3), `MAA.NDM.3` 3 (max 4), `MAA.NDM.4` 1 (max 1), `MAA.NDM.5` 1 (max 1), `MAA.NDM.6` 5–6 (max 8), `MAA.NDM.7` 2–4 (max 5), `MAA.NDM.8` 1–2 (max 3), `MAA.NDM.10` 9 (max 9), `MAA.NDM.11` 2–6 (max 6), `MAA.NDM.12` 1–3 (max 5), `MAA.NDM.13` 2 (max 3), `MAA.NDM.14` 1–2 (max 2), `MAA.NDM.15` 2–3 (max 3)
  - Growth and decay in sequences: `MAA.SEQ.1` 2 (max 2), `MAA.SEQ.2` 2–4 (max 4), `MAA.SEQ.4` 2 (max 3), `MAA.SEQ.5` 4–7 (max 10), `MAA.SEQ.6` 1–3 (max 3), `MAA.SEQ.7` 2 (max 3), `MAA.SEQ.8` 1–2 (max 5), `MAA.SEQ.9` 2–4 (max 4)
  - Time series analysis: `MAA.TSI.1` 2 (max 2), `MAA.TSI.2` 1–2 (max 2), `MAA.TSI.3` 2–3 (max 5), `MAA.TSI.4` 4–5 (max 6), `MAA.TSI.5` 2–4 (max 4), `MAA.TSI.6` 2–3 (max 3), `MAA.TSI.7` 3–5 (max 5), `MAA.TSI.8` 2 (max 2)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `MAA.BIV.11` 100%, `MAA.GRF.3` 100%, `MAA.GRF.5` 100%, `MAA.GRF.6` 100%, `MAA.GRF.8` 100%, `MAA.NDM.2` 100%, `MAA.TSI.1` 100%, `MAA.BIV.8` 90%, `MAA.BIV.6` 89%, `MAA.BIV.7` 89%, `MAA.BIV.14` 83%, `MAA.BIV.15` 83%, `MAA.BIV.16` 83%, `MAA.BIV.9` 83%, `MAA.TSI.3` 83%, `MAA.BIV.4` 82%, `MAA.BIV.5` 82%, `MAA.BIV.3` 75%, `MAA.NDM.1` 75%, `MAA.NDM.11` 75%, `MAA.TSI.6` 75%, `MAA.NDM.13` 71%, `MAA.GRF.4` 67%, `MAA.NDM.12` 62%, `MAA.NDM.8` 62%, `MAA.TSI.4` 62%, `MAA.NDM.3` 60%, `MAA.NDM.6` 60%, `MAA.NDM.7` 60%, `MAA.TSI.5` 57%, `MAA.TSI.7` 57%, `MAA.NDM.15` 50%, `MAA.NDM.5` 50%, `MAA.SEQ.6` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `MAA.TSI.1` 100%, `MAA.BIV.14` 83%, `MAA.BIV.15` 83%, `MAA.BIV.16` 67%, `MAA.BIV.5` 55%, `MAA.BIV.3` 50%, `MAA.NDM.1` 50%, `MAA.TSI.6` 50%, `MAA.NDM.12` 38%, `MAA.NDM.2` 33%, `MAA.NDM.6` 20%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Loans, investments and annuities + Growth and decay in sequences: `MAA.FIN.4` Reducing-balance loan recurrence + `MAA.SEQ.5` Geometric nth term and growth or decay prediction (1); `MAA.FIN.5` Repayment, rate and payoff duration + `MAA.SEQ.5` Geometric nth term and growth or decay prediction (1); `MAA.FIN.6` Total loan interest and final adjusted repayment + `MAA.SEQ.5` Geometric nth term and growth or decay prediction (1)
  - Graphs and networks + Networks and decision mathematics: `MAA.GRF.4` Shortest path in a weighted graph + `MAA.NDM.1` Spanning trees and minimum spanning trees (1); `MAA.GRF.4` Shortest path in a weighted graph + `MAA.NDM.12` Cut capacity and flow upper bounds (1); `MAA.GRF.4` Shortest path in a weighted graph + `MAA.NDM.13` Path bottlenecks and path-flow allocation (1); `MAA.GRF.4` Shortest path in a weighted graph + `MAA.NDM.8` Maximum flow and minimum cut (1)

<!-- blueprint:end -->
