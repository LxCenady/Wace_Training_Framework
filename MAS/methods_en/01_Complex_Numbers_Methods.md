# MAS · Complex Numbers — Question Patterns and Solution Approaches

> Source: marking keys + exam reports for 43 past complex number questions from 2016–2025. Original questions in `topics/01_Complex_Numbers.pdf`. Numerical examples have been checked with sympy. Also references 2 questions from the 2016 sample paper (`2016S-F1`, `2016S-A18`; original papers in `papers/2016Sample_*`).
> Review status: has undergone one round of independent review and been revised according to feedback (see `Review_log.md`).

## Marking panel reminders

- **Use polar form when you should** (2016 report: people who did not convert (√3 − i)⁵ to polar form lost a lot of marks). For powers and roots, always use polar form; for multiplication and division, it depends on the form (e.g. for (2+i)/(1−i)², using the conjugate is faster, 2016F-Q2(a)).
- **Arguments in the third quadrant** (2020 report specifically names 2020A-Q15(a): complex numbers in the third quadrant converted to polar form incorrectly): e.g. the principal argument of −1 − i is −3π/4, not π/4, and it cannot be written as 5π/4 (outside the principal value range). Draw a diagram first to confirm the quadrant.
- **Vector interpretation of complex numbers** (2018, 2021, 2025 reports: z + r, argument of −z, regular hexagon): z + r, z − k (e.g. 2023A-Q12), and −z must all be done by drawing them as vectors (rhombus, isosceles triangle, regular hexagon).
- **Basic skill of expanding brackets** (2021, 2023, 2024 reports): (z − (2+4i))(z − (2−4i)) = z² − 4z + 20 is often calculated incorrectly; z² − 2z + 3 = 0 must be solved by completing the square or the quadratic formula, and **must not** be split into (z − 3)(z + 1).
- **Know exact trigonometric values** (2019, 2021, 2023 reports).
- “Show that (z − 2i) is a factor”: after substituting, you must write out the **calculation of each term**; the key says “provides evidence, i.e. not just the statement P(2i) = 0”.

---

## Pattern 1: Algebraic form operations and conversion between forms (mostly in CF)

**Approach**
- Division: multiply the numerator and denominator by the conjugate of the denominator.
- Converting to polar form: r = √(a² + b²); θ is determined by the quadrant. Example: given z = 3 + bi and tan θ = 2 ⇒ b = 6, r = √45 = 3√5 (2024F-Q1).
- Higher powers: (√3 − i)⁵ = (2 cis(−π/6))⁵ = 32 cis(−5π/6) = −16√3 − 16i. The key also accepts binomial expansion, but it takes several more steps.

**Marking points**: ✓ modulus ✓ argument ✓ use De Moivre ✓ convert to a + bi.
**Past questions**: 2016F-Q2, 2017A-Q10(a), 2019A-Q12(a)(b), 2021A-Q11(a)(b), 2024F-Q1.

---

## Pattern 2: Solving zⁿ = w (finding nth roots) ★ appears every year

**Standard method**
1. Write w as R cis φ (1 mark for modulus, 1 mark for argument).
2. z = R^{1/n} cis((φ + 2kπ)/n), k = 0, 1, …, n−1 (1 mark for writing the general form).
3. List **all** n roots within the range required by the question (commonly −π < θ ≤ π); the arguments of adjacent roots differ by **2π/n**.
4. Example: z⁴ = −16i = 16 cis(−π/2) ⇒ z = 2 cis(−5π/8), 2 cis(−π/8), 2 cis(3π/8), 2 cis(7π/8).
   z⁴ = 2 − 2√3 i = 4 cis(−π/3) ⇒ √2 cis(−7π/12), √2 cis(−π/12), √2 cis(5π/12), √2 cis(11π/12).

**Variations**
- Given the diagram of one root, work backwards to find k (2025F-Q1): w₂³ = ki.
- Number of roots in the first quadrant ⇒ find the possible values of n, giving reasons (2017A-Q19(b)).
- Roots of zⁿ = 1: on the unit circle, equally spaced, separated by 2π/n (2024A-Q9(c) has 2 marks for the explanation: circle of radius 1, equal spacing).
- Product of roots (2019F-Q9): product of all roots = (−1)^{n+1}; 1 when n is odd, −1 when n is even.
- Common roots: z⁴³ = 1 and z⁴⁷ = 1 have only z = 1 as a common root, because 43 and 47 are coprime (2021F-Q7).

