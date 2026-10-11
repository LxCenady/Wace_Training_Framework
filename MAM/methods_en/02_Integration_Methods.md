# MAM · Integration and Its Applications — Patterns and Solution Approaches

> Basis: marking keys + exam reports for a total of 39 past exam questions containing integration, 2016–2025. Original questions in `topics/02_Integration.pdf`. Integration is mainly Calculator-free (when it is the main knowledge point: CF 16 questions, CA 7 questions). Also cites 2 questions from the 2016 sample paper (`2016S-F1`, `2016S-A20`; original paper in `papers/2016Sample_*`).
> Review status: has been through one round of independent review and revised in line with feedback (see `Review_log.md`).

## First, remember: where the marking panel repeatedly deducts marks

- **FTC (Fundamental Theorem of Calculus) has repeatedly been called out in reports** (2016, 2017, 2018, 2022, 2025 reports): not recognising the different uses of the FTC; the 2022 report specifically calls out the FTC combined with the chain rule (when the upper limit is g(x), multiply by g′(x)).
- **Area ≠ integral**: parts below the x-axis must be taken as absolute value, or subtracted piecewise (all 4 marks of 2018A-Q16(b) are here).
- **dx must be written after the integral sign** (2023 report: marks deducted for notation; 2025F-Q5 awarded 1 mark for "uses correct notation including dx on all integrals").
- **Areas whose upper/lower boundaries are made up of multiple functions** must be split into multiple integrals (called out in the 2024 report).
- **Indefinite integrals must include + c** (the key sometimes gives 1 mark for this on its own).
- **"Show that" — you must not skip steps**.

---

## Pattern 1: Basic indefinite integrals and finding f from f′

**Recognition**: "Determine ∫…dx", "If f′(x) = …, find f(x) given f(0) = −2".

**Approach**
1. Memorise the antiderivatives: ∫eᵏˣdx = eᵏˣ/k; ∫cos kx dx = sin kx / k; ∫(ax+b)ⁿdx = (ax+b)ⁿ⁺¹/[a(n+1)] (n ≠ −1); ∫f′/f dx = ln|f| + c (in exams f(x) > 0 generally, and the key usually writes ln f(x) + c).
4. **Evaluating definite integrals** (commonly 3 marks in CF): ✓ antiderivative ✓ substitute the upper and lower limits ✓ simplify to an exact value (2017F-Q6(a), 2021F-Q4(b), 2023F-Q1(b), 2023F-Q2(a)(iii)).
2. **When the numerator is a multiple of the derivative of the denominator**: first pull out the coefficient, e.g. ∫(3x+1)/(3x²+2x+1)dx = ½∫(6x+2)/(…)dx = ½ln(…) + c. The key gives 1 mark specifically for "modifies the integrand so the numerator is the derivative of the denominator".
3. Finding f from f′: integrate and write + c → substitute the known point to find c → write the full f(x). When the answer involves ln, simplify using log laws (e.g. ln 32 − ln 4 = ln 8).

**Mark allocation**: ✓ correct antiderivative ✓ include the constant c ✓ substitute the point to find c ✓ write the final expression (simplified as required).

**Past questions**: 2018F-Q3(c)(d), 2019F-Q1(c), 2021F-Q1(c), 2021F-Q4(a), 2022F-Q1(b), 2024F-Q1(b), 2020A-Q10(b).

---

## Pattern 2: "Hence" — use the derivative just found to find the integral ★ CF frequently tested

**Recognition**: (a) first find d/dx(x ln x) or d/dx(2x sin 3x) (2017F-Q8); (b) "Hence show that ∫ln x dx = x ln x − x + c".

**The three fixed steps** (the key usually awards marks by these three steps: 2017F-Q8 and 2022F-Q6 are exactly 3 marks; 2018F-Q7 is split into 4 marks, 2023F-Q2 is combined into 2 marks)
1. **Integrate both sides**: ∫ d/dx(x ln x) dx = ∫(ln x + 1)dx.
2. **Apply the FTC to the left side**: left side = x ln x (the antiderivative and derivative cancel).
3. **Split the right side and rearrange**: x ln x + c₁ = ∫ln x dx + x + c₂ ⇒ ∫ln x dx = x ln x − x + c (the two constants are combined into c).

