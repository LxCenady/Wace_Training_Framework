# WACE Mathematics Methods · Cheat Sheet (Patterns + Notes)

**General rules**: show that: write every step · for optimisation questions that require using calculus, you must verify the extremum (f″ or sign table, 1 mark) · calculator in radians (if π/180 appears when differentiating sin, it is set to degrees) · include units in application questions · in explanations, state clearly "which quantity + when + how much it changes + units", in context · probabilities to at least 4 decimal places (if the question specifies 3 decimal places, exact or integer, follow that) · for CA questions, write the equation you solve and the key output; do not write calculator syntax · read the question carefully for "first / initially" (t = 0), "more than" (≥ k+1), "at least"

## 1 Differentiation and its applications

**① Direct differentiation** (CF opening 2–4 marks)
- First decide the structure: product → product; fraction → quotient; composite → chain, often used together (e.g. x² ln(4x + 3)).
- Basic formulas: (eᵏˣ)′ = keᵏˣ; (ln f)′ = f′/f; (sin kx)′ = k cos kx; (tan x)′ = 1/cos²x (2017A-Q10 requires proof using the quotient rule).
- ⚠ The method mark requires writing the two-term structure **and at least one term correct**; for (2x³+1)⁵ do not forget to multiply by 6x²; when differentiating e⁻ˣ do not miss the negative sign; if it says "do not simplify", you do not need to simplify.

**② Differentiation from table / graph values**
- First write the general formula (1 mark): (fg)′ = f′g + fg′; (g/h)′ = (g′h − gh′)/h²; [h(g(x))]′ = h′(g(x))·g′(x).
- ⚠ For composites, evaluate the inner layer first: h′(g(1)) = h′(3), not h′(1) (2019 report: poor responses on composite differentiation).
- Graph: the gradient of a straight-line segment is the derivative; at a corner (sharp point) it is not differentiable.

**③ "rate of change of f′(x)" / interpreting the derivative**
- This means finding f″(a) (recognising this is worth 1 mark by itself).
- Explanation template: "When x = a, the gradient of f is increasing at a rate of … per unit of x"; f′(a) = 0 and f″(a) < 0 ⇒ local maximum.

**④ Full function analysis** (10–15 mark extended question)
- Factorise f′, state eˣ > 0 (never zero) → solve f′ = 0 → substitute back into the **original function** to find y-coordinates (marked separately).
- Nature: f″(a) > 0 minimum, < 0 maximum; ⚠ **when f″(a) = 0 you must use a sign table instead** (2023 report).
- Points of inflection: f″ = 0 **and** f″ changes sign on both sides. ⚠ f′ = f″ = 0 alone is not enough (x⁴ has a minimum at 0).
- Sketching: label coordinates of intercepts, stationary points and points of inflection; write equations of asymptotes (for ln(x + 3), domain x > −3 and vertical asymptote are worth 1 mark separately); use open/closed circles at endpoints; concavity matches the sign of f″.
- Example: 2021A-Q12 total 15 marks = differentiation 2 + stationary points and nature 7 + points of inflection 2 + sketching 4.

**⑤ Finding coefficients from conditions / sketching from conditions**
- Passes through point f(a) = b; turning point f′(a) = 0; point of inflection f″(a) = 0; area ∫f = A. First write the general forms of f′ and f″.
- Example: 2018A-Q15's "growth pauses at t = 6, then continues increasing" ⇒ horizontal point of inflection ⇒ P′(6) = 0 and P″(6) = 0.
- Sketching from conditions (2022F-Q5): f″(−1) > 0 ⇒ minimum; only two stationary points and f′(2) > 0 ⇒ x = 1 is a horizontal point of inflection.

**⑥ Optimisation** ★
- show that: use the constraint (fixed volume, perimeter 500 m, Pythagoras relationship) to eliminate one variable, substitute into the objective function, and simplify to the form given in the question.
- Set derivative = 0, reject unreasonable solutions (r = 0, θ outside range) → **verify**: calculate A″(x₀) < 0 at the stationary point, or draw a sign table → answer with **all dimensions** (both radius and height), round as required and include units.
- If the question says "You do not need to verify", you can omit verification; if only integers are allowed, compare the values of the two adjacent integers (2020A-Q13: 74 and 75).

