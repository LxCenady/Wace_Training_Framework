# MAM · Sample Proportions and Confidence Intervals — Patterns and Solution Approaches

> Basis: marking keys for 29 past exam questions from 2016–2025 + exam reports (almost every year they specifically mention "can calculate but cannot explain"). Original questions in `topics/07_Sample_Proportions_CI.pdf`. Numerical examples in this document have been checked using Python.
> Review status: one round of independent review has been completed and revisions made according to feedback (see `Review_log.md`).

## Formula card

- p̂ = x/n; approximate distribution of p̂: **p̂ ~ N(p, p(1−p)/n)** (when n is large enough).
- Confidence interval: p̂ ± z·√(p̂(1−p̂)/n); margin of error E = z·√(p̂(1−p̂)/n); interval width = 2E.
- z-values: 90% → 1.645, 95% → 1.960, 99% → 2.576.
- Back-calculate from the interval: p̂ = (upper bound + lower bound)/2, E = (upper bound − lower bound)/2.
- Sample size: n = z²p̂(1−p̂)/E². **For minimum sample size (minimum / guarantee / ensure margin at most …), always use p̂ = 0.5** (worst case), **even if p̂ has already been calculated earlier** (the keys for 2023A-Q7(c), 2024A-Q10(f), 2025A-Q16(e) all do this; the 2023 report specifically reminds you). Only substitute a particular sample proportion when the question explicitly requires it (2016A-Q10(d): "Using the sample proportion of the survey…").

## Marking-key reminders (the reports say the most about this chapter)

1. **You must take a position when drawing a conclusion from an interval** (2023 report): you cannot avoid a conclusion by saying "cannot be 100% certain". Example (2024A-Q11(b)): "The claimed value 0.74 lies inside the 95% CI (0.652, 0.748), so there is insufficient evidence to reject the claim."
2. **Bias questions require specific detail** (2022–2024 reports): state the source of bias + explain **which type of person is more likely or less likely to be selected** + relate it to the context. Time and place are **two** different sources of bias; do not combine them into one point.
3. **Sample sizes must be rounded up**; when back-calculating sample size, round to the nearest whole number (for the difference between the two, see Pattern 4).
4. Meaning of "95% confidence": if sampling were repeated many times, about 95% of intervals would contain the true p; **any particular interval either contains p or does not contain p**.

---

## Pattern 1: Write down the distribution of p̂ and find a probability

**Identification**: "What is the (approximate) distribution of the sample proportion?" "P(p̂ < 0.58)".

**Approach (3-mark template)**: ✓ "approximately normal (since n is large)" ✓ mean = p ✓ variance p(1−p)/n (or write the standard deviation). Then use normCdf to calculate, and write the probability expression.
**When the normal approximation cannot be used**: the distribution graph is clearly right-skewed, n is small, np is too small (2023A-Q10(a): n = 36, p = 0.05, the graph is not symmetric ⇒ not appropriate). For (a), just write "not symmetric" as the reason. In (b), n is changed to 500 and the question asks for the number X, so use the binomial; in (c), at n = 500 the normal approximation can be used again.
**What happens when the sample size increases**: the standard deviation of p̂ becomes smaller and the distribution becomes more concentrated, so P(p̂ ≤ 0.03) becomes **larger** (2017A-Q18(d)(ii): the two marks are awarded for "SD decreases" and "distribution more concentrated ⇒ probability higher").

**Past questions**: 2016A-Q14(b), 2017A-Q18(d), 2018A-Q17(a)(b), 2019A-Q13(a), 2020A-Q12(b)(c), 2021A-Q11(a)(b), 2022A-Q13(a), 2023A-Q10, 2024A-Q10(b), 2025A-Q10(d).

---

## Pattern 2: Calculate confidence intervals and margin of error

**Approach**: p̂ → choose the correct z → substitute into the formula (or use the CAS 1-Prop z Interval) → round to the required number of decimal places.
Example (2023A-Q7): 76/200 = 0.38, 95% CI ≈ (0.3127, 0.4473).
**Assumptions**: p̂ is approximately normal (n is large enough) — the key for 2016A-Q10(a) requires this statement; random sampling can be added as a supplement.

**Past questions**: 2016A-Q10, 2017A-Q18(b)(c), 2018A-Q17(e), 2019A-Q8, 2020A-Q12(d)(e), 2021A-Q11(d)(e), 2023A-Q7(b), 2024A-Q9(a), 2025A-Q16(b)(c).

---

## Pattern 3: Use a confidence interval to test a claim ★ tested every year

**Standard two sentences (the 2 marks in the key)**
1. "The claimed proportion p = 0.6 is **not** within the 95% confidence interval (0.4562, 0.5438)."
2. "Therefore there is sufficient evidence (at the 95% level) to conclude that the claim is incorrect / that Tina is unlikely to be correct."

Conversely, if the claimed value lies inside the interval: "not enough evidence to conclude that the proportion has changed".
**Comparing two intervals** (2020A-Q12(f)): the two intervals overlap ⇒ there is not enough evidence to say that the financial advice reduced the failure rate.
**Why the true value not being in the interval does not necessarily mean a mistake was made** (2019A-Q8(b), 2021A-Q13(g)): "Not all 95% confidence intervals contain the true proportion; about 5% will not, and this may be one of them."

**Distinguish the two types of wording** (2025 report: statistical significance, as distinct from proving a result):
- If it asks "is it different / what does it suggest" ⇒ state a conclusion using the two sentences above.
- If it asks "does it **prove** the claim is incorrect / was a mistake made" ⇒ answer **No**: an interval cannot prove anything, not all intervals contain p, and you do not know whether this interval is one of those that does not contain p (2025A-Q15(f)).

