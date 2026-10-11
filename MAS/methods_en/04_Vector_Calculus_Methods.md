# MAS · Vector Calculus and Motion — Patterns and Solution Approaches

> Based on: 12 past exam questions from 2016–2025 with marking keys + examiner reports. Appears only in the Calculator-assumed paper. Original questions: see `topics/04_Vector_Calculus.pdf`.
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`). On 2026-10-09, per user feedback, 2017A-Q18 and 2019A-Q18, which do not involve vectors, were moved out of this topic (into "Rates of Change and Differential Equations").

## Marking-key reminders

- **Difference between distance travelled and displacement vector** (2025 report focus): ∫ₐᵇ v(t) dt is the **change in displacement vector** (has direction), while ∫ₐᵇ |v(t)| dt is the **distance travelled** (scalar).
- **The constant of integration is a vector** (2018 report: many students did not clearly show how to use the constant of integration to derive r(t)): r(t) = ∫v dt + **c**, then use r(0) to solve for each component of c.
- **Notation**: vectors must be marked (tilde or bold); velocity vector and speed must be written separately; the keys for 2019A-Q13 and 2022A-Q10 each award 1 mark specifically for notation.
- After eliminating the parameter to obtain a Cartesian equation, **you must state the restrictions on the variables** (often both x and y must be restricted) (the keys for 2016A-Q16, 2024A-Q18 and 2025A-Q12 each award this mark).

## Formula card

| Quantity | Expression |
|---|---|
| Velocity | v(t) = r′(t) (differentiate component by component) |
| Acceleration | a(t) = v′(t) |
| Speed | \|v(t)\| = √(ẋ² + ẏ² (+ ż²)) |
| Distance travelled (arc length) | ∫ₐᵇ \|v(t)\| dt |
| Change in displacement | ∫ₐᵇ v(t) dt = r(b) − r(a) |
| Direction of motion | angle with the x-axis tan⁻¹(ẏ/ẋ), note the quadrant |

---

## Pattern 1: Given r(t), find velocity, acceleration and speed

**Approach**: differentiate component by component → substitute the time → take the magnitude for speed → draw the vector on the diagram (place its tail at the position at that time, with the arrow pointing in the direction of motion).
**Constant speed test** (2020A-Q12): r = (10cos 0.1t, 10sin 0.1t, 0.2t) ⇒ v = (−sin 0.1t, cos 0.1t, 0.2) ⇒ |v| = √(sin² + cos² + 0.04) = √1.04 ≈ 1.02 m/s, independent of t ⇒ **constant speed**, but the direction of the velocity vector is always changing, so it is not uniform straight-line motion. You must state that sin² + cos² = 1 was used (1 mark on its own). Observation deck height = 0.2 × 65 = 13 m.

**Past questions**: 2016A-Q16(b), 2017A-Q15(a)(d), 2019A-Q13(a)(b), 2020A-Q12, 2023A-Q16(a), 2024A-Q18(b)(d).

---

## Pattern 2: Given a(t) or v(t), integrate to find r(t)

**Standard procedure**
1. Integrate component by component, adding the **constant vector** c = (c₁, c₂).
2. Use the initial conditions (r(0), v(0)) to solve for each component.
3. Write the complete r(t).

**Projectile motion, two models**:
- Gravity + wind (2018A-Q19): a = (0, −9.8) ⇒ v = (70cos θ + w, 70 sin θ − 9.8t) ⇒ r = ((70cos θ + w)t, 70 sin θ · t − 4.9t²). Wind affects only the horizontal component.
- Horizontal drag + vertical lift (2021A-Q19): launched horizontally from E(100, 120); x′ = 32e^{−0.05t}; vertical acceleration h″ = s − 9.8 (where s is the lift), and back-solve for s = 4.8 from the given r, so r = (740 − 640e^{−0.05t}, 120 − 2.5t²).
**Range or landing point**: y(t) = 0 (or equal to the height of the slope) ⇒ solve for t ⇒ substitute into x(t). Maximum range ⇒ differentiate with respect to θ or use CAS to find the extremum.
**Landing angle**: use the angle between the velocity vector at the instant of landing and the slope or horizontal plane (2021A-Q19(e)).

**Past questions**: 2017A-Q15(c), 2018A-Q19(a)(c), 2021A-Q19, 2022A-Q10(b).

---

## Pattern 3: Eliminate the parameter to obtain a Cartesian equation ★

**Common identities**
- cos²t + sin²t = 1 ⇒ circle or ellipse (2022A-Q10(c));
- cos 2t = 1 − 2sin²t or 2cos²t − 1, directly gives the relationship between x and y ⇒ a segment of a parabola (2016A-Q16: x = 2y² − 4);
- first use double-angle formulas to reduce both components to the same angle, then use sin² + cos² = 1 to eliminate the parameter ⇒ a general curve (2019A-Q13(d): (1 − y)² + (x²/2 − 1)² = 1, a figure-eight);
- x is linear in t: solve for t directly from x and substitute into y (2018A-Q19(b); the 2018 report singled out this part as poorly answered);
- (eᵗ + e⁻ᵗ)² − (eᵗ − e⁻ᵗ)² = 4 ⇒ hyperbola x² − y² = 4 (2024A-Q18(e));
- exponential parameter: solve t = ln(…) from x, then substitute into y (2025A-Q12(a)).

**Do not omit the final step**: state the range of the actual path, **deduced from the range of t**; the keys state: 2016A-Q16: −2 ≤ y ≤ 2 (or −4 ≤ x ≤ 4); 2024A-Q18: x ≥ 2 **and y ≥ 0** (writing only x ≥ 2 would include the lower branch and lose the mark); 2025A-Q12: 1 ≤ x ≤ e³.

**Past questions**: 2016A-Q16(a), 2018A-Q19(b), 2019A-Q13(d), 2022A-Q10(c), 2024A-Q18(e), 2025A-Q12(a).

---

## Pattern 4: Interpreting distance travelled (arc length) and displacement

**Approach**
1. Find the start and end times. **The time for one circuit = the least common multiple of the periods of the components**: 2022A-Q10 is 2π, 2019A-Q13 is 4π (contains t/2), 2017A-Q15 is 6π (contains t/3). These two questions each award 1 mark for correct limits. You can also back-solve for t from the coordinates: point B is (10/3, 8/3) at t = ln 3.
2. Write **∫ₐᵇ √(ẋ² + ẏ²) dt** (the usual marking points: the start and end t-values or limits, the speed expression, and the calculated result or notation; the allocation varies by year; "Do not evaluate" questions have no mark for calculation).
3. When the question says "Do not evaluate", just write the integral expression containing the trigonometric functions.

**Explain the meaning of the integrals (2 marks)**
- ∫₀¹ v(t) dt: "the change in displacement (position vector) during the first second".
- ∫₀^{2π} |v(t)| dt: "the distance travelled in one complete circuit (2π seconds)" (2022A-Q10).
- ∫₀³ r′(t) dt: the change in displacement vector, drawn on the diagram as an arrow from r(0) to r(3) (2025A-Q12(c)).

**Past questions**: 2016A-Q16(c), 2017A-Q15(b)(e), 2019A-Q13(c), 2022A-Q10(a), 2023A-Q16(b), 2024A-Q18(c), 2025A-Q12(b)–(d).

---

## Pattern 5: Closest distance between objects moving in straight lines (3D)

**Approach**
1. Write the positions of the two objects: r_K(t) = r_K0 + t·v_K, r_B(t) = r_B0 + t·v_B.
2. Relative position d(t) = r_K(t) − r_B(t). The position of P relative to Q = r_P − r_Q; when the question asks for a relative position vector, the order must be correct (2017A-Q14(b): "from the top of the tower" ⇒ r_drone − r_tower, the key awards 1 mark). When only distance is required, the order does not affect the magnitude.
3. Closest distance: set d(t)·(v_K − v_B) = 0, or use CAS to find the minimum of |d(t)|.
4. "Time interval within 50 m": solve |d(t)| < 50 and find the length of the time interval (2017A-Q14(c)).
5. Shortest distance between two paths (2024A-Q16(c): the **speed and departure time** can be adjusted, so the problem reduces to the shortest distance between two straight lines): use two independent parameters λ, μ, and require the common perpendicular vector to be perpendicular to both direction vectors (2024A-Q16(c)).
6. Angle of descent (angle with the horizontal plane): first find the angle φ between the velocity vector and k; angle of descent = **|90° − φ|** (Ben's v = (−0.5, 1, −1.5), φ ≈ 143.3°, 90° − φ = −53.3°, answer 53°; 2024A-Q16(b)). You can also use sin⁻¹(|v_z| / |v|) directly.

(The Ferris wheel and carousel questions (2017A-Q18, 2019A-Q18) do not involve vectors and have been moved to the related rates pattern in the "Rates of Change and Differential Equations" notes.)

**Past questions**: 2017A-Q14, 2024A-Q16.
