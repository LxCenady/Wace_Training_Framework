# MAS · Statistical Inference (Sample Mean) — Patterns and Solution Approaches

> Basis: 17 past exam questions from 2016–2025, marking key + exam reports. Appears only in Calculator-assumed papers. Original questions: see `topics/07_Statistical_Inference.pdf`. Numerical examples have been verified with scipy. Also cites 2016 sample paper A9, A13 (original papers: see `papers/2016Sample_*`).
> Review status: has undergone one round of independent review and has been revised according to feedback (see `Review_log.md`).

## Formula card

- Sample mean: **X̄ ~ N(μ, σ²/n)** (approximate). If the population itself is normal, it is exact for any n; if the population is not normal, by the Central Limit Theorem it is approximately true when n is large enough (empirically ≥ 30), regardless of the population shape.
- Standard deviation of the sample mean (standard error): σ_X̄ = σ/√n.
- Sum of n variables: key's method is to convert "sum < T" into "X̄ < T/n" (2016A-Q19(b), 2020A-Q18(a)). Sum ~ N(nμ, nσ²) is only used for checking; key does not give this form.
- Confidence interval for μ: x̄ ± z·σ/√n (when σ is unknown, use sample standard deviation s instead); z = 1.645 / 1.960 / 2.576.
- Working backwards from an interval: x̄ = interval midpoint; z·σ/√n = half-width ⇒ can solve for σ/√n, s or n.

## Marking panel reminders

