# MAS · Rates of Change and Differential Equations — Patterns and Solution Approaches

> Basis: marking keys + exam reports for 41 past questions from 2016–2025. Appears almost exclusively in Calculator-assumed papers. Original questions are in `topics/06_Rates_DiffEq.pdf`. Numerical examples have been checked with Python.
> Review status: has undergone one round of independent review and been revised according to feedback (see `Review_log.md`).

## Marking panel reminders

- **Motion when v is a function of x** (2018, 2020, 2022 reports **mentioned it three times**): a = dv/dt = (dv/dx)(dx/dt) = v·dv/dx = d(½v²)/dx. **dv/dx itself is not acceleration**; after differentiating with respect to x, multiply by v.
- **Implicit differentiation**: many students are unwilling to use it (2017 report), or cannot do the second derivative (2025 report).
- **Not all growth is logistic** (2025 report): for equations such as dP/dt = 0.001(100 − P)², many students draw the S-shape of rP(k − P) and get it wrong. Analyse the slope from the given equation itself.
- **Where the slope is undefined in a slope field** (2019 report): when the numerator is not 0, the solution curve has a vertical tangent there; the curve turns back at this point and is symmetric about that line.
- Rates of change must include **units** (2020, 2021 reports).
- **Use of the logistic equation** was a difficulty named in the 2024 report (Q13(c), finding r and k from the explicit solution).
- **Recognising standard differential equations**: SHM and exponential decay (2017 report).
- Antiderivatives involving ln must include absolute values (2022 report).

---

## Pattern 1: Implicit Differentiation (tangents, horizontal points, second derivative)

**Standard procedure**
1. Differentiate both sides with respect to x: terms containing y must be multiplied by dy/dx; use the product rule for products and the chain rule for composites, e.g. 3(x² + y² − 1)²(2x + 2y y′).
2. Solve for dy/dx if the question requires it; you can also substitute the point directly to find the value (2018A-Q20 explicitly asks you **not** to solve for dy/dx: "Do not attempt to obtain dy/dx as the subject").
3. **Horizontal tangents**: dy/dx = 0 ⇒ numerator = 0; then solve simultaneously with the original equation to find the points (2018A-Q20(c), 2021A-Q18(b)).
4. **Second derivative** (2025F-Q5): differentiate the once-differentiated expression again, then substitute the values of x, y and y′.
5. Derivatives of inverse trigonometric functions (2020F-Q6(b), 2024F-Q8(d)): x = 2 tan y ⇒ 1 = 2 sec²y·y′ ⇒ use 1 + tan²y to rewrite the result in terms of x.

**Past questions**: 2016A-Q13(a), 2017A-Q12(a), 2018A-Q15(a), 2018A-Q20, 2021A-Q18, 2022F-Q7(a), 2025F-Q5.

---

## Pattern 2: Related Rates ★

**Standard procedure (4–5 marking points)**
1. Write the relationship between the quantities (geometric or physical); **set up a relationship between the variables and eliminate any unnecessary variables if needed** (alternatively, keep two variables and differentiate implicitly with respect to t): V = 4h² (triangular-prism water tank), area of a regular hexagon A = (3√3/2)s², x = 50 tan θ (lighthouse), s(10 − h) = 30 (shadow).
2. Differentiate with respect to t (chain rule or implicit differentiation): dA/dt = 3√3 s · ds/dt.
3. Substitute the known rate of change and the **values at that instant** (sometimes θ or h must be found first).
4. Include units. Example: s = 4, ds/dt = 0.5 ⇒ dA/dt = 6√3 ≈ 10.39 cm²/s (2022A-Q8).
5. Lighthouse type (2021A-Q9): 3 revolutions per minute ⇒ dθ/dt = 6π rad/min = π/10 rad/s; when x = 100, sec²θ = 1 + (100/50)² = 5.

**Past questions**: 2016S-A11(a), 2016A-Q15, 2017A-Q18(c), 2019A-Q18(c), 2020A-Q20(b), 2021A-Q9, 2022A-Q8, 2023A-Q19, 2025A-Q14(b). (2023A-Q17(c) is an increment formula question; see Pattern 8.)

---

**Related rates in circular motion (Ferris wheel, carousel)**