**⑦ Increment formula** δy ≈ f′(a)·δx
- Write δx (⚠ 1° = π/180 rad; 1 month = 1/12 year) → differentiate at the **starting point** → multiply; if asked for the new value, add f(a).
- Example: ln 2.02 ≈ ln 2 + (1/2)(0.02) = 0.703 (2021F-Q3).

**⑧ Related rates / tangents**
- dy/dt = (dy/dθ)(dθ/dt): first use the geometric relationship to write the function (lighthouse y = 12 tan θ) → differentiate → substitute the values at that time (first use y = 5 to find cos θ = 12/13).
- Tangent: the point of tangency satisfies f′(a) = gradient, f(a) = value on the tangent; tangent equation y − f(a) = f′(a)(x − a).

**⑨ Describing and interpreting** (1–3 marks each year)
- Piecewise description: "For … the company makes a loss; profit increases to a maximum of $… at x = …; then decreases."
- The maximum rate of increase is where the graph has its greatest gradient, i.e. the point of inflection (2025A-Q9(c)).

## 2 Integration and its applications

**① Antiderivatives and finding f from f′**
- ∫eᵏˣ = eᵏˣ/k; ∫cos kx = sin kx/k; ∫(ax + b)ⁿ = (ax + b)ⁿ⁺¹/[a(n + 1)] (n ≠ −1); ∫f′/f = ln f(x) + c (in exams, usually f > 0).
- Make the numerator into the derivative of the denominator: ∫(3x + 1)/(3x² + 2x + 1) = ½ ln(…) (adjusting the coefficient is worth 1 mark separately).
- Find f from f′: integrate and write + c → substitute the known point → write the full f(x), simplifying with logarithm laws if needed.

**② "Hence" integration** (common in CF)
- Fixed three steps: integrate both sides → cancel the left-hand side using FTC → split the right-hand side and rearrange.
- Example: d/dx(x ln x) = ln x + 1 ⇒ ∫ln x dx = x ln x − x + c. This is often followed by a part asking for expected value, a definite integral or area.

**③ Definite integrals from graphs**
- Split the region into rectangles, triangles and sectors; above the x-axis is positive, below is negative. ∫(f − 2) = ∫f − 2 × interval length; ∫ₐᵇ f′ = f(b) − f(a) (read the two values directly from the graph).
- Find α such that ∫₀^α f = 0: set the area above equal to the area below.

**④ FTC and functions defined by integrals** ★ (flagged repeatedly in reports)
- d/dx ∫ₐˣ f(t)dt = f(x) (answer as a function of x); if the upper limit is g(x), multiply by g′(x), e.g. D(t) = ∫₀^(πt) … ⇒ D′(t) = π·(…).
- If the lower limit is the variable: ∫ₜ³ f = −∫₃ᵗ f ⇒ derivative is −f(t).
- Sketch A(x) = ∫ₐˣ f: A(a) = 0; f changes from positive to negative ⇒ A has a maximum, from negative to positive ⇒ A has a minimum; a turning point of f ⇒ a point of inflection of A; label the value of A at endpoints.
- Determine the sign of F(x): compare the positive and negative areas between 0 and x, and refer to areas in your reasoning.

**⑤ Area**
- First find intersection points (often worth 1 mark separately) → ∫(top − bottom)dx → the integral expression must include limits and **dx** (2025F-Q5 gives 1 mark specifically for notation).
- Cases requiring splitting: finding area between the curve and the x-axis when the curve crosses the x-axis; or when the top/bottom relationship of two curves swaps. Also split when the upper/lower boundaries are made up of multiple functions (2024 report).
- Rectangle subtraction: area enclosed by y = eˣ, y = 2 and the y-axis = 2 ln 2 − ∫₀^(ln2) eˣ dx = 2 ln 2 − 1.
- Inverse function area: ln x lies below the x-axis when x < 1, so add a negative sign (2020A-Q11(e)).

