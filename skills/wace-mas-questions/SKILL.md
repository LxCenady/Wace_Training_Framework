---
name: wace-mas-questions
description: Generate original WACE Mathematics Specialist ATAR (MAS, Units 3–4) exam-style questions with SCSA-style marking keys, by topic (complex numbers, functions & graphs, 3D vectors & linear systems, vector calculus, integration, rates of change & differential equations, statistical inference), calibrated against every 2016–2025 past paper. Use when the user asks for Specialist / MAS / 专业数学 / 特殊数学 practice questions, 出题, a topic quiz, or a mock section.
---

# WACE Mathematics Specialist — topic question generator

## Locating `<ROOT>` (live path — never hard-code)

All paths below are relative to `<ROOT>`, the data folder that contains `MAM/`, `MAS/`, `tools/` and `wace.db`. Resolve it once per session, in this order:

1. Environment variable `WACE_MATHS_ROOT`, if set and it contains `MAS/`.
2. Walk up from this SKILL.md's real location: the first ancestor folder containing both `MAM/` and `MAS/` (the canonical copy lives at `<ROOT>/skills/<skill>/SKILL.md`, so normally two levels up).
3. Fallback `E:\WACE_Maths`. If none exists, ask the user where the folder is.

Python: `<ROOT>\.venv\Scripts\python.exe` if present, otherwise any Python 3 with sympy/scipy.

Indexed database `<ROOT>\wace.db` (SQLite, built by `tools/build_db.py`): every past question is tagged per sub-question with pattern codes like `MAS.DE.4` (= topic code + 题型 number in the methods notes). Useful queries:
- similar past questions: `SELECT DISTINCT qid FROM part_patterns WHERE pattern='<code>'`
- the pattern's method text: `SELECT title, method FROM patterns WHERE code='<code>'`
- one-row-per-mark marking scheme: `SELECT label, text FROM points WHERE qid='<qid>' ORDER BY ord` (trust it only when `questions.points_ok=1`; otherwise read the key PDF crop).

Past-paper corpus (2016–2025, 193 questions, 1391 marks), split by topic, lives on disk:

