# MAS · Integration Techniques and Applications — Question Patterns and Solution Approaches

> Based on: 44 past exam questions from 2016–2025, marking key + exam reports. Original questions in `topics/05_Integration.pdf`. Numerical examples verified with sympy.
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`).

## Marking panel reminders

- **The antiderivative of ln must include absolute value signs** (2022 report). In recent keys this is counted in the "antiderivative" mark, so omitting the absolute value signs may mean the mark is not awarded at all; when the argument is always positive (e.g. ln(x² + 2)), the key notes that they may be omitted.
- **Indefinite integrals must include + c** (almost every partial fractions question has this 1 mark).
- **Basic algebra skills**: more than 30% of candidates expanded (√3 tan u + 1)² incorrectly (2018 report); misused the distributive law by writing √(2 − sin²θ) as √2 − sin θ (2021 report, F-Q8(c)); wrote the numerator expression incorrectly after finding a common denominator in partial fractions (2024 report).
- When integrating using a given substitution, **simplify fully** after substituting before integrating (2020, 2023 reports).
- Volume formulas must include π; all integral expressions must include dx/dy and the limits (the keys for 2022A-Q17 and 2021A-Q13 combine "limits + correct notation" for 1 mark).

---

## Pattern 1: Definite integrals with a given substitution ★ CF tested almost every year (from 2016–2025, only 2022 did not test it), 4–7 marks

**Fixed five steps (the key's 5 marks are basically these five steps)**
1. Find dx from the substitution: u = 1 − x ⇒ dx = −du; x = 2 sin θ ⇒ dx = 2cos θ dθ.
2. **Change the limits**: x = 0 → u = 1, x = 1 → u = 0.
3. Write the integrand completely in terms of the new variable and simplify (commonly 1 − sin²θ = cos²θ, 1 + tan²u = sec²u).
4. Find the antiderivative.
5. Substitute the limits and give the exact value.

**Three types of substitution**
- Linear or radical: u = 1 − x, u = √(x + 2), x = 119u + 1 (2020F-Q7, 2021F-Q3, 2023F-Q3, 2024F-Q3).
- Power-function substitutions (reverse chain rule): u = sin 2x, u = cos 2x (2016F-Q5(a), 2018F-Q5).
- **Trigonometric substitution**: x = a sin θ for √(a² − x²); x = a tan u for (x² + a²).

**Trigonometric substitution example** (2019F-Q6): ∫₀^√3 √(1 − x²/4) dx, let x = 2 sin θ; the limits become 0 → π/3 ⇒ ∫₀^{π/3} 2cos²θ dθ = ∫(1 + cos 2θ)dθ = **π/3 + √3/4**.

**Past exam questions**: 2016F-Q5, 2017F-Q3, 2018F-Q5, 2018F-Q9, 2019F-Q6, 2020F-Q7, 2021F-Q3 (you must choose the substitution yourself), 2021F-Q8(c), 2023F-Q3, 2023F-Q7(b), 2024F-Q3, 2025F-Q6.
**Indefinite integral version** (2016A-Q9, ∫x(1 + x)ⁿ dx): there is no step for changing the limits, and you must substitute back to x at the end.

---

## Pattern 2: Integration after simplifying with trigonometric identities (CF 3–5 marks)

**Common identities**
- cos²x = ½(1 + cos 2x), sin²x = ½(1 − cos 2x);
- (sin x + cos x)² = 1 + sin 2x ⇒ ∫₀^{π/2} = **π/2 + 1** (2022F-Q3);
- Product-to-sum: 2 sin A cos B = sin(A + B) + sin(A − B) ⇒ ∫₀^{π/2} 6 sin(5x/2) cos(x/2) dx = **4** (2019F-Q1);
- tan²x = sec²x − 1 (2016F-Q5(b));
- ∫₀^π (4cos²x − sin x) dx = ∫(2 + 2cos 2x − sin x)dx = **2π − 2** (2020F-Q1).

**Past exam questions**: 2016F-Q5(b), 2019F-Q1, 2020F-Q1, 2022F-Q3.

---

## Pattern 3: Partial fractions ★ CF high-frequency (tested in 8 of 10 years, not tested in 2017 or 2023)

**Standard procedure**
1. Set up the form:
   - Distinct linear factors: A/(x − a) + B/(x − b);
   - **Repeated root**: A/(x + 1) + B/(x + 1)² (2024F-Q4); A/x + B/x² + C/(x + 3) (2019F-Q3);
   - **Irreducible quadratic**: A/(x − 2) + (Bx + C)/(x² + 2) (2021F-Q5; x² + 4 in 2020F-Q6).
   - When the question specifies the form, follow it: 2022F-Q4 requires writing it as a/(x − 1) + (bx + c)/(x² + 3x + 1) (this quadratic can actually factorise, since its discriminant is 5 > 0).
2. After finding a common denominator, equate the numerators, substitute special values or compare coefficients, and find the constants ("equivalence of numerators" 1 mark, solving for the constants 1 mark).
3. Integrate term by term: A/(x − a) → A ln|x − a|; B/(x + 1)² → −B/(x + 1); for terms such as (2x + 3)/(x² + 3x + 1) (where the numerator is exactly the derivative of the denominator) → ln|x² + 3x + 1|; q/(x² + 4) → (q/2) tan⁻¹(x/2) (obtained from the derivative of inverse trigonometric functions, 2020F-Q6).
4. Write **+ c**.

**Example**: 1/(x² − 1) = ½[1/(x − 1) − 1/(x + 1)] ⇒ ∫ = ½ ln|(x − 1)/(x + 1)| + c (2018F-Q6). (5x + 3)/(x + 1)² = 5/(x + 1) − 2/(x + 1)² ⇒ ∫ = 5 ln|x + 1| + 2/(x + 1) + c (2024F-Q4).
**When no hint is given** (2025F-Q3): first factorise the denominator yourself (the first mark in the key).

**Past exam questions**: 2016F-Q4, 2018F-Q6, 2019F-Q3, 2020F-Q6(c)(d), 2021F-Q5, 2022F-Q4, 2024F-Q4, 2025F-Q3.

---

## Pattern 4: Area (integrating with respect to x or y)

**Approach**
1. Find intersection points or points of tangency to use as limits.
2. **Choose the variable of integration**: when the curve is more conveniently written as x = g(y), integrate with respect to y (2x = sin y in 2016A-Q13; 2017A-Q12; 2022F-Q7). The key often awards marks for both methods, but integrating with respect to y usually requires only one integral.
3. Area = ∫(right − left)dy or ∫(top − bottom)dx.
4. Use symmetry: ellipse 2025A-Q8; 2022A-Q13(c) multiply by 2 due to symmetry about the x-axis; the 4 in the cardioid 2021F-Q8 = (the 2 from symmetry about the y-axis) × (the 2 in the difference between the upper and lower branches, 2√(2 − x²)).
5. Interpret a definite integral as an area: 2017A-Q16 (after substitution u = 2x − a it equals the area of some region), 2024A-Q15(c) (triangle area = 2k).
5. Area of a circular segment: solve the circle equation for y = 4 ± √(4 − (x − 3)²); the difference between the upper and lower branches = 2√(…) (2023F-Q7(a)).
6. Determine whether a curve is a circle: compare the numerical area with πr² (2020A-Q16(b)).

**Past exam questions**: 2016A-Q13, 2017A-Q12, 2017A-Q16, 2022A-Q13(c), 2024A-Q15(c), 2018A-Q15(b), 2020A-Q16, 2021F-Q8, 2022F-Q7, 2023A-Q18(b), 2023F-Q7, 2024F-Q8(e), 2025A-Q8.

---

## Pattern 5: Volume of solids of revolution ★ CA high-frequency

**Formulas**
- About the x-axis: V = π∫ₐᵇ y² dx; about the y-axis: V = π∫ₐᵇ x² dy (**first write x² as a function of y**).
- Region between two curves: V = π∫(y_{out}² − y_{in}²)dx (**not** π∫(y_{out} − y_{in})²dx).
- Annulus (doughnut, 2024A-Q11): x = 3 ± √(4 − y²) ⇒ V = π∫(R² − r²)dy = ∫₋₂² 12π√(4 − y²) dy.

**Contextual question types**
- Volume formula for a cup: derive using an integral with letters a, b, h (2017F-Q8).
- Depth when filled to 80%: set ∫₀ʰ π x² dy = 0.8 × V_{full}, solve for h (2020A-Q9).
- Related rates for filling with water: dV/dt = (dV/dh)·(dh/dt) (2025A-Q14(b): find dV/dh from V = ah³).
- Increment formula: δh ≈ δV ÷ (dV/dh), where dV/dh = πx²|_{y=h} (2023A-Q17(c)).
- The volume integral in 2022A-Q17 is in (a); (b)–(d) are about increments, flow rate and separation of variables for dV/dt = 300e^{−V/12000} (see the 'Rates of Change and Differential Equations' handout).
- Spherical cap (2021A-Q13): from the circle equation get y² = 20x − x², integrate with respect to x from 0 to h.

**Marking points**: ✓ express the radius in terms of x or y ✓ correct integral expression (limits + π + square) ✓ calculation (including units, rounding).
**Past exam questions**: 2016A-Q17(c), 2017F-Q8, 2018A-Q15(c), 2019F-Q8, 2020A-Q9, 2021A-Q13, 2022A-Q17, 2023A-Q17, 2024A-Q11, 2025A-Q14.