**⑥ Definite integral equations with parameters**: evaluate the expression containing the parameter = given value, then solve (ln b − ln a = ln 3 ⇒ b = 3a).

**⑦ Riemann sums**
- For a lower sum take the smaller function value on each subinterval, for an upper sum take the larger; **for increasing functions the left endpoint underestimates and the right endpoint overestimates; for decreasing functions it is the opposite** (1/x). The explanation is worth 1 mark separately.
- Best estimate = (L + U)/2; ways to improve: add more rectangles, or find the function and integrate.

**⑧ Contextual applications**: cross-sectional area × length (width) = volume; total change = ∫rate of change; when the water level is unknown, first write the cross-sectional area as a function of h (with h in the upper limit), then solve for h; make sure units are consistent (cm and m).

## 3 Rectilinear motion

**Concept comparison**
- Displacement x can be positive or negative; "at rest" ⇔ v = 0; changing direction ⇔ v **changes sign** (v touching 0 and returning to the original sign does not count, e.g. v = (t − 2)²).
- Returning to the starting point ⇔ x(t) = x(0); passing through the origin ⇔ x(t) = 0 (the two are the same only when x(0) = 0).
- Time terminology: "first appears / initially" is t = 0 (2024 report: many substituted t = 1); "during the fifth second" is 4 ≤ t ≤ 5.

**① Speeding up or slowing down** ★
- v and a have the **same sign** ⇒ speeding up; **opposite signs** ⇒ slowing down. ⚠ Just saying "acceleration is negative" does not get the mark (exact wording in the 2024F-Q2 key).
- ⚠ The 2018A-Q11(c) key treats "heading south and decelerating at 0.5" as a = −0.5; for wording like this, state your interpretation and positive direction.

**② Working backwards by integrating a(t) or v(t)**
- Add a constant at each integration; use v(0), x(0) to determine the constants; with two position conditions, solve simultaneously to find the parameters and constants (2017A-Q20: p = 12).
- For trigonometric integrals, divide by the inner coefficient: ∫2 sin(t/3 + π/6) dt = −6 cos(t/3 + π/6) + C.

**③ Distance travelled and change in displacement** ★ examined every year
- Distance travelled: solve v = 0 to find all stopping times → split into intervals → put a negative sign in front of the integral for the interval where v < 0 (or add absolute values for each interval) → sum with units. The sign is worth 1 mark on its own, and **writing dt in every integral** is also worth 1 mark (2023A-Q8(c)).
- It can also be written as |x(t₁) − x(0)| + |x(t₂) − x(t₁)| + … (2024F-Q2(d)).
- Interpreting ∫ₐᵇ v dt: "the change in displacement from t = a s to t = b s" (the start and end times must be written; 1 mark on its own).
- ⚠ Do not directly use x(final) − x(initial) as distance travelled.

**④ Maximum velocity / acceleration zero**
- At an interior extremum of the interval, a = 0 must occur, but the converse is not necessarily true (in a constant-velocity interval, a is always 0); verify using v″ < 0 or a sign table (marks are available when the question requires using calculus).
- When finding maximum **speed**, also compare |v| at the endpoints.

**⑤ Interpreting graphs and sign tables**: Use the sign of a to explain whether v is increasing or decreasing; the two parts before and after are worth 1 mark each; when there is only a sign table for x, v, and a: x changes sign ⇒ passes through the origin, v changes sign ⇒ stops and turns around, v and a have opposite signs ⇒ slowing down.

## 4 Exponentials and logarithms

**① Logarithm laws and expressing in letters** (CF)
- log(mn) = log m + log n; log(m/n) = log m − log n; log mᵏ = k log m; change of base logₐb = log_c b / log_c a.
- Write constants as logarithms: 4 = ln e⁴, 2 = log₁₀100, 9 = log₁₀10⁹ (this is a key step in several questions).
- Example: p = ln 2, r = ln 5 ⇒ ln 6.25 = ln(5²/2²) = 2r − 2p; m = log₃6, n = log₆5 ⇒ log₃10 = (m − 1) + mn; e^(ln2 + ln3) = 6.

