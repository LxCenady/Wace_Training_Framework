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