**Approach**
1. Angular speed: one revolution is 2π radians and takes T seconds ⇒ dθ/dt = 2π/T ("show that" 1 mark).
2. Model with a geometric relationship: cosine rule s² = 89 − 80cos θ (2017A-Q18(b)), or height relative to the centre y = 80 sin(θ − π/2) (2019A-Q18(b), explaining the value of the phase α; height above the ground = y + 80, so 100 m above the ground corresponds to y = 20).
3. Differentiate implicitly with respect to t: 2s·ds/dt = 80 sin θ · dθ/dt.
4. Find the maximum rate of change: differentiate again and set it equal to 0; you can also understand it geometrically: ds/dt is greatest when PC is tangent to the circle.

**Past questions**: 2017A-Q18, 2019A-Q18.

---

## Pattern 3: Slope Fields

**Common question types and approaches**
- Find the slope value at a point: substitute directly (1 mark).
- Deduce the equation from a slope field: observe whether the slope changes only with x (segments on the same vertical line are parallel) or only with y; where the slope is 0; and where the slope is undefined. For example, 2016A-Q18: dy/dx = a − bx (a, b > 0); one condition is read from the diagram (slope is 0 at x = 2) and one is given in the question (slope is 0.5 at A(1, 2)) ⇒ dy/dx = 1 − 0.5x. The marking point in (a) requires stating that the intercept is positive and the slope is negative.
- Draw solution curves: pass through the specified point, **follow the direction of the short line segments**, and mark any symmetry; where the slope is undefined the tangent is vertical (2019A-Q11(b), 2021A-Q10(c)); where the slope is 0 there is a horizontal tangent; on the line where the slope is greatest, the curve has a point of inflection. 2025A-Q16: dy/dx = (x − 1)/((y + 1)² + 1), there is a minimum at x = 1, and the **point of inflection is at (3, −1)** (the slope is greatest on y = −1), worth 1 mark in the key.
- Analytical solution: solve by separation of variables (see Pattern 4).

**Past questions**: 2016A-Q18, 2016S-A21, 2017A-Q11, 2019A-Q11, 2021A-Q10, 2023A-Q11, 2025A-Q16.

---

## Pattern 4: Separation of Variables

**Standard procedure (3–4 marks)**
1. Write it as g(y) dy = f(x) dx and **put integral signs on both sides** (the exact wording in the key for 2021A-Q10(b), 2022A-Q17(d) is "separates the variables as an integration statement"; in other years it says "separates the variables correctly").
2. Integrate both sides, adding only **one** constant; ln must include absolute values.
3. Substitute the initial condition to find the constant.
4. Write it in the explicit form y = … if required.

**Common models**
- dP/dt = kP ⇒ P = P₀eᵏᵗ (2019A-Q17(a): the **instantaneous** growth rate is 10% of the population, i.e. dP/dt = 0.1P; using P(45) = 30000 to work back to 1963 gives P₀ = 30000e^{−4.5} ≈ 333. It must not be treated as "10% growth per year" using 1.1ᵗ, which gives about 412).
- dA/dt = −0.4A ⇒ A = 8e^{−0.4t} (2017A-Q17(c)).
- dh/dt = −1/(100h) ⇒ h² = h₀² − t/50 (2016A-Q15(d)).
- dv/dt = −9.8 − 2v ⇒ v = 4.9(e^{−2t} − 1); **depth requires integrating v** (2024A-Q17).
- dV/dt = 300e^{−V/12000} ⇒ separating gives e^{V/12000}dV = 300 dt (2022A-Q17(d)).

**Past questions**: 2016A-Q15, 2016S-F3, 2017A-Q11(c), 2019A-Q11(c), 2021A-Q10(b), 2022A-Q17(d), 2023A-Q11(b), 2024A-Q17(c), 2025A-Q17(c).

---

## Pattern 5: Logistic Growth ★

**Formula**: dP/dt = rP(k − P) ⇔ P(t) = k / (1 + Ae^{−rkt}).
- Limiting value (carrying capacity) = k (t → ∞);
- **Growth is fastest when P = k/2** (point of inflection), maximum growth rate = r(k/2)²;
- Find r and k from the explicit solution: for example, P = 18000/(10.25e^{−0.15t} + 1) ⇒ k = 18000, rk = 0.15. When the question writes dP/dt = (1/r)P(k − P), 1/r = 0.15/18000 ⇒ r = 120000; maximum growth rate = 0.15 × 9000 × ½ = **675 horses/year** (2024A-Q13, consistent with the key).

