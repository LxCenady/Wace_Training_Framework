# MAM · Rectilinear Motion — Patterns and Solution Strategies

> Based on: the marking keys + exam reports for 13 rectilinear motion questions from 2016–2025 (the 2018, 2024 and 2025 reports explicitly list rectilinear motion as a weak area; the 2021 report reminds students to distinguish distance from displacement; the 2023 report names signed area and the dt notation). Original questions are in `topics/03_Rectilinear_Motion.pdf`.
> Review status: has been through one round of independent review and revised in line with the feedback (see `Review_log.md`).

## Concept quick reference (the reports say these are the concepts most easily confused)

| Quantity | Definition | Watch out for |
|---|---|---|
| Displacement x(t) | Position relative to the origin, positive or negative | 'Returning to the starting point' is x(t) = x(0), not v = 0 |
| Velocity v = x′(t) | Positive or negative (direction) | 'at rest' is v = 0; 'changes direction' is v changing sign |
| Speed = \|v\| | Non-negative | For maximum speed, compare \|v\| at the local extrema **and** at the endpoints |
| Acceleration a = v′(t) | Positive or negative | Where the velocity takes a local extremum **inside** the interval, a = 0 is guaranteed; the converse is not true (e.g. v = t³ at t = 0; on a constant-velocity section a is always 0); endpoints are compared separately |
| Change in displacement = ∫ₐᵇ v dt | Signed area | 'What does the signed area represent?' = change in displacement from t=a to t=b |
| Distance travelled = ∫ₐᵇ \|v\| dt | Non-negative | Must be split into sections at v = 0 |

**Speeding up or slowing down**: v and a with the **same sign** is speeding up; with **opposite signs** is slowing down. The exact words in the 2024F-Q2 key: saying only that acceleration is negative is not a valid reason.
**Note**: the key for 2018A-Q11(c) treats "heading south and decelerating at 0.5" as a = −0.5 (by the definition above, v and a then have the same sign, so it is actually speeding up). With wording like this, state your interpretation clearly and specify the positive direction.

**Time wording**: 'when it first appears' and 'initially' mean t = 0 (2024 report: many students substituted t = 1 by mistake); 'during the fifth second' means 4 ≤ t ≤ 5.

---

## Pattern 1: Given x(t), find v, a and what they mean

**Approach**: differentiate to get v; differentiate again to get a; substitute the time asked for; **write the units**; in your explanation state the direction clearly (what the positive direction is — for example north, up, to the right (in 2024F-Q2, x is the distance from the left edge of the screen; the key writes "to the right")).

**Mark-scoring points**: ✓ expression for v(t) ✓ substituted value (with units) ✓ expression for a(t) ✓ conclusion with reason (same sign/opposite signs).

**Past questions**: 2016F-Q4, 2016A-Q19(a), 2022A-Q10(b), 2024F-Q2(a)(b).

---

## Pattern 2: Given a(t) or v(t), work backwards using the initial conditions

**How to recognise it**: 'initial velocity is 5 cm/s', 'x(0) = 0', 'After 2 seconds displacement is −50 cm', and you have to find the constants p, k.

**Approach**
1. Integrate a → v (**+c**) → use v(0) to determine c.
2. Integrate again, v → x (**+c₂**) → use the known position to determine c₂.
3. When the equation contains an unknown parameter p: write each of the two position conditions as an equation, then solve simultaneously for p and the constants (2017A-Q20).
4. For a trigonometric v (e.g. v = 2 sin(t/3 + π/6)), when integrating divide by the inner coefficient 1/3, i.e. multiply by 3, giving −6cos(t/3 + π/6) + C; set your calculator to radians.

**Mark-scoring points (2018A-Q11(a))**: ✓ integrate to obtain the cos form ✓ write the constant and form an equation using x(0) = 0 ✓ find C and write down x(t).

**Past questions**: 2017A-Q20(b), 2018A-Q11, 2019A-Q9(c), 2021A-Q17(a), 2022A-Q11(c), 2023A-Q8(e) (equate coefficients to find A, B).

---

## Pattern 3: When it is at rest / changes direction / returns to the starting point

