# MAS · Complex Numbers — Question Patterns and Solution Strategies

> Basis: marking keys + exam reports for a total of 43 past complex-number questions from 2016–2025. Original questions in `topics/01_Complex_Numbers.pdf`. Numerical examples verified with sympy. Also cites 2 questions from the 2016 sample paper (`2016S-F1`, `2016S-A18`; original paper in `papers/2016Sample_*`).
> Review status: has been through one round of independent review and revised according to the feedback (see `Review_log.md`).

## Examiner reminders

- **Use polar form when you should** (2016 report: those who didn't convert (√3 − i)⁵ to polar form lost a lot of marks). Always use polar form for powers and roots; for multiplication and division it depends on the form (e.g. (2+i)/(1−i)² is faster using the conjugate, 2016F-Q2(a)).
- **Arguments in the third quadrant** (the 2020 report specifically names 2020A-Q15(a): a third-quadrant complex number was not converted to polar form correctly): for example, the principal argument of −1 − i is −3π/4, not π/4, and 5π/4 is not allowed either (outside the principal range). Sketch first to confirm the quadrant.
- **Vector interpretation of complex numbers** (2018, 2021, 2025 reports: z + r, the argument of −z, regular hexagon): do z + r, z − k (e.g. 2023A-Q12) and −z by drawing them as vectors (rhombus, isosceles triangle, regular hexagon).
- **Basics of expanding brackets** (2021, 2023, 2024 reports): (z − (2+4i))(z − (2−4i)) = z² − 4z + 20 is often miscalculated; for z² − 2z + 3 = 0 use completing the square or the quadratic formula, and **do not** split it into (z − 3)(z + 1).
- **Know your exact trig values** (2019, 2021, 2023 reports).
- "Show that (z − 2i) is a factor": after substituting, you must write out the **calculation for each term**; the key says "provides evidence, i.e. not just the statement P(2i) = 0".

---

## Pattern 1: Operations in Cartesian form and converting between forms (mostly in CF)

**Approach**
- Division: multiply the numerator and denominator by the conjugate of the denominator.
- Converting to polar form: r = √(a² + b²); determine θ from the quadrant. Example: given z = 3 + bi and tan θ = 2 ⇒ b = 6, r = √45 = 3√5 (2024F-Q1).
- Higher powers: (√3 − i)⁵ = (2 cis(−π/6))⁵ = 32 cis(−5π/6) = −16√3 − 16i. The key also accepts binomial expansion, but it takes several more steps.

**Mark-earning points**: ✓ modulus ✓ argument ✓ use De Moivre ✓ convert to a + bi.
**Past questions**: 2016F-Q2, 2017A-Q10(a), 2019A-Q12(a)(b), 2021A-Q11(a)(b), 2024F-Q1.

---

## Pattern 2: Solving zⁿ = w (finding nth roots) ★ tested every year

**Standard procedure**
1. Write w as R cis φ (1 mark for modulus, 1 mark for argument).
2. z = R^{1/n} cis((φ + 2kπ)/n), k = 0, 1, …, n−1 (1 mark for writing the general form).
3. Within the range required by the question (commonly −π < θ ≤ π), list **all** n roots; adjacent roots differ in argument by **2π/n**.
4. Example: z⁴ = −16i = 16 cis(−π/2) ⇒ z = 2 cis(−5π/8), 2 cis(−π/8), 2 cis(3π/8), 2 cis(7π/8).
   z⁴ = 2 − 2√3 i = 4 cis(−π/3) ⇒ √2 cis(−7π/12), √2 cis(−π/12), √2 cis(5π/12), √2 cis(11π/12).

**Variations**
- Given the diagram of one root, work backwards to find k (2025F-Q1): w₂³ = ki.
- Number of roots in the first quadrant ⇒ find the possible values of n; you must give a reason (2017A-Q19(b)).
- Roots of zⁿ = 1: on the unit circle, evenly spaced, separated by 2π/n (2024A-Q9(c) explanation worth 2 marks: circle of radius 1, equal spacing).
- Product of the roots (2019F-Q9): the product of all roots = (−1)^{n+1}; it is 1 when n is odd and −1 when n is even.
- Common roots: z⁴³ = 1 and z⁴⁷ = 1 have only z = 1 as a common root, because 43 and 47 are coprime (2021F-Q7).

- zⁿ a positive real number (2022F-Q6(c)): n·arg z must be an integer multiple of 2π. z₁ = 4 cis(5π/6) ⇒ 5n/6 = 2k ⇒ smallest n = 12, r = 4¹² = 2²⁴.

**Past questions**: 2016A-Q14, 2017A-Q19, 2018F-Q7(a), 2020A-Q13, 2022A-Q18(b), 2022F-Q6, 2023F-Q6, 2024A-Q9, 2025F-Q1.

---

## Pattern 3: Complex roots of polynomials (factor theorem + conjugate root theorem)

**Standard procedure**
1. "Show that (z − α) is a factor": calculate P(α), **writing out each term**, and get 0.
2. A polynomial with real coefficients ⇒ the conjugate ᾱ is also a root ⇒ (z − α)(z − ᾱ) = z² − 2Re(α)z + |α|² is a **real quadratic factor**.
3. Polynomial division or equating coefficients to find the remaining factor(s).
4. Solve the remaining quadratic (completing the square or the quadratic formula).

Example (2021F-Q6): P(2 + 4i) = 0 ⇒ factor z² − 4z + 20 ⇒ P = (z² − 4z + 20)(z² − 2z + 3) ⇒ z = 2 ± 4i, 1 ± √2 i.

**Working backwards to find coefficients (2023F-Q2)**: given roots 1 + i and 2 + √3 i ⇒ the conjugate roots are also roots ⇒ Q(z) = (z² − 2z + 2)(z² − 4z + 7) ⇒ use the constant term 14 to deduce the real root z₀, then expand and equate coefficients.

**Past questions**: 2016F-Q3, 2016S-F1, 2017F-Q2, 2018F-Q7(b)(c), 2019F-Q2, 2021F-Q6, 2022A-Q13(a)(b), 2023F-Q2, 2024F-Q7.

---

## Pattern 4: Geometric meaning of multiplication (rotation + dilation)

**Recognition**: "Describe the geometric transformation performed by successive multiplication by z".

**Template (2 marks)**: "Multiplication by w = r cis θ **dilates** the modulus by a factor r and **rotates** the vector **anticlockwise by θ** (or clockwise by |θ| if θ < 0) about the origin." 1 mark for each of the two elements; multiplying by z⁻¹ takes the reciprocal of the factor and reverses the direction of rotation (2023A-Q10(d)).

**Extensions**
- Find all n for which zwⁿ lies in the second quadrant: each multiplication by w rotates 30°, so list the n with 90° < argument < 180°. When |w| = 1 it returns to its original position every 12 multiplications, so the answer must be complete: n = 3 + 12k, 4 + 12k, 5 + 12k (k a non-negative integer); writing only 3, 4, 5 does not earn the "all the possible values" mark (2025A-Q19(b)).
- Read the modulus and argument of z from the diagram, then write the polar form (2019A-Q12(b)).

**Past questions**: 2017A-Q10, 2019A-Q12, 2023A-Q10, 2025A-Q19.

---

## Pattern 5: Loci — sketching from an equation

| Equation or inequality | Graph |
|---|---|
| \|z − a\| = r | Circle with centre a and radius r |
| \|z − a\| = \|z − b\| | Perpendicular bisector of the line segment joining a and b |
| Arg(z − a) = θ | Ray starting at a (**the endpoint a is not on the locus**; draw an open circle) |
| \|z − a\| + \|z − b\| = k | An ellipse when k > \|a − b\|; **degenerates to the line segment ab when k = \|a − b\|** (2022A-Q9(a)) |
| \|z + 2\| = \|z − i\| + √5 | The difference equals the distance between the two points ⇒ a ray starting at i and extending in the direction −2→i; **the endpoint i is on the locus (solid dot)**, the opposite of an Arg-type ray (the 2020A-Q10(b) key gives 1 mark specifically for this) |
| (z + i)·conj(z + i) = 2 | \|z + i\|² = 2 ⇒ centre −i, radius √2 (2022A-Q9(b)) |
| z − z̄ ≤ 6i | 2i·Im(z) ≤ 6i ⇒ Im(z) ≤ 3 (2024A-Q10(b)) |

**Mark-earning points for the sketch**: ✓ key points or centre ✓ position of the boundary ✓ solid/dashed boundary ✓ correct shaded region.

**Past questions**: 2016A-Q10(a)(b), 2016S-A18, 2020A-Q10(b), 2022A-Q9(a)(b), 2024A-Q10(b), 2025A-Q10(b).

---

## Pattern 6: Loci — writing an equation from a graph

**Approach**: identify the shape first, then write the equation in terms of z (you cannot use x, y): circle ⇒ \|z − centre\| ≤ r; ray ⇒ Arg(z − endpoint) = θ; sector ⇒ use two Arg inequalities plus one modulus inequality. Work out the angle at the endpoint exactly using trigonometry (2020A-Q10(a)).

**Past questions**: 2018A-Q11(a)(b), 2019A-Q10(a), 2020A-Q10(a), 2021A-Q11(d), 2022A-Q9(c), 2025A-Q10(a).

---

## Pattern 7: Maximum and minimum values on a locus

**Approach**: sketch → find the geometric position where the maximum/minimum occurs → calculate using Pythagoras or trigonometry.
- Maximum distance from a point on the circle to c = \|centre − c\| + r, minimum distance = \|centre − c\| − r (when c is outside the circle; when c is inside, it is r − \|centre − c\|) (2016A-Q10(c), 2024A-Q10(a)(ii)).
- Maximum argument of a point on the circle: occurs at the **tangent** position. The θ from sin θ = r/d is only "the angle between the tangent and the line O→centre"; you then have to add or subtract the argument of the centre, and watch the argument range specified in the question (2018A-Q11(c): 0 ≤ arg z < 2π, answer 2π − α ≈ 5.64).
- Minimum distance from a point on the ray to i: drop a perpendicular (2019A-Q10(b)).

**Mark-earning points**: ✓ indicate on the diagram where the maximum/minimum occurs ✓ write the expression ✓ exact value.

---

## Pattern 8: Finding modulus and argument using vectors or geometry (appears in both CF and CA)

**Approach**: Draw z + w as a parallelogram and z − k as a triangle, then use:
- equal moduli of two vectors ⇒ rhombus ⇒ diagonals bisect the angle: arg(z + r) = θ/2 (2018F-Q3(b)(ii));
- isosceles triangle, inscribed angle theorem, sine rule or cosine rule (2017F-Q6, 2021F-Q1(b), 2023A-Q12);
- regular hexagon: when **centred at the origin**, adjacent vertices differ in argument by π/3 and have equal moduli. For 2025F-Q7, the vertex z₀ is **at the origin**, and the hexagon is not centred at the origin: the side vectors rotate successively by π/3; using the cosine rule gives \|z₂\| = \|z₄\| = √3r, \|z₃\| = 2r, so \|z₁z₂z₃z₄z₅\| = r·√3r·2r·√3r·r = **6r⁵**; z₃ = 2r cis(π/3), Arg(z₅ − z₃) = −5π/6 (the 2025 report specifically highlights the hexagon geometry in this question).

**Past questions**: 2017F-Q1, 2017F-Q6, 2018F-Q3, 2020A-Q11, 2020A-Q15, 2021F-Q1, 2023A-Q12, 2025F-Q7.

---

## Pattern 9: Proof and technique questions

- Identities: use conj(z) = r cis(−θ), together with cos being even and sin being odd (2018A-Q10).
- Summation by grouping: n·iⁿ is not itself periodic, but every 4 consecutive terms (terms 4m+1 to 4m+4) sum to 2 − 2i, with 505 groups in total ⇒ Σₙ₌₁²⁰²⁰ n iⁿ = 505 × (2 − 2i) = 1010 − 1010i = 1010√2 cis(−π/4) (2020F-Q8).
- Solving real simultaneous equations using complex numbers: (a + bi)³ = (a³ − 3ab²) + i(3a²b − b³) = 14 − 2√5 i ⇒ taking the modulus: (a² + b²)³ = 196 + 20 = 216 ⇒ **a² + b² = 6** (2023F-Q8).
- Using complex multiplication to prove the arctangent sum (2025A-Q19(c)).
