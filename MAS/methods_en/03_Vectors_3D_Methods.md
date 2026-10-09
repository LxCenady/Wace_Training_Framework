# MAS · 3D Vectors and Systems of Linear Equations — Patterns and Solution Approaches

> Source: 25 past exam questions from 2016–2025, marking keys + exam reports. Original questions in `topics/03_Vectors_3D.pdf`. Systems of equations examples verified with sympy. Also cites two 2016 sample paper questions (`2016S-A8`, `2016S-A10`; original papers in `papers/2016Sample_*`).
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`).

## Marking panel reminders

- **How to write when the three planes do not have a unique solution**: understanding of “no unique solution” and its geometric meaning was called out in the 2018, 2020, 2021, 2022, 2023 and 2024 reports. The 2022 report specifically notes that many people stopped after writing “there are infinitely many solutions” (the 2023 report mentions a similar issue). You must **write the solution set**—using a parameter, or expressing the other variables in terms of one variable (key: "expresses correct relationships between variables"); when the question asks for a vector equation, write it as r = p + t·d (2023F-Q5(c)). You also need to state the geometric meaning.
- “No solution” has two geometric cases, and they must be distinguished: there are **parallel planes**; or the three planes **intersect pairwise in three parallel lines** (like a triangular prism; 2020F-Q4 is exactly this case; the report says this case was never tested from 2016–2019, and some candidates were completely unprepared).
- **Proving two lines do not intersect**: you must write the component equations and show there is no solution; “CAS says no solution” is not a proof (2021 report).
- **Vector notation**: distinguish position vectors from direction vectors within a plane (2017 report); reports criticised incorrect vector notation (2018, 2022, 2025), and the keys for 2020A-Q20 and 2025A-Q18 have marks tied to correct notation. (Editor's suggestion: add a wavy underline or bold to vectors; do not mix dot and cross product symbols.)
- Cross product calculation errors are a common source of lost marks in CF (2020 report).

## Toolkit

- Line: r = a + λd; plane: r·n = p·n (p is a point on the plane) ⇔ ax + by + cz = k, where n = (a, b, c); parametric form r = a + λu + μv, where **n = u × v**.
- Sphere: |r − c| = R ⇔ (x − c₁)² + (y − c₂)² + (z − c₃)² = R² (obtained by completing the square from the general form).
- Angle between a line and a plane: cos φ = |d·n| / (|d||n|) (take the absolute value to ensure φ is acute), angle between line and plane = 90° − φ; equivalently sin θ = |d·n| / (|d||n|).
- Distance from a point to a plane = |n·(P − A)| / |n|, where A is any point on the plane. **This formula is not on the formula sheet** (2019A-Q19 asks you to prove it); in CA questions, if using it directly it is best to add a one-line derivation, or use the “draw the normal through the point and find the intersection” method (2018A-Q17(c)); volume of a parallelepiped = |c·(a × b)|.

---

## Pattern 1: Solving systems of linear equations and discussing solution cases ★★ appeared in CF in 7 of the last 10 years (also in CA in 2021)

**Standard procedure**
1. Elimination: use two pairs of equations to eliminate the same variable (key mark 1), solve for the first variable (key mark 2), then substitute back to find the other two (key mark 3).
2. **With parameter k**: reduce to (coefficient containing k)·z = (constant containing k), e.g. (k − 2)z = c − 5 (2025F-Q4):
   - k − 2 ≠ 0 ⇒ **unique solution** (c can be any real number) ⇒ the three planes intersect at a point;
   - k − 2 = 0 and c − 5 ≠ 0 ⇒ **no solution**;
   - k − 2 = 0 and c − 5 = 0 ⇒ **infinitely many solutions** ⇒ they intersect in a line.
3. **When there are infinitely many solutions, write the line** (2022F-Q5): let z = t ⇒ y = t − 1, x = (11 − 3t)/2 ⇒ r = (11/2, −1, 0) + t(−3/2, 1, 1).
4. **Determining parallelism**: normal vectors are scalar multiples of each other ⇔ planes are parallel. Check the normal vectors first, then decide whether it is “no solution caused by parallel planes” or “three parallel lines of intersection (prism)”.

**Geometric interpretation template**
| Algebraic result | Geometric meaning |
|---|---|
| unique solution | three planes intersect at a single point |
| infinitely many solutions (with one parameter) | three planes intersect in a common line (two of the planes may coincide, e.g. 2021A-Q14; the key requires both points to be written) |
| infinitely many solutions (with two parameters) | three planes coincide (the solution set is a plane) |
| no solution, some normal vectors are scalar multiples | at least two planes are parallel (and distinct) |
| no solution, normal vectors are pairwise non-parallel | planes intersect pairwise in three parallel lines (triangular prism) |

**Past exam questions**: 2016F-Q6, 2016S-A8, 2018F-Q2, 2020F-Q4, 2021A-Q14, 2022F-Q5, 2023F-Q5, 2024F-Q6, 2025F-Q4.

---

## Pattern 2: Equation of a plane (finding the normal vector)

**Approach**
- Given parametric form: n = u × v (write each component of the cross product clearly), then substitute a point to find d (2020F-Q2, 2018A-Q17(b)).
- Through three points: cross product two edge vectors (2022A-Q19(a)), or set ax + by + cz = d and substitute the three points to solve.
- Given z = 2x + y + 4 ⇒ rewrite as 2x + y − z = −4 ⇒ n = (2, 1, −1) (2019A-Q16(a), 2023A-Q14(a)).
- Contains a line and is perpendicular to another plane ⇒ n₂ = d_L × n₁ (2019A-Q16(c), 2023A-Q14(d)).
- Contains two intersecting lines ⇒ n = d₁ × d₂ (2025A-Q11(b)).

**Past exam questions**: 2016F-Q7(b), 2017F-Q7(a)(ii), 2018A-Q17, 2019A-Q16, 2020F-Q2, 2022A-Q19(a), 2023A-Q14, 2025A-Q11.

---

## Pattern 3: Intersections, angles, closest point

**Intersection of a line and a plane**: substitute r = a + λd into the plane equation ⇒ solve for λ ⇒ find the point (3 marks: substitute, solve for λ, write the point).
**Line and sphere**: after substitution, get a quadratic equation in λ. Two solutions ⇒ two intersection points; one repeated root ⇒ tangent; no real roots ⇒ no intersection (2019A-Q16(d), 2023A-Q9(b)). Alternative method: compare the distance from the centre of the sphere to the line with the radius.
**Two lines**: equate components to get three equations, use two of them to solve for λ and μ, **then substitute into the third to check**. If it does not hold ⇒ no intersection (this is the “proof” required by 2021A-Q16(c)).
**Closest point on a plane to point L**: draw the line through L in the direction of the normal, L + λn, and find its intersection with the plane (2022A-Q19(b)).
**Angle between a line and a plane**: cos φ = |d·n| / (|d||n|), required angle = 90° − φ (2023A-Q14(c), 2024A-Q16(b) angle of descent).

**Past exam questions**: 2016A-Q20(a), 2019A-Q16(b)(d), 2021A-Q16(c), 2022A-Q19(b), 2023A-Q9, 2023A-Q14(c), 2025A-Q11(a).

---

## Pattern 4: Sphere

**Approach**
- From endpoints of a diameter: centre = midpoint (report: many people calculated the position vector incorrectly), radius = |AB|/2 (2016F-Q7(a)).
- General form → standard form: complete the square. Example: x² + y² + z² − 4x + 2y − 6z + 5 = 0 ⇒ (x − 2)² + (y + 1)² + (z − 3)² = 9 ⇒ |r − (2, −1, 3)| = 3 (2023A-Q9(a)).
- Tangent to a plane: radius = distance from the centre of the sphere to the plane; or draw the normal through the centre and find its intersection with the plane (2018A-Q17(c)).
- Passes through all vertices of a rectangular prism: the centre is the midpoint of a space diagonal (2021A-Q16(b)).

---

## Pattern 5: Vector proofs (appears in both CF and CA)

**Standard working**
1. Express the required vector using the given basis vectors (a, b, e): PQ = OQ − OP = (a + kb) − ka.
2. Calculate the dot product and expand (the key gives a mark for “expanding to get 4 terms”).
3. **Use the given conditions**: square ⇒ a·b = 0 and |a| = |b|; midpoint ⇒ ½(a + b).
4. State the conclusion: PQ·QR = 0 ⇒ ∠PQR = 90°.

**Past exam questions**: 2016S-A10 (proof of the point-to-line distance formula), 2019A-Q19 (distance between parallel planes), 2020A-Q20 (right angle in a square), 2018F-Q8(b) (why c·(a × b) is the volume: |a × b| is the base area, and the projection of c onto the normal is the height), 2025A-Q18 (pyramid).

---

## Pattern 6: Contextual applications (laser reflection, steepest descent on a ramp, drone approaching a tower)

- Reflection (2016A-Q20(b)): the unit vector **from B to S** + the unit vector **from B to R** = k·n (the diagonal of a rhombus). Equivalent form: d̂_out − d̂_in ∥ n. Note: the key wording says "direction of SB", but what is actually substituted is the B→S direction; adding in the S→B direction gives a vector parallel to the mirror, not parallel to n.
- Steepest descent direction on a ramp: lies in the ramp plane and is perpendicular to the horizontal line AB (2022A-Q19(c)).
- Motion and distance must be split into two types (see the “Vector Calculus” notes for details):
  - (i) Same time parameter t: to find the closest distance, use r(t)·(relative velocity) = 0; to find how long |r(t)| < R lasts, solve an inequality (2017A-Q14(c)).
  - (ii) Shortest distance between two lines in space: use two independent parameters λ and μ, and set PQ·d₁ = PQ·d₂ = 0 (2024A-Q16(c): Ben can adjust speed and departure time; an alternative solution to 2021A-Q16(c)).