- **Write mathematical statements, not calculator language** (2016, 2017, 2018 reports): write P(X̄ > 83) = P(Z > 1.5) = 0.0668, not normCdf(83, ∞, 80, 2).
- **"State the distribution" 3 marks**: ✓ state that X̄ is approximately normal (writing n > 30 or CLT as well is safer; in each year's key the first mark only requires writing "normal") ✓ mean ✓ standard deviation σ/√n (or variance).
- **When explaining, make clear which quantity is meant**: "the standard deviation **of the sample mean** decreases", not just "standard deviation decreases", and do not use "it" (2019 report).
- **Answer the question asked**; do not copy sentences from previous years' standard answers (2025 report).

---

## Pattern 1: Write the distribution of X̄ and find probabilities ★ High frequency

**Standard procedure**
1. "By the Central Limit Theorem, since n = 100 is large, X̄ is approximately normal with mean μ = 80 and standard deviation σ/√n = 20/10 = 2."
2. Write the probability expression, then calculate.
3. "differs from μ by less than d" = P(|X̄ − μ| < d) = P(μ − d < X̄ < μ + d).
4. Sum type: 50 times total < 8.96 kL ⇔ X̄ < 179.2 L ⇒ X̄ ~ N(175, 2.1213²) ⇒ P ≈ **0.9761** (2016A-Q19(b)).

**When the population is not normal** (uniform distribution 2017A-Q9, exponential distribution 2018A-Q12, right-skewed pdf 2021A-Q15, dart distance 2025A-Q13): the method is the same as for a normal population, because n is large enough, X̄ is still approximately normal. 2018A-Q12(c) specifically tests this (2 marks: answer unchanged + reason is CLT).
**Drawing the distribution of X̄**: a bell shape centred at μ, width about ±3σ/√n, much narrower than the original distribution; if the question requires it, mark on the diagram the probability region calculated in the previous part (2017A-Q9(b) has 1 mark, 2021A-Q15(b)).

**Past exam questions**: 2016A-Q19(a)(b), 2017A-Q9, 2018A-Q12(a)(b), 2019A-Q14(a)(b), 2020A-Q18(a), 2021A-Q15(a), 2022A-Q12(a)(b), 2023A-Q13(a)(b), 2024A-Q14(a)(b), 2025A-Q13(a)(b).

---

## Pattern 2: Find the sample size n (so that a probability or interval meets a requirement)

**Standard procedure**
1. First draw a diagram to decide whether it is two-tailed, one-tailed or half-interval, then write the probability statement. Two-tailed: P(|X̄ − μ| < 0.2) = 0.98; one-tailed: P(X̄ > 25) = 0.03 ⇒ z = 1.881 (2018A-Q12(d)); half-interval: P(80 < X̄ < 82) > 0.4 ⇒ P(0 < Z < k) = 0.4, k = 1.282, n = 165 (2019A-Q14(d)).
2. Find the critical z (98% ⇒ z = 2.326).
3. Set up an equation or inequality: z·σ/√n = d ⇒ n = (zσ/d)².
4. **Rounding**: when "at least" is required, round up. Example: (2.326 × 1.5/0.2)² = 304.3 ⇒ **n = 305** (2020A-Q18(b)); 600.25 ⇒ 601 (2024A-Q14(f), when "at least" is required, round up no matter how small the decimal part is). When working backwards from a known interval to find n, take the nearest integer (2022A-Q14(a): using z = 2.576 gives 200.0 ⇒ 200, key also accepts using 2.58 to get 201; 2025A-Q13(c): 283.0 ⇒ 283, also accepts 284).

**Past exam questions**: 2016A-Q19(d), 2018A-Q12(d), 2019A-Q14(d), 2020A-Q18(b), 2022A-Q14(a), 2024A-Q14(f), 2025A-Q13(c); 2016S-A9, 2016S-A13(b) (sample paper). Finding the error bound in reverse: 2024A-Q14(c) (50% probability corresponds to m ≈ 1.7 minutes).

---

## Pattern 3: Confidence interval calculations and working backwards

**Calculation**: x̄ ± z·s/√n. Example: x̄ = 10300, s = 400, n = 100, 95% ⇒ 10300 ± 1.96 × 40 = (10221.6, 10378.4) (2017A-Q13(a): 1 mark each for centre, standard error, z, upper and lower limits).
**Working backwards**
- Upper limit 40.62, width 1.08 ⇒ x̄ = 40.08; 0.54 = 2.576 × s/20 ⇒ s ≈ **4.19** (2018A-Q16).
- Interval 150 ≤ μ ≤ 200 ⇒ x̄ = 175, σ_X̄ = 25/1.96 ≈ 12.76; after doubling the sample size, σ_X̄ = 12.76/√2 ≈ 9.02 ⇒ P(|X̄ − μ| < 10) ≈ **0.7325** (2020A-Q17).
- Given the interval and n, find the confidence level in reverse: first find z = half-width / standard error, then look up the corresponding percentage (2017A-Q13(d)).
- Changes in sample size: width ∝ 1/√n ⇒ to make the width 1/4, 16n is needed (2021A-Q17(c)); if the sample size becomes 2n, the standard error is divided by √2.

**Past exam questions**: 2016S-A13, 2017A-Q13, 2018A-Q16, 2019A-Q15, 2020A-Q17, 2021A-Q17, 2022A-Q12(c), 2023A-Q13(c)(d), 2023A-Q15, 2024A-Q14(d).

---

## Pattern 4: Interpreting confidence intervals (true/false) ★ tested almost every year (except 2016, 2020)

**Correct statements to memorise**
1. μ is a **fixed but unknown** number. A particular interval either contains μ or does not, and **there is no way to know which** (2018A-Q16(d), 2019A-Q15(d), 2021A-Q17(e), 2022A-Q14(c)).
2. "95% confidence" means that when sampling is repeated, about 95% of intervals will contain μ; **it is not** "the probability that μ lies in this interval is 95%" (2023A-Q15(c): Ali's statement is incorrect).
3. A wider interval does not mean it is more likely to contain μ (2022A-Q14(c): James is incorrect).
4. The mean of the next sample **does not necessarily** fall in this interval (2017A-Q13(b)(i)); an individual value is even less likely to, because the variation of individuals is much greater than the variation of sample means (2017A-Q13(b)(ii)).
5. Having 10 out of 50 intervals with a lower limit below 1.00 does not indicate that the setup is wrong; this is normal variation from random sampling (2023A-Q13(e)).
   **Conversely**: if, among a large number of intervals, the proportion that do not contain μ is far above 5%, that is evidence. In 2025A-Q13(e), 298 of 500 95% intervals do not contain μ = 100; key judges Chen's statement 1 (the sample is unlikely to come from a population with μ = 100) **correct**; but the cause still cannot be determined, so statement 2 (the athlete did not stand at 3.50 m) is **incorrect**.
6. Two intervals being nested or overlapping **does not** imply that the two population means are the same; nor can a lower sample mean alone be used to say the new method is better (2024A-Q14(e); key's reason for Sanjeet is: the two intervals are based on different sample sizes, so they cannot be compared directly in this way).
7. Duplicating **the same sample** to make 2n is not a new random sample, does not reflect real variation, and the interval does not truly become narrower (2022A-Q12(d)). Note: combining two **independent** random samples is valid; n is larger and precision is higher (2019A-Q15(c)).

**Writing style**: first state a position (True / False / Not correct), then give one reason in the context of the question; 1 mark each.

---

## Pattern 5: Using an interval to test a claim (does a company use more water?)

**Standard procedure (4 marks)**
1. From the new sample, find x̄ and s: 6.57 kL / 36 = 182.5 L, s = 15.
2. Construct a confidence interval for μ_new: 182.5 ± 1.96 × 15/6 = (177.6, 187.4).
3. Compare: the original μ = 175 **is not** in the interval.
4. Conclusion: there is evidence to support "WolliWorks uses significantly more water" (2016A-Q19(e)); conversely, if it is in the interval, there is not enough evidence (2020A-Q18(c)).

**Note**: you can only draw a conclusion about "whether the means are different"; you cannot infer the source of the sample (for example, Anika's claim "probably taken from 100 teenagers"), because the source is unknown (2021A-Q15(c)).

**Past exam questions**: 2016A-Q19(e), 2020A-Q18(c), 2021A-Q15(c), 2025A-Q13(d)(e).

---

## Pattern 6: Factors affecting precision

| Change | Standard deviation of X̄ | Interval width | Tail probabilities such as “X̄ > 83” (2019A-Q14: μ = 80, threshold 83 is above μ) |
|---|---|---|---|
| n increases | decreases | becomes narrower | decreases (83 is relatively more extreme) |
| Confidence level increases | — | becomes wider | — |
| σ (or s) increases | increases | becomes wider | increases |

The larger the sample and the smaller the standard error, the higher the precision (2019A-Q15(c): the combined sample 3n has the highest precision).
To compare which of two intervals is narrower: compare z·s/√n (2021A-Q17(f)).