**Approach**
- At rest: solve v(t) = 0. Changes direction: v must **change sign** (check whether v really changes sign either side of that point; if v merely touches 0 and returns to the same sign, e.g. v = (t − 2)², the object has not changed direction).
- Returns to the starting point: solve x(t) = x(0); passes through the origin: solve x(t) = 0 (these are the same only when x(0) = 0). Take the 'first' positive root the question asks for.
- When you only have a sign table (2025F-Q6): x changes sign → passes through the origin; v changes sign → stops and turns around; v and a with opposite signs → slowing down. In your explanation, state that the basis is 'the sign of v changes'.

**Past questions**: 2016A-Q19(a), 2017A-Q20(c), 2021A-Q17(b), 2022A-Q10(a)(c), 2023A-Q8(a), 2025F-Q6.

---

## Pattern 4: Total distance travelled vs displacement ★ guaranteed to appear

**How to recognise it**: 'total distance travelled', 'How far has … travelled' (these ask for distance) vs 'Evaluate ∫v dt and explain' (this asks for the change in displacement).

**Standard procedure (total distance travelled)**
1. Solve v = 0 to find all the times t₁, t₂… within the interval at which it stops.
2. Write the expression for the distance travelled; either form is acceptable:
   - |x(t₁) − x(0)| + |x(t₂) − x(t₁)| + … (the form used in the key for 2024F-Q2(d));
   - ∫|v(t)| dt, or integrate in sections: **put a negative sign in front of the section where v < 0** (or put absolute value signs around each section). In 2023A-Q8(c), v = −2t sin t is negative on (π/3, π) and positive on (π, 4π/3), so it is written as −∫_{π/3}^{π} v dt + ∫_{π}^{4π/3} v dt. The key awards 1 mark separately for the signs, and 1 mark for **including dt on every integral**.
3. Calculate and include units.

**Explaining ∫ₐᵇ v dt**: 'the change in displacement (position) of … from t = a s to t = b s' — you must also state the start and end times (in 2024F-Q2(c), 1 mark is awarded specifically for the start and end times).

**Mark-scoring points**: ✓ find the stopping times ✓ correct sectioned expression ✓ numerical value.

**Common errors**: treating x(15) − x(0) directly as the distance travelled; missing the turning points in the middle when splitting into sections.

**Past questions**: 2016A-Q19(b)(d), 2017A-Q20(d), 2018A-Q11(c), 2021A-Q14, 2021A-Q17(c), 2023A-Q8(b)(c), 2024F-Q2(c)(d).

---

## Pattern 5: Maximum velocity / zero acceleration

**Approach**: set a(t) = v′(t) = 0 and solve for t → substitute into v → **verify it is a maximum**: confirm using v″ < 0 (or a sign test); this step carries marks when the question says using calculus (2022A-Q11(b) key: confirms that v″ < 0); if the question asks for the maximum on the interval, also compare with the endpoints. If it asks for the maximum **speed**, also compare |v| at the endpoints (2016A-Q19(c) key: examines velocity at endpoints).

**Past questions**: 2016A-Q19(c), 2022A-Q11(b), 2023A-Q8(d), 2021A-Q14, 2019A-Q12(c) (the first 2 minutes are at constant velocity, a is always 0, so it is not an extremum).

---

## Pattern 6: Interpreting context and graphs

**How to recognise it**: you are given a graph of a(t) or v(t) and asked to 'explain what is happening to the velocity in 0 < t < 8'.

**How to write it**: 'Since a(t) > 0 for 0 < t < 8, the (upward) velocity is increasing; since a(t) < 0 for 8 < t < 16, the velocity is decreasing (but still positive, still moving up).' Marking requirements: ✓ refer to the graph or sign of a ✓ conclusion for the first part ✓ conclusion for the second part.

**Sketching (2025F-Q6(d))**: the graph of x(t) must satisfy all three sets of signs — x, v and a — at the same time: it starts at the origin with positive initial slope and crosses the t-axis only between 3 < t < 4; the sign of the slope corresponds to v, and the concavity corresponds to a.

**Past questions**: 2019A-Q9(a)(b), 2025F-Q6(d), 2022A-Q10(d) (amplitude envelope 3e⁻ᵗ = 0.01).
