# MAA Solution Notes · Independent Review Record

**Review method**: Six sets of notes were drafted by three writing subagents (Haiku 5.5) using the evidence packs in `evidence/maa/notes/`; they were then checked item by item by two independent review subagents (Haiku 5.5, not involved in writing, fresh context) against the original papers, marking key PDF pages (key sections rendered as images for checking) and the 2016–2025 exam reports, with factual errors corrected directly. Items with insufficient evidence were kept as “pending review”. Issues with the labels themselves were recorded only as suggestions; labels were not changed. The lead agent (Claude Opus 5.5) checked the structure (the pattern numbering in each set of notes corresponds one-to-one with `tools/catalogue_MAA.json`) and copyright (no verbatim overlap of more than 12 words with the evidence packs), and spot-read the content.

**Scope note**: There is no usable marking key for 2019, so it is not included in the basis. Labels are draft (some reviewed by the lead agent); see `MAA/README.md`.

---


**Reviewer**: Haiku 5.5 (claude-haiku-5-5). Worked with independent context; did not take part in writing.
**Scope**: `01_Bivariate_Data_解题思路.md` (BIV), `02_Sequences_解题思路.md` (SEQ), `03_Graphs_Networks_解题思路.md` (GRF). Only these three sets of notes were changed; labels, catalogue, `tools/`, and `questions.json` were not changed.

**Basis**: Original papers and marking key PDFs (read with pymupdf; key sections rendered as PNGs, see `evidence/maa/review/`); full text of the 2016–2025 exam reports; `evidence/maa/labels.json`.

**Checking method**:
- Mechanical check: Every question-number reference in the three sets of notes (BIV 280, SEQ 178, GRF 180, including repeated occurrences) can be found in `labels.json`, the sub-question exists, and the label code matches the pattern it appears in. Except for noted cross-references, there were no mismatches.
- Bidirectional check: Each pattern’s “exam questions” list corresponds one-to-one with the set of sub-questions for that code in the label database, completely consistent in both directions; the “N sub-questions in total” numbers match the label counts (BIV 26 questions, 173 sub-questions; SEQ 23 questions, 101 sub-questions; GRF 23 questions, 91 sub-questions after de-duplication).
- Manual spot checks: marking points, key wording, numerical calculations, report quotations. Across the three sets, about 145 items (BIV about 58, SEQ about 37, GRF about 50), estimated at more than 30% of the other factual statements in each file.
- Numerical verification: Checked with Python iteration and equation solving (see individual entries).

**Handling principles**: High-severity items were changed only after returning to the original paper/key wording to verify. Anything that could be calculated was calculated. Label issues were written only into “Labelling suggestions”; labels were not changed.

---

## 01 Bivariate Data Analysis (BIV)

| # | Severity | Location | Issue | Evidence | Action |
|---|---|---|---|---|---|
| 1 | Medium | Pattern 1 Step 3 | The item “if the explanatory variable is in the rows, use row percentages” was marked as pending review, on the grounds that “the explanatory variable was not checked question by question” | Explanatory variables and key determinations checked question by question: 2017F-Q5(b) (key p10, age) and (c) (p11, row percentages); 2022F-Q3(b) (p5, age) and (c)(ii) (p6, row percentages); 2021F-Q4(b) (p8, response variable opinion, so age is the explanatory variable) and (c) (p8, row percentages); 2023F-Q1(b) (p2, response variable category, so age is the explanatory variable) and (c)(i) (p3, row percentages); 2024F-Q2(b)(i) (p4, purchase price precedes complaint) and (c)(i) (p5, column percentages) | Accepted: the determinations for the five percentage tables agree with the explanatory variables; removed pending review; wrote the basis in the text |
| 2 | Medium | Pattern 12 exam questions | 2018A-Q10(c) has only BIV12; pending review whether to add BIV2 | key p6: 1 mark, the conclusion is that passenger car sales were always greater than sports car sales; this is a quantity comparison and does not involve percentages. Catalogue BIV12 note: if the question explicitly discusses association, label BIV2 as well | Partly accepted: notes clarify that this sub-question is not a rate comparison; adding BIV2 is listed as labelling suggestion T1. Label not changed; kept as pending review |
| 3 | Low | Pattern 13 exam questions | 2016A-Q11(e) marked as pending review, “calculation subject to key” | key p13 (rendered `2016A_Q11e_key.png`): 61.4/100 × Total = 1449.6 (thousands), Total = 2360.912 thousand, i.e. about 2 360 912 people, about 2.36 million. The question table notes the unit is “thousands” | Accepted: verified, removed pending review, wrote in the calculation |
| 4 | Low | Marking panel reminder item 1 | “All numerical calculations in the CA paper are done with a calculator” was written as a rule, but the 2025 report is encouraging advice | 2025 report p2 advice for teachers: encourages using a calculator for all numerical calculations in the CA section | Accepted: changed to “suggested” |
| 5 | Low | Pattern 7 steps | Numbering “2.Interpret” is non-standard | — | Accepted: changed to “2. Interpret” |
| 6 | Low | File header | ★ is undefined; review status still says “draft, not yet reviewed” | — | Accepted: added ★ definition (roughly the top quarter; for this topic, Patterns 1, 4, 5, 8; checked against INDEX marks 46, 43, 38, 27); updated status |
| 7 | Low | Pattern 4, Pattern 16 | 2023A-Q7(d) (label BIV3) appears as a strength example in Pattern 4; 2021F-Q7(d) (label BIV4) appears in Pattern 16 common errors | 2023A-Q7(d) key p3: r = 0.814, strong positive (content true); 2021F-Q7(d) key p15: r = 0.42, low correlation, used to support “the model is not appropriate” (content true). Both are cross-references | Rejected (no change): cross-references, not an error |