- Topic guides (syllabus + what SCSA actually asks): `topics/<NN_Topic>.md` next to this file — read the one for the requested topic first.
- Question bank (stem text of every past question in that topic, with page refs): `<ROOT>\MAS\topics\<NN_Topic>.md`
- Same questions as PDF (original exam crop + ratified marking key crop, vector quality): `<ROOT>\MAS\topics\<NN_Topic>.pdf`
- Solving-method notes (题型 patterns, step-by-step method, where each mark is awarded, examiners' report warnings; Chinese with English terms): `<ROOT>\MAS\methods\<NN_Topic>_解题思路.md`
- Full original papers, keys, exam reports, formula sheets: `<ROOT>\MAS\papers\` (citations like "2016S F4" = 2016 official sample exam; those are only in papers/, not in the topic files)

| code | topic file | 中文 | share of marks (primary) | calc-free / calc-assumed questions |
|---|---|---|---|---|
| C | 01_Complex_Numbers | 复数 | 18% | 21 / 21 |
| F | 02_Functions_Graphs | 函数与图像 | 14% | 21 / 7 |
| V | 03_Vectors_3D | 三维向量与线性方程组 | 12% | 11 / 12 |
| VC | 04_Vector_Calculus | 向量微积分与运动 | 8% | 0 / 12 |
| I | 05_Integration | 积分技巧与应用 | 17% | 25 / 14 |
| DE | 06_Rates_DiffEq | 变化率与微分方程 | 18% | 2 / 30 |
| S | 07_Statistical_Inference | 统计推断（样本均值） | 13% | 0 / 17 |

VC and S have never appeared in the calculator-free section; DE almost never. Do not put them there unless the user insists (then keep numbers exact and tiny).

## Workflow

1. **Pin down the request.** Topic(s), number of questions, difficulty (基础 / 中等 / 压轴), section (default: where the table says the topic usually lives), language (default English, exactly like the real paper; explanations in Chinese if the user writes Chinese). Use sensible defaults and state them rather than asking.
2. **Calibrate.** Read `topics/<topic>.md` and the matching `methods\<NN_Topic>_解题思路.md` (pick which 题型 pattern(s) each new question tests; the marking key must award marks where that pattern's 得分点 says). Grep the bank file for 2–4 past questions nearest to what you will write. For long/hard questions open the matching PDF pages with Read (`pages` param) to see how the ratified key splits marks.
3. **Write original questions.** New context, numbers and structure — never copy or lightly reword a past question. SCSA voice: "Determine…", "Show that…", "Hence…", "Prove, using a vector method…", "Justify your answer.", "correct to 0.01". Header `Question N (x marks)`, parts (a), (b)(i) with marks.
   - Calculator-free: exact values (surds, π, cis(π/6)), polynomials with integer/Gaussian-integer roots, substitutions that collapse cleanly.
   - Calculator-assumed: realistic contexts, stated rounding, CAS steps allowed but the setup (integral, equation) must be written.
4. **Write the marking key** in SCSA format for every part:
   ```
   Solution
   <full worked solution>
   Specific behaviours
   ✓ <one observable action per mark>
   ```
   ✓ count = marks; parts sum to the total. Sketch questions: one ✓ per feature (asymptote, intercept, shape, endpoint, open/closed boundary, shading).
5. **Verify before showing.** Solve every part independently with `<ROOT>\.venv\Scripts\python.exe` (sympy: complex roots, integrals, DE solutions via dsolve, plane/line algebra; scipy.stats for sample-mean probabilities). Fix any mismatch; confirm calculator-free answers are hand-computable. Report that verification ran.
6. **Output.** Questions first, separator, then marking key. LaTeX (`$...$`); vectors as column vectors or with ~ underneath like the papers. After the key, list "最接近的真题: <year> <section> Q<n> (PDF p.x)". If the user wants a file, save to `<ROOT>\generated\MAS\<topic>_<YYYYMMDD>.md`.

## Mock section mode

Calculator-free ≈ 45–54 marks / 50 min, 7–9 questions (C, F, I, V dominate); calculator-assumed ≈ 85–100 marks / 100 min, 10–13 questions (DE, VC, S, C, V, I). Weight by the share column; order easy → hard.

## Conventions every key must follow

- One ✓ per mark; partial credit per behaviour.
- Complex numbers: polar form as r cis θ with the stated principal range (−π < θ ≤ π unless told otherwise).
- Vectors: accept either column or i, j, k notation; planes as r·n = c and Cartesian ax + by + cz = d.
- Sample means: X̄ ~ N(μ, σ²/n) for large n (CLT, n ≥ 30); CI x̄ ± z·s/√n with z = 1.645 / 1.960 / 2.576.
- Formula sheet reference: `<ROOT>\MAS\papers\2022_MAS_FormulaSheet.pdf` (identities, SHM, logistic, CLT).

## Explain mode

If the user asks how to solve a type of question (怎么做 / 解题思路 / 讲一下) rather than for new questions: answer from the methods note for that topic — identify the pattern, give the steps and the mark-earning lines, cite 1–2 past questions with their PDF pages — then offer a fresh practice question of that pattern.

<!-- blueprint:start (generated by tools/blueprint.py from wace.db — do not edit by hand) -->
## Paper blueprint (from the 2016–2025 papers)

Use this when writing a set or a mock paper: **randomise** (vary question count, marks per question, which patterns appear, and order within the difficulty ramp — never the same paper twice), but keep the **topic mark distribution** close to the real one below, and make the stated share of questions **cross-topic** (two topics in one question), using only pairings that real papers use.

### Calculator-free

- Questions per paper (2020–2025): 7–8; marks per question: 3–13 (median 5).
- Share of marks by topic: Integration techniques & applications 31%, Functions & sketching graphs 29%, Complex numbers 23%, Vectors in 3D, lines, planes, spheres, linear systems 14%, Rates of change & differential equations 3%.
- Cross-topic questions: 5% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Rates of change & differential equations** — 75% of its questions are cross-topic; pairs with Integration techniques & applications 100%, Functions & sketching graphs 67%.
  - **Integration techniques & applications** — 15% of its questions are cross-topic; pairs with Rates of change & differential equations 75%, Functions & sketching graphs 75%.
  - **Functions & sketching graphs** — 13% of its questions are cross-topic; pairs with Integration techniques & applications 100%, Rates of change & differential equations 67%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Complex numbers: `MAS.C.1` 3–7 (max 7), `MAS.C.2` 2–4 (max 5), `MAS.C.3` 5–6 (max 6), `MAS.C.4` 3 (max 3), `MAS.C.6` 2 (max 2), `MAS.C.8` 4 (max 6), `MAS.C.9` 3 (max 4)
  - Rates of change & differential equations: `MAS.DE.1` 4–5 (max 5)
  - Functions & sketching graphs: `MAS.F.1` 4–5 (max 7), `MAS.F.2` 2–5 (max 6), `MAS.F.3` 4–7 (max 7), `MAS.F.4` 2–5 (max 5), `MAS.F.5` 4–6 (max 6), `MAS.F.6` 2–6 (max 6)
  - Integration techniques & applications: `MAS.I.1` 4–5 (max 7), `MAS.I.2` 3–4 (max 5), `MAS.I.3` 5–7 (max 8), `MAS.I.4` 3–6 (max 6), `MAS.I.5` 3–5 (max 5)
  - Vectors in 3D, lines, planes, spheres, linear systems: `MAS.V.1` 6–7 (max 7), `MAS.V.2` 4–5 (max 5), `MAS.V.3` 3 (max 3), `MAS.V.4` 3 (max 3), `MAS.V.5` 3–5 (max 5)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `MAS.F.3` 100%, `MAS.F.4` 100%, `MAS.F.5` 100%, `MAS.F.6` 100%, `MAS.I.4` 100%, `MAS.I.5` 100%, `MAS.F.2` 67%, `MAS.DE.1` 50%, `MAS.V.5` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `MAS.F.3` 80%, `MAS.F.4` 80%, `MAS.F.6` 67%, `MAS.F.2` 56%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Rates of change & differential equations + Integration techniques & applications: `MAS.DE.1` Implicit Differentiation (tangents, horizontal points, second derivative) + `MAS.I.4` Area (integrating with respect to x or y) (2); `MAS.DE.1` Implicit Differentiation (tangents, horizontal points, second derivative) + `MAS.I.3` Partial fractions (1); `MAS.DE.1` Implicit Differentiation (tangents, horizontal points, second derivative) + `MAS.I.2` Integration after simplifying with trigonometric identities (CF 3–5 marks) (1)
  - Functions & sketching graphs + Integration techniques & applications: `MAS.F.2` Inverse functions (existence, expression, graph) + `MAS.I.3` Partial fractions (1); `MAS.F.4` Absolute value functions + `MAS.I.1` Definite integrals with a given substitution (1); `MAS.F.4` Absolute value functions + `MAS.I.4` Area (integrating with respect to x or y) (1); `MAS.F.2` Inverse functions (existence, expression, graph) + `MAS.I.4` Area (integrating with respect to x or y) (1)
  - Rates of change & differential equations + Functions & sketching graphs: `MAS.DE.1` Implicit Differentiation (tangents, horizontal points, second derivative) + `MAS.F.2` Inverse functions (existence, expression, graph) (2)

### Calculator-assumed

- Questions per paper (2020–2025): 10–13; marks per question: 3–16 (median 7).
- Share of marks by topic: Rates of change & differential equations 27%, Statistical inference (sample means) 20%, Complex numbers 16%, Vector calculus & motion 12%, Vectors in 3D, lines, planes, spheres, linear systems 11%, Integration techniques & applications 9%, Functions & sketching graphs 5%.
- Cross-topic questions: 15% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Integration techniques & applications** — 70% of its questions are cross-topic; pairs with Rates of change & differential equations 71%, Functions & sketching graphs 21%, Complex numbers 7%.
  - **Functions & sketching graphs** — 38% of its questions are cross-topic; pairs with Integration techniques & applications 100%.
  - **Rates of change & differential equations** — 30% of its questions are cross-topic; pairs with Integration techniques & applications 91%, Vectors in 3D, lines, planes, spheres, linear systems 9%.
  - **Vectors in 3D, lines, planes, spheres, linear systems** — 21% of its questions are cross-topic; pairs with Vector calculus & motion 67%, Rates of change & differential equations 33%.
  - **Vector calculus & motion** — 17% of its questions are cross-topic; pairs with Vectors in 3D, lines, planes, spheres, linear systems 100%.
  - **Complex numbers** — 5% of its questions are cross-topic; pairs with Integration techniques & applications 100%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Complex numbers: `MAS.C.1` 1–4 (max 4), `MAS.C.2` 4–6 (max 7), `MAS.C.3` 4 (max 4), `MAS.C.4` 3–6 (max 7), `MAS.C.5` 3–5 (max 6), `MAS.C.6` 2–4 (max 5), `MAS.C.7` 3 (max 3), `MAS.C.8` 5–6 (max 6), `MAS.C.9` 3–4 (max 4)
  - Rates of change & differential equations: `MAS.DE.1` 2–6 (max 8), `MAS.DE.2` 3–9 (max 16), `MAS.DE.3` 3–4 (max 5), `MAS.DE.4` 3–4 (max 9), `MAS.DE.5` 6–8 (max 8), `MAS.DE.6` 4–8 (max 8), `MAS.DE.7` 2–6 (max 9), `MAS.DE.8` 2–3 (max 3)
  - Functions & sketching graphs: `MAS.F.3` 4 (max 4), `MAS.F.4` 5–6 (max 6), `MAS.F.5` 3–5 (max 5)
  - Integration techniques & applications: `MAS.I.1` 5 (max 5), `MAS.I.3` 2 (max 2), `MAS.I.4` 3–5 (max 5), `MAS.I.5` 3–6 (max 7)
  - Statistical inference (sample means): `MAS.S.1` 5–7 (max 9), `MAS.S.2` 3–4 (max 4), `MAS.S.3` 2–5 (max 7), `MAS.S.4` 2–4 (max 6), `MAS.S.5` 4 (max 4), `MAS.S.6` 2 (max 2)
  - Vectors in 3D, lines, planes, spheres, linear systems: `MAS.V.1` 10 (max 10), `MAS.V.2` 3–6 (max 8), `MAS.V.3` 3–4 (max 5), `MAS.V.4` 3–6 (max 6), `MAS.V.5` 5–8 (max 8), `MAS.V.6` 3–7 (max 7)
  - Vector calculus & motion: `MAS.VC.1` 2–6 (max 9), `MAS.VC.2` 3–5 (max 5), `MAS.VC.3` 2–3 (max 3), `MAS.VC.4` 2–5 (max 5), `MAS.VC.5` 4 (max 4)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `MAS.C.1` 100%, `MAS.C.4` 100%, `MAS.C.5` 100%, `MAS.C.6` 100%, `MAS.C.7` 100%, `MAS.DE.1` 100%, `MAS.DE.3` 100%, `MAS.F.3` 100%, `MAS.F.4` 100%, `MAS.F.5` 100%, `MAS.I.4` 100%, `MAS.V.6` 100%, `MAS.VC.2` 100%, `MAS.VC.3` 100%, `MAS.VC.4` 100%, `MAS.VC.1` 91%, `MAS.DE.4` 78%, `MAS.I.5` 75%, `MAS.DE.5` 67%, `MAS.DE.8` 67%, `MAS.I.3` 67%, `MAS.DE.2` 50%, `MAS.I.1` 50%, `MAS.V.5` 50%, `MAS.VC.5` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `MAS.C.5` 80%, `MAS.C.4` 60%, `MAS.F.4` 60%, `MAS.DE.3` 50%, `MAS.DE.5` 50%, `MAS.F.3` 50%, `MAS.VC.1` 36%, `MAS.C.8` 25%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Rates of change & differential equations + Integration techniques & applications: `MAS.DE.1` Implicit Differentiation (tangents, horizontal points, second derivative) + `MAS.I.4` Area (integrating with respect to x or y) (3); `MAS.DE.2` Related Rates + `MAS.I.5` Volume of solids of revolution (3); `MAS.DE.1` Implicit Differentiation (tangents, horizontal points, second derivative) + `MAS.I.5` Volume of solids of revolution (2); `MAS.DE.5` Logistic Growth + `MAS.I.3` Partial fractions (2)
  - Functions & sketching graphs + Integration techniques & applications: `MAS.F.4` Absolute value functions + `MAS.I.1` Definite integrals with a given substitution (1); `MAS.F.5` Rational functions — determining parameters from a graph + `MAS.I.3` Partial fractions (1); `MAS.F.5` Rational functions — determining parameters from a graph + `MAS.I.4` Area (integrating with respect to x or y) (1); `MAS.F.4` Absolute value functions + `MAS.I.4` Area (integrating with respect to x or y) (1)
  - Vectors in 3D, lines, planes, spheres, linear systems + Vector calculus & motion: `MAS.V.3` Intersections, angles, closest point + `MAS.VC.1` Given r(t), find velocity, acceleration and speed (2); `MAS.V.3` Intersections, angles, closest point + `MAS.VC.5` Closest distance between objects moving in straight lines (3D) (2)
  - Rates of change & differential equations + Vectors in 3D, lines, planes, spheres, linear systems: `MAS.DE.2` Related Rates + `MAS.V.5` Vector proofs (appears in both CF and CA) (1)
  - Complex numbers + Integration techniques & applications: `MAS.C.3` Complex roots of polynomials (factor theorem + conjugate root theorem) + `MAS.I.4` Area (integrating with respect to x or y) (1)

<!-- blueprint:end -->