**② Solving exponential / logarithmic equations** (CF exact values)
- Collect like terms: 4e²ˣ = 81 − 5e²ˣ ⇒ e²ˣ = 9 ⇒ x = ln 3.
- Quadratic in eˣ: let u = eˣ, factorise, discard u ≤ 0.
- Logarithmic equations: first combine into a single logarithm, then remove the log; ⚠ check the domain, 2 ln x = … only the positive root is allowed (2025F-Q7 only awards marks for one solution).

**③ Logarithmic graphs and transformations**
- y = m logₐ(x − p) + q: vertical asymptote x = p, passes through (p + 1, q); determine p from the asymptote, then substitute two points to solve for m and q.
- Graphing is worth 3 marks: asymptote (draw it and write its equation), one special point, correct shape.
- Transformations: ln 4x = ln x + ln 4 (vertical translation up); ln√x = ½ ln x (vertical dilation); ln x + 4 = ln(e⁴x) (horizontal dilation); log₂(1/(x − 1)) = −log₂(x − 1).
- When reading values from a graph, show the reading process on the graph (2024A-Q15 "show clearly how you used the graph").

**④ Growth / decay model P = P₀eᵏᵗ** ★ high frequency in CA
- Initial value: t = 0; find k from the half-life ½ = e^(k·T½); reaching a certain value: set the model equal to the target value and solve using ln.
- Convert to a time and **round as required by the question**: e.g. 4e^(−0.05t) = 2.5 ⇒ t ≈ 9.40 h ⇒ 9 am + 9 h 24 min = 6:24 pm (for "latest", round down; 6:25 is already too late).
- Rate of change dP/dt = kP: if asked for rate of change, give the signed value; if asked for rate of decrease, write it as a positive number and state decreasing.
- Piecewise model: the initial value of the later piece equals the value at the end of the earlier piece; long-term behaviour: as t → ∞, e^(−kt) → 0.

**⑤ Logarithmic scales** (decibels, Richter, site rankings)
- L = k·log(I/I₀) ⇒ I₂/I₁ = 10^((L₂ − L₁)/k). ⚠ k differs between questions: decibels k = 10 (90 dB is 1000 times 60 dB); sound pressure k = 20; Richter k = 1; site ranking k = 2.
- The difference in readings is not the answer; it must also be converted to a power of 10; to find I₀: substitute a set of (L, I) and then convert to exponential form.
- log P is a straight line against t ⇒ P = 10^B·(10^A)ᵗ; use the slope to compare growth rates.

**⑥ Logarithmic model + differentiation**: determine parameters from known points (A(0) = 21, A(1) = 53 ⇒ c = 21, b = 64); ds/dD = 40.6/D decreases as D increases, use this to draw a conclusion; round quantity down; 1 < x < 2 belongs to "week 2".

## 5 Discrete random variables and the binomial distribution

**① Distribution tables**
- For equally likely outcomes, list the sample space (for two dice, use a table); when there are unknowns, use ΣP = 1 and E(X) = μ to set up two equations (1 mark each).
- From the cumulative distribution P(X ≤ x): P(X = k) = F(k) − F(k − 1); conditional probability P(X = 1 | X ≤ 3) = P(X = 1)/P(X ≤ 3).
- For a new variable, split into cases: number unsold Y = max(0, 3 − X).

**② Expectation, variance, linear transformations**
- E(X) = Σxp; Var(X) = Σx²p − μ²; E(aX + b) = aE(X) + b; Var(aX + b) = a²Var(X); SD(aX + b) = |a|·SD.
- ⚠ Var(25 − 2X) = 4Var(X); a constant does not affect the variance.
- Scaling to a new mean and standard deviation: **find a from the SD first** (take a > 0 to preserve the ranking order), then find b from the mean. A cost increase of 20% plus an extra $1 ⇒ new mean 1.2μ + 1, new SD 1.2σ.

