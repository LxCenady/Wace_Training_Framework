---
name: wace-acf-questions
description: Generate original WACE Accounting and Finance ATAR (ACF, Units 3–4, syllabus 2026–2027) exam-style questions with marking keys written mark by mark, by topic (finance products and asset management, costing and variances, CVP and operating decisions, budgets and performance control, capital investment appraisal, the reporting framework, equity records, financial statements and adjustments, cash flow statements, ratios and reporting analysis, regulation/audit/ethics/sustainability), calibrated against the 2020–2025 papers. Use when the user asks for Accounting and Finance / ACF / 会计与金融 / 会计 practice questions, 出题, a topic quiz, or a mock section.
---

# WACE Accounting and Finance ATAR — topic question generator

## Locating `<ROOT>` (live path — never hard-code)

All paths below are relative to `<ROOT>`, the data folder that contains `ACF/`, `CHE/`, `MAA/`, `MAM/`, `MAS/`, `tools/` and `skills/`. Resolve it once per session, in this order:

1. Environment variable `WACE_MATHS_ROOT`, if set and it contains `ACF/`.
2. Walk up from this SKILL.md's real location: the first ancestor folder containing both `ACF/` and `CHE/` (the canonical copy lives at `<ROOT>/skills/wace-acf-questions/SKILL.md`, so normally two levels up).
3. Fallback `E:\WACE_Maths`. If none exists, ask the user where the folder is.

Python: `<ROOT>\.venv\Scripts\python.exe` if present, otherwise any Python 3. Checks use only the standard library (`fractions`, `decimal`). Write scratch scripts to the session scratchpad, not into the repo.

## Data status (checked 2026-10-15)

