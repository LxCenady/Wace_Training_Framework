# MAM Solution Approaches · Independent Review Record

**Review method**: Each set of notes is reviewed by an independent subagent. The reviewer did not take part in writing, works with fresh context, and only reads, does not modify. Evidence checked includes: the original "Specific behaviours" text in each question's marking key in `evidence/`, the full text of the 2016–2025 exam reports, the PDF pages of the original papers and keys, with independent verification using sympy/scipy.

**Handling principles**: The author reviews the review comments one by one. All high-severity comments were only changed after going back to the original paper wording and verifying; everything that could be verified by calculation was checked. Items marked "doubtful" by the reviewer were changed only when supporting evidence could be found.

**Outcome categories**: Accepted = changed in line with the comment; Partially accepted = wording changed but the suggestion was not followed completely; Rejected = not changed, with reasons given.

---

## 01 Differentiation and its applications (15 items: accepted 15)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | "If you do not verify the extremum you get at most half marks" is an invention by the author; the 2024 report does not say this; in 2024A-Q12(c), verification accounts for only 1 of the 4 marks | Accepted: changed to "verification is usually worth 1 mark on its own" |
| 2 | Medium | "2019 report: one of the worst on the paper, typical error h′(1)" does not match the original report | Accepted: changed to the report's exact words, with h′(1) noted as an author reminder, and added 2020 report Q5(c) |
| 3 | Medium | "Verification is guaranteed marks and must not be omitted" overstates it: the wording of 2025A-Q12(b) and 2025A-Q14(c) states that verification is not required | Accepted |
| 4 | Low | "Missing one type of label loses one mark" is not the report's exact wording; the question number format was wrong | Accepted: changed to the actual 4 marking points for 2020F-Q7(d) |
| 5 | Medium | "Horizontal point of inflection (f′=f″=0)" may be mistaken for a test condition; counterexample x⁴ | Accepted |
| 6 | Low | "Writing the two-term structure earns marks" is inaccurate; the key requires at least one term to be correct | Accepted |
| 7 | Low | "2023 report: the conclusion was judged invalid" is not the report's exact wording | Accepted |
| 8 | Low | "The report warns not to write it" cannot be found in the MAM reports | Accepted: changed to the actual statements in the 2018, 2019 and 2025 reports |
| 9 | Low | 2025F-Q3 is not related rates | Accepted: moved out of Pattern 8 |
| 10 | Low | Pattern 3 incorrectly cites 2017F-Q6(b)(ii); omitted 2018F-Q3(b) and 2019F-Q7(b) | Accepted |
| 11 | Low | The reason for deducing P″(6)=0 in 2018A-Q15 was not clearly written | Accepted: added "continues to increase afterwards ⇒ horizontal point of inflection", and checked a=−18, b=108 |
| 12 | Low | "Each condition is worth 1 mark" is an overgeneralisation | Accepted |
| 13 | Low | "The derivative does not exist at a turning point" is ambiguous wording | Accepted: changed to "corner point (sharp corner)" |
| 14 | Low | The numbering explanation did not explain 2016S (sample paper) | Accepted |
| 15 | Low | The expressions "x²eˣ → xeˣ(x+2)" and "A″(x)<0" were unclear | Accepted |

## 03 Rectilinear motion (11 items: accepted 11)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | "When a = 0, velocity is at an extremum" is an overgeneralisation: v = t³ is a counterexample; in the constant-velocity section of 2019A-Q12(c), a is always 0; endpoints can also give an extremum | Accepted |
| 2 | Medium | In "hits 0 and turns back", the meaning of "turns back" is exactly the opposite | Accepted |
| 3 | Medium | The piecewise integral was written as "+ −", opposite to the cited 2023A-Q8(c) (that question is negative first, then positive) | Accepted: after the author verified v = −2t sin t by calculation and confirmed, changed to "add a negative sign for the v<0 section" and gave the working for that question |
| 4 | Medium | Report years were wrong: 2021 was not listed as a major weakness; 2018 and 2023 were omitted | Accepted |
| 5 | Medium | The key for 2018A-Q11(c) treats "decelerating 0.5" as a = −0.5, which conflicts with the same-sign/opposite-sign rule | Accepted: the author checked the original question wording and added a note as a reminder |
| 6 | Medium | "Returns to the origin" and "returns to the starting point" were used interchangeably | Accepted |
| 7 | Low-Medium | "v″<0 or compare endpoints": questions using calculus must use v″ or a sign test | Accepted |
| 8 | Low | "Leaves the left side of the screen" is ambiguous | Accepted: changed to "to the right" |
| 9 | Low | The graphing requirements for 2025F-Q6(d) were written imprecisely | Accepted |
| 10 | Low | "Divide by the inner coefficient" is easy to miscalculate | Accepted: added "i.e. multiply by 3" |
| 11 | Low | Omitted citations of 2017A-Q20(c)(d) and 2019A-Q12 | Accepted |