**Common errors**: writing the conclusion directly; forgetting + c; not splitting the right side using linearity.

**Past questions**: 2016F-Q2(b), 2017F-Q8(b), 2018F-Q7(b), 2022F-Q6(a)(ii), 2023F-Q2(c)(ii). This is usually followed by a further part that uses this result to find an expectation, definite integral or area (2022F-Q6(b)(ii), 2023F-Q2(c)(iii), 2018F-Q7(c)).

---

## Pattern 3: Definite integral = signed area (reading values from a graph)

**Recognition**: a graph made up of line segments, semicircles or quarter-circles is given, and you are asked for ∫₀¹² f(x)dx, ∫(f(x) − 2)dx, ∫f′(x)dx.

**Approach**
1. Split the region into rectangles, triangles and sectors; **above the x-axis is positive, below is negative**.
2. ∫(f(x) − k)dx = ∫f dx − k·(length of the interval).
3. ∫ₐᵇ f′(x)dx = f(b) − f(a) (FTC; read the two function values directly from the graph).
4. To find α such that ∫₀^α f = 0: set the positive area above equal to the negative area below and set up an equation.

**Mark allocation**: ✓ split areas ✓ add with signs ✓ result (exact value, including π).

**Past questions**: 2016S-F1, 2016F-Q7, 2022F-Q2.

---

## Pattern 4: FTC and functions defined by integrals ★ Frequently tested (appears in 2016–18, 2021–23, 2025), and repeatedly called out in reports

**Recognition**: A(x) = ∫ₐˣ f(t)dt; d/dx ∫ₐ^{g(x)} f(t)dt; d/dt ∫ₜ³ f(x)dx; "Sketch A(x)", "Is F(2π) positive or negative?".

**Core formulas**
- d/dx ∫ₐˣ f(t)dt = f(x) (the result must be written as a function of x);
- d/dx ∫ₐ^{g(x)} f(t)dt = f(g(x))·g′(x) (2022A-Q15: D(t) = ∫₀^{πt}… ⇒ D′(t) = π·√(1+3cos²(πt)));
- when the lower limit is the variable, swap the limits first: ∫ₜ³ f = −∫₃ᵗ f, so the derivative is −f(t) (2022F-Q1(c));
- ∫ₐᵇ f′(x)dx = f(b) − f(a) (2018A-Q16(a), 2023F-Q2(a)(iii), 2016F-Q4(c)).
- Linearity + integral function: ∫₂⁴ (f + 2)dx = F(4) − F(2) + 4 (2023F-Q5(b)).

**Rules for sketching A(x) (the integral function)**
- A(a) = 0 (at the lower limit); mark the zeros of A;
- where f changes from positive to negative, A has a local maximum; where f changes from negative to positive, A has a local minimum;
- turning points of f correspond to points of inflection of A;
- whether A is increasing or decreasing is determined by the sign of f; mark the value of A at the endpoints.

**Deciding whether F(x) is positive or negative (2025F-Q2)**: F(x) equals the signed area from 0 to x; look at whether the positive or negative area on the graph is larger. The reason must refer to the areas — you cannot just state the conclusion.

**Past questions**: 2016F-Q5, 2016S-A20, 2017A-Q15(a), 2018A-Q16, 2021F-Q4(c), 2022A-Q15, 2022F-Q1(c), 2023F-Q5(b)(c), 2025F-Q2.

---

## Pattern 5: Area under a curve / between curves

**Recognition**: "Determine the (exact) area bounded by …", or "Write an integral expression for the area".

