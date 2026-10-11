# MAM · Rectilinear Motion — Patterns and Solution Approaches

> Source: marking keys for 13 past rectilinear motion questions from 2016–2025 + exam reports (the 2018, 2024 and 2025 reports explicitly list rectilinear motion as a weakness; the 2021 report reminds students to distinguish between distance and displacement; the 2023 report specifically mentions signed area and dt notation). Original questions are in `topics/03_Rectilinear_Motion.pdf`.
> Review status: has undergone one round of independent review and been revised according to feedback (see `Review_log.md`).

## Concept Quick Reference (the reports say this is where concepts are most easily confused)

| Quantity | Definition | Note |
|---|---|---|
| Displacement x(t) | position relative to the origin, can be positive or negative | 'returns to the starting point' is x(t) = x(0), not v = 0 |
| Velocity v = x′(t) | can be positive or negative (direction) | 'at rest' is v = 0; 'changes direction' is v changing sign |
| Speed = \|v\| | non-negative | For maximum speed, compare \|v\| at the extremum points **and** endpoints |
| Acceleration a = v′(t) | can be positive or negative | Where velocity has an extremum in the **interior** of the interval, a = 0 must occur; the converse is not necessarily true (e.g. v = t³ at t = 0; in a constant-velocity section a is always 0); compare the endpoints separately |
| Change in displacement = ∫ₐᵇ v dt | signed area | 'What does signed area represent?' = change in displacement from t=a to t=b |
| Distance travelled = ∫ₐᵇ \|v\| dt | non-negative | must split into intervals at v = 0 |

**Speeding up or slowing down**: v and a with the **same sign** means speeding up; with **opposite signs** means slowing down. The exact wording of the 2024F-Q2 key: saying only that acceleration is negative is not a valid reason.
**Note**: The 2018A-Q11(c) key treats "heading south and decelerating at 0.5" as a = −0.5 (by the definition above, v and a then have the same sign, so it is actually speeding up). When you encounter this kind of wording, write your interpretation clearly and state the positive direction.

**Time wording**: 'when it first appears' and 'initially' mean t = 0 (2024 report: many students substituted t = 1 by mistake); 'during the fifth second' means 4 ≤ t ≤ 5.

---

## Pattern 1: Given x(t), find v, a and their meaning

**Approach**: differentiate to get v; differentiate again to get a; substitute the time asked; **write units**; when explaining, make the direction clear (what the positive direction is, e.g. north, up, to the right (in 2024F-Q2, x is the distance from the left edge of the screen, and the key writes "to the right")).

**Marks awarded for**: ✓ expression for v(t) ✓ substitution (including units) ✓ expression for a(t) ✓ conclusion with reason (same sign/opposite signs).

**Past questions**: 2016F-Q4, 2016A-Q19(a), 2022A-Q10(b), 2024F-Q2(a)(b).

---

## Pattern 2: Given a(t) or v(t), work backwards using initial conditions

**Identify**: "initial velocity is 5 cm/s", "x(0) = 0", "After 2 seconds displacement is −50 cm"; find constants p, k.

**Approach**
1. Integrate a → v (**+c**) → use v(0) to determine c.
2. Integrate again v → x (**+c₂**) → use the known position to determine c₂.
3. When the equation contains unknown parameter p: write each of the two position conditions as an equation, then solve simultaneously for p and the constant (2017A-Q20).
4. When integrating a trigonometric v (e.g. v = 2 sin(t/3 + π/6)), divide by the inner coefficient 1/3, i.e. multiply by 3, giving −6cos(t/3 + π/6) + C; set the calculator to radians.

**Marks awarded for (2018A-Q11(a))**: ✓ integrate to obtain a cos form ✓ write the constant and form an equation using x(0) = 0 ✓ find C and write x(t).

**Past questions**: 2017A-Q20(b), 2018A-Q11, 2019A-Q9(c), 2021A-Q17(a), 2022A-Q11(c), 2023A-Q8(e) (compare coefficients to find A, B).

---

## Pattern 3: When it is at rest / changes direction / returns to the starting point