- zⁿ is a positive real number (2022F-Q6(c)): n·arg z must be an integer multiple of 2π. z₁ = 4 cis(5π/6) ⇒ 5n/6 = 2k ⇒ smallest n = 12, r = 4¹² = 2²⁴.

**Past questions**: 2016A-Q14, 2017A-Q19, 2018F-Q7(a), 2020A-Q13, 2022A-Q18(b), 2022F-Q6, 2023F-Q6, 2024A-Q9, 2025F-Q1.

---

## Pattern 3: Complex roots of polynomials (factor theorem + conjugate root theorem)

**Standard method**
1. “Show that (z − α) is a factor”: calculate P(α), **write out each term**, and obtain 0.
2. A polynomial with real coefficients ⇒ the conjugate ᾱ is also a root ⇒ (z − α)(z − ᾱ) = z² − 2Re(α)z + |α|² is a **real quadratic factor**.
3. Use polynomial division or compare coefficients to find the remaining factor.
4. Solve the remaining quadratic equation (completing the square or quadratic formula).

Example (2021F-Q6): P(2 + 4i) = 0 ⇒ factor z² − 4z + 20 ⇒ P = (z² − 4z + 20)(z² − 2z + 3) ⇒ z = 2 ± 4i, 1 ± √2 i.

**Finding coefficients in reverse (2023F-Q2)**: given roots 1 + i, 2 + √3 i ⇒ the conjugate roots are also roots ⇒ Q(z) = (z² − 2z + 2)(z² − 4z + 7) ⇒ use the constant term 14 to deduce the real root z₀, then expand and compare coefficients.

**Past questions**: 2016F-Q3, 2016S-F1, 2017F-Q2, 2018F-Q7(b)(c), 2019F-Q2, 2021F-Q6, 2022A-Q13(a)(b), 2023F-Q2, 2024F-Q7.

---

## Pattern 4: Geometric meaning of multiplication (rotation + dilation)

**Recognition**: “Describe the geometric transformation performed by successive multiplication by z”.

**Template (2 marks)**: “Multiplication by w = r cis θ **dilates** the modulus by a factor r and **rotates** the vector **anticlockwise by θ** (or clockwise by |θ| if θ < 0) about the origin.” 1 mark for each of the two elements; for multiplication by z⁻¹, take the reciprocal of the scale factor and reverse the direction of rotation (2023A-Q10(d)).

**Extensions**
- Find all n for which zwⁿ lies in the second quadrant: each multiplication by w rotates by 30°, list the n for which 90° < argument < 180°. When |w| = 1, it returns to the original position every 12 times, so the answer must be complete: n = 3 + 12k, 4 + 12k, 5 + 12k (k a non-negative integer); writing only 3, 4, 5 does not earn the "all the possible values" mark (2025A-Q19(b)).
- Read the modulus and argument of z from the diagram, then write the polar form (2019A-Q12(b)).

**Past questions**: 2017A-Q10, 2019A-Q12, 2023A-Q10, 2025A-Q19.

---

## Pattern 5: Loci — sketching from equations

| Equation or inequality | Graph |
|---|---|
| \|z − a\| = r | circle with centre a and radius r |
| \|z − a\| = \|z − b\| | perpendicular bisector of the line segment joining a and b |
| Arg(z − a) = θ | ray starting at a (**endpoint a is not included in the locus**; draw an open circle) |
| \|z − a\| + \|z − b\| = k | ellipse when k > \|a − b\|; **when k = \|a − b\| it degenerates to the line segment ab** (2022A-Q9(a)) |
| \|z + 2\| = \|z − i\| + √5 | the difference equals the distance between the two points ⇒ a ray starting at i and extending in the direction −2→i; **the endpoint i is included in the locus (solid dot)**, unlike an Arg-type ray (the 2020A-Q10(b) key has 1 mark specifically for this point) |
| (z + i)·conj(z + i) = 2 | \|z + i\|² = 2 ⇒ centre −i, radius √2 (2022A-Q9(b)) |
| z − z̄ ≤ 6i | 2i·Im(z) ≤ 6i ⇒ Im(z) ≤ 3 (2024A-Q10(b)) |