## 05 Discrete random variables (13 items: accepted 13)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | 2018A-Q12(f) omitted the "additional $1 charge"; the new mean should be 1.2μ + 1 | Accepted: the author confirmed after checking the original question |
| 2 | Medium | "4 decimal places, otherwise marks are deducted": the report does not say marks are deducted; the key for 2019A-Q18(c) requires at least 5 places | Accepted: the author verified P≈3.0×10⁻⁵ by calculation |
| 3 | Medium | Y = 3 − X is negative when X = 4 | Accepted: changed to max(0, 3 − X) |
| 4 | Medium | "Every year" is untrue; in fact it is 6 out of 10 years | Accepted |
| 5 | Medium (doubtful) | Assumptions question: the key only gives "independent" and "same p"; "two outcomes" and "n fixed" are given in the question | Accepted: supported by the original key |
| 6 | Medium | "binomial and parameters worth 1 mark separately" is ambiguous | Accepted |
| 7 | Medium | Pattern 5 incorrectly cites 2022A-Q12 (there is no binomial sub-question); the single-item probability in 2023A-Q13(b) comes from a uniform distribution | Accepted: deleted the former, replaced it with 2021A-Q8(d), and added a note to the latter |
| 8 | Low | a = ±15/22, with no explanation of why the positive value is taken | Accepted |
| 9 | Low | "2020 report Q1" is not labelled F | Accepted |
| 10 | Low | 2016S-F4 is cited, but it is not stated that it is not among the 28 questions | Accepted |
| 11 | Low | The marking points for 2017A-Q13 omitted the 2 marks for (d) | Accepted |
| 12 | Low | Pattern 6 incorrectly classified 2021A-Q10(b) and 2023A-Q13(a) as "use binomial" | Accepted |
| 13 | Low | "Probability expression worth 1 mark separately" is an overgeneralisation | Accepted: changed to "most questions" |

## 06 Continuous random variables and the normal distribution (13 items + 1 doubtful: accepted 13, partially accepted 1)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | High | Applying (b−a)²/12 directly for the variance of a uniform distribution loses marks: the key awards marks for "pdf and domain" and "integral expression", and this formula is not on the formula sheet either | Accepted: changed to writing an integral for the answer, with the formula used only for checking |
| 2 | Medium | "Keep 4 decimal places" is an overgeneralisation; some questions specify 3 places or exact | Accepted |
| 3 | Medium | It reminds students to distinguish cdf, but does not teach the cdf question type (2023A-Q11(d)(e)) | Accepted: added to Pattern 2 |
| 4 | Medium | In 2021F-Q6(b)(ii), comparing using σ does not lead to the conclusion; the key uses area | Accepted: changed to the key's reasoning, and added a strict bound (author verified 0.383) |
| 5 | Low | "Designed according to the 68-95-99.7 rule" is inaccurate | Accepted |
| 6 | Low | "2.9 h → 2:54 pm" is not data from the actual exam question | Accepted: changed to 3.8 h → 3:48 pm from 2023A-Q11(c) |
| 7 | Low | 2025F-Q4 is "Show that k", not "Determine" | Accepted: both questions cited |
| 8 | Low | "Probability expression worth 1 mark separately" is an overgeneralisation | Accepted |
| 9 | Low | Unit conversion omitted the variance, and also reverse-finding a and b | Accepted |
| 10 | Low | The unit of variance was omitted | Accepted |
| 11 | Low | The histogram question type omitted frequency-to-probability conversion, cumulative tables, and estimating the expected value from class midpoints | Accepted |
| 12 | Low | The notation for 2016S-A12 is inconsistent | Accepted |
| 13 | Low | Quotation marks were added around an identifying sentence, making it look like the original wording when it was actually a paraphrase | Accepted |
| Doubtful | — | "2021 report: many people did not write uniform" goes beyond the original report wording | Partially accepted: changed to the report's actual statement plus the key answer |

## 02 Integration and its applications (16 items: accepted 14, partially accepted 2)