**Common question types**
- Find the proportionality constant from the initial rate of change (in 2018A-Q18(a) the question calls it k: 60 = k·100·1500 ⇒ k = 0.0004; carrying capacity is 1600). **Use the letters given in the question**: carrying capacity = the non-zero P that makes dP/dt = 0.
- Increment estimate: δP ≈ (dP/dt)·δt; watch the time units (1 month = 1/12 year, 15 minutes = 0.25 hours).
- Use partial fractions to separate variables and derive the explicit solution (2016S-A20, 2018A-Q18(c)).
- Explain the growth: "when P < k/2, the growth rate increases as P increases; when P > k/2, the growth rate decreases and P approaches k" (2022A-Q16(a)).
- Sketch after the carrying capacity changes: new point of inflection, new horizontal asymptote (2022A-Q16(b)); **when k/2 < P₀ < k, the curve is concave down throughout, increasing towards k, with no point of inflection** (2020A-Q19(e): P₀ = 1.3, k = 2.4); when P₀ > k, the curve decreases and approaches k.
- **Non-logistic** (2025A-Q17): dP/dt = 0.001(100 − P)² ⇒ the slope decreases monotonically as P increases, there is no point of inflection, and the asymptote is P = 100.

**Past questions**: 2016S-A20, 2018A-Q18, 2019A-Q17(b)–(d), 2020A-Q19, 2022A-Q16, 2024A-Q13, 2025A-Q17.

---

## Pattern 6: Velocity as a function of displacement (v = f(x)) ★★ Report focus

**Standard procedure**
1. **Acceleration**: a = v·dv/dx (or d(½v²)/dx).
   - v = −0.2x ⇒ a = (−0.2x)(−0.2) = 0.04x;
   - v = x/8 ⇒ a = (x/8)(1/8) = x/64.
2. **Find x(t)**: dx/dt = v(x) ⇒ separate the variables ⇒ substitute the initial position.
   - v = x/8, x(0) = 192 ⇒ x = 192e^{t/8}, v(0) = 24 matches the given information ⇒ at 11 seconds the velocity is 24e^{11/8} ≈ 94.92 m/s, distance travelled 192(e^{11/8} − 1) ≈ 567.37 m (2022A-Q11).
   - v = −0.2x, x(0) = 4 ⇒ x = 4e^{−0.2t} ⇒ when x = 2, t = 5 ln 2 ≈ 3.47 s (2020A-Q14).
3. **Decide whether it is SHM**: it is SHM only if a is proportional to the displacement (from the equilibrium point) and in the opposite direction, i.e. a = −n²(x − c). For a = 0.04x the coefficient is positive, so it is not SHM (2020A-Q14(b)).

**Past exam questions**: 2018A-Q13, 2020A-Q14, 2022A-Q11.

---

## Pattern 7: Simple harmonic motion (SHM)

**Formulas**: ẍ = −n²x ⇒ x = A cos(nt + φ) or A sin(nt + φ); period T = 2π/n; maximum speed = An; v² = n²(A² − x²).

**Common question types**
- Determine A and the phase from the initial conditions: x(0) = 0 and v(0) > 0 ⇒ x = A sin(nt) (2017A-Q17). 2024A-Q12 only says it starts from the equilibrium position and gives no direction, so both ±25 sin(πt/2) are awarded marks (total vertical span 50 cm ⇒ A = 25).
- Find the amplitude from v² = n²(A² − x²): n = 2, x(0) = −1, v(0)² = 32 ⇒ 32 = 4(A² − 1) ⇒ **A = 3**, T = π (2025A-Q15).
- **Distance travelled**: 4A per period, 2A per half period. 2025A-Q15(b): 10π seconds = 10 periods ⇒ 4 × 3 × 10 = **120 cm**. 2017A-Q17(b): T = 2, 5 seconds = 2.5 periods ⇒ 10A = 80 cm. When the time is less than half a period and the starting point is neither the equilibrium position nor an endpoint, use ∫|v| dt.
- Amplitude decay (damping): dA/dt = −kA ⇒ A = A₀e^{−kt}; the condition for appearing to stop is A < 0.01 (2017A-Q17(d)).

**Past exam questions**: 2016S-A15, 2017A-Q17, 2019A-Q18(d) (show that the Ferris wheel's y(t) satisfies d²y/dt² = −(π/36)²y), 2021A-Q12, 2024A-Q12, 2025A-Q15.

---

## Pattern 8: Increments formula (MAS version)

δy ≈ (dy/dx)δx, which also applies to differential equations: δN ≈ (dN/dt)·δt, where dN/dt is given directly by the equation (2018A-Q18(b), 2020A-Q19(c), 2025A-Q17(b)); δh ≈ δV / (dV/dh) (2023A-Q17(c)).
**Past exam questions**: 2016A-Q11(b), 2018A-Q18(b), 2020A-Q19(c), 2022A-Q17(b), 2023A-Q17(c), 2025A-Q17(b).