**Summary (BIV)**: About 58 items spot-checked, 280 references checked mechanically (0 missing), exam-question lists bidirectionally checked across all 16 patterns and all consistent. Factual errors corrected: 0; wording and formatting corrections: 3 (#4, #5, #6). Originally 3 pending-review items: 2 resolved (#1, #3), 1 still pending review (#2, a labelling issue).

---

## 02 Sequences: Growth and Decay (SEQ)

| # | Severity | Location | Issue | Evidence | Action |
|---|---|---|---|---|---|
| 1 | High | Pattern 7 pending-review section (original text “pending review: 2018A-Q9(c)…”) | “42 and 27 are inconsistent” was caused by the notes themselves: pairing (c) with the N model (0.8). (c) uses the M model from the start of the question stem (0.9); steady state M = 42, correct; the N model steady state 27 appears in (d)(ii), and the key also writes 27 | Original paper 2018 CalcAssumed p6 (rendered `2018A_Q9_stem_p6.png`) and p7 (`2018A_Q9_N_model_p7.png`): the two recurrence relations are clear; text extraction has no garbled text. key p4: (c) is 42; key p5: (d)(ii) is 27, (e) is k = 14. Verification: 0.1M = 4.2 ⇒ M = 42; 0.2N = 5.4 ⇒ N = 27 | Accepted: resolved, removed pending review, rewrote as the steady state of each of the two models |
| 2 | High | Pattern 6 marking points | The notes say the term-by-term values in 2018A-Q9(b) are “correct”, but the fifth week from the recurrence relation in the question stem is 47.249 (rounded about 47), while the key text answers 48 | key p4 (rendered `2018A_Q9b_key_p4.png`): the key’s own CAS table has 47.249 in row 5, but the written answer says 48. Iteration check: M4 = 47.832, M5 = 47.249 | Partly accepted: removed the “correct” attribution for this sub-question; the notes use 47 as the value; the key’s 48 is recorded as observation O1; key not changed |
| 3 | Medium | Pattern 8 pending-review section; Pattern 6 exam-question parenthetical note | b in 2024A-Q7(e) was marked as pending review, and the units of a and b were not made clear | key p5: a = 0.986, b = 100; the unit of T in the question stem is thousands, and “100 000 people per week” corresponds to b = 100 (thousands) | Accepted: resolved, both pending-review notes removed, sources of a and b written out |
| 4 | Medium | Pattern 5 note (2022A-Q9(a)) | Wording of the alternative argument was pending review | 2022 CalcAssumed key p3: the main solution treats it as 14% per week (r = 0.86, initial value 1200); the alternative solution points out that if it were per year, the formula would represent n years. The question stem says “decreases by 14% per year” but asks for n weeks | Accepted: verified, removed pending review, wrote out the difference between the question stem and the key’s main solution |
| 5 | Low | Pattern 8 Step 3 | 2024A-Q7(f)(i) is used as an example of “interpreting a coefficient”, but the label only has SEQ5 | key p5: interpreting 0.99 as a 1% cancellation rate belongs to the Pattern 8 “interpret coefficient” operation | Label not changed; noted in the notes and listed as labelling suggestion T4 |
| 6 | Low | File header | ★ is undefined; review status outdated | According to INDEX marks, SEQ5 = 75, SEQ2 = 45, the rest no more than 22; roughly the top quarter are Patterns 2, 5 | Accepted: added ★ definition, updated status |

**Summary (SEQ)**: About 37 items spot-checked, 178 references checked mechanically (0 missing; the cross-reference from Pattern 6 to Pattern 8, 2025A-Q6(f), is not counted). Factual errors corrected: 2 (#1 pairing, #2 attribution of term-by-term correctness); wording and formatting corrections: 1 (#6). All 3 original pending-review items (2024A-Q7(e) marked in two places) were resolved; 0 still pending review.

---

## 03 Graphs and Networks (GRF)

| # | Severity | Location | Issue | Evidence | Action |
|---|---|---|---|---|---|
| 1 | High | File header ★ note | “GRF3, GRF1, GRF5 tied for highest” is inaccurate: GRF3 is first with 29 marks; GRF1 and GRF5 are tied with 28 marks | INDEX.md marks: GRF3 29, GRF1 28, GRF5 28, GRF4 25 | Accepted: rewrite as GRF3 first, GRF1 and GRF5 tied |
| 2 | High | Pattern 4 Step 5 | The stopover question is mis-cited as 2025F-Q3(c); the stopover question is (d) | 2025 CalcFree key p7: (c) is the 15-minute shortest route ABHJK; (d) is the K→B route via F, KJEDFDCB, travel time 28 minutes, plus 45-minute stop = 73 minutes | Accepted: change to (d), write out the calculation, remove pending review |
| 3 | Medium | Pattern 4 marking points | 2020A-Q13(c) is written as “compare the length of the original route A–C–H”; the key compares A–C–H via the new road CH with the original shortest route ACFH (44 km) | 2020 CalcAssumed key p15: (b) is ACFH, 44 km; (c) bounds are that the reduction is greater than 4 and less than 26 | Accepted: rewrite, add the numerical bounds, remove pending review |
| 4 | Medium | Pattern 1 common error | The claim that “the 2024F-Q5(a)(ii) question stem and key do not correspond” does not hold: the stem asks for the additional implication of planarity, and the key answers “connected”, which is exactly the precondition for Euler’s formula to hold | 2024 CalcFree key p12 | Accepted: rephrase, remove pending review |
| 5 | Low | Pattern 3 | The wording “the author independently verifies from the question stem” is inappropriate; the data in that example is the given information for 2017F-Q3(a)(i) (5 faces, 5 vertices) | 2017 CalcFree p7 | Accepted |
| 6 | Medium | Pattern 5 Step 5 | The answer for 2021F-Q3(c) is not written, only “refer to key (pending review)” | 2021 CalcFree key p6: semi-Eulerian trail | Accepted: write out the answer, remove pending review |
| 7 | Medium | Pattern 6 marking points | The two properties in 2016A-Q14(c) are not written out, only “refer to key” | 2016 CalcAssumed key p17: each vertex is visited only once (except the start/end vertices); the start and end vertices are the same (closed) | Accepted: write out the two properties, remove pending review |
| 8 | High | Pattern 9 whole section | The definition in Pattern 9 is “allows repeated visits to vertices”, but the key routes for 2020A-Q13(a) and 2022A-Q10(b)(ii) do not repeat vertices: the former is a Hamiltonian path, and the latter is a Hamiltonian cycle. Only 2017F-Q6(a) explicitly allows repetition in its question stem | 2020 CalcAssumed key p14: ADCBEGHF, 70 km; 2022 CalcAssumed key p7: CBAGHFEDC, 47, i.e. 4700 m | Partially accepted: state the actual properties of the two sub-questions in the body, and keep pending review; label suggestions see T2, T3, labels unchanged |
| 9 | Low | Pattern 9 marking points | 2022A-Q10(b)(ii) lists only length and distance, omitting the route item | 2022 CalcAssumed key p7: three items worth 1 mark each (route starts and ends at C and passes through all vertices, length, distance) | Accepted: complete as three items |
| 10 | Low | Pending review items section | The list is outdated and still keeps resolved items in it | — | Accepted: rewrite as the 2 items still pending review, and list the 5 resolved items |

**Reviewed labels confirmed correct** (no change needed): 2017F-Q6(a) GRF9; 2016A-Q14(c) GRF6; 2021F-Q3(c) GRF5; 2025F-Q3(c)(d) GRF4; 2020A-Q13(c) GRF4; 2024F-Q5(c) GRF6 (key p13: closed path, each vertex once).

**Summary (GRF)**: About 50 items sampled, 180 citations mechanically checked (0 missing). 4 false GRF9 reports appeared in the “Pending review items” section; this is a section attribution issue, not real citations. 4 factual or quotation errors corrected (#1, #2, #3, #4); 4 wording and completion items (#5, #7, #9, #10); 1 Pattern 9 definition issue (#8, partially accepted). Original pending review: 6 items; 5 resolved (2024F-Q5(a)(ii), 2025F-Q3(d), 2020A-Q13(c), 2021F-Q3(c), 2016A-Q14(c)), 1 still pending review (2020A-Q13(a), label issue). Also, because of the Pattern 9 label issue, this review adds 1 new pending review item (2022A-Q10(b)(ii), also a label issue).

---

## Labelling suggestions (not modified)

| # | Sub-question | Current label | Suggestion | Rationale |
|---|---|---|---|---|
| T1 | 2018A-Q10(c) | BIV12 | Add BIV2 | key p6 requires describing association; catalogue BIV12 note: when a question explicitly discusses association, also label BIV2 |
| T2 | 2020A-Q13(a) | GRF9 | Change to GRF6 (Hamiltonian path); add GRF4 to the length part | key p14–15: ADCBEGHF, does not repeat vertices; GRF9 is defined as allowing repetition |
| T3 | 2022A-Q10(b)(ii) | GRF9 | Change to GRF6 (Hamiltonian cycle); add GRF4 to shortest length | key p7: CBAGHFEDC, does not repeat vertices |
| T4 | 2024A-Q7(f)(i) | SEQ5 | Add SEQ8 | key p5: explain the contextual meaning of the coefficient 0.99, consistent with Pattern 8 “interpret coefficient” |
| T5 | 2024F-Q5(a)(ii) | GRF1 | Consider adding GRF3 (asks about the additional implication of planarity, related to the precondition for Euler’s formula). Low confidence, left to the labeller’s discretion | key p12: answer is connected |

Labels confirmed correct and needing no change are shown in the GRF summary above.

---

## Observations (data issues, not in the notes, not modified)

| # | Location | Observation |
|---|---|---|
| O1 | 2018 CalcAssumed key p4, Q9(b) | The key text answers 48; the key’s own CAS table row 5 is 47.249. The notes take 47 as correct. The original paper or official confirmation of the key’s formal answer is needed |
| O2 | `MAA/questions.json` `key_regions` | Chunk records are incorrect or truncated; this does not affect the notes, but will affect the function that extracts text by key_regions. e.g. the key for 2018A-Q10 is actually on p6, but the record is p5 (which is the end of Q9); the p11 recorded for 2016A-Q11 is the TSI ice-cream question; (e) is actually on p13; 2018A-Q9 omits (d)(e) on p5; the regions for 2024A-Q7, 2020A-Q13, 2023F-Q1, 2024F-Q2, 2025F-Q3, and 2017F-Q5 are truncated mid-sub-question, with subsequent sub-questions on the next page |
| O3 | `tools/catalogue_MAA.json` name_zh, description; `evidence/maa/labels.json` reason | Displayed as garbled text when read (suspected GBK and UTF-8 mis-decoding). The notes do not cite these fields; if used in the interface or review, the encoding needs checking |

---

## Summary

| File | Items sampled (approx.) | Citations mechanically checked | Factual errors corrected | Original pending review (unique items) | Resolved | Still pending review |
|---|---|---|---|---|---|---|
| 01 BIV | 58 | 280 items, 0 missing | 0 | 3 | 2 | 1 (2018A-Q10(c) labelling) |
| 02 SEQ | 37 | 178 items, 0 missing | 2 | 3 | 3 | 0 |
| 03 GRF | 50 | 180 items, 0 missing | 4 | 6 | 5 | 2 (2020A-Q13(a) original; 2022A-Q10(b)(ii) new, both labelling issues) |

**Conclusion**: The factual errors in the three notes are concentrated in the SEQ 2018A-Q9 pairing and the GRF question-number citations, the ★ note, and the Pattern 9 definition. 2018A-Q9(c)’s 42 is correct; 27 corresponds to (d)(ii). The Pattern 9 definition in GRF does not match the actual routes for 2020A-Q13(a) and 2022A-Q10(b)(ii); it should be changed to the Hamiltonian type (GRF6), and the label issue is left for the labeller to decide.

---

**Review method**: The reviewer is Haiku 5.5 (claude-haiku-5-5), who did not participate in writing and worked with a fresh context. The basis is the original papers and marking keys (PDFs under `MAA/papers/`, with text extracted using pymupdf; layout-dependent pages rendered as PNGs for checking, stored in `evidence/maa/review/`), cross-checked against the original 2016–2025 exam reports. Numerical values were recalculated with Python. `evidence/maa/labels.json` and `tools/` were not modified.

**Handling principles**: Where the notes disagree with the original papers, keys, or reports, correct them directly. Any “pending review” that can be determined from the original paper or key is resolved and the marker removed; where the original paper itself is ambiguous, keep “pending review” and state the reason. Label concerns are recorded only in “Labelling suggestions (not modified)”.

**Conclusion categories**: Factual errors corrected / Pending review resolved / Pending review retained / Labelling suggestions.

---

## 04 Time Series (TSI)

| # | Severity | Location | Issue | Evidence | Resolution |
|---|---|---|---|---|---|
| 1 | High | Pattern 5 Approach 2 example | It says 2024A-Q8(f) requires first finding the Day 1 value from the least-squares line of the deseasonalised data. Incorrect: the deseasonalised value for that day is already given in the table as 42.4 | 2024 CalcAssumed key Q8(f): 42.4 × 0.896 = 38 | Change to use the table's deseasonalised value directly, and note that the least-squares line is not needed |
| 2 | Medium | Pattern 4 marking points | 2024A-Q8(a) says "one mark for each correct value". Actually it is 2 marks, for the two blanks Saturday and Sunday (130.9%, 121.4%) | The two marking points in 2024 CalcAssumed key Q8(a) | Correct to two blanks, 1 mark each |
| 3 | Medium | Pattern 4 marking points | 2025A-Q7(c) is written as "___% of the trend value". It is actually a fill-in-the-blank of the form ___ % ___ the trend value; the key accepts 10.21% below or 89.79% of | 2025 CalcAssumed key Q7(c) | Correct the wording |
| 4 | Low | Pattern 5 Approach 5 | The reason for deseasonalising is written as "to make the long-term change (trend) clear". The key for 2022F-Q5(c)(i) only requires "remove the seasonal effect" | 2022 CalcFree key Q5(c)(i) | Change to the key's reason |
| 5 | Low | Examiner's report reminder (calculator and working) | "For two-mark questions, working must also be shown, otherwise marks cannot be awarded (2019, 2020, 2022 reports)". The 2022 report actually means keep working so follow-through marks can be awarded, not "marks cannot be awarded" | 2019, 2020, 2022 reports | Separate the statements |
| 6 | Medium | Pattern 7 Approach 4, marking points | Under the general rule "outside the data range means extrapolation, so the conclusion is that the prediction is unreliable", the key for 2017A-Q15(b)(vi) judges the prediction reliable, because it is "within one cycle of the known data" (last data December 2016, prediction December 2017). The note originally only wrote "pending review" | 2017 CalcAssumed key Q15(b)(vi); the prediction in 2023A-Q8(h)–(i) (t = 24) is two years from the last data (t = 16), and the key judges it as extrapolation | State the exception and that the boundary between the two questions follows their respective keys (also resolves pending review #9) |

Pending reviews resolved (not counted as errors):

| # | Original pending review item | Original paper conclusion | Resolution |
|---|---|---|---|
| 7 | Pattern 2: insufficient evidence for outlier | Among the 2016–2025 TSI sub-questions there is no outlier question. The 2024 outlier question is 2024A-Q11(b), labelled BIV, outside the scope of this note | Delete the false pending review, rewrite as an explanation (already amended) |
| 8 | Pattern 2: 2020A-Q14(d) seasonal selection | Key is Winter, based on the winter seasonal index 74.6 being the lowest of the four seasons | State the answer, remove pending review |
| 9 | Pattern 3: 2018A-Q12(c) most suitable moving average | Key is a 5-point moving average; the reason is that the data has a 5-point cycle, or the 5-point column continues to decrease | State the answer, remove pending review |
| 10 | Pattern 3: 2025A-Q7(a) window and centring | Key is a 6-point centred moving average; the two marking points are "write the correct moving average" and "state that it is centred" | State the answer, remove pending review |
| 11 | Pattern 3: 2021A-Q8(a) 5-point moving average | Key is 5 point moving average (1 mark) | Remove "key wording pending review", change to the key answer |
| 12 | Pattern 4: 2023A-Q8(b) normalisation | In the key table the four indices are 58.83%, 76.19%, 155.72% and 109.26%, summing to 400%; a key note says directly averaging the winter component gives 155.55%, different from the 155.72% written in the table | Write per the key, note the remark, remove pending review |
| 13 | Pattern 4: 2016A-Q10(b)(i) Wednesday index (about 0.590) | Key main answer is 0.625 (mean of the three Wednesday percentages (63.3 + 60.8 + 63.4)/3 = 62.5%); the key also lists "5 minus the sum of the other four days' indices" giving 0.590 (59.0%). 0.590 is not a result unique to the note author | Write both methods, remove the "author's check" pending review |
| 14 | Pattern 5: fraction for B in 2024A-Q8(c) | List 45 ÷ 0.883 = 50.96, take 51.0 | State the fraction and result, remove pending review |
| 15 | Pattern 7: t = 30 in 2024A-Q8(g) | Key also uses t = 30; trend value 55.8, predicted value 49 | Remove pending review |

**Summary (TSI)**: Checked 82 items (sub-question number, mark value, numerical value, key marking point, and report wording each count as one item). Fixed 5 factual errors or inaccurate statements (#1–#5); fixed 1 rule description that conflicts with the key (#6, also resolving the pending review for 2017A-Q15(b)(vi)). There were 10 pending review items in total, all resolved (#6 and #7–#15). Still pending review: 0 items.

---

## 05 Loans, Investments and Annuities (FIN)

| # | Severity | Location | Issue | Evidence | Resolution |
|---|---|---|---|---|---|
| 1 | High | Pattern 4 Approach 2 | It says "2016A-Q12(b) requires finding two coefficients". Incorrect: that sub-question asks for A and B in the table, i.e. the Month 6 interest 219.91 and closing balance 14 380.32 | 2016 CalcAssumed key Q12(b) | Delete the incorrect parenthetical, and state A and B in the marking points |
| 2 | Medium | Examiner's report reminder (2024 report) | "Applying steady-state solutions is a weak area, but the report does not state which specific pattern it belongs to (pending review)". The report does not name the question number; the key question involving a steady-state value is 2024A-Q7(f)(ii), which belongs to the sequences topic (SEQ7), not annuities | 2024 CalcAssumed key Q7(f)(ii) (steady-state value 9.5 million); labels.json marked as SEQ7; 2024 report Section Two | Change to point to the SEQ7 note, remove pending review |
| 3 | Low | Pattern 6 common errors | The statement "the key for 2022A-Q15(b)(iii), (iv) notes that the final repayment changes with previous rounding" is inaccurate. The key note is: if 6.1 ÷ 1200 is used instead of the rounded 0.00508, the final repayment is 5161.09 (rather than 4858.42), and total interest changes accordingly | Note in 2022 CalcAssumed key Q15(b)(iii), (iv) | Change to the key's specific note |
| 4 | — | 2017A-Q8(b) | Originally pending review. Recalculated with Python: with 5.4% per annum, compounded monthly, the future value after five years of an initial deposit of 1000, then equal quarterly payments at the end of each quarter to top up to 98 974, gives a quarterly payment of 4283.77, matching the key | 2017 CalcAssumed key Q8(b) | Remove pending review (resolved) |
| 5 | — | 2017A-Q8(a) | The payment timing is still ambiguous: the question says "at the start of the year", but the key's solution is x = x(1 + 5.9%/12)¹² − 6000, equivalent to end-of-period payments, giving 98 974; with start-of-period payments it should be 104 974 (= 6000 + 6000/i) | 2017 CalcAssumed key page 2 render: `evidence/maa/review/2017A_Q8_key_p2.png` | Keep pending review, and state in the marking points that the key's solution conflicts with the question wording |

**Summary (FIN)**: Checked 72 items. Fixed 3 factual errors (#1–#3). Resolved 2 pending review items (2017A-Q8(b), steady-state attribution). Still pending review: 1 item (2017A-Q8(a) payment timing; the original paper itself is ambiguous and cannot be determined unilaterally by the note).

---

## 06 Networks and Decision Mathematics (NDM)

| # | Severity | Location | Issue | Evidence | Resolution |
|---|---|---|---|---|---|
| 1 | High | Pattern 4 Approach 3, past question; Pattern 5 marking points | 2018F-Q6(d)(ii) was originally listed as ES. The key calculation is latest starting time: project duration 9.5 hours (including a 30-minute break), finish at 4 pm, V must start before 1:30 pm. But the question says earliest starting time. The question and key are inconsistent | 2018 CalcFree Q6(d)(ii) question and key | Move from the ES example to the LST marking points, and note that the question and key are inconsistent |
| 2 | Medium | Pattern 4, 5 past question lists | 2020A-Q16(b) and 2021A-Q13(d) are listed as examples of ES/LST, but the key only awards marks for critical activities or the critical path and duration; ES/LST are not marked separately | 2020 CalcAssumed key Q16(b); 2021 CalcAssumed key Q13(d) | Keep in the lists, note that the key only awards marks for the critical path and duration (label suggestion below, not changed) |
| 3 | Low | Pattern 6 common errors | 2020A-Q16(e) "shortening only E or F cannot shorten the project duration" is inaccurate. Key: B lies on both critical paths (BCE, BDG), so shortening B can reduce the duration by 1 day; F is non-critical, so it has no effect; E lies on only one critical path, so D or G must also be shortened for it to be effective | 2020 CalcAssumed key Q16(e) | Correct |
| 4 | Low | File header and Pattern 12 | The file header says "this file has no pending review items", but the Pattern 12 body still has "(pending review)", which is inconsistent | — | Pattern 12 has been resolved, so the file header statement becomes accurate |
| 5 | — | Pattern 12 common errors, 2025A-Q13(f) | Originally pending review. The original key's reason is that cut 3 does not separate sink H from source A, i.e. it does not satisfy the definition of a cut (source and sink, see 2025 key Q13(a)) | 2025 CalcAssumed key Q13(a), (f) | State the key's reason, remove pending review (resolved) |

**Summary (NDM)**: Checked 73 items. Made 4 changes (#1–#4, of which #2 is a note rather than a change). Resolved 1 pending review item (2025A-Q13(f)). Still pending review: 0 items.

---

## Report and numerical checks (combined across the three study notes)

- Exam report citations: the cited years, exact wording and percentages in TSI, FIN and NDM (2016 Q16 average 42.26%, 2017 Q14 average 28.3%, 2016 Q1 average 86.94%, 2017 Q2 average 80.45%, 2023 Q5 average 82.04%, 2023 Q14 average 41.05%, 2024 Q6(d) average 27.12%, 2024 Q13(d)(i) and (e) averages 33.84%, 34.74%, 2024 report steady-state weak areas, 2025 report moving average and cut weak areas, 2019 report CAS calculator use) are all consistent with the report PDFs; no misquotations found.
- Numerical recalculations: 98 974 and 4283.77 for 2017A-Q8, the 365 compounding periods for 2016A-Q13(b), the effective annual interest rates for 2024A-Q10(d) and 2016A-Q13(b), the 5-year balance for 2025A-Q12(b), etc., are all consistent with the key.
- The original wording "in context" in the 2025 report differs slightly from "in the context of the question" in the notes; this is a paraphrase and has not been changed.

---

## Tagging recommendations (not modified)

Per the rules, `labels.json` and `tools/` are not changed; the following is for annotators' review only:

1. 2018 CalcFree Q6 (d)(ii): label NDM4 (ES). The key calculates LST (V starts before 1:30 pm); suggest changing to NDM5. The question stem says earliest, which is inconsistent with the key; suggest also checking the original exam paper question stem.
2. 2020 CalcAssumed Q16 (b): labels NDM4, NDM5, NDM6. The key awards marks only for "critical activities" and "duration"; suggest removing NDM4 and NDM5 and keeping only NDM6.
3. 2021 CalcAssumed Q13 (d): labels NDM4, NDM5, NDM6. The key awards marks only for "critical path" and "duration"; suggest removing NDM4 and NDM5.
4. 2018 CalcAssumed Q13 (d)(iii): label TSI7. The question converts deseasonalised values back to actual values (multiplying by seasonal indices), consistent with the definition of TSI5; suggest adding TSI5; whether to keep TSI7 depends on the forecasting convention.
5. 2017 CalcAssumed Q15 (b)(vi): label TSI7, no change needed. The key judges the forecast reliable, contrary to TSI7's "extrapolation is unreliable" rule; the notes already state the exception.


## 2026-10-12 Study note sync after tagging revision

**Basis**: `tools/parttags_MAA.txt` (final labels: 41 sub-question label changes; the review flag on 2017A-Q8 has been cleared) and `evidence/maa/tag_review/arbiter.md`. This revision changes only the study note body and the header counts; it does not change labels, `tools/`, `labels.json`, `app/`, `wace.db`; the "past exam question" rows are not touched, and pattern headings are unchanged.

| File (Chinese/English) | Change | Count |
|---|---|---|
| 01 BIV | In Pattern 1, the per-question determination of explanatory variables now points to Pattern 11 (2017F-Q5(b), 2022F-Q3(b), 2024F-Q2(b)(i) are now BIV11); in Pattern 4, 2023A-Q7(d) (now BIV3) now points to Pattern 3; in Pattern 16, 2021F-Q7(d) (now BIV4) now points to Pattern 4; in the English version, the "pending review (label)" note for 2018A-Q10(c) has been deleted (now labelled BIV2 only); the header review-status sentence has been changed to a revision note | 26 questions, 173 sub-questions, 16 patterns, unchanged |
| 02 SEQ | In Pattern 6, 2025A-Q6(f) (now SEQ8) now points to Pattern 8; in Pattern 8, 2021F-Q6(c) (now SEQ7) now points to Pattern 7; the "SEQ5 only" note for 2024A-Q7(f)(i) has been deleted (now SEQ5+SEQ8); the sub-question count for Pattern 5 has been changed from 39 to 37; header review-status sentence | 23 questions, 101 sub-questions, 9 patterns; Pattern 5 has 37 sub-questions |
| 03 GRF | In Pattern 5, 2021F-Q3(c) (now GRF8) now points to Pattern 8; Pattern 9 deletes 2020A-Q13(a), 2022A-Q10(b)(ii) (now GRF6+GRF4), keeps only 2017F-Q6(a), and points to Pattern 6; "Items pending review" has been changed to "Review verification"; the GRF9 pending-review item has been deleted; in the verification list, 2021F-Q3(c) has been changed to Pattern 8; the header sub-question label count has been changed from 96 to 98 | 23 questions, 98 sub-question labels, 91 unique sub-questions, 9 patterns |
| 04 TSI | In Pattern 1, 2017A-Q15(b)(iv), 2018A-Q13(b)(i) (now TSI6) now point to Pattern 6; in Pattern 5, 2025A-Q7(e) (now TSI7) now points to Pattern 7; in Pattern 2, the question number for 2024A-Q11(b) (now BIV3) has been removed; in the review conclusion, "label suggestions" has been changed to a revision note | 10 questions, 68 sub-question labels, 64 unique sub-questions, 8 patterns (header already consistent, unchanged) |
| 05 FIN | The payment timing in 2017A-Q8 has been changed to "marking key inconsistent with the question stem (known issue)" (header, Pattern 9); in Pattern 1, 2025A-Q8(b) (now FIN7+FIN10) points to Pattern 10; in Patterns 1 and 5, 2020A-Q12(b) and 2020A-Q11(c) (now FIN4) point to Pattern 4; in Pattern 7, 2016A-Q16(a)(ii) (now FIN8) points to Pattern 8; in Pattern 8, 2022A-Q15(b)(i) (now FIN7+FIN10) points to Pattern 7; note in Pattern 10: FIN10 changed from 4 to 15 labels | 25 questions (F 1, A 24), 10 patterns; FIN10 has 15 labels |
| 06 NDM | In Pattern 4, the 2018F-Q6 example points to the note in Pattern 5; in Pattern 9, 2018F-Q4(b) (now NDM10) points to Pattern 10; in Pattern 12, 2016A-Q9(e) (now NDM14) has been moved out and points to Pattern 14; in Pattern 14, 2024F-Q3(e) (now NDM8+NDM12) points to Patterns 8 and 12; note counts: NDM4 changed from 5 to 2, NDM5 from 7 to 6, NDM15 from 3 to 5 | 37 questions (F 20, A 17), 15 patterns, unchanged |

**Unchanged, to be confirmed**:

1. 03 header and ★ markers for Patterns 1, 3 and 5: by summing the sub-question marks (`evidence/maa/labels.json`), under the final labels GRF4 is 31, higher than GRF3's 29; GRF1 and GRF6 are 28, and GRF5 is 27. The header statement "GRF3 is highest, GRF1 and GRF5 tied" is inconsistent with this sum, and the pre-revision labels cannot reproduce it either. ★ unchanged.
2. Question-stem-level references (2016A-Q15(b), 2017A-Q15(a), 2017A-Q15(b), 2025A-Q10(e), 2017A-Q13(c)) have no separate labels themselves, but their sub-questions (e.g. (bi)–(biii)) all carry corresponding labels, so they are retained.
3. The payment timing in 2017A-Q8 remains a known issue (the question stem says payment at the beginning of the year, while the key uses payment at the end of the period); see 05 Pattern 9 and the header.