**Binomial distribution assumptions question** (2020A-Q12(h) 4 marks, 2021A-Q11(g) 3 marks; the 2020 report specifically notes poor answers): write the assumptions (each object is independent, the probability p is the same and constant) → judge whether they are reasonable in context → give a reason.

**Past questions**: 2016A-Q20(f), 2017A-Q12(e), 2018A-Q17(f), 2020A-Q12(f), 2021A-Q11(f), 2022A-Q12(g), 2023A-Q12(e), 2023A-Q13(d), 2024A-Q10(d), 2024A-Q11(b), 2025A-Q16(f).

---

## Pattern 4: Sample size / back-calculating from an interval ★

**A. Find the minimum sample size (round up)**
- "within 0.01 with 95% confidence" ⇒ n = 1.96² × 0.25 / 0.01² = 9604 (using the exact z from the CAS gives 9603.6, which also rounds up to **9604**) (2019A-Q14(a)).
- 2023A-Q7(c): p̂ = 0.38 has already been calculated earlier, but for "at least how many birds" still use 0.5 ⇒ n = 2400.9 ⇒ **2401** (substituting 0.38 gives 2263 and loses marks).
- 2018A-Q13(b): 99%, E = 0.08 ⇒ n = 259.2 ⇒ **260** (exact wording in the key: rounds up to 260).
- 2018A-Q13(a) requires **using calculus to prove that the error is greatest when p̂ = 0.5**: E ∝ √(p̂(1−p̂)), differentiate and set it to 0 ⇒ p̂ = 0.5, then use the second derivative or a sign table to confirm it is a maximum.

**B. Back-calculate p̂, E, n and the number of people from an interval (round to the nearest whole number)**
- 2024A-Q11: p̂ = 0.70, width 0.096 ⇒ E = 0.048 ⇒ n = 1.96² × 0.21 / 0.048² = 350.1 ⇒ **350**.
- 2018A-Q13(c): (0.342, 0.558) ⇒ p̂ = 0.45, E = 0.108 ⇒ n ≈ 140.8 ⇒ 141, number of people ≈ 0.45 × 141 ≈ 63.
- 2022A-Q13(d), 2023A-Q12(c)(d): given the interval and n, back-calculate the confidence level: first find E, then find z = E/SE, and finally obtain the confidence level from z (e.g. z = 1.645 ⇒ 90%).

**C. Proportional relationships (CF)**: E ∝ 1/√n ⇒ halving the margin of error requires n × 4 (2017F-Q4); making the width 1/3 requires n × 9 (2018F-Q5: 200 → 1800).

**Past questions**: 2016A-Q10(d), 2017F-Q4, 2018A-Q13, 2018F-Q5, 2019A-Q14, 2020A-Q14, 2022A-Q12(f), 2022A-Q13(d), 2023A-Q7(c), 2024A-Q10(f), 2024A-Q11(a), 2025A-Q16(e).

---

## Pattern 5: Factors affecting interval width

| Change | Interval width | Reason |
|---|---|---|
| n increases | becomes narrower | SE = √(p̂(1−p̂)/n) becomes smaller |
| Confidence level increases (90% → 99%) | becomes wider | z becomes larger |
| p̂ closer to 0.5 | becomes wider | p̂(1−p̂) becomes larger (2025A-Q16(d)(iii): p̂ further from 0.5 ⇒ E decreases) |

When answering, write “direction + reason” together (2019A-Q14(b), 4 marks: for each of the two factors, 1 mark for the “factor” and 1 mark for the “effect”). If n becomes 4 times as large, the width is halved (2021A-Q13(f)).

**Past questions**: 2016A-Q14(c), 2019A-Q14(b), 2020A-Q12(g), 2021A-Q13(d)(f), 2022A-Q12(e), 2023A-Q12(f), 2024A-Q10(e), 2024A-Q11(c), 2025A-Q16(d).

---

## Pattern 6: Sampling bias ★ appears in most years

**Answer template** (usually 1–2 marks per source: identify the source + explain)
1. **Identify the source**: location (only outside a shopping centre/library), time (weekday morning, lunchtime), self-selection (voluntary response), wording (leading question, e.g. “or an inferior brand?”), sampling frame (only calling mobile numbers, only sampling referred medical records), convenience (the first 200 copies printed, the newest printing machine).
2. **Explain which types of people are more or less likely to be sampled**, and link to the context: time and location should be written as two separate points (2022 report). Example (2020A-Q14(c)):
   - Location: “Surveying outside the library over-represents people who already use the library, so p̂ would overestimate the proportion of residents who use it.”
   - Time: “Surveying only at lunchtime under-represents residents who work or study during the day and cannot be there then.”

**Improvement method**: randomly sample from the whole population (the whole week, all four printing machines); use random numbers to select times and subjects.

**Past questions**: 2017A-Q12(a), 2018A-Q17(c), 2019A-Q13(b)(c), 2020A-Q14(c), 2022A-Q13(b), 2023A-Q7(d), 2024A-Q10(a), 2025A-Q16(a).

---

## Pattern 7: Binomial distribution of the number of intervals

**Identification**: “20 students each compute a 90% CI. X = number of intervals containing the true proportion.”
**Approach**: X ~ Bin(20, 0.9), E(X) = 18, Var(X) = 1.8; “3 intervals do not contain p” ⇔ X = 17 (the key for 2024A-Q9(d) gives 1 mark for this conversion).
**Past questions**: 2016A-Q20(d), 2024A-Q9(b)–(d).