**③ Game / fundraising expectation** (examined in 6 out of 10 years)
- First define the payoff variable; be clear whose perspective you are taking (player or organiser) → make a "net payoff + probability" table → E = Σ(value × probability) → state a conclusion ("on average / in the long run").
- Pricing: set the expected profit equal to the target; minimum charge = expected payout (2025A-Q8: E = 0.8, $5 per red ball ⇒ at least $4).

**④ Binomial distribution** ★
- Write X ~ Bin(n, p); usually the name is worth 1 mark and the parameters 1 mark; state what n and p mean in context.
- E = np, Var = np(1 − p); work backwards from the mean and variance: np = ½, np(1 − p) = 5/12 ⇒ p = 1/6, n = 3.
- Boundaries: more than three ⇒ X ≥ 4; system has fewer than 2 working ⇔ at least 4 broken; change parameters when the situation changes (remove one ⇒ Bin(4, p)).
- Assumptions (2 marks): trials are **mutually independent**; the probability of success **p is the same and constant**, write in context. "Two outcomes" and "n fixed" are usually given in the question; writing them may not earn marks.
- Not binomial: the number of trials is not fixed; sampling without replacement makes the trials not independent (improvement: sample with replacement).
- For very small probabilities, keep more decimal places (2019A-Q18(c) about 0.00003; the key requires at least 5 decimal places).

**⑤ Normal → binomial**: first use the normal distribution to find the single-item probability p (keep enough decimal places) → Y ~ Bin(n, p) (write "binomial" and the parameters) → find P(Y ≥ k).

**⑥ Paths and counting**: translate the event into the number of successes. Example: returning to the origin ⇔ number of forward steps = number of backward steps (impossible with an odd number of steps, probability 0; write a reason); moving forward ≥ 20 cm (5 cm per step) ⇔ at least 7 forward steps out of 10.

## 6 Continuous random variables and the normal distribution

**① Histogram → probability** (CF)
- Add relative frequencies; for a **frequency** histogram, first divide by the total number.
- If an endpoint falls inside a bar, interpolate proportionally (provided the question states "uniform distribution within classes"); E ≈ Σ class midpoint × probability; distinguish cumulative probability tables from individual probabilities.

**② The four pdf essentials**
- Total area = 1 (write this step when finding k or proving k); P(a < X < b) = ∫ₐᵇ f; E = ∫x f; Var = ∫x²f − μ² or ∫(x − μ)²f; median ∫^M f = 0.5.
- Given cdf F(x): P(a < X ≤ b) = F(b) − F(a); pdf = F′(x).
- In CF papers, for pdfs made of straight-line segments, use triangle and trapezium areas; for piecewise pdfs, integrate each piece separately.
- Example: f = 1/(x ln 5), 1 ≤ x ≤ 5 ⇒ E = 4/ln 5, median √5.
- Convert the expectation to the context units or time (3.8 h after noon ⇒ 3:48 pm); the units of variance are squared units.

**③ Uniform distribution**
- f = 1/(b − a), write the domain a ≤ x ≤ b and 0 otherwise; E = (a + b)/2.
- ⚠ For variance, answer with an integral expression (the key gives 1 mark each for "pdf and domain" and "integral expression"); (b − a)²/12 is not on the formula sheet, so use it only to check. Example: E = 6, maximum value 9 ⇒ U(3, 9), Var = ∫₃⁹ (x − 6)²/6 dx = 3.
- Conditional probability: P(X < −0.35 | X < 0) = 0.15/0.5; X² < 0.09 ⇔ −0.3 < X < 0.3.

