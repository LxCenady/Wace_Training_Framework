# MAM · Differentiation and Its Applications — Question Patterns and Solution Approaches

> Based on: the ratified marking key for the 51 past exam questions involving differentiation from 2016–2025 (the "Specific behaviours" point-by-point scoring points) + past exam reports.
> Past exam question numbering: `2021A-Q12` = 2021 Calculator-assumed Question 12, `F` = Calculator-free; `2016S-A19` = 2016 official sample paper (not among the 51 questions; original paper see `papers/2016Sample_*`). Original questions and marking: see `topics/01_Differentiation.pdf`.
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`).

## First, Remember: Where Markers Repeatedly Deduct Marks

- **Optimisation questions must verify the extremum**: The 2024 report states: for optimisation questions requiring calculus, full marks require using the second derivative test or sign test to verify the nature of the stationary point. Verification is usually worth 1 mark on its own (e.g. 1 of the 4 marks in 2024A-Q12(c)).
- **The second derivative test fails when f″=0** (2023 report): in this case you must use a sign table (sign test) to determine the nature.
- **Graphs must label all key points**: label coordinates of intercepts, stationary points and points of inflection; write equations for asymptotes; use open/closed circles for endpoints. The 2020 report specifically named Q7(d): many people did not label key points and could not get full marks (the 4 marks for that question were allocated to intercepts, stationary point + point of inflection, concavity, and limiting behaviour).
- **"Show that" questions must not skip steps** (2022, 2023, 2025 reports): every substitution and simplification must be written out.
- **Calculators must be in radian mode** (2022, 2024, 2025 reports): if differentiating sin gives π/180, the calculator is in degree mode.
- **Application questions must include units**.

---

## Pattern 1: Direct Differentiation (Combining Rules)

**Recognition**: "Differentiate …", "Determine f′(x)", "Do not simplify / Simplify your answer". A 2–4 mark question at the start of a CF paper.

**Approach**
1. First identify the structure: product → product rule; fraction → quotient rule (or rewrite as a product); composite → chain rule. Often two or three rules are combined, e.g. x² ln(4x+3) is a product with a chain rule inside.
2. Memorise the basic derivatives: (eᵏˣ)′ = keᵏˣ, (ln f)′ = f′/f, (sin kx)′ = k cos kx, (tan x)′ = 1/cos²x.
3. If the question says simplify, factor out common factors, e.g. xeˣ(x+2); if it says do not simplify, don't waste time simplifying.

**Marking points (typical wording in the key)**: ✓ correct use of product/quotient/chain rule (the mark is only awarded if the two-term structure is written and at least one term is correct, e.g. 2018F-Q3(b)) ✓ derivative completely correct ✓ simplification (if required by the question).

**Common errors**: missing the inner derivative 6x² when differentiating (2x³+1)⁵; writing the numerator of the quotient rule in reverse order; missing the negative sign when differentiating e⁻ˣ.

**Past questions**: 2016F-Q2(a), 2018F-Q3(a), 2020F-Q2, 2021F-Q1(a), 2023F-Q1(a), 2024F-Q1(a), 2017A-Q10 (prove the derivative of tan).

---

## Pattern 2: Table / Graph Gives Function Values, Find Derivative of Composite or Product

**Recognition**: A table giving g(x), h(x), g′(x), h′(x) at several x-values, or two function graphs.

**Approach**
1. First write the general formula: product (fg)′(5) = f′(5)g(5) + f(5)g′(5); quotient (g/h)′(3) = [g′(3)h(3) − g(3)h′(3)] / h(3)² (2019F-Q2(a) is a quotient); composite [h(g(x))]′ = h′(g(x))·g′(x). **The general formula itself is worth 1 mark**.
2. For composite functions, always evaluate the inner function first: h′(g(1)) = h′(3), not h′(1).
3. Graph questions: the slope of a straight-line segment is the derivative; at the corner (sharp point) between two straight-line segments the derivative does not exist. The points asked about will generally avoid corners; if the inner function value g(a) falls exactly on a corner, the derivative cannot be found.

**Marking points**: ✓ use the correct product/chain rule to write the expression ✓ substitute values correctly.

**Common errors**: 2019 report: Q2(b) (differentiating composite functions) was poorly answered; 2020 report: many people did not realise Q5(c) required the chain rule. Common error (editor's note, not in the original report): calculating h′(g(1)) as h′(1).

**Past questions**: 2019F-Q2, 2020F-Q5, 2023F-Q5(a).

---

## Pattern 3: “rate of change of f′(x)”, “Explain the meaning of f″”

**Recognition**: Given f′(x), asked for the rate of change of f′(x), or asked to explain the meaning of your answer.

**Approach**
- The rate of change of f′ is **f″(x)**. The key has a dedicated mark for "indicates rate of change of f′(x) is f″(x)".
- When explaining the meaning, put it in context: "when x = 1, the gradient of f is increasing at a rate of … per unit of x". If f′(a)=0 and f″(a)<0 at x=a, this shows the point is a local maximum.

**Marking points**: ✓ recognise that f″ is required ✓ differentiate correctly ✓ substitute the value ✓ (explanation questions) state both "what quantity it is the rate of change of" and "at which x / when".

**Past questions**: 2018F-Q3(b), 2019F-Q1(a)(b), 2019F-Q7(b), 2021F-Q1(b), 2022F-Q1(a), 2019F-Q2(c).

---

## Pattern 4: Full Function Analysis (Stationary Points + Nature + Points of Inflection + Sketching)

**Recognition**: A 10–15 mark question, often the last question on a CA or CF paper. "Use calculus to determine all stationary points and their nature", "points of inflection", "Hence sketch".

**Standard procedure**
1. **Factorise f′(x)**, e.g. if f = x²eˣ then f′ = xeˣ(x+2). Since eˣ>0 is never zero, write this as the reason.
2. f′ = 0 → stationary point x-values → substitute back into the **original function** to find y-coordinates (finding y-coordinates is marked separately).
3. Determine the nature: f″(a)>0 is a local minimum, f″(a)<0 is a local maximum; **if f″(a)=0 you must use a sign test instead**.
4. Points of inflection: f″=0, and confirm that f″ changes sign on either side of the point. Horizontal point of inflection: f′(a)=0 and f″ changes sign on either side of a (equivalently, f′ has the same sign on either side of a). **Having f′=f″=0 is not enough**, e.g. for f = x⁴ at x=0, f′=f″=0 but it is a local minimum, so a sign table is needed to confirm.
5. Sketching: label coordinates of intercepts, stationary points and points of inflection; draw asymptotes (vertical asymptote for ln, horizontal asymptote for eˣ) and domain endpoints (open/closed circles); the concavity shape must match the sign of f″.

**Marking points (using 2021A-Q12 as an example, 15 marks)**: (a) 2 marks: product rule, factorisation. (b) 7 marks: f′=0, two solutions, find f″, determine that x=0 is a local minimum, y-coordinate of the local minimum, determine that x=−2 is a local maximum, y-coordinate of the local maximum. (c) 2 marks: f″=0, two points of inflection. (d) 4 marks: local minimum, local maximum, points of inflection, overall shape.

**Common errors**
- writing only x and not the y-coordinate;
- when determining nature, only saying "f″ is positive" without writing the value of f″(a) or a sign table;
- forgetting the domain x>−3 for functions such as ln(x+3), and not drawing the vertical asymptote (2017A-Q14 has 1 mark specifically for the asymptote);
- 2023 report reminder: when y″=0, the second derivative test is inconclusive, so a sign test must be used instead (corresponding to x=4 in 2023F-Q5(d)).

**Past questions**: 2016A-Q13, 2016F-Q3, 2017A-Q14, 2020F-Q7, 2021A-Q12, 2023F-Q5(d)(e).

---

## Pattern 5: Find Coefficients from Conditions / Sketch from Conditions

**Recognition**: "Determine a, b, c, d" with several conditions (turning point, point of inflection, area, passing through a point), or a set of conditions such as f(2)=0, f′(−1)=0, f″(−1)=4 for you to sketch the graph.

**Approach**
1. Translate each condition into an equation: passes through a point → f(a)=b; turning point → f′(a)=0; point of inflection → f″(a)=0; area → ∫f dx = A.
2. First write the general forms of f′ and f″ (this step is usually worth 1 mark on its own).
3. Number of unknowns = number of equations; solve the simplest equation first (e.g. f″(0)=0 ⇒ b=0).
4. Sketching: convert each condition into a graph feature (f″(−1)>0 → local minimum; f′(1)=0 but only two stationary points and f′(2)>0 → horizontal point of inflection).

**Marking points**: ✓ write f′, f″ ✓ form one equation for each condition (usually about 1 mark each; 2018A-Q15 gives 1 mark for two derivative equations combined) ✓ solve all coefficients. Sketching: ✓ intercepts ✓ increasing intervals ✓ local minimum ✓ horizontal point of inflection ✓ continuous and smooth.

**Past questions**: 2018A-Q15 (growth pauses at t=6 then continues increasing ⇒ t=6 is a horizontal point of inflection ⇒ P′(6)=0 and P″(6)=0; solving gives a=−18, b=108), 2020F-Q3, 2022F-Q5.

## Pattern 6: Optimisation ★ Frequently tested

**Identify**: a context question with “Show that the area/volume/surface is given by …”, then “Using calculus, determine the dimensions that maximise/minimise …”.

**Standard procedure**
1. **Show that**: introduce the constraint (fixed volume, perimeter 500 m, Pythagorean relationship) → use the constraint to eliminate one variable → substitute into the objective function → simplify to the form given in the question. Write out every step.
2. Differentiate → set it to 0 → solve for candidate values; state why any invalid solutions are rejected (e.g. r=0, θ outside the range).
3. **Verify the nature of the extremum**: when the question requires using calculus, this must be written and is usually worth 1 mark. The method is to calculate A″(x₀)<0 at the stationary point, or write a sign table (f′ changes from positive to negative). If the question states "You do not need to verify" (e.g. 2025A-Q12(b), 2025A-Q14(c)), it can be omitted; if unsure, write it—you will not lose marks for including it.
4. Answer the question: if it asks for dimensions, give all dimensions (both radius and height); note the rounding required by the question (e.g. nearest mm), and include units.
5. When there is a discrete constraint (only whole numbers can be produced), compare the values of the two neighbouring integers before drawing a conclusion (2020A-Q13).

**Marking points (2024A-Q12(c))**: ✓ correct derivative ✓ solve A′=0 ✓ use the second derivative or a sign table to verify a maximum ✓ find the other dimension y.

**Common errors**
- omitting the verification (identified in the report);
- giving only x and not y / h;
- in a show that question, working backwards from the conclusion;
- using CAS but not writing the equation (2022 report: write the equation being solved and the key output).

**Past questions**: 2016F-Q8, 2016S-A19, 2017A-Q17, 2018A-Q13(a), 2018F-Q6(b), 2019A-Q16, 2020A-Q17, 2024A-Q12, 2025A-Q9(d).

---

## Pattern 7: Increments formula δy ≈ (dy/dx)·δx

**Identify**: “Use the increments formula to estimate / approximate the change”.

**Approach**
1. Write down δx (**note unit conversions**: 1° = π/180 rad; 1 month = 1/12 year).
2. Find dy/dx and evaluate it at the **starting point**.
3. δy ≈ f′(a)·δx; if asked for the new value, add f(a).
4. Include units; if the question asks for an exact value, leave it in terms of π or as a fraction.

**Marking points**: ✓ correct increment δx ✓ find f′(a) ✓ substitute into the formula to get the result (with units).

**Common errors**: not converting degrees to radians (2024F-Q7(d) 45°→46° requires δθ = π/180); inconsistent time units; treating the estimate as the new value (or vice versa).

**Past questions**: 2016A-Q11, 2017A-Q15(c)(iii), 2019F-Q7(c), 2021F-Q3 (ln 2.02), 2022A-Q15(b), 2023A-Q14(b), 2024F-Q7(d), 2025F-Q3(c).

---

## Pattern 8: Rates of change under the chain rule / related rates

**Identify**: given dθ/dt or dh/dt, asked for the rate of change of another quantity with respect to time; the question often hints dy/dt = dy/dθ × dθ/dt.

**Approach**
1. First use a geometric relationship to write y as a function of θ (or V as a function of h), e.g. y = 12 tan θ.
2. Differentiate with respect to the intermediate variable.
3. Multiply by the known rate, and **substitute the value at the specified time** (often you must first find cos θ from y=5).
4. Write units, and explain the meaning of the direction/sign.

**Marking points**: ✓ establish the relationship ✓ differentiate ✓ multiply using the chain rule ✓ substitute values.

**Past questions**: 2016A-Q21 (lighthouse), 2017A-Q15(c). (2025F-Q3 gives h(t) directly; it is just differentiation plus substitution, and is classified under Patterns 1 and 7.)

---

## Pattern 9: Tangents / tangent-related geometry

**Identify**: “The line y = x + c is tangent to f(x)” “the tangent line connects the dog and the ball”.

**Approach**: at the point of tangency there are two conditions: f′(a) = gradient of the tangent, f(a) = y-value on the tangent. Use the first to solve for a, then use the second to find the intercept. Use y − f(a) = f′(a)(x − a) for the tangent equation.

**Past questions**: 2020A-Q11, 2016S-A11, 2019A-Q15(d) (the top edge of the window is tangent to the line AB: set the derivative equal to the gradient of AB), 2025A-Q12(c).

---

## Pattern 10: Interpretation and description (the 1–3 marks that appear every year)

**Identify**: “Describe how … varies” “Explain the meaning of your answer” “What is the meaning of …”.

**Response template**
- Describing change: explain it clearly in intervals. For example “For $1.50 < x < … the company makes a loss; profit increases to a maximum of $… at x = …; then decreases.” (2018F-Q6(a) 1 mark per interval.)
- Interpreting a derivative: “At t = …, [quantity] is increasing/decreasing at a rate of [value + units] per [unit of the independent variable].”
- Reports repeatedly point out: writing only the calculation without explaining what is being calculated loses marks (2018, 2019 reports), and answers must use accurate terminology (2025 report). Write the name of the specific quantity, include units, and relate it to the context.

**Past questions**: 2017A-Q15(b), 2017F-Q6(b)(ii), 2018F-Q6(a), 2019F-Q1(b), 2025A-Q9(c) (the maximum rate of increase is at the point of inflection: the point where the graph has the greatest gradient).