**Marking points for sketching**: ✓ key points or centre ✓ boundary position ✓ solid/dashed boundary ✓ correct shaded region.

**Past questions**: 2016A-Q10(a)(b), 2016S-A18, 2020A-Q10(b), 2022A-Q9(a)(b), 2024A-Q10(b), 2025A-Q10(b).

---

## Pattern 6: Loci — writing equations from diagrams

**Approach**: first recognise the shape, then write the equation using z (do not use x, y): circle ⇒ \|z − centre\| ≤ r; ray ⇒ Arg(z − endpoint) = θ; sector ⇒ use two Arg inequalities plus one modulus inequality. The angle at the endpoint must be found exactly using trigonometry (2020A-Q10(a)).

**Past questions**: 2018A-Q11(a)(b), 2019A-Q10(a), 2020A-Q10(a), 2021A-Q11(d), 2022A-Q9(c), 2025A-Q10(a).

---

## Pattern 7: Maximum and minimum values on loci

**Approach**: sketch → find the geometric position where the maximum/minimum occurs → calculate using Pythagoras' theorem or trigonometry.
- Maximum distance from a point on the circle to c = \|centre − c\| + r, minimum distance = \|centre − c\| − r (when c is outside the circle; when c is inside the circle it is r − \|centre − c\|) (2016A-Q10(c), 2024A-Q10(a)(ii)).
- Maximum argument of a point on the circle: occurs at the **tangent** position. The θ found from sin θ = r/d is only “the angle between the tangent and the line O→centre”; you must then add or subtract the argument of the centre, and note the argument range specified in the question (2018A-Q11(c): 0 ≤ arg z < 2π, answer 2π − α ≈ 5.64).
- Minimum distance from a point on the ray to i: draw a perpendicular (2019A-Q10(b)).

**Marking points**: ✓ indicate on the diagram the position where the maximum/minimum occurs ✓ write the expression ✓ exact value.

---

## Pattern 8: Using vectors or geometry to find modulus and argument (appears in both CF and CA)

**Approach**: Draw z + w as a parallelogram and z − k as a triangle, then use:
- Equal moduli of two vectors ⇒ rhombus ⇒ the diagonal bisects the angle: arg(z + r) = θ/2 (2018F-Q3(b)(ii));
- Isosceles triangles, the inscribed angle theorem, the sine or cosine rule (2017F-Q6, 2021F-Q1(b), 2023A-Q12);
- Regular hexagon: when **centred at the origin**, adjacent vertices differ in argument by π/3 and all moduli are equal. In 2025F-Q7, vertex z₀ is **at the origin**, so the hexagon is not centred at the origin: the side vectors rotate by π/3 successively; using the cosine rule gives \|z₂\| = \|z₄\| = √3r and \|z₃\| = 2r, so \|z₁z₂z₃z₄z₅\| = r·√3r·2r·√3r·r = **6r⁵**; z₃ = 2r cis(π/3), Arg(z₅ − z₃) = −5π/6 (the 2025 report calls out the hexagon geometry in this question).

**Past exam questions**: 2017F-Q1, 2017F-Q6, 2018F-Q3, 2020A-Q11, 2020A-Q15, 2021F-Q1, 2023A-Q12, 2025F-Q7.

---

## Pattern 9: Proof and technique questions

- Identities: use conj(z) = r cis(−θ), together with cos being even and sin being odd (2018A-Q10).
- Grouped summation: n·iⁿ is not itself periodic, but the sum of every 4 consecutive terms (terms 4m+1 to 4m+4) is always 2 − 2i; there are 505 groups ⇒ Σₙ₌₁²⁰²⁰ n iⁿ = 505 × (2 − 2i) = 1010 − 1010i = 1010√2 cis(−π/4) (2020F-Q8).
- Solving a real system of equations using complex numbers: (a + bi)³ = (a³ − 3ab²) + i(3a²b − b³) = 14 − 2√5 i ⇒ taking the modulus: (a² + b²)³ = 196 + 20 = 216 ⇒ **a² + b² = 6** (2023F-Q8).
- Use complex multiplication to prove the arctangent sum (2025A-Q19(c)).
