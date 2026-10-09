# MAM · Discrete Random Variables and the Binomial Distribution — Patterns and Solution Approaches

> Based on: 27 past exam questions on discrete random variables from 2016–2025 with marking keys + exam reports (the 2016 official sample paper `2016S-F4` is also cited; original paper in `papers/2016Sample_*`). Original questions are in `topics/05_Discrete_RV.pdf`. Numerical examples in this document have been checked with Python.
> Review status: one round of independent review has been completed and revisions have been made according to feedback (see `Review_log.md`).

## Marking panel reminders

- **Recognising a binomial distribution and stating the parameters**: "State the distribution" is usually 1 mark for the name and 1 mark for the parameters (occasionally combined into 1 mark, e.g. 2023A-Q13(b)); write it as X ~ Bin(5, 0.05). 2020 report: many did not recognise that 2020F-Q1 was a binomial distribution, and when finding the mean and variance in (c) they calculated in an unnecessarily complicated way.
- **Writing the probability expression** (e.g. P(X ≥ 4) = 1 − P(X ≤ 3)) is worth 1 separate mark in most questions; do not just write the calculator result.
- Keep intermediate probabilities to at least **4 decimal places** (2020 report: keeping only 2 decimal places makes later answers inaccurate). For very small probabilities, keep enough significant figures: the answer to 2019A-Q18(c) is about 0.00003, and the key requires at least 5 decimal places.
- **Distinguish between the probability distribution and the cumulative distribution**: do not mix up tables of P(X = x) and P(X ≤ x) (2023 report).
- Questions of the "Explain / justify / state assumptions" type must be answered in context (the 2020 report specifically names 9(c) and 12(h)).

---

## Pattern 1: Completing a distribution table / finding unknown probabilities

**Approach**
1. Equally likely cases: list the sample space, e.g. use a 4×4 table for the sum of two four-sided dice (2016A-Q15); for selection without replacement, use the multiplication rule or combinations.
2. When there are unknowns a, b: solve simultaneously using **ΣP = 1** (1 mark) and **E(X) = Σx·P = μ** (1 mark) (2019A-Q10).
3. Construct a distribution table from raw data: frequency ÷ total (2018F-Q4).
4. Given the cumulative distribution P(X ≤ x): P(X = k) = P(X ≤ k) − P(X ≤ k−1) (2024F-Q3).
5. New variable (e.g. number of unsold cakes Y = max(0, 3 − X), i.e. Y = 3 − X when X ≤ 3, and Y = 0 when X ≥ 3): Y = 0 corresponds to X ≥ 3 ⇒ P(Y=0) = P(X=3) + P(X=4) (2020A-Q9(c)).

**Past exam questions**: 2016A-Q15, 2018F-Q1(a), 2018F-Q4, 2019A-Q10, 2020A-Q9, 2024F-Q3, 2025A-Q8(a).

---

## Pattern 2: Expected value, variance and linear transformations

**Formulas**: E(X) = Σx·p; Var(X) = Σx²p − [E(X)]²; E(aX + b) = aE(X) + b; Var(aX + b) = a²Var(X); SD(aX + b) = |a|·SD(X).

