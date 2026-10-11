# MAM · Continuous Random Variables and Normal Distribution — Patterns and Solution Approaches

> Source: marking keys + exam reports for 32 past exam questions from 2016–2025. Original questions: see `topics/06_Continuous_RV_Normal.pdf`. Numerical examples in this document have been checked with Python (scipy/sympy). `2016SA-Q12` refers to the 2016 official sample paper (not among the 32 questions; original paper: see `papers/2016Sample_*`).
> Review status: has been through one round of independent review and revised according to feedback (see `Review_log.md`).

## Marking-key reminders

- **Distinguish between pdf and cumulative distribution function** (2023 report: mixing up pdf and cdf is very common).
- When finding k or justifying k, always first write "total area = 1" then solve; do not just write the result (2023A-Q11(a) has 1 mark for "area under the curve must equal 1"; 2025F-Q4(a) key: no mark for simply writing the value of k without justification).
- Be able to **name the distribution** (2021 report: in CF continuous probability questions, the distribution name is a mark-losing point; the key answer for 2021F-Q2(a) is "continuous uniform distribution").
- Expected values must be converted into the units or time in context: hours to minutes; E(B) = 3.8 h after noon written as 3:48 pm (2023A-Q11(c)). 2017A-Q11 and 2023A-Q11 each have 1 mark specifically for conversion. The units of variance are squared units (e.g. L²), and must also be written (2022A-Q8(a) key: units for both expected value and variance).
- When the question specifies precision (three decimal places, exact, integer), follow it strictly (e.g. 2022A-Q12(a) has 1 mark for rounds to three decimal places); when not specified, keep at least 4 decimal places (2020 report), and do not round intermediate steps to only 2 places. Percentage questions must be converted to percentages.

---

## Pattern 1: Relative frequency histogram → probability (CF)

**Approach**: probability = sum of the relative frequencies of the corresponding bars; when an interval endpoint falls inside a bar, **interpolate linearly assuming a uniform distribution** (this is what the 2023F-Q3(c) key does). Conditional probability = intersection ÷ condition. On time all three days = p³ (assuming independence).
- For a **frequency** histogram, first divide by the total to convert to probability (2023F-Q3: 20 solar farms).
- Distinguish between a cumulative probability table P(W ≤ w) and individual probabilities (specifically mentioned in the 2023 report CF section).
- Expected value estimate: E ≈ Σ class midpoint × probability (2023F-Q3(c)(ii), 2024A-Q13(e)).
- Linear interpolation requires the question to state "assuming … uniformly distributed within each interval".

**Past questions**: 2017F-Q1, 2020F-Q4(a)(b), 2023F-Q3, 2024A-Q13(e).

---

## Pattern 2: Basic operations with pdf ★

**The four core formulas**
- Total area: ∫f(x)dx = 1 (used to find k or a);
- Probability: P(a < X < b) = ∫ₐᵇ f(x)dx;
- Expected value: E(X) = ∫x f(x)dx; variance: Var(X) = ∫x² f(x)dx − μ², or ∫(x − μ)² f(x)dx;
- Median M: ∫_{lower bound}^{M} f(x)dx = 0.5 (same for quantiles).
- **Given cumulative distribution function F(x) = P(X ≤ x)**: P(a < X ≤ b) = F(b) − F(a); pdf = F′(x) (2023A-Q11(d)(e): key gives 1 mark each for "express as P(A ≤ 4) − P(A ≤ 3)" and "find the pdf").

**CF tips**
- When the pdf consists of straight-line segments, **use triangle/trapezium areas instead of integration** (accepted by the keys for 2019F-Q3, 2022F-Q3 and 2025F-Q4).
- Piecewise pdf: integrate each segment separately; when finding k for the latter segment, set the latter segment's area = 1 − the former segment's area (2020F-Q4(d)).
- Example (2025F-Q1): f(x) = 1/(x ln 5), 1 ≤ x ≤ 5. E(X) = ∫₁⁵ 1/ln5 dx = **4/ln 5**; median: ln M / ln 5 = ½ ⇒ **M = √5**.

**CA tips**: write the integral expression (1 mark), then let CAS calculate; to find c such that P(X > c) = 0.01, write the equation ∫_c^1 f = 0.01 (2022A-Q8(b), units 10 000 L, finally convert to "nearest litre").

**Mark-earning points**: ✓ correct integral expression (including limits) ✓ calculation ✓ unit or time conversion.

**Past questions**: 2017A-Q11, 2018A-Q10, 2019F-Q3, 2020F-Q4(c)(d), 2022A-Q8, 2022F-Q6(b), 2023A-Q11, 2025A-Q13(c)(d), 2025F-Q1, 2025F-Q4.

---

## Pattern 3: Uniform distribution

**Formulas**: X ~ U(a, b): f(x) = 1/(b − a) (a ≤ x ≤ b; 0 elsewhere); E(X) = (a + b)/2; Var(X) = (b − a)²/12.
**Note**: The formula sheet only lists Var(X) = ∫(x − μ)²p(x)dx, and **does not** include (b − a)²/12. The key awards marks for "write the pdf and domain" + "write the variance integral" + "calculate the result" (2024F-Q4(a), 2019F-Q6(e), 2016A-Q16(b)). So (b − a)²/12 is only for checking; in a formal answer you must write the integral.

