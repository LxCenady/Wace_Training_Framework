# MAS · Functions and Graphs — Patterns and Solution Strategies

> Basis: marking keys and exam reports for 31 past questions from 2016–2025. Original questions: see `topics/02_Functions_Graphs.pdf`. Predominantly CF (when it is the main knowledge point, CF 21 questions, CA 7 questions).
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`).

## Marking panel reminders

- **Domain of composite functions is the most frequently flagged source of lost marks in this topic**: the 2016, 2017, 2022, 2023, 2024 and 2025 reports all flagged it (2018 instead listed it as well answered). The 2017 report identifies the cause as reluctance to set up inequalities and inability to solve them.
- **Do not use "it" when explaining** (2018, 2019, 2021, 2022, 2024 reports): “g is not one-to-one because g(1) = g(−1) = 1”, not “it is many to one”.
- The range can be found using the graph of the reciprocal function (the 2019 report suggests: first draw the graph of 1/f, then read off the range).
- The antiderivative of ln must include the absolute value (2022 report; e.g. ln|x − 3| in 2020F-Q6(d)).

---

## Pattern 1: Expressions, domains and ranges of composite functions ★★

**Key principle**: f(g(x)) is defined ⇔ ① x is in the domain of g, **and** ② g(x) lies in the domain of f.

**Standard procedure**
1. Write out f(g(x)); after substituting, **do not simplify first**, or restrictions may be lost.
2. List two sets of conditions: the restrictions on g itself (denominator ≠ 0, under the square root ≥ 0, **square root in the denominator > 0**, argument of ln > 0; e.g. y = 1/√f(x) in 2025F-Q2(a) requires f(x) > 0), and the inequality obtained from “g(x) ∈ dom f”.
3. Solve the inequalities and take the intersection.

**Example**
- 2017F-Q4: f(x) = 1 − √(x − 4), g(x) = 1/x² ⇒ f(g(x)) = 1 − √(1/x² − 4). Conditions: x ≠ 0, and 1/x² ≥ 4 ⇒ x² ≤ ¼ ⇒ **−½ ≤ x ≤ ½, x ≠ 0**.
- 2022F-Q1: f(x) = √(4 − x), g(x) = 1/x² ⇒ 4 − 1/x² ≥ 0 ⇒ x² ≥ ¼ ⇒ **x ≤ −½ or x ≥ ½**.
- 2016F-Q1: g∘f = 1/ln x ⇒ domain x > 0 and x ≠ 1; range y ≠ 0.
- 2019F-Q4(d): f(h(g(x))) = 1/(√(x²) − 1) = 1/(|x| − 1), **not equal to** f(x), because √(x²) = |x|.

**Marks awarded**: usually 1 mark for each restriction (e.g. “states x ≠ 0”, “states −½ ≤ x ≤ ½”).
**Past questions**: 2016F-Q1, 2017F-Q4(c)(d), 2018F-Q1, 2019F-Q4, 2021F-Q2(d)(e), 2022F-Q1, 2023F-Q4(b)(c), 2024F-Q2(a), 2025F-Q2(a).

---

## Pattern 2: Inverse functions (existence, expression, graph)

**Standard procedure**
1. **Existence**: f must be one-to-one; this can be checked using the horizontal line test. If it is not, restrict the domain; the “largest possible domain” goes up to the vertex, e.g. x ≤ 1 (2016F-Q8(c)).
2. **Find the expression**: swap x and y (the key awards 1 mark specifically for “interchanges x, y”) → solve for y → according to **ran f⁻¹ = dom f** (i.e. the restriction from the original function's domain), **choose the sign**; dom f⁻¹ = ran f (2016F-Q8(d) key: y − 1 = −√(x + 4) since R_{f⁻¹} = D_f; the 2016 report lists this step as an area of concern).
3. **Swap domain and range**: dom f⁻¹ = ran f.
4. **Graphing**: symmetric about y = x; mark corresponding points for endpoints and intercepts, e.g. (a, b) ↔ (b, a).
5. “Is f⁻¹(−1) = 4 correct?”: check whether −1 is in the range of f. f(x) = √(x − 3) ≥ 0, so f⁻¹(−1) is undefined (2018F-Q1(c)).

**Inverse trigonometric functions (2020F-Q6, 2024F-Q8)**: y = 2 tan x ⇒ f⁻¹(x) = tan⁻¹(x/2). To differentiate, use implicit differentiation: x = 2 tan y ⇒ 1 = 2 sec²y · y′ ⇒ y′ = 1/(2(1 + tan²y)) = 2/(4 + x²).

**Past questions**: 2016F-Q8(c)(d), 2017F-Q4(a)(b), 2019F-Q5, 2019F-Q7, 2020F-Q6, 2021F-Q2, 2023F-Q4(a), 2024F-Q8, 2025F-Q2(b).

---

## Pattern 3: Graphs of reciprocal functions y = 1/f(x) ★ frequent in CF

**Graphing rules (mark-earning points in the key)**
| Feature of f(x) | Corresponding feature of 1/f(x) |
|---|---|
| Zero at x = a | Vertical asymptote x = a |
| As x → ±∞, f → ±∞ | 1/f has horizontal asymptote y = 0 |
| Vertical asymptote of f at x = b | Open circle of 1/f at (b, 0) (1/f is undefined at x = b, and 0 is removed from the range; 2025A-Q9(b)) |
| Horizontal asymptote of f at y = c (c ≠ 0) | Horizontal asymptote of 1/f at y = 1/c (in 2025A-Q9(b), y = 2 → y = 0.5) |
| Local maximum (a, m), m ≠ 0 | Local minimum (a, 1/m) (and vice versa) |
| Points where f(x) = ±1 | Points common to f and 1/f (position unchanged) |
| f > 0 / f < 0 | Sign unchanged |
| Open circle of f at (a, b), b ≠ 0 | Open circle of 1/f at (a, 1/b) (2018A-Q14(a)); if b = 0, this corresponds to a one-sided vertical asymptote (2022F-Q2) |

**Range**: read the range from the graph of 1/f, and note values that cannot be reached (2020F-Q5(b), 2024F-Q2(b), 2025A-Q9(b)).

**Past questions**: 2016F-Q8(a), 2018A-Q14(a), 2020F-Q5, 2022F-Q2(b), 2024F-Q2(b), 2025A-Q9(b).

---

## Pattern 4: Absolute value functions

**Three transformations**
- y = |f(x)|: reflect the part below the x-axis above the x-axis.
- y = f(|x|): keep the x ≥ 0 part, then mirror it about the y-axis.
- y = f(−|x|): keep the x ≤ 0 part, then mirror it to the right (2023F-Q4(d)).

**Common question types**
- Determine the parameters of y = a|x − b| + c from the graph (the vertex gives b and c, the gradient gives a) (2016A-Q12, 2017A-Q16(a)).
- |f(x)| = d has exactly 4 solutions (2016A-Q12(b), f(x) = −2|x − 3| + 5): first draw the graph of |f| (W-shaped), then use the horizontal line y = d to cut it and find the interval for d (0 < d < 5); check the endpoints d = 0 and d = 5 separately.
- Function N(k) for the number of solutions: sweep y = k across the graph of |f(x)| and record the number of intersections section by section (2020A-Q21).
- The solution set of |x + 1| = k − |x + a| is an interval ⇒ rewrite as |x + 1| + |x + a| = k. The sum of two absolute values is constant |a − 1| between −a and −1 (flat bottom), and the interval of the flat bottom is the solution set ⇒ a = 3, k = 2 (2023F-Q4(e); the key's wording is that the two graphs coincide along a line segment).
- W-shaped graph W_k(x) = |k/2 · |x − k| − k|: draw the inner expression first, then reflect; ∫_{k−2}^{k+2} W_k dx = the area of one triangle between the two zeros k ± 2 = ½·4·k = 2k (2024A-Q15).

**Past questions**: 2016A-Q12, 2016F-Q8(b), 2017A-Q16, 2018A-Q14(b)(c), 2019F-Q7, 2022F-Q2(a) (|f(x)| = x, the key requires excluding x = 0 and including x = 2), 2020A-Q21, 2023F-Q4(d)(e), 2024A-Q15, 2025F-Q2(c)(d).

---

## Pattern 5: Rational functions — determining parameters from a graph

**Approach**: x-intercept ⇒ factor in the numerator; vertical asymptote ⇒ factor in the denominator; horizontal asymptote ⇒ ratio of leading coefficients (e.g. a(x² − b)/((x + c)(x − d)) → a); repeated root (x − c)² means the graph **touches but does not cross** the x-axis there, or the asymptote has the same sign on both sides; finally use the y-intercept or a known point to determine k.

**Reasons must be written** (the key usually has 1 mark specifically for justification): e.g. “c = 3 since x = 3 is a vertical asymptote” (2023F-Q1, 2024F-Q5). When the denominator has a repeated factor (x − c)², the asymptote has the same sign on both sides (in 2023F-Q1 both sides tend to −∞); when the numerator has a repeated factor, the graph touches the x-axis there but does not cross it.

**Oblique asymptote**: polynomial division, f(x) = quotient + remainder/denominator ⇒ asymptote y = quotient (2024F-Q5(b), 2023A-Q18(a)).

**Rational function with a given axis of symmetry** (2022A-Q15): q(x) = a(x − 3)² + c, **a and c have the same sign** (key: a, b > 0) is needed to ensure there are no zeros; the result is f = 2/(x² − 6x + 10).

**Past questions**: 2018F-Q4, 2020F-Q3, 2022A-Q15, 2023A-Q18, 2023F-Q1, 2024F-Q5, 2025A-Q9(a).

---

## Pattern 6: Sketching rational functions

**Checklist (1 mark each)**: x-intercepts, y-intercept, vertical asymptotes, horizontal or oblique asymptotes, turning points (mark them if present; marks may be awarded even if the question does not explicitly ask, e.g. 2017F-Q5), and the bending direction near asymptotes (when approaching from left and right → ±∞).

**Tip**: factorise first, check for cancelled factors (holes); a form such as f(x) = x − 1 − 3/(x + 1) lets you read off the oblique asymptote y = x − 1 directly (2021F-Q4).

**Past questions**: 2017F-Q5, 2021F-Q4.
