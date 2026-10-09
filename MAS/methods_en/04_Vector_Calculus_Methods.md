# MAS · Vector Calculus and Motion — Patterns and Solution Approaches

> Source: 12 past exam questions from 2016–2025, marking keys + exam reports. Appears only in the Calculator-assumed paper. Original questions: see `topics/04_Vector_Calculus.pdf`.
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`). On 2026-10-09, following user feedback, 2017A-Q18 and 2019A-Q18, which do not involve vectors, were moved out of this topic (into "Rates of Change and Differential Equations").

## Marking panel reminders

- **Difference between distance travelled and displacement vector** (2025 report focus): ∫ₐᵇ v(t) dt is the **change in displacement vector** (has direction), while ∫ₐᵇ |v(t)| dt is the **distance travelled** (scalar).
- **The constant of integration is a vector** (2018 report: many people cannot clearly show how to use the constant of integration to obtain r(t)): r(t) = ∫v dt + **c**, then use r(0) to solve for each component of c.
- **Notation**: Vectors must be labelled (with a wavy underline or bold), and velocity vector and speed must be written separately; the keys for 2019A-Q13 and 2022A-Q10 each have 1 mark specifically for notation.
- After eliminating the parameter to obtain the Cartesian equation, **you must state the value restrictions** (often both x and y need restrictions) (the keys for 2016A-Q16, 2024A-Q18 and 2025A-Q12 all have this mark).

## Formula sheet

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

**Approach**: Differentiate component by component → substitute the time → take the magnitude for speed → draw the vector on the diagram (tail at the position at that time, arrow pointing in the direction of motion).
**Constant speed check** (2020A-Q12): r = (10cos 0.1t, 10sin 0.1t, 0.2t) ⇒ v = (−sin 0.1t, cos 0.1t, 0.2) ⇒ |v| = √(sin² + cos² + 0.04) = √1.04 ≈ 1.02 m/s, independent of t ⇒ **the speed is constant** (constant speed), but the direction of the velocity vector is always changing, so it is not uniform straight-line motion. You must state that sin² + cos² = 1 is used (1 mark separately). Observation deck height = 0.2 × 65 = 13 m.

**Past exam questions**: 2016A-Q16(b), 2017A-Q15(a)(d), 2019A-Q13(a)(b), 2020A-Q12, 2023A-Q16(a), 2024A-Q18(b)(d).

---

## Pattern 2: Given a(t) or v(t), integrate to find r(t)

**Standard procedure**
1. Integrate component by component, adding the **constant vector** c = (c₁, c₂).
2. Use the initial conditions (r(0), v(0)) to solve for each component.
3. Write the full r(t).

**Projectile motion, two models**:
- Gravity + wind (2018A-Q19): a = (0, −9.8) ⇒ v = (70cos θ + w, 70 sin θ − 9.8t) ⇒ r = ((70cos θ + w)t, 70 sin θ · t − 4.9t²). Wind affects only the horizontal component.
- Horizontal drag + vertical lift (2021A-Q19): launched horizontally from E(100, 120); x′ = 32e^{−0.05t}; vertical acceleration h″ = s − 9.8 (s is the lift), use the given r to solve backwards for s = 4.8, so r = (740 − 640e^{−0.05t}, 120 − 2.5t²).
**Range or landing point**: y(t) = 0 (or equal to the slope height) ⇒ solve for t ⇒ substitute into x(t). Maximum range ⇒ differentiate with respect to θ or use CAS to find the maximum.
**Landing angle**: use the angle between the velocity vector at the instant of landing and the slope or horizontal plane (2021A-Q19(e)).

**Past exam questions**: 2017A-Q15(c), 2018A-Q19(a)(c), 2021A-Q19, 2022A-Q10(b).

---

## Pattern 3: Eliminate the parameter to obtain the Cartesian equation ★

**Common identities**
- cos²t + sin²t = 1 ⇒ circle or ellipse (2022A-Q10(c));
- cos 2t = 1 − 2sin²t or 2cos²t − 1, which directly gives the relationship between x and y ⇒ a segment of a parabola (2016A-Q16: x = 2y² − 4);
- First use double-angle formulas to turn the two components into the same angle, then use sin² + cos² = 1 to eliminate the parameter ⇒ a general curve (2019A-Q13(d): (1 − y)² + (x²/2 − 1)² = 1, a figure-eight shape);
- x is linear in t: solve directly for t from x and substitute into y (2018A-Q19(b); the 2018 report specifically identifies this part as poorly answered);
- (eᵗ + e⁻ᵗ)² − (eᵗ − e⁻ᵗ)² = 4 ⇒ hyperbola x² − y² = 4 (2024A-Q18(e));
- Exponential parameter: solve x for t = ln(…), then substitute into y (2025A-Q12(a)).

**The final step must not be missed**: state the range of the actual path, **derived from the range of t**, key wording: 2016A-Q16: −2 ≤ y ≤ 2 (or −4 ≤ x ≤ 4); 2024A-Q18: x ≥ 2 **and y ≥ 0** (writing only x ≥ 2 includes the lower branch and loses marks); 2025A-Q12: 1 ≤ x ≤ e³.

**Past exam questions**: 2016A-Q16(a), 2018A-Q19(b), 2019A-Q13(d), 2022A-Q10(c), 2024A-Q18(e), 2025A-Q12(a).

---

## Pattern 4: Distance travelled (arc length) and interpretation of displacement

**Approach**
1. Find the start and end times. **The time for one complete circuit = the least common multiple of the periods of the components**: 2022A-Q10 is 2π, 2019A-Q13 is 4π (contains t/2), 2017A-Q15 is 6π (contains t/3). These two questions each have 1 mark for the correct limits. You can also work backwards from the coordinates to find t: point B is (10/3, 8/3) when t = ln 3.
2. Write **∫ₐᵇ √(ẋ² + ẏ²) dt** (the usual mark-earning points: start/end t-values or limits, speed expression, evaluated result or notation; allocation varies by year; "Do not evaluate" questions have no mark for evaluating).
3. When the question says "Do not evaluate", just write the integral expression containing trigonometric functions.

**Explain the meaning of the integral (2 marks)**
- ∫₀¹ v(t) dt: "the change in displacement (position vector) during the first second".
- ∫₀^{2π} |v(t)| dt: "the distance travelled in one complete circuit (2π seconds)" (2022A-Q10).
- ∫₀³ r′(t) dt: the change in displacement vector, drawn on the diagram as an arrow from r(0) to r(3) (2025A-Q12(c)).

**Past exam questions**: 2016A-Q16(c), 2017A-Q15(b)(e), 2019A-Q13(c), 2022A-Q10(a), 2023A-Q16(b), 2024A-Q18(c), 2025A-Q12(b)–(d).

---

## Pattern 5: Closest distance between objects moving in straight lines (3D)

**Approach**
1. Write the positions of the two objects: r_K(t) = r_K0 + t·v_K, r_B(t) = r_B0 + t·v_B.
2. Relative position d(t) = r_K(t) − r_B(t). The position of P relative to Q = r_P − r_Q; when the question asks for a relative position vector, the order must be correct (2017A-Q14(b): "from the top of the tower" ⇒ r_drone − r_tower, with 1 mark in the key). When only finding distance, the order does not affect the magnitude.
3. Closest distance: set d(t)·(v_K − v_B) = 0, or use CAS to find the minimum of |d(t)|.
4. "Time period within 50 m": solve |d(t)| < 50 and find the length of the time interval (2017A-Q14(c)).
5. Shortest distance between two paths (2024A-Q16(c): **velocity and departure time** can be adjusted, so the problem reduces to the shortest distance between two straight lines): use two independent parameters λ, μ and require the common perpendicular vector to be perpendicular to both direction vectors (2024A-Q16(c)).
6. Angle of descent (angle with the horizontal plane): first find the angle φ between the velocity vector and k, then angle of descent = **|90° − φ|** (for Ben's v = (−0.5, 1, −1.5), φ ≈ 143.3°, 90° − φ = −53.3°, answer 53°; 2024A-Q16(b)). You can also use sin⁻¹(|v_z| / |v|) directly.

(Ferris wheel and carousel questions (2017A-Q18, 2019A-Q18) do not involve vectors and have been moved into the related rates pattern in the "Rates of Change and Differential Equations" notes.)

**Past exam questions**: 2017A-Q14, 2024A-Q16.