**Common variations**
- Given E(X) = 6 and maximum 9 ⇒ minimum 3 ⇒ f(x) = 1/6, 3 ≤ x ≤ 9 ⇒ Var = ∫₃⁹ (x − 6)²·(1/6) dx = **3** (2024F-Q4(a); can check with 6²/12 = 3).
- Conditional probability: P(X < −0.35 | X < 0) = 0.15/0.5 (2019F-Q6(c)).
- "the square is less than 0.09" ⇒ −0.3 < X < 0.3 (2019F-Q6(d), the key has one mark for "express the required probability in terms of X").
- "exactly 2 days out of 3 …" ⇒ first find the one-day probability, then use Bin(3, p) (2025F-Q4(c)).
- "latest time to leave so that the probability of being late is no more than 4%" ⇒ cut off 4% of the area from the right end of the distribution (2021F-Q2(d)).

**Past questions**: 2016A-Q16, 2017F-Q2, 2019F-Q6, 2021F-Q2, 2024F-Q4(a), 2023A-Q13(a).

---

## Pattern 4: Normal distribution — forward probability and inverse quantiles

**Approach**
1. Write the probability expression: P(X > 3.7), P(395 < X < 405) (most keys award 1 mark separately, so always write it first).
2. Use CAS normCdf to calculate, then round to the required decimal places or convert to a percentage.
3. Inverse: "heaviest 0.05%" ⇒ P(X > m) = 0.0005 ⇒ invNorm(0.9995); similarly for "top 1%".
4. Conditional probability: P(X < 75 | X > 67) = P(67 < X < 75) / P(X > 67) (2020A-Q8(b), the key has one mark for "recognising the restriction to the jumbo range").
5. Unit transformations: Y = aX + b ⇒ μ_Y = aμ + b, σ_Y = |a|σ, Var(Y) = a²Var(X) (°C → °F, km → mile; 2024A-Q13(c) asks for variance). Inverse: given μ_Y, σ_Y, set up equations to find a, b (2025A-Q10(f)).

**Past questions**: 2016SA-Q12 (sample), 2017A-Q19, 2018A-Q12(a), 2019A-Q11, 2020A-Q8, 2021A-Q8, 2022A-Q12(a), 2024A-Q13, 2025A-Q10.

---

## Pattern 5: Finding μ and σ from two probabilities ★

**Recognition**: Given two tail probabilities, find the mean and standard deviation. For example, 2016A-Q18: passengers wait for less than 55 minutes, 5% of the time, while there is a 13% chance that the waiting times will be greater than 100 minutes.

**Fixed three steps (key mark allocations)**
1. Find the two z-values separately (1 mark on its own): z₁ = invNorm(0.05) = −1.6449, z₂ = invNorm(0.87) = 1.1264.
2. Set up the system of equations: μ − 1.6449σ = 55, μ + 1.1264σ = 100.
3. Solve to get σ ≈ 16.24, μ ≈ 81.71 (2016A-Q18).

Another example (2023A-Q12): P(X ≤ 150) = 0.0228 ⇒ z = −2, P(X ≥ 165) = 0.1587 ⇒ z = 1 ⇒ σ = 5, μ = 160 (0.0228 and 0.1587 are exactly the tail probabilities for z = −2 and z = 1, so z can be taken as an integer).
When only the mean is known: one z-value is enough (2024A-Q13(a), 2019A-Q11(d)).

**Past questions**: 2016A-Q18, 2019A-Q11(d), 2023A-Q12(a), 2024A-Q13(a), 2025A-Q10(e).

---

## Pattern 6: The 68–95–99.7 rule (CF)

**Approach**: Convert values into "mean ± k standard deviations": 163 ± 3×7 = 142 to 184 ⇒ about 99.7%; 170 = μ + σ ⇒ about 16% above it; the shortest 2.5% lie below μ − 2σ.
**Graph question (2021F-Q6)**: The lower and wider the curve, the larger the standard deviation; whether P(6 ≤ X ≤ 9) ≥ 0.5: the key's reason is "total area = 1, the shaded area is clearly less than half". You can also argue this way: μ = 7, σ ≈ 3, interval width 3 = σ, and the maximum probability for an interval of width σ is only P(μ − σ/2 < X < μ + σ/2) ≈ 0.38 < 0.5. For a continuous distribution P(Y = 2) = 0, so P(Y ≥ 2) > P(Y > 2) shows Y cannot be normal, but can be binomial.

**Past questions**: 2018F-Q2, 2021F-Q6.

---

## Pattern 7: Deciding whether a model is appropriate (explanation question)

**Wording**: "The normal distribution is not appropriate because the histogram is not symmetric / is skewed to the right / is bounded at 0, whereas a normal distribution is symmetric and unbounded." or "the model gives P(X < 0) = 0.0013, but weight cannot be negative" (2018A-Q12(g)).
**Past questions**: 2018A-Q12(g), 2020A-Q16(c), 2024A-Q13(d), 2025A-Q13(a).