| # | Severity | Issue | Action |
|---|---|---|---|
| 1 | Medium | "FTC is named and examined every year" is untrue (it was not examined in 2019, 2020 or 2024, and many years' reports do not name it) | Accepted: changed to "high-frequency + named many times" and listed the years |
| 2 | Medium | 2021A-Q9 does not involve integration | Accepted: moved out of Pattern 8 and a note added |
| 3 | Medium | "The 3 marking points in the key are exactly these three steps" is an overgeneralisation | Accepted |
| 4 | Medium | The rectangle estimate only covered increasing functions; 2021F-Q7 is decreasing (1/x) | Accepted |
| 5 | Medium | "Set the cross-sectional area equal to the volume" is dimensionally incorrect | Accepted: changed to "cross-sectional area × length = volume" |
| 6 | Low | 2023F-Q5(b) is not of the form ∫f′ | Accepted: replaced with 2023F-Q2(a)(iii), with Q5(b) listed separately |
| 7 | Low | The A(x) rule omitted "f changes from negative to positive → local minimum" | Accepted |
| 8 | Low-Medium | The question type involving direct evaluation of a definite integral was omitted, and 2020F-Q3 was not classified | Accepted: added to Pattern 1 (2020F-Q3 was already cited in Pattern 5) |
| 9 | Low (doubtful) | "The report says many people lost marks here" is unsupported | Accepted: changed to the actual statement in the 2017 report |
| 10 | Low | "Use CAS to calculate the exact value" does not match the CF paper | Partially accepted: changed to "find the function then integrate", with the trapezium retained |
| 11 | Low | The constant c appears out of nowhere | Accepted |
| 12 | Low | d/dx(x sin 3x) should be 2x sin 3x | Accepted |
| 13 | Low | 2023F-Q2(c)(iii) is not an area question | Accepted |
| 14 | Low | "Crossing the x-axis requires splitting into intervals" is an overgeneralisation | Accepted |
| 15 | Low | Missing n ≠ −1; WACE convention is to write ln f(x) | Accepted |
| 16 | Low | The explanation and question numbering format for the 2016 sample paper | Partially accepted: an explanation was added at the beginning, but the question numbering format was kept as `2016S-F1` and not changed |

## 04 Exponentials and Logarithms (12 items: accepted 11, partially accepted 1)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | Medium | Summary of correspondence between report years and weak areas is inaccurate | Accepted: list item by item by year |
| 2 | Medium | The 2023 report refers to readings (2023F-Q4(c)), not ratios; "cannot be subtracted" conflicts with the key | Accepted |
| 3 | Medium | The value in "9 am + 4.7 h ⇒ 1:42 pm" is wrong; 2018A-Q9(d) is actually 9.40 h ⇒ 6:24 pm | Accepted: after the editor checked ln1.6/0.05 = 9.40, corrected it and added rounding down for latest |
| 4 | Medium | The ratio formula only had /10; 2016S-A13 (k=20), 2016A-Q12 (k=1), and 2023F-Q4 (k=2) differ | Accepted: changed to the general formula L = k·log |
| 5 | Medium | "Write the rate of decrease as a positive number" is overgeneralised; the key for 2018A-Q9(c) gives a negative number | Accepted |
| 6 | Medium-high | Missing the "calculus of eˣ / ln x" pattern; 13 questions are unassigned | Partially accepted: added cross-reference Pattern 7; methods are in the differentiation and integration notes to avoid duplication |
| 7 | Low | 2016 sample paper not specified | Accepted |
| 8 | Low | "Almost every question's first step is converting between forms" is overgeneralised | Accepted |
| 9 | Low | Pattern 1 incorrectly cites past exam questions 2016F-Q1 and 2025F-Q7(a) | Accepted |
| 10 | Low | Missing context-based rounding rules | Accepted |
| 11 | Low | WACE key often writes ln f(x) | Accepted |
| 12 | Low | "Dashed lines" are not a key requirement | Accepted |

## 07 Sample Proportions and Confidence Intervals (11 items: accepted 11)

| # | Severity | Issue | Resolution |
|---|---|---|---|
| 1 | High | **The p̂ rule for minimum sample size is reversed**: the key still uses 0.5 when p̂ is known (2023A-Q7(c), 2024A-Q10(f), 2025A-Q16(e); the 2023 report specifically warns about this) | Accepted: the editor checked the question stems for all three questions and corrected it; under the old rule, 2023A-Q7(c) would give 2263 instead of 2401. The question-writing skill was also corrected |
| 2 | Medium | The 2023 report's warning was paired with a 2024 example | Accepted |
| 3 | Medium | 2025A-Q15(f) is a "prove" question, the answer is No, and it was categorised incorrectly | Accepted: listed separately as "distinguishing the two question types" |
| 4 | Medium | The example combined time and location into one bias, violating the rule on the same page | Accepted: split into two |
| 5 | Medium | Missing binomial distribution assumption questions (2020A-Q12(h), 2021A-Q11(g)) | Accepted |
| 6 | Low | "2–4 marks per year / 2 marks per source" is overgeneralised | Accepted |
| 7 | Low | 2024A-Q10(e) belongs to Pattern 5; Pattern 5 is missing a list of past exam questions | Accepted |
| 8 | Low | The calculation with 9603.6 and 1.96 is inconsistent | Accepted |
| 9 | Low | "Switch to the binomial distribution" was mistakenly written as a remedy for (a) | Accepted |
| 10 | Low | "Random" is not a key requirement for 2016A-Q10(a) | Accepted |
| 11 | Low (doubtful) | Reverse-solving for the confidence level omitted 2023A-Q12(c)(d) | Accepted |

---

**Summary (7 MAM papers)**: 92 comments in total (including 1 "doubtful"), 88 accepted, 4 partially accepted, 0 rejected. There are 5 high-severity items; all were revised after checking against the original exam paper wording.

---

## Category Corrections After User Feedback (2026-10-09)

After a user pointed out that the vector question bank contained unrelated questions, all tags were keyword-reviewed, and the key was checked item by item:
- MAM 2021A-Q9 removed the "Integration" tag (the whole question only involves solving equations, differentiation, and finding extrema; there is no integration; the integration notes reviewer also pointed this out).
- MAM 2024A-Q10 removed the "Discrete Random Variable" tag (the whole question has no binomial distribution).