**Approach**
- At rest: solve v(t) = 0. Changes direction: v must **change sign** (check whether v actually changes sign either side of that point; if v only touches 0 and returns to its original sign, e.g. v = (t − 2)², the object has not changed direction).
- Returns to the starting point: solve x(t) = x(0); passes through the origin: solve x(t) = 0 (these are the same only when x(0) = 0). Take the positive root that is the 'first' one required by the question.
- When only a sign table is given (2025F-Q6): x changes sign → passes through the origin; v changes sign → stops and turns around; v and a have opposite signs → slowing down. In the explanation, state that the reason is 'the sign of v changes'.

**Past questions**: 2016A-Q19(a), 2017A-Q20(c), 2021A-Q17(b), 2022A-Q10(a)(c), 2023A-Q8(a), 2025F-Q6.

---

## Pattern 4: Total distance travelled vs displacement ★ must-know

**Identify**: "total distance travelled" and "How far has … travelled" ask for distance travelled, whereas "Evaluate ∫v dt and explain" asks for change in displacement.

**Standard procedure (total distance travelled)**
1. Solve v = 0 to find all times t₁, t₂… in the interval when it is stationary.
2. Write the distance expression; either form is acceptable:
   - |x(t₁) − x(0)| + |x(t₂) − x(t₁)| + … (the key's method for 2024F-Q2(d));
   - ∫|v(t)| dt, or split into intervals: **put a negative sign in front of the section where v < 0** (or put absolute value signs around each section). In 2023A-Q8(c), v = −2t sin t is negative on (π/3, π) and positive on (π, 4π/3), so it is written as −∫_{π/3}^{π} v dt + ∫_{π}^{4π/3} v dt. The key awards 1 mark separately for the signs, and there is also 1 mark for **including dt in every integral**.
3. Calculate and include units.

**Interpreting ∫ₐᵇ v dt**: "the change in displacement (position) of … from t = a s to t = b s" — the start and end times must also be written (2024F-Q2(c) has 1 mark specifically for the start and end times).

**Marks awarded for**: ✓ find the stationary times ✓ correct split expression ✓ numerical value.

**Common errors**: treating x(15) − x(0) directly as distance travelled; missing an intermediate turning point when splitting intervals.

**Past questions**: 2016A-Q19(b)(d), 2017A-Q20(d), 2018A-Q11(c), 2021A-Q14, 2021A-Q17(c), 2023A-Q8(b)(c), 2024F-Q2(c)(d).

---

## Pattern 5: Maximum velocity / zero acceleration

**Approach**: set a(t) = v′(t) = 0 to find t → substitute into v → **verify the maximum**: confirm using v″ < 0 (or a sign test); when the question requires using calculus, this step earns marks (2022A-Q11(b) key: confirms that v″ < 0); when asked for the maximum on an interval, also compare with the endpoints. When asked for maximum **speed**, also compare |v| at the endpoints (2016A-Q19(c) key: examines velocity at endpoints).

**Past questions**: 2016A-Q19(c), 2022A-Q11(b), 2023A-Q8(d), 2021A-Q14, 2019A-Q12(c) (constant velocity for the first 2 minutes, a is always 0, not an extremum).

---

## Pattern 6: Interpreting context and graphs

**Identify**: A graph of a(t) or v(t) is given, and the question asks "explain what is happening to the velocity in 0 < t < 8".

**How to write it**: "Since a(t) > 0 for 0 < t < 8, the (upward) velocity is increasing; since a(t) < 0 for 8 < t < 16, the velocity is decreasing (but still positive, still moving up)." Marking requirements: ✓ refer to the graph or sign of a ✓ conclusion for the first part ✓ conclusion for the second part.

**Sketching (2025F-Q6(d))**: the x(t) graph must satisfy all three sets of signs for x, v and a at the same time: start at the origin, have a positive initial slope, and cross the t-axis only between 3 < t < 4; the sign of the slope corresponds to v, and concavity corresponds to a.

**Past questions**: 2019A-Q9(a)(b), 2025F-Q6(d), 2022A-Q10(d) (amplitude envelope 3e⁻ᵗ = 0.01).

---