- **Pack**: `<ROOT>\ACF\pack.json`, version `2026.10.1`. Papers 2020–2025, shared paper layout, `key_style: description-marks`, `checker: none` (no automatic accounting answer checker exists; every number must be recomputed by hand).
- **Catalogue**: `<ROOT>\tools\catalogue_ACF.json`, 114 patterns in 12 topic codes. The file's `catalogue_status` says `approved`, but `<ROOT>\ACF\README.md` still lists catalogue approval, blind assignment review and installation parity as open gates. Treat pattern boundaries as provisional, and read each pattern's `not` field before using it near a boundary.
- **Pattern flags**: `examined: false` on CVP10, BUD12, RAT12, GOV10, GOV11, GOV12, OUT5, OUT6 (no past questions). `historical_only: true` on RAT12 and OUT1–OUT6. `diagnostic: false` on RAT12.
- **Method notes**: `<ROOT>\ACF\methods_en\NN_<Topic>_Methods.md` (English) with PDF twins. They are calibration sources only: read them for method and mark placement, quote nothing from them, and do not rely on them being complete.
- **Question bank**: `<ROOT>\ACF\questions.json`. Inspect its keys before use; do not assume a schema. The pack lists `papers.acknowledged["2021M-Q2"]`: that item was awarded to all candidates and must not be used as mastery evidence.
- **Source papers, keys and reports**: `<ROOT>\ACF\papers\` (exam, marking key, information booklet and specifications booklet for each year). Every year needs its own exam, key and applicable booklets. The 2026 booklet is comparison evidence only and never substitutes for a missing historical edition.
- **wace.db**: if `SELECT COUNT(*) FROM questions WHERE subject='ACF'` returns rows, use the CHE-style queries (`part_patterns`, `patterns`, `pattern_marks`, `points`). If it returns zero, use `ACF/questions.json` and the key PDFs instead.

## Topic files

Each topic has a guide in this skill's `topics/` folder. Read the guide before writing. Cite a topic only by its file name below.

| code | topic file | 中文 | patterns (examined) |
|---|---|---|---|
| FIN | `topics/01_Finance.md` | 融资、金融产品与资产管理 | 5 (5) |
| CST | `topics/02_Costing.md` | 成本核算与标准成本差异 | 13 (13) |
| CVP | `topics/03_CVP.md` | 本量利与经营决策 | 10 (9; CVP10 not examined) |
| BUD | `topics/04_Budgets.md` | 预算与绩效控制 | 12 (11; BUD12 not examined) |
| INV | `topics/05_Investment.md` | 资本投资评价 | 6 (6) |
| FRM | `topics/06_Framework.md` | 公司与财务报告概念框架 | 9 (9) |
| EQT | `topics/07_Equity.md` | 股本、股利与权益记录 | 8 (8) |
| STM | `topics/08_Statements.md` | 财务报表、调整与附注 | 9 (9) |
| CSH | `topics/09_Cash_Flow.md` | 现金流量表 | 12 (12) |
| RAT | `topics/10_Ratios.md` | 财务比率与报告分析 | 11 current (RAT12 is historical and cancelled, excluded) |
| GOV | `topics/11_Governance.md` | 监管、审计、伦理与可持续性 | 12 (9; GOV10–12 are current but unexamined) |
| OUT | `topics/12_Historical.md` | 现行大纲外的历史内容 | 6 historical only (default excluded) |

Pattern counts in the table are from the catalogue; the topic files hold the per-pattern detail. For `examined: false` patterns, present them as current syllabus content and do not invent past frequencies.

## Paper format (2020–2025 shared paper, mapped to 2026–2027)

- **Whole paper**: 10 minutes reading time, 180 minutes working time. Information booklet supplied; specifications booklet applies where the year's paper names it.
- **Section One: Multiple-choice**: 15% of the paper, suggested 25 minutes. Single answer, one mark per item. Write MC items with four options, one correct answer, and a one-line justification in the key.
- **Section Two: Short answer**: 70% of the paper, suggested 120 minutes. Several questions with lettered parts. Raw totals vary by year, so do not write a raw total as a constant.
- **Section Three: Extended answer**: 15% of the paper, suggested 35 minutes. Each extended-answer section supplies **two questions but the student answers ONE**. Write the set as two questions, and make the key and the attainable-mark plan assume one answer. Never present an average of the two alternatives as an individual's score.
- Question headers: `Question N (x marks)`. Parts `(a)`, `(b)`, with `(i)`, `(ii)` sub-parts. Parts sum to the question total.
- Weighted percentages use the section weights (15 / 70 / 15) and the question the student chose. Pooled raw marks across years are not a weighted examination percentage.

## Workflow

1. **Pin down the request.** Topic(s), number of questions, section (default: Section Two for single-concept parts; Section Three for multi-part business scenarios), difficulty (基础 / 中等 / 压轴 ≈ early / mid / last part), language (default English like the paper; explanations in Chinese if the user writes Chinese). State the defaults you used rather than asking.
2. **Apply the exclusion rules before selecting patterns** (see Exclusions below).
3. **Calibrate.** Read the topic file and the method note for the topic (`ACF\methods_en\`). Pick the pattern(s) to test; read each pattern's `not` field. Find 2–4 past parts that carry the same pattern (from the bank or wace.db) and read their stems. Do not copy or lightly reword any of them.
4. **Write original questions.** New company, new figures, new structure. Use Australian contexts and currently named standards (AASB, the conceptual framework, AASB S2 for climate disclosure). Use the exam voice: "Identify…", "Describe…", "Explain…", "Prepare…", "Calculate…", "Evaluate…", "Justify your choice…". Give every figure with its unit (AUD) and its date. Where a question asks for a chart or sketch (for example a break-even chart, a cash-flow timeline), state the required content in text and say a sketch is required; do not rely on a figure that is not provided.
5. **Write the marking key** in the description-marks format described under Conventions. One award per mark.
6. **Verify before showing.** Run every check below that applies, and report which ran (see Verification).
7. **Output.** Questions first, then a separator, then the key, so the user can attempt first. Use a clean table for journal entries and financial statements. After the key, one line per question: "最接近的真题: 2024 SA Q18 (ACF/questions.json; key ACF/papers/2024_ACF_MarkingKey.pdf)" when a real item is the closest match, or "最接近的真题: none in the bank" when none is. If the user wants a file, save to `<ROOT>\generated\ACF\<topic>_<YYYYMMDD>.md`.

## Exclusions and currency (hard rules)

- **OUT (topic 12) is excluded by default.** Generate OUT content only when the user explicitly asks for historical practice, and then label every item "historical — outside the current syllabus" in the stem's heading, never as current content.
- **RAT12 (the cancelled 2021 item, administrative credit) is never generated** in any mode. It carries no assessable EPS knowledge. Do not use the 2021 Section One Q2 as a worked example of earnings per share, and do not state that it demonstrates mastery.
- **GOV10–12 (climate risks and emissions scopes, AASB S2 disclosure pillars, sustainability claims) are current syllabus content and may be generated**, even though they are unexamined. Present them as current content without a frequency. Do not infer AASB S2 coverage from the superseded corporate social-disclosure requirements in OUT1.
- **Superseded terms**: the 2026–2027 syllabus prints the one-statement financial report title that the 2027 change summary replaces. Do not treat that as a removed concept. Prior Year 11 knowledge is not automatically excluded from the Year 12 course.
- **Unexamined patterns** (CVP10, BUD12, GOV10–12, OUT5–6): give current syllabus content and do not state a past mark value or frequency for them.

## Marking conventions (WACE style, mark by mark)

- **One award per mark.** Each mark in the key names one distinct, identifiable point. Do not give a mark for a restatement of the stem, and do not split one point into two marks.
- **Any-N lists are capped at N.** For "identify any three…", the key lists more than three acceptable responses, with the cap written in the key: "Any three of the following; maximum 3 marks." Count the accepted responses; do not award a mark for each distinct response beyond the cap.
- **Descriptor levels are not added up.** Where a part is marked by levels (for example a 4-mark "discuss" part with a level table), award the level that the response best fits. Do not add level marks across criteria. Put the level table in the key, and say the level is awarded as a whole.
- **Description required.** Where the pattern says "identify and describe", a bare label earns only the identification mark (for example a cash strategy named but not described earns 1 of 2). Write the description requirement in the key.
- **Follow-through does not require a correct earlier number.** A later mark can follow an earlier wrong value only where the method is correct and the response is consistent with the wrong value. Write this as "follow-through from the incorrect value in (a), provided the method is correct" in the key. Never write a key that makes a correct final figure depend on a correct intermediate figure.
- **Consequential errors**: say explicitly what gains credit when a value is carried forward. Where the question is a journal or statement table, award the table row marks by row ownership (the right line and column), and the debit and credit columns separately.
- **Equal mark totals do not fix criterion boundaries.** Two keys with the same total can split marks differently; write each boundary explicitly.
- **Alternative formats**: list "or" alternatives for equally acceptable answers, and "accept other relevant answers" only where the wording is genuinely open.
- **Calculations**: show the formula line, then the working, then the answer with units, to the precision the stem asks for. State the rounding rule in the stem if rounding matters.
- **Notes**: state any reduced maximum in a `Note:` line, for example "maximum 2 marks where the journal is not balanced".

## Verification (run and report honestly)

- **Balance check**: every journal entry has debits equal to credits; the trial balance and the statement of financial position balance (assets = liabilities + equity); the statement of comprehensive income reconciles to the change in retained earnings where the question gives both.
- **Totals check**: every subtotal and total in a statement, schedule, budget or variance table adds up; part marks sum to the question total; the section totals match the paper plan.
- **Recompute every number** with `fractions` or `decimal` at the precision the stem gives. Check each ratio, each variance (favourable or unfavourable sign stated), each cash-flow subtotal, and each NPV or payback figure against the stated discount rate and cash-flow timing.
- **Cash-flow sign check**: operating, investing and financing sections have the right signs and the closing cash equals opening cash plus net movement.
- **Mark totals check**: the sum of the key's marks equals the question's total; no mark is awarded for a point that was not asked.
- **Currency check**: no historical name, pattern or content in a current-content item (see Exclusions).
- **Report** as: "Verified: balance ✓, totals ✓, recompute ✓, cash-flow signs ✓, mark sum ✓, currency ✓" with any item not applicable marked as such. Do not claim a check that did not run. No automatic accounting checker exists, so say the arithmetic was checked by recomputation, not by a tool, unless a script actually ran.

## Mock section mode

If asked for a 模拟卷 or mock:
- Section One: 15% of the paper's marks, 25 minutes, written only if asked.
- Section Two: 70% of the paper's marks, 120 minutes, 6–8 questions with lettered parts.
- Section Three: 15% of the paper's marks, 35 minutes; two questions offered, student answers ONE.
Use the paper's total mark count from the year's exam header when one is given; do not assume a total the header does not state.
Weight topics by the pattern counts and the examined patterns (more weight on CST, CVP, STM, CSH and RAT, which carry the most examined patterns). Add GOV10–12 at a light weight as current content. Exclude OUT and RAT12. State the mock's total marks and the exclusions used.

## Explain mode

If the user asks how to solve a type of question (怎么做 / 解题思路 / 讲一下) rather than for new questions: answer from the topic file. Identify the pattern code, give the steps and the mark-earning lines, and cite one or two past items by year, section and question number (not by copying wording). Then offer a fresh practice question of that pattern. Do not explain RAT12 as worked EPS practice; say it was cancelled.

## Known caveats (keep generated keys honest)

- **2021 Section One Q2 (weighted-average shares)**: the key awards all candidates one mark because a date is missing. Do not use it as a model for an earnings-per-share item, and do not present its credit as evidence of mastery.
- **Any-N response counts are not attempts**: the number of accepted responses (for example ten accepted choices in one 2021 item) is capped at the stated N. The legacy fractional credit used in frequency tables is not a student's observed mastery.
- **Catalogue status**: the pattern descriptions are generator descriptions, not SCSA wording. Quote no key text; write keys from the rules above.
- **Quoting limit**: quote at most a short phrase (8 words or fewer) from any SCSA paper, key or report. Write everything else in your own words.
- **Unverified numbers**: where the bank or key is unclear, say so and leave the figure out rather than inventing a value.

<!-- blueprint:start (generated by tools/blueprint.py from wace.db — do not edit by hand) -->
## Paper blueprint (from the 2016–2025 papers)

Use this when writing a set or a mock paper: **randomise** (vary question count, marks per question, which patterns appear, and order within the difficulty ramp — never the same paper twice), but keep the **topic mark distribution** close to the real one below, and make the stated share of questions **cross-topic** (two topics in one question), using only pairings that real papers use.

### Multiple-choice

- Questions per paper (2020–2025): 15–15; marks per question: 1–1 (median 1).
- Share of marks by topic: Companies and the financial reporting framework 17%, Financial ratios and reporting analysis 17%, Regulation, audit, ethics and sustainability 14%, Finance products and asset management 12%, Budgets and performance control 9%, Costing and standard-cost variances 9%, Cost–volume–profit and operating decisions 7%, Statements of cash flows 4%, Share capital, dividends and equity records 4%, Capital investment appraisal 4%, Financial statements, adjustments and notes 2%.
- Cross-topic questions: 0% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):


- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Budgets and performance control: `ACF.BUD.1` 1 (max 1), `ACF.BUD.7` 1 (max 1), `ACF.BUD.8` 1 (max 1), `ACF.BUD.11` 1 (max 1)
  - Statements of cash flows: `ACF.CSH.1` 1 (max 1), `ACF.CSH.11` 1 (max 1), `ACF.CSH.12` 1 (max 1)
  - Costing and standard-cost variances: `ACF.CST.1` 1 (max 1), `ACF.CST.2` 1 (max 1), `ACF.CST.9` 1 (max 1), `ACF.CST.10` 1 (max 1), `ACF.CST.11` 1 (max 1)
  - Cost–volume–profit and operating decisions: `ACF.CVP.1` 1 (max 1), `ACF.CVP.4` 1 (max 1), `ACF.CVP.5` 1 (max 1), `ACF.CVP.9` 1 (max 1)
  - Share capital, dividends and equity records: `ACF.EQT.3` 1 (max 1), `ACF.EQT.5` 1 (max 1), `ACF.EQT.6` 1 (max 1), `ACF.EQT.7` 1 (max 1)
  - Finance products and asset management: `ACF.FIN.1` 1 (max 1), `ACF.FIN.2` 1 (max 1), `ACF.FIN.3` 1 (max 1)
  - Companies and the financial reporting framework: `ACF.FRM.1` 1 (max 1), `ACF.FRM.2` 1 (max 1), `ACF.FRM.3` 1 (max 1), `ACF.FRM.4` 1 (max 1), `ACF.FRM.5` 1 (max 1), `ACF.FRM.9` 1 (max 1)
  - Regulation, audit, ethics and sustainability: `ACF.GOV.1` 1 (max 1), `ACF.GOV.2` 1 (max 1), `ACF.GOV.4` 1 (max 1), `ACF.GOV.6` 1 (max 1)
  - Capital investment appraisal: `ACF.INV.2` 1 (max 1), `ACF.INV.6` 1 (max 1)
  - Financial ratios and reporting analysis: `ACF.RAT.1` 1 (max 1), `ACF.RAT.2` 1 (max 1), `ACF.RAT.3` 1 (max 1), `ACF.RAT.4` 1 (max 1), `ACF.RAT.5` 1 (max 1), `ACF.RAT.10` 1 (max 1)
  - Financial statements, adjustments and notes: `ACF.STM.9` 1 (max 1)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): none. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): `ACF.FRM.2` 50%. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:


### Short answer

- Questions per paper (2020–2025): 5–6; marks per question: 15–57 (median 27).
- Share of marks by topic: Budgets and performance control 15%, Costing and standard-cost variances 15%, Statements of cash flows 14%, Share capital, dividends and equity records 13%, Financial statements, adjustments and notes 12%, Capital investment appraisal 11%, Financial ratios and reporting analysis 8%, Cost–volume–profit and operating decisions 7%, Companies and the financial reporting framework 3%, Regulation, audit, ethics and sustainability 1%, Finance products and asset management 0%.
- Cross-topic questions: 36% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Financial statements, adjustments and notes** — 100% of its questions are cross-topic; pairs with Companies and the financial reporting framework 67%, Share capital, dividends and equity records 50%, Budgets and performance control 17%, Financial ratios and reporting analysis 17%, Statements of cash flows 17%.
  - **Companies and the financial reporting framework** — 100% of its questions are cross-topic; pairs with Financial statements, adjustments and notes 67%, Share capital, dividends and equity records 67%, Costing and standard-cost variances 17%, Cost–volume–profit and operating decisions 17%, Regulation, audit, ethics and sustainability 17%.
  - **Regulation, audit, ethics and sustainability** — 100% of its questions are cross-topic; pairs with Share capital, dividends and equity records 100%, Companies and the financial reporting framework 50%.
  - **Finance products and asset management** — 100% of its questions are cross-topic; pairs with Capital investment appraisal 100%.
  - **Share capital, dividends and equity records** — 86% of its questions are cross-topic; pairs with Companies and the financial reporting framework 67%, Financial statements, adjustments and notes 50%, Regulation, audit, ethics and sustainability 33%, Financial ratios and reporting analysis 17%.
  - **Financial ratios and reporting analysis** — 75% of its questions are cross-topic; pairs with Statements of cash flows 67%, Financial statements, adjustments and notes 33%, Share capital, dividends and equity records 33%.
  - **Statements of cash flows** — 40% of its questions are cross-topic; pairs with Financial ratios and reporting analysis 100%, Financial statements, adjustments and notes 50%.
  - **Cost–volume–profit and operating decisions** — 25% of its questions are cross-topic; pairs with Costing and standard-cost variances 100%, Companies and the financial reporting framework 100%.
  - **Capital investment appraisal** — 20% of its questions are cross-topic; pairs with Finance products and asset management 100%.
  - **Budgets and performance control** — 20% of its questions are cross-topic; pairs with Financial statements, adjustments and notes 100%.
  - **Costing and standard-cost variances** — 17% of its questions are cross-topic; pairs with Companies and the financial reporting framework 100%, Cost–volume–profit and operating decisions 100%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Budgets and performance control: `ACF.BUD.1` 3–4 (max 4), `ACF.BUD.2` 10–15 (max 15), `ACF.BUD.3` 4–6 (max 6), `ACF.BUD.4` 3–5 (max 5), `ACF.BUD.5` 3–5 (max 5), `ACF.BUD.6` 3–5 (max 5), `ACF.BUD.7` 8–25 (max 25), `ACF.BUD.9` 6 (max 6)
  - Statements of cash flows: `ACF.CSH.1` 6 (max 6), `ACF.CSH.2` 5 (max 5), `ACF.CSH.3` 5 (max 5), `ACF.CSH.4` 4–5 (max 5), `ACF.CSH.5` 4–5 (max 5), `ACF.CSH.6` 4 (max 4), `ACF.CSH.7` 4–5 (max 5), `ACF.CSH.8` 4–5 (max 5), `ACF.CSH.9` 4–5 (max 5), `ACF.CSH.10` 6 (max 6), `ACF.CSH.11` 2 (max 2), `ACF.CSH.12` 2 (max 2)
  - Costing and standard-cost variances: `ACF.CST.1` 3 (max 3), `ACF.CST.3` 3 (max 3), `ACF.CST.4` 2–3 (max 6), `ACF.CST.5` 2–3 (max 5), `ACF.CST.6` 2–3 (max 8), `ACF.CST.7` 2 (max 3), `ACF.CST.8` 2 (max 4), `ACF.CST.9` 2–4 (max 4), `ACF.CST.10` 4 (max 4), `ACF.CST.11` 4–5 (max 5), `ACF.CST.12` 4 (max 4), `ACF.CST.13` 4–5 (max 5)
  - Cost–volume–profit and operating decisions: `ACF.CVP.1` 2–4 (max 4), `ACF.CVP.2` 6–8 (max 8), `ACF.CVP.3` 4 (max 4), `ACF.CVP.4` 3 (max 3), `ACF.CVP.5` 2 (max 2), `ACF.CVP.6` 11 (max 11), `ACF.CVP.7` 9 (max 9), `ACF.CVP.8` 19 (max 19)
  - Share capital, dividends and equity records: `ACF.EQT.1` 5 (max 5), `ACF.EQT.2` 4–5 (max 5), `ACF.EQT.3` 4–10 (max 10), `ACF.EQT.4` 5–12 (max 12), `ACF.EQT.5` 3–7 (max 7), `ACF.EQT.6` 6 (max 6), `ACF.EQT.7` 5–12 (max 12), `ACF.EQT.8` 2–10 (max 10)
  - Finance products and asset management: `ACF.FIN.3` 4 (max 4)
  - Companies and the financial reporting framework: `ACF.FRM.1` 4–8 (max 8), `ACF.FRM.2` 2 (max 2), `ACF.FRM.5` 3 (max 3), `ACF.FRM.6` 6 (max 6), `ACF.FRM.8` 4 (max 4)
  - Regulation, audit, ethics and sustainability: `ACF.GOV.1` 3 (max 3), `ACF.GOV.2` 6 (max 6), `ACF.GOV.4` 4 (max 4)
  - Capital investment appraisal: `ACF.INV.1` 8–10 (max 10), `ACF.INV.2` 3–5 (max 5), `ACF.INV.3` 5–6 (max 6), `ACF.INV.4` 3–4 (max 13), `ACF.INV.5` 2–4 (max 4), `ACF.INV.6` 3 (max 3)
  - Financial ratios and reporting analysis: `ACF.RAT.1` 4 (max 4), `ACF.RAT.2` 5–8 (max 8), `ACF.RAT.3` 4 (max 4), `ACF.RAT.4` 3–5 (max 5), `ACF.RAT.5` 3–14 (max 14), `ACF.RAT.6` 4 (max 4), `ACF.RAT.7` 2–8 (max 8), `ACF.RAT.8` 3 (max 3), `ACF.RAT.9` 4 (max 4)
  - Financial statements, adjustments and notes: `ACF.STM.1` 3–5 (max 5), `ACF.STM.2` 5–7 (max 7), `ACF.STM.3` 7–9 (max 9), `ACF.STM.4` 4 (max 4), `ACF.STM.5` 4–7 (max 7), `ACF.STM.6` 4–8 (max 8), `ACF.STM.8` 4–10 (max 10), `ACF.STM.9` 4 (max 4)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `ACF.CST.10` 50%, `ACF.CST.11` 50%, `ACF.CST.12` 50%, `ACF.CST.13` 50%, `ACF.CST.4` 50%, `ACF.CST.5` 50%, `ACF.CST.6` 50%, `ACF.CST.7` 50%, `ACF.INV.5` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): none. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Share capital, dividends and equity records + Companies and the financial reporting framework: `ACF.EQT.2` Post share receipts and allotment in ledgers + `ACF.FRM.1` Explain company structures and capital-raising requirements (2); `ACF.EQT.3` Record and transfer share issue costs + `ACF.FRM.1` Explain company structures and capital-raising requirements (2); `ACF.EQT.2` Post share receipts and allotment in ledgers + `ACF.FRM.6` Explain the purposes of accounting standards (1); `ACF.EQT.3` Record and transfer share issue costs + `ACF.FRM.6` Explain the purposes of accounting standards (1)
  - Companies and the financial reporting framework + Financial statements, adjustments and notes: `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.STM.1` Prepare profit and comprehensive income (1); `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.STM.3` Calculate depreciation for the reporting period (1); `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.STM.4` Calculate doubtful debts through the allowance (1); `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.STM.5` Calculate income tax and after-tax profit (1)
  - Share capital, dividends and equity records + Financial statements, adjustments and notes: `ACF.EQT.2` Post share receipts and allotment in ledgers + `ACF.STM.1` Prepare profit and comprehensive income (1); `ACF.EQT.2` Post share receipts and allotment in ledgers + `ACF.STM.3` Calculate depreciation for the reporting period (1); `ACF.EQT.2` Post share receipts and allotment in ledgers + `ACF.STM.4` Calculate doubtful debts through the allowance (1); `ACF.EQT.2` Post share receipts and allotment in ledgers + `ACF.STM.5` Calculate income tax and after-tax profit (1)
  - Statements of cash flows + Financial ratios and reporting analysis: `ACF.CSH.5` Calculate interest received and paid + `ACF.RAT.2` Calculate and identify efficiency ratios (2); `ACF.CSH.5` Calculate interest received and paid + `ACF.RAT.4` Calculate and identify financial stability ratios (2); `ACF.CSH.5` Calculate interest received and paid + `ACF.RAT.3` Calculate and identify profitability ratios (1); `ACF.CSH.5` Calculate interest received and paid + `ACF.RAT.5` Calculate and identify market ratios (1)
  - Share capital, dividends and equity records + Regulation, audit, ethics and sustainability: `ACF.EQT.1` Journalise share applications and allotment + `ACF.GOV.1` Identify and explain reporting bodies (1); `ACF.EQT.1` Journalise share applications and allotment + `ACF.GOV.2` Apply director duties and shareholder rights (1); `ACF.EQT.3` Record and transfer share issue costs + `ACF.GOV.1` Identify and explain reporting bodies (1); `ACF.EQT.3` Record and transfer share issue costs + `ACF.GOV.2` Apply director duties and shareholder rights (1)
  - Budgets and performance control + Financial statements, adjustments and notes: `ACF.BUD.1` Explain master-budget components and purposes + `ACF.STM.3` Calculate depreciation for the reporting period (1); `ACF.BUD.1` Explain master-budget components and purposes + `ACF.STM.5` Calculate income tax and after-tax profit (1); `ACF.BUD.7` Prepare a budgeted income statement + `ACF.STM.3` Calculate depreciation for the reporting period (1); `ACF.BUD.7` Prepare a budgeted income statement + `ACF.STM.5` Calculate income tax and after-tax profit (1)
  - Statements of cash flows + Financial statements, adjustments and notes: `ACF.CSH.5` Calculate interest received and paid + `ACF.STM.5` Calculate income tax and after-tax profit (1); `ACF.CSH.9` Reconcile financing cash movements + `ACF.STM.5` Calculate income tax and after-tax profit (1)
  - Financial ratios and reporting analysis + Financial statements, adjustments and notes: `ACF.RAT.2` Calculate and identify efficiency ratios + `ACF.STM.5` Calculate income tax and after-tax profit (1); `ACF.RAT.3` Calculate and identify profitability ratios + `ACF.STM.5` Calculate income tax and after-tax profit (1); `ACF.RAT.4` Calculate and identify financial stability ratios + `ACF.STM.5` Calculate income tax and after-tax profit (1); `ACF.RAT.5` Calculate and identify market ratios + `ACF.STM.5` Calculate income tax and after-tax profit (1)
  - Costing and standard-cost variances + Cost–volume–profit and operating decisions: `ACF.CST.4` Calculate direct materials cost + `ACF.CVP.1` Calculate total, unit contribution and contribution ratio (1); `ACF.CST.5` Calculate direct labour cost + `ACF.CVP.1` Calculate total, unit contribution and contribution ratio (1); `ACF.CST.6` Determine manufacturing overhead and recovery rate + `ACF.CVP.1` Calculate total, unit contribution and contribution ratio (1); `ACF.CST.7` Apply overhead to a batch or unit + `ACF.CVP.1` Calculate total, unit contribution and contribution ratio (1)
  - Costing and standard-cost variances + Companies and the financial reporting framework: `ACF.CST.4` Calculate direct materials cost + `ACF.FRM.8` Compare internal and external reporting (1); `ACF.CST.5` Calculate direct labour cost + `ACF.FRM.8` Compare internal and external reporting (1); `ACF.CST.6` Determine manufacturing overhead and recovery rate + `ACF.FRM.8` Compare internal and external reporting (1); `ACF.CST.7` Apply overhead to a batch or unit + `ACF.FRM.8` Compare internal and external reporting (1)
  - Cost–volume–profit and operating decisions + Companies and the financial reporting framework: `ACF.CVP.1` Calculate total, unit contribution and contribution ratio + `ACF.FRM.8` Compare internal and external reporting (1)
  - Companies and the financial reporting framework + Regulation, audit, ethics and sustainability: `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.GOV.4` Explain external audit and stakeholder assurance (1)
  - Share capital, dividends and equity records + Financial ratios and reporting analysis: `ACF.EQT.7` Prepare the statement of changes in equity + `ACF.RAT.5` Calculate and identify market ratios (1); `ACF.EQT.7` Prepare the statement of changes in equity + `ACF.RAT.9` Evaluate investor appeal and profitability (1)
  - Finance products and asset management + Capital investment appraisal: `ACF.FIN.3` Apply principles of asset and funding management + `ACF.INV.1` Estimate relevant investment cash flows (1); `ACF.FIN.3` Apply principles of asset and funding management + `ACF.INV.3` Discount project cash flows and calculate NPV (1); `ACF.FIN.3` Apply principles of asset and funding management + `ACF.INV.4` Recommend an investment using appraisal results (1)

### Extended answer

- Questions per paper (2020–2025): 1–1; marks per question: 30–30 (median 30).
- Share of marks by topic: Regulation, audit, ethics and sustainability 29%, Companies and the financial reporting framework 21%, Budgets and performance control 15%, Financial ratios and reporting analysis 11%, Statements of cash flows 7%, Capital investment appraisal 5%, Finance products and asset management 4%, Costing and standard-cost variances 4%, Cost–volume–profit and operating decisions 2%, Financial statements, adjustments and notes 1%.
- Cross-topic questions: 100% of real questions combine two topics. How likely each topic is to pair, and with what (P(partner | topic) in real cross-topic questions):

  - **Companies and the financial reporting framework** — 100% of its questions are cross-topic; pairs with Regulation, audit, ethics and sustainability 71%, Budgets and performance control 57%, Financial ratios and reporting analysis 29%, Cost–volume–profit and operating decisions 14%, Costing and standard-cost variances 14%, Capital investment appraisal 14%.
  - **Budgets and performance control** — 100% of its questions are cross-topic; pairs with Regulation, audit, ethics and sustainability 100%, Companies and the financial reporting framework 67%, Cost–volume–profit and operating decisions 33%, Costing and standard-cost variances 33%, Financial ratios and reporting analysis 17%.
  - **Cost–volume–profit and operating decisions** — 100% of its questions are cross-topic; pairs with Budgets and performance control 100%, Regulation, audit, ethics and sustainability 100%, Companies and the financial reporting framework 50%, Costing and standard-cost variances 50%.
  - **Regulation, audit, ethics and sustainability** — 100% of its questions are cross-topic; pairs with Budgets and performance control 75%, Companies and the financial reporting framework 62%, Costing and standard-cost variances 38%, Cost–volume–profit and operating decisions 25%, Financial ratios and reporting analysis 12%, Finance products and asset management 12%, Financial statements, adjustments and notes 12%.
  - **Financial ratios and reporting analysis** — 100% of its questions are cross-topic; pairs with Companies and the financial reporting framework 50%, Statements of cash flows 50%, Regulation, audit, ethics and sustainability 25%, Budgets and performance control 25%, Capital investment appraisal 25%, Finance products and asset management 25%.
  - **Costing and standard-cost variances** — 100% of its questions are cross-topic; pairs with Regulation, audit, ethics and sustainability 100%, Budgets and performance control 67%, Companies and the financial reporting framework 33%, Cost–volume–profit and operating decisions 33%.
  - **Capital investment appraisal** — 100% of its questions are cross-topic; pairs with Finance products and asset management 50%, Financial ratios and reporting analysis 50%, Statements of cash flows 50%, Companies and the financial reporting framework 50%.
  - **Finance products and asset management** — 100% of its questions are cross-topic; pairs with Capital investment appraisal 50%, Financial ratios and reporting analysis 50%, Statements of cash flows 50%, Regulation, audit, ethics and sustainability 50%, Financial statements, adjustments and notes 50%.
  - **Statements of cash flows** — 100% of its questions are cross-topic; pairs with Financial ratios and reporting analysis 100%, Capital investment appraisal 50%, Finance products and asset management 50%.
  - **Financial statements, adjustments and notes** — 100% of its questions are cross-topic; pairs with Finance products and asset management 100%, Regulation, audit, ethics and sustainability 100%.

- **Marks one pattern carries within a question** (middle half of real questions, and the largest seen). A question is the sum of its patterns' parts: a 10-mark question is three or four patterns' parts, or one pattern that real papers really do run that long — never one routine step inflated to fill the marks:

  - Budgets and performance control: `ACF.BUD.1` 6 (max 6), `ACF.BUD.8` 10 (max 10), `ACF.BUD.10` 4–8 (max 8), `ACF.BUD.11` 2–8 (max 8)
  - Statements of cash flows: `ACF.CSH.1` 5 (max 5), `ACF.CSH.11` 8 (max 8), `ACF.CSH.12` 11 (max 11)
  - Costing and standard-cost variances: `ACF.CST.1` 7 (max 7), `ACF.CST.2` 4 (max 4), `ACF.CST.9` 5 (max 5)
  - Cost–volume–profit and operating decisions: `ACF.CVP.9` 3–4 (max 4)
  - Finance products and asset management: `ACF.FIN.2` 6 (max 6), `ACF.FIN.4` 4 (max 4), `ACF.FIN.5` 4 (max 4)
  - Companies and the financial reporting framework: `ACF.FRM.1` 4–8 (max 8), `ACF.FRM.2` 6 (max 6), `ACF.FRM.3` 3–8 (max 8), `ACF.FRM.4` 2 (max 2), `ACF.FRM.6` 9–10 (max 10), `ACF.FRM.7` 6–11 (max 11), `ACF.FRM.9` 4 (max 4)
  - Regulation, audit, ethics and sustainability: `ACF.GOV.1` 4–6 (max 6), `ACF.GOV.2` 6–10 (max 10), `ACF.GOV.3` 4–9 (max 9), `ACF.GOV.4` 4–7 (max 7), `ACF.GOV.5` 6–9 (max 9), `ACF.GOV.6` 4 (max 4), `ACF.GOV.7` 3–4 (max 4), `ACF.GOV.8` 3–4 (max 4), `ACF.GOV.9` 3–4 (max 4)
  - Capital investment appraisal: `ACF.INV.4` 3 (max 3), `ACF.INV.5` 4 (max 4), `ACF.INV.6` 4 (max 4)
  - Financial ratios and reporting analysis: `ACF.RAT.6` 3 (max 3), `ACF.RAT.7` 7–8 (max 8), `ACF.RAT.8` 3 (max 3), `ACF.RAT.11` 7–11 (max 11)
  - Financial statements, adjustments and notes: `ACF.STM.7` 4 (max 4)

- **Figures and drawing parts.** Patterns whose real questions usually show a figure (share of questions): `ACF.FRM.7` 50%, `ACF.OUT.1` 50%, `ACF.RAT.7` 50%. Patterns whose real questions often ask the student to draw — sketch a graph, draw a solution curve on a slope field, shade a region, plot on an Argand diagram, mark a point (share of questions): none. Give these a figure (the axes or diagram the student works on) and, about as often as real papers do, a drawing part whose marks reward visible features; put the completed drawing in the marking key.

- Tag combinations real questions used (pattern codes, count), by topic pair — combine patterns like these; other patterns of the same two topics are fine when the pairing is natural:

  - Budgets and performance control + Regulation, audit, ethics and sustainability: `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.GOV.5` Evaluate ethical financial conduct (2); `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.GOV.7` Explain voluntary administration (2); `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.GOV.1` Identify and explain reporting bodies (1); `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.GOV.3` Explain internal audit and control responses (1)
  - Companies and the financial reporting framework + Regulation, audit, ethics and sustainability: `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.GOV.2` Apply director duties and shareholder rights (2); `ACF.FRM.7` Explain the accountant role in business operations + `ACF.GOV.1` Identify and explain reporting bodies (1); `ACF.FRM.7` Explain the accountant role in business operations + `ACF.GOV.5` Evaluate ethical financial conduct (1); `ACF.FRM.9` Distinguish cash and accrual accounting + `ACF.GOV.3` Explain internal audit and control responses (1)
  - Budgets and performance control + Companies and the financial reporting framework: `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.FRM.7` Explain the accountant role in business operations (1); `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.FRM.9` Distinguish cash and accrual accounting (1); `ACF.BUD.8` Interpret performance reports and budget variances + `ACF.FRM.9` Distinguish cash and accrual accounting (1); `ACF.BUD.1` Explain master-budget components and purposes + `ACF.FRM.1` Explain company structures and capital-raising requirements (1)
  - Costing and standard-cost variances + Regulation, audit, ethics and sustainability: `ACF.CST.9` Use and explain cost mark-up pricing + `ACF.GOV.2` Apply director duties and shareholder rights (1); `ACF.CST.9` Use and explain cost mark-up pricing + `ACF.GOV.4` Explain external audit and stakeholder assurance (1); `ACF.CST.1` Classify direct, indirect, product and period costs + `ACF.GOV.2` Apply director duties and shareholder rights (1); `ACF.CST.2` Explain fixed and variable cost behaviour + `ACF.GOV.4` Explain external audit and stakeholder assurance (1)
  - Budgets and performance control + Cost–volume–profit and operating decisions: `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.CVP.9` Explain cost-volume-profit changes (2); `ACF.BUD.1` Explain master-budget components and purposes + `ACF.CVP.9` Explain cost-volume-profit changes (1)
  - Cost–volume–profit and operating decisions + Regulation, audit, ethics and sustainability: `ACF.CVP.9` Explain cost-volume-profit changes + `ACF.GOV.1` Identify and explain reporting bodies (1); `ACF.CVP.9` Explain cost-volume-profit changes + `ACF.GOV.5` Evaluate ethical financial conduct (1); `ACF.CVP.9` Explain cost-volume-profit changes + `ACF.GOV.4` Explain external audit and stakeholder assurance (1); `ACF.CVP.9` Explain cost-volume-profit changes + `ACF.GOV.7` Explain voluntary administration (1)
  - Companies and the financial reporting framework + Financial ratios and reporting analysis: `ACF.FRM.9` Distinguish cash and accrual accounting + `ACF.RAT.6` Interpret liquidity and cash constraints (1); `ACF.FRM.9` Distinguish cash and accrual accounting + `ACF.RAT.8` Interpret financial stability and financing risk (1); `ACF.FRM.7` Explain the accountant role in business operations + `ACF.RAT.11` Explain limitations of financial analysis (1); `ACF.FRM.7` Explain the accountant role in business operations + `ACF.RAT.7` Interpret efficiency and recommend management action (1)
  - Budgets and performance control + Costing and standard-cost variances: `ACF.BUD.11` Apply cost leadership and differentiation strategies + `ACF.CST.9` Use and explain cost mark-up pricing (1); `ACF.BUD.1` Explain master-budget components and purposes + `ACF.CST.2` Explain fixed and variable cost behaviour (1); `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.CST.2` Explain fixed and variable cost behaviour (1)
  - Statements of cash flows + Financial ratios and reporting analysis: `ACF.CSH.11` Explain the benefits of cash-flow information + `ACF.RAT.11` Explain limitations of financial analysis (1); `ACF.CSH.1` Explain cash and cash equivalents + `ACF.RAT.11` Explain limitations of financial analysis (1); `ACF.CSH.1` Explain cash and cash equivalents + `ACF.RAT.7` Interpret efficiency and recommend management action (1); `ACF.CSH.12` Interpret cash-flow categories and business implications + `ACF.RAT.11` Explain limitations of financial analysis (1)
  - Cost–volume–profit and operating decisions + Companies and the financial reporting framework: `ACF.CVP.9` Explain cost-volume-profit changes + `ACF.FRM.7` Explain the accountant role in business operations (1)
  - Budgets and performance control + Financial ratios and reporting analysis: `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.RAT.6` Interpret liquidity and cash constraints (1); `ACF.BUD.10` Evaluate business planning and stakeholder consequences + `ACF.RAT.8` Interpret financial stability and financing risk (1); `ACF.BUD.8` Interpret performance reports and budget variances + `ACF.RAT.6` Interpret liquidity and cash constraints (1); `ACF.BUD.8` Interpret performance reports and budget variances + `ACF.RAT.8` Interpret financial stability and financing risk (1)
  - Regulation, audit, ethics and sustainability + Financial ratios and reporting analysis: `ACF.GOV.3` Explain internal audit and control responses + `ACF.RAT.6` Interpret liquidity and cash constraints (1); `ACF.GOV.3` Explain internal audit and control responses + `ACF.RAT.8` Interpret financial stability and financing risk (1)
  - Costing and standard-cost variances + Companies and the financial reporting framework: `ACF.CST.1` Classify direct, indirect, product and period costs + `ACF.FRM.1` Explain company structures and capital-raising requirements (1); `ACF.CST.1` Classify direct, indirect, product and period costs + `ACF.FRM.6` Explain the purposes of accounting standards (1)
  - Statements of cash flows + Finance products and asset management: `ACF.CSH.11` Explain the benefits of cash-flow information + `ACF.FIN.2` Classify and select financing products (1)
  - Statements of cash flows + Capital investment appraisal: `ACF.CSH.11` Explain the benefits of cash-flow information + `ACF.INV.4` Recommend an investment using appraisal results (1); `ACF.CSH.11` Explain the benefits of cash-flow information + `ACF.INV.5` Evaluate non-financial investment factors (1)
  - Finance products and asset management + Capital investment appraisal: `ACF.FIN.2` Classify and select financing products + `ACF.INV.4` Recommend an investment using appraisal results (1); `ACF.FIN.2` Classify and select financing products + `ACF.INV.5` Evaluate non-financial investment factors (1)
  - Finance products and asset management + Financial ratios and reporting analysis: `ACF.FIN.2` Classify and select financing products + `ACF.RAT.11` Explain limitations of financial analysis (1)
  - Capital investment appraisal + Financial ratios and reporting analysis: `ACF.INV.4` Recommend an investment using appraisal results + `ACF.RAT.11` Explain limitations of financial analysis (1); `ACF.INV.5` Evaluate non-financial investment factors + `ACF.RAT.11` Explain limitations of financial analysis (1)
  - Costing and standard-cost variances + Cost–volume–profit and operating decisions: `ACF.CST.2` Explain fixed and variable cost behaviour + `ACF.CVP.9` Explain cost-volume-profit changes (1)
  - Finance products and asset management + Regulation, audit, ethics and sustainability: `ACF.FIN.4` Explain cash requirements for business viability + `ACF.GOV.1` Identify and explain reporting bodies (1); `ACF.FIN.4` Explain cash requirements for business viability + `ACF.GOV.3` Explain internal audit and control responses (1); `ACF.FIN.4` Explain cash requirements for business viability + `ACF.GOV.8` Explain receivership (1); `ACF.FIN.4` Explain cash requirements for business viability + `ACF.GOV.9` Explain liquidation (1)
  - Finance products and asset management + Financial statements, adjustments and notes: `ACF.FIN.4` Explain cash requirements for business viability + `ACF.STM.7` Identify and explain financial statements (1); `ACF.FIN.5` Recommend cash-management controls + `ACF.STM.7` Identify and explain financial statements (1)
  - Regulation, audit, ethics and sustainability + Financial statements, adjustments and notes: `ACF.GOV.1` Identify and explain reporting bodies + `ACF.STM.7` Identify and explain financial statements (1); `ACF.GOV.3` Explain internal audit and control responses + `ACF.STM.7` Identify and explain financial statements (1); `ACF.GOV.8` Explain receivership + `ACF.STM.7` Identify and explain financial statements (1); `ACF.GOV.9` Explain liquidation + `ACF.STM.7` Identify and explain financial statements (1)
  - Companies and the financial reporting framework + Capital investment appraisal: `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.INV.5` Evaluate non-financial investment factors (1); `ACF.FRM.1` Explain company structures and capital-raising requirements + `ACF.INV.6` Explain capital investment and time value of money (1); `ACF.FRM.2` Explain company formation and internal rules + `ACF.INV.5` Evaluate non-financial investment factors (1); `ACF.FRM.2` Explain company formation and internal rules + `ACF.INV.6` Explain capital investment and time value of money (1)

<!-- blueprint:end -->