**④ Normal distribution**
- Write the probability statement first (most keys award 1 mark separately) then calculate; for inverse quantile: P(X > m) = 0.0005 ⇒ invNorm(0.9995).
- Conditional probability: P(X < 75 | X > 67) = P(67 < X < 75)/P(X > 67).
- Linear transformation Y = aX + b: μ_Y = aμ + b, σ_Y = |a|σ, Var(Y) = a²Var(X); you may also have to work backwards to find a, b from μ_Y, σ_Y.

**⑤ Finding μ, σ from two tail probabilities** ★
- Find two z-values (1 mark) → set up simultaneous equations → solve. Example: 5% below 55, 13% above 100 ⇒ z = −1.6449, 1.1264 ⇒ σ ≈ 16.24, μ ≈ 81.71.
- P(X ≤ 150) = 0.0228, P(X ≥ 165) = 0.1587 correspond exactly to z = −2, z = 1 ⇒ σ = 5, μ = 160. When only the mean is known, one z is enough.

**⑥ 68–95–99.7** (CF): write values as μ ± kσ; the flatter and wider the curve, the larger σ; the probability of an interval of width σ is at most about 0.38.

**⑦ Reasons a normal model is unsuitable**: histogram is asymmetric or skewed; variable is bounded; model gives impossible values (e.g. P(weight < 0) > 0).

## 7 Sample proportions and confidence intervals

**① Distribution of p̂**
- Write "approximately normal (n sufficiently large) + mean p + variance p(1 − p)/n", 3 marks in total, then find the probability.
- Distribution is not symmetric (e.g. n = 36, p = 0.05) ⇒ the normal approximation cannot be used.
- As n increases ⇒ the standard deviation of p̂ decreases and the distribution becomes more concentrated ⇒ probabilities such as P(p̂ ≤ 0.03) increase (1 mark for each point).

**② Calculating a confidence interval**
- p̂ ± z√(p̂(1 − p̂)/n), z = 1.645 (90%) / 1.960 (95%) / 2.576 (99%); round to the required number of decimal places.
- Work backwards from the interval: p̂ = midpoint, E = half-width; given the interval and n, find the confidence level: z = E/SE, then look up the percentage.

**③ Sample size** ⚠ most error-prone
- When finding the minimum sample size (minimum / guarantee / ensure margin at most), **always use p̂ = 0.5**, even if p̂ has already been calculated earlier (2023A-Q7(c): using 0.5 gives 2401, substituting 0.38 gives 2263, losing marks). Only substitute a particular sample proportion if the question explicitly says to use it.
- "At least" ⇒ round up (259.2 ⇒ 260); working back from an interval to the original n ⇒ round to nearest integer (350.1 ⇒ 350).
- Proportional relationships: halving the error ⇒ n × 4; width becomes 1/3 ⇒ n × 9.

**④ Using an interval to test a claim** ★ appears every year
- Two sentences: "The claimed value … is (not) within the CI …" + "so there is sufficient / insufficient evidence to conclude …". ⚠ You must take a position; you cannot avoid it by saying "cannot be 100% certain" (2023 report).
- Two intervals overlap ⇒ insufficient evidence to say the two are different.
- If asked "does it **prove** … / was a mistake made" ⇒ answer **No**: not all intervals contain p, and we do not know whether this interval happened to miss it (2025 report).

**⑤ Factors affecting interval width** (1 mark for factor + 1 mark for effect): increasing n makes it narrower; increasing the confidence level makes it wider; the closer p̂ is to 0.5, the wider it is.

**⑥ Sampling bias**
- How to write: identify the source + explain **which types of people are more or less likely to be sampled** + link to the context; time and location are two sources and must be written separately (2022 report).
- Common sources: location (only outside shopping centres and libraries), time (weekday lunchtime), voluntary response, leading questions, sampling frame (mobile phones only), convenience sampling (the first 200 copies printed).
- Improvement: random sampling across the whole population (the whole week, all printing presses).

**⑦ Other common question types**
- The number of p-containing intervals among k 90% intervals ~ Bin(k, 0.9); "3 intervals do not contain p" ⇔ X = k − 3.
- Assumptions of the binomial distribution: write the assumptions → decide whether they are reasonable in context → give reasons.