**Approach**
1. **Find the intersection points first** as the limits of integration (the intersection points themselves often earn 1 mark).
2. Decide which is on top: area = ∫(top − bottom)dx.
3. When finding the area between a curve and the x-axis and the curve crosses the x-axis, or when the top/bottom relationship between the two curves swaps, you must **split into pieces** (when finding only the area between two curves, a curve crossing the x-axis does not by itself require splitting).
4. When the area is not convenient to integrate with respect to x, use "rectangle − area under the curve", e.g. the area bounded by y = eˣ, y = 2 and the y-axis = 2·ln 2 − ∫₀^{ln2} eˣ dx (2017F-Q5, 2019F-Q5).
5. Inverse-function area (2020A-Q11(e)): first recognise that the inverse of eˣ is g(x) = ln x (1 mark on its own); then note that ln 2 ≈ 0.69 < 1, so the region is **below** the x-axis, and the area = −∫_{ln2}^{1} ln x dx (or written as ∫_{ln2}^{1} −ln x dx).
6. "Why are the two areas equal?": the two functions are moved by the same translation, so the shape is unchanged (2021F-Q5(b), two points: translated in the same direction and by the same distance, shape unchanged).

**Mark allocation**: ✓ intersection points/limits ✓ correct integral expression (integrand + limits + dx) ✓ antiderivative ✓ exact value.

**Past questions**: 2016A-Q13(d), 2016F-Q6, 2017F-Q5, 2018F-Q7(c), 2019F-Q5, 2020A-Q11(d)(e), 2021F-Q5, 2025F-Q5.

---

## Pattern 6: Definite integral equations with an unknown parameter

**Recognition**: "If the area … is to equal 2, determine the exact value of k", "∫ₐᵇ 1/x dx = ln 3, find the relationship between a and b".

**Approach**: write down the integral → use the FTC to obtain an expression in terms of the parameter → set it equal to the given value → solve the equation (often using log laws: ln b − ln a = ln 3 ⇒ b = 3a).

**Past questions**: 2017F-Q5(b), 2021F-Q7(a)(ii), 2020A-Q10(d).

---

## Pattern 7: Riemann sums (rectangle estimates)

**Recognition**: Rectangles are drawn on the diagram, "demonstrate and explain why L < ∫ < U", "best estimate", "state one way to improve".

**Approach**
1. The lower sum uses the **smaller** function value on each subinterval (left endpoint or right endpoint, depending on whether the function is increasing or decreasing), and the upper sum uses the **larger** value; write out each expression separately.
2. **Explanation**: When the function is increasing on the interval, the left-endpoint rectangles are all below the curve, so it is an underestimate, and the right-endpoint rectangles are an overestimate; **when the function is decreasing, the opposite is true** (e.g. 1/x in 2021F-Q7). When the function is not monotonic on the interval, you cannot simply judge by endpoints. This explanation is worth 1 mark on its own (the 2017 report indicated that area-related explanation questions are generally weak).
3. Best estimate = (L + U)/2 (trapezium).
4. Ways to improve: increase the number of rectangles (reduce the width); use trapeziums; find the function expression and then use integration to calculate the exact value (the 2017F-Q9 key accepts the first and last).

**Past questions**: 2017F-Q9, 2021F-Q7(b), 2024F-Q6.

---

## Pattern 8: Integral applications in context (cross-sectional area, volume, total change)

**Recognition**: Building or window cross-sections, trenches, dams, shampoo bottles; or "rate is … determine the total change".

**Approach**
1. Volume = cross-sectional area × thickness/length. Calculate the cross-sectional area using integration; units must be consistent (centimetres and metres).
2. Find intersection points or boundaries (e.g. h(W) = 0 to find the width, D(x) = −2 to find the trench edge).
3. Total change = ∫ₐᵇ rate of change dt.
4. When the water level h is unknown: write the cross-sectional area as a function of h (the upper limit is an expression in h) → **cross-sectional area × length (width) = volume** → solve for h (2024A-Q16(b): width 4 cm). 2023A-Q14(a) uses the same method to derive the expression for V(h).

**Marking points (2023A-Q14(a))**: ✓ upper limit expressed in terms of h ✓ correct integral expression ✓ antiderivative ✓ substitute upper and lower limits ✓ simplify to the target expression.

**Past questions**: 2019A-Q15(c), 2020A-Q10(c)(d), 2022A-Q7, 2023A-Q9, 2023A-Q14, 2024A-Q16. (2021A-Q9 is the same kind of context, but the whole question does not involve integration.)