**Common pitfalls**
- Var(25 − 2X) = 4Var(X): the coefficient is (−2)² = 4, and **the constant 25 has no effect on the variance** (key's wording: uses a positive factor of four).
- Scaling to a new mean and standard deviation (2016A-Q17(c)): **use the standard deviation to determine a first** (|a|·22 = 15 ⇒ a = 15/22, take a > 0 to preserve the ranking order), then use the mean to determine b (75a + b = 60 ⇒ b = 195/22). The first mark in the key is "determines change on standard deviation first".
- Costs rise by 20% and then an extra $1 is charged (2018A-Q12(f)) ⇒ new mean = 1.2μ + 1, new standard deviation = 1.2σ (adding a constant does not affect the standard deviation).

**Past exam questions**: 2016A-Q17, 2017A-Q19(c), 2018A-Q12(d)–(f), 2019A-Q10(b), 2023F-Q3(d), 2025A-Q8(b).

---

## Pattern 3: Expected return from games / fundraising ★ high frequency (appeared in 6 of the last 10 years: 2017, 2020, 2021, 2022, 2024, 2025)

**Identification**: "expected profit/loss", "who is better off in the long term", "what should be charged", "is it a good idea for the organisers".

**Standard process**
1. Define the return variable (**from whose perspective**: player or organiser).
2. Make a table of "net return for each outcome + probability".
3. E(return) = Σ value × probability.
4. State the conclusion: E < 0 means the player loses in the long run; say "on average / in the long run".
5. Pricing: set expected profit = target (e.g. 20% of the charge) and solve; "minimum charge so that expected profit is not negative" = expected payout (2025A-Q8(c): E(X) = 0.8, $5 per red ball ⇒ charge at least $4).

**Scoring points (2017A-Q13, 9 marks total)**: (a)–(c): ✓ top row of the return table ✓ probabilities ✓ expectation expression ✓ expected value ✓ new expected payout ✓ conclusion (who is better off) ✓ explain the meaning of expectation; (d): ✓ set up equation ✓ solve for the charge.

**Past exam questions**: 2017A-Q13, 2020A-Q9(b), 2021A-Q13(c), 2022A-Q9(c)–(f), 2024A-Q14(c)–(e), 2025A-Q8(c).

---

## Pattern 4: Bernoulli and binomial distributions

**Identification**: fixed number n of trials, only two outcomes each time, trials independent, constant probability of success p, asks for "number of …".

**Approach**
1. **Write X ~ Bin(n, p)**, and state what n and p mean in context.
2. P(X = k) = C(n,k)pᵏ(1−p)ⁿ⁻ᵏ; CF papers require hand calculation (2018F-Q1(e): Bin(5, 0.8), P(X=2) = 10 × 0.8² × 0.2³ = 32/625).
3. E(X) = np, Var(X) = np(1−p). **Find n and p from the mean and variance** (2024F-Q4(b)): np = ½, np(1−p) = 5/12 ⇒ 1 − p = 5/6 ⇒ p = 1/6, n = 3 ⇒ P(W=1) = 3 × (1/6) × (5/6)² = 25/72.
4. Get the boundaries right for "at least / at most / more than": more than three ⇒ X ≥ 4; system fails if fewer than 2 work ⇒ 4 or more fail.
5. Change the parameters when the situation changes: after removing one alarm it becomes Bin(4, 0.05) (2019A-Q18(d)).

**Assumptions question (2 marks)**: prefer these two — the objects are **mutually independent**; the success/failure **probability is the same and constant** for each object (the keys for 2019A-Q18(b) and 2020A-Q12(h) only give these two types). "Only two outcomes" and "n is fixed" are generally given in the question and should not be written as assumptions. Write them in context, e.g. "the failure of one alarm does not affect another". 2020A-Q12(h) also requires discussing whether the assumptions are reasonable.

**Why it is not binomial** (2024A-Q14(b), 2025A-Q8(d)): the number of trials is not fixed; selection without replacement means the trials are not independent and p changes. Improvement: sample with replacement.

**Past exam questions**: 2016S-F4, 2018F-Q1, 2019A-Q18, 2020F-Q1, 2021A-Q13, 2022A-Q9, 2025A-Q15.

---

## Pattern 5: Combined with the normal distribution ("at least k out of n items …")

**Identification**: first use the normal distribution to find the probability p that a single item meets the condition, then ask how many out of n items meet it.

**Two-step method**
1. Normal: p = P(X > 3.7). Keep enough decimal places.
2. Binomial: Y ~ Bin(20, p), find P(Y ≥ 10). **The key requires writing "binomial" and the parameters**, usually 1 mark for the name and 1 mark for the parameters (2017A-Q19(b), 2018A-Q12(b), 2023A-Q12(b)).

**Past exam questions**: 2017A-Q19(b), 2018A-Q12(b), 2019A-Q11(b), 2021A-Q8(d), 2023A-Q12(b); 2023A-Q13(b) is similar, but the single-item probability comes from a uniform distribution.

---

## Pattern 6: Path / combinatorial counting type (robot, Lucky 7)

**Approach**: first translate the event into a condition on the "number of successes". For example, the robot returning to the origin ⇔ number of forward steps = number of backward steps (an odd number of steps cannot return to the origin, the probability is 0, and the reason must be written); forward ≥ 20 cm ⇔ number of forward steps − number of backward steps ≥ 4 ⇔ forward at least 7 times out of 10, then calculate using the binomial distribution (P ≈ 0.3823).

**Past exam questions**: 2025A-Q15. Related counting or geometric probability: 2021A-Q10(b) (list the combinations with sum ≥ 7, weighted sum gives p = 7/24, no binomial needed), 2023A-Q13(a) (θ is uniformly distributed, geometric probability α/π).
