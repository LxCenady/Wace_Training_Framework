# MAM · Differentiation and Its Applications — Patterns and Solution Approaches

> Based on: ratified marking keys for 51 past exam questions containing differentiation from 2016–2025 ("Specific behaviours" point-by-point marking criteria) + past exam reports.
> Question numbering: `2021A-Q12` = 2021 Calculator-assumed Question 12, `F` = Calculator-free; `2016S-A19` = 2016 official sample paper (not included in the 51 questions; original paper at `papers/2016Sample_*`). Original questions and marking can be found in `topics/01_Differentiation.pdf`.
> Review status: has undergone one round of independent review and was revised according to feedback (see `Review_log.md`).

## First, remember: where the marking panel repeatedly deducted marks

- **Optimisation questions must verify the nature of the extremum**: The 2024 report states: for optimisation questions requiring calculus, full marks require using the second derivative test or sign test to verify the nature of the stationary point. Verification is usually worth 1 mark on its own (e.g. 1 of the 4 marks in 2024A-Q12(c)).
- **The second derivative test fails when f″=0** (2023 report): in this case you must use a sign table (sign test) to determine the nature.
- **Graph sketches must label all key points**: label coordinates for intercepts, stationary points and inflection points; write equations for asymptotes; use open/closed circles for endpoints. The 2020 report specifically named Q7(d): many students did not label key points and could not get full marks (the 4 marks for this question were for intercepts, stationary point + inflection point, concavity, and limiting behaviour).
- **"Show that" questions must not skip steps** (2022, 2023, 2025 reports): every substitution and simplification must be written out.
- **Calculators must be in radian mode** (2022, 2024, 2025 reports): a π/180 appearing when differentiating sin indicates degree mode.
- **Applied questions must include units**.

---

## Pattern 1: Direct differentiation (combining rules)

**Identification**: "Differentiate …", "Determine f′(x)", "Do not simplify / Simplify your answer". Early 2–4 mark questions at the start of the CF paper.

**Approach**
1. First identify the structure: product → product rule; fraction → quotient rule (or rewrite as a product); composite → chain rule. It is common for two or three rules to be combined, e.g. x² ln(4x+3) is a product with a chain rule inside.
2. Memorise the basic derivatives: (eᵏˣ)′ = keᵏˣ, (ln f)′ = f′/f, (sin kx)′ = k cos kx, (tan x)′ = 1/cos²x.
3. When the question says simplify, factor out common factors, e.g. xeˣ(x+2); when it says do not simplify, don't waste time simplifying.

**Marking points (typical key wording)**: ✓ correct use of product/quotient/chain rule (the mark is awarded for writing the two-term structure with at least one term correct, e.g. 2018F-Q3(b)) ✓ derivative completely correct ✓ simplification (if required by the question).

**Common errors**: omitting the inner derivative 6x² when differentiating (2x³+1)⁵; reversing the numerator order in the quotient rule; omitting the negative sign when differentiating e⁻ˣ.

**Past questions**: 2016F-Q2(a), 2018F-Q3(a), 2020F-Q2, 2021F-Q1(a), 2023F-Q1(a), 2024F-Q1(a), 2017A-Q10 (proving the derivative of tan).

---

## Pattern 2: Tables / graphs giving function values, finding derivatives of composites or products

**Identification**: A table of g(x), h(x), g′(x), h′(x) at several x-values, or two function graphs.

**Approach**
1. First write the general formula: product (fg)′(5) = f′(5)g(5) + f(5)g′(5); quotient (g/h)′(3) = [g′(3)h(3) − g(3)h′(3)] / h(3)² (2019F-Q2(a) is a quotient); composite [h(g(x))]′ = h′(g(x))·g′(x). **The general formula itself is worth 1 mark**.
2. For composite functions, always evaluate the inner function first: h′(g(1)) = h′(3), not h′(1).
3. Graph questions: the gradient of a straight-line segment is the derivative; at a corner (sharp point) between two straight segments the derivative does not exist. The point asked about will usually avoid the corner; if the inner function value g(a) falls exactly on the corner, the derivative cannot be found.

**Marking points**: ✓ correct expression using product/chain rule ✓ correct substitution of values.

**Common errors**: 2019 report: Q2(b) (differentiating a composite function) was poorly answered; 2020 report: many students did not realise Q5(c) required the chain rule. Common error (author's note, not from the report): calculating h′(g(1)) as h′(1).

**Past questions**: 2019F-Q2, 2020F-Q5, 2023F-Q5(a).

---

## Pattern 3: "rate of change of f′(x)", "explain the meaning of f″"

**Identification**: Given f′(x), asked for the rate of change of f′(x), or asked to explain the meaning of your answer.

**Approach**
- The rate of change of f′ is **f″(x)**. The key has a dedicated mark for "indicates rate of change of f′(x) is f″(x)".
- When explaining meaning, put it in context: "when x = 1, the gradient of f is increasing at a rate of … per unit of x". At x=a, f′(a)=0 and f″(a)<0 means the point is a local maximum.

**Marking points**: ✓ recognise that f″ is required ✓ correct differentiation ✓ correct substitution ✓ (explanation questions) state both "the rate of change of what quantity" and "at which x / when".

**Past questions**: 2018F-Q3(b), 2019F-Q1(a)(b), 2019F-Q7(b), 2021F-Q1(b), 2022F-Q1(a), 2019F-Q2(c).

---

## Pattern 4: Full function analysis (stationary points + nature + inflection points + graph sketching)

**Identification**: A 10–15 mark question, commonly the final question on a CA paper or CF paper. "Use calculus to determine all stationary points and their nature", "points of inflection", "Hence sketch".

**Standard procedure**
1. **Factorise f′(x)**, e.g. for f = x²eˣ, f′ = xeˣ(x+2). eˣ>0 is never zero; write this as a reason.
2. f′ = 0 → stationary point x-values → substitute back into the **original function** to find y-coordinates (finding y-coordinates is marked separately).
3. Determine the nature: f″(a)>0 is a local minimum, f″(a)<0 is a local maximum; **when f″(a)=0 you must use a sign test instead**.
4. Inflection points: f″=0, and confirm that f″ changes sign on either side of the point. Horizontal inflection point: f′(a)=0 and f″ changes sign on either side of a (equivalently, f′ has the same sign on either side of a). **Having only f′=f″=0 is not enough**, e.g. for f = x⁴ at x=0, f′=f″=0 but it is a local minimum, so a sign table is needed to confirm.
5. Graph sketching: label coordinates for intercepts, stationary points and inflection points; draw asymptotes (vertical asymptote for ln, horizontal asymptote for eˣ) and domain endpoints (open/closed circles); the concavity shape must match the sign of f″.

**Marking points (using 2021A-Q12 as an example, 15 marks)**: (a) 2 marks: product rule, factorisation. (b) 7 marks: f′=0, two solutions, find f″, classify x=0 as a local minimum, y-coordinate of the local minimum, classify x=−2 as a local maximum, y-coordinate of the local maximum. (c) 2 marks: f″=0, two inflection points. (d) 4 marks: local minimum, local maximum, inflection point, overall shape.

**Common errors**
- writing only x and not the y-coordinate;
- when determining nature, saying only "f″ is positive" without writing the value of f″(a) or a sign table;
- for functions such as ln(x+3), forgetting the domain x>−3 and not drawing the vertical asymptote (2017A-Q14 has 1 mark specifically for the asymptote);
- 2023 report reminder: when y″=0 the second derivative test is inconclusive, so a sign test must be used instead (corresponding to x=4 in 2023F-Q5(d)).

**Past questions**: 2016A-Q13, 2016F-Q3, 2017A-Q14, 2020F-Q7, 2021A-Q12, 2023F-Q5(d)(e).

---

## Pattern 5: Finding coefficients from conditions / sketching from conditions

**Identification**: "Determine a, b, c, d" with several conditions (turning point, inflection point, area, passing through a point), or a set of conditions such as f(2)=0, f′(−1)=0, f″(−1)=4 from which you must sketch a graph.

**Approach**
1. Translate each condition into an equation: passes through a point → f(a)=b; turning point → f′(a)=0; inflection point → f″(a)=0; area → ∫f dx = A.
2. First write the general forms of f′ and f″ (this step is usually worth 1 mark on its own).
3. Number of unknowns = number of equations; solve the simplest equation first (e.g. f″(0)=0 ⇒ b=0).
4. Graph-sketching questions: convert each condition into a graphical feature one by one (f″(−1)>0 → local minimum; f′(1)=0 but there are only two stationary points and f′(2)>0 → horizontal inflection point).

**Marking points**: ✓ write f′ and f″ ✓ form one equation for each condition (usually about 1 mark each; 2018A-Q15 combined the two derivative equations for 1 mark) ✓ solve all coefficients. Graph sketching: ✓ intercepts ✓ increasing intervals ✓ local minimum ✓ horizontal inflection point ✓ continuous and smooth.

**Past questions**: 2018A-Q15 (growth pauses at t=6 and then continues to increase ⇒ t=6 is a horizontal inflection point ⇒ P′(6)=0 and P″(6)=0; solving gives a=−18, b=108), 2020F-Q3, 2022F-Q5.

---

## Pattern 6: Optimisation (optimisation) ★ High frequency

**Identification**: A contextual question with “Show that the area/volume/surface is given by …”, then “Using calculus, determine the dimensions that maximise/minimise …”.

**Standard procedure**
1. **Show that**: introduce the constraint (fixed volume, perimeter 500 m, Pythagorean relation) → use the constraint to eliminate one variable → substitute into the objective function → simplify to the form given in the question. Write out every step.
2. Differentiate → set it equal to 0 → solve for candidate values; state why unreasonable solutions are discarded (e.g. r=0, θ outside the range).
3. **Verify the nature of the extremum**: when the question says using calculus, this is required and usually worth 1 mark. The method is to calculate A″(x₀)<0 at the stationary point, or write a sign table (f′ changes from positive to negative). If the question states “You do not need to verify” (e.g. 2025A-Q12(b), 2025A-Q14(c)), you may omit it; if unsure, write it—you won't lose marks.
4. Return to the question to answer: if the question asks for dimensions, give all dimensions (both radius and height), note the rounding required by the question (e.g. nearest mm), and include units.
5. When there is a discrete constraint (only whole numbers can be produced), compare the values for the two neighbouring integers before drawing a conclusion (2020A-Q13).

**Scoring points (2024A-Q12(c))**: ✓ correct derivative ✓ solve A′=0 ✓ use the second derivative or a sign table to verify a maximum ✓ find the other dimension y.

**Common errors**
- omitting the verification (pointed out in reports);
- giving only x and not y / h;
- working backwards directly from the result in a show that question;
- using CAS but not writing the equation (2022 report: write the equation being solved and the key output).

**Past exam questions**: 2016F-Q8, 2016S-A19, 2017A-Q17, 2018A-Q13(a), 2018F-Q6(b), 2019A-Q16, 2020A-Q17, 2024A-Q12, 2025A-Q9(d).

---

## Pattern 7: Increments formula δy ≈ (dy/dx)·δx

**Identification**: “Use the increments formula to estimate / approximate the change”.

**Approach**
1. Write down δx (**note unit conversion**: 1° = π/180 rad; 1 month = 1/12 year).
2. Find dy/dx and evaluate it at the **starting point**.
3. δy ≈ f′(a)·δx; if asked for the new value, add f(a).
4. Include units; if the question asks for an exact value, keep π or fractions.

**Scoring points**: ✓ correct increment δx ✓ find f′(a) ✓ substitute into the formula to get the result (with units).

**Common errors**: not converting angles to radians (2024F-Q7(d) 45°→46° requires δθ = π/180); inconsistent time units; treating the estimate as the new value (or vice versa).

**Past exam questions**: 2016A-Q11, 2017A-Q15(c)(iii), 2019F-Q7(c), 2021F-Q3 (ln 2.02), 2022A-Q15(b), 2023A-Q14(b), 2024F-Q7(d), 2025F-Q3(c).

---

## Pattern 8: Rates of change under the chain rule / related rates

**Identification**: given dθ/dt or dh/dt, asked for the rate of change of another quantity with respect to time; the question often hints dy/dt = dy/dθ × dθ/dt.

**Approach**
1. First use the geometric relationship to write y as a function of θ (or V as a function of h), e.g. y = 12 tan θ.
2. Differentiate with respect to the intermediate variable.
3. Multiply by the known rate of change, and **substitute the values at the specified time** (often you must first use y=5 to find cos θ).
4. Write units and explain the meaning of the direction/sign.

**Scoring points**: ✓ establish the relationship ✓ differentiate ✓ multiply using the chain rule ✓ substitute values.

**Past exam questions**: 2016A-Q21 (lighthouse), 2017A-Q15(c). (2025F-Q3 gives h(t) directly, so it is just differentiation plus substitution; classified under Pattern 1 and Pattern 7.)

---

## Pattern 9: Tangents / tangent-related geometry

**Identification**: “The line y = x + c is tangent to f(x)”, “the tangent line connects the dog and the ball”.

**Approach**: At the point of tangency there are two conditions: f′(a) = gradient of the tangent, f(a) = y-value on the tangent. Solve for a from the first, then find the intercept from the second. Use y − f(a) = f′(a)(x − a) for the tangent equation.

**Past exam questions**: 2020A-Q11, 2016S-A11, 2019A-Q15(d) (top edge of the window is tangent to line AB: set the derivative equal to the gradient of AB), 2025A-Q12(c).

---

## Pattern 10: Interpretation and description (1–3 marks every year)

**Identification**: “Describe how … varies”, “Explain the meaning of your answer”, “What is the meaning of …”.

**Writing template**
- Describing change: explain it in sections. For example, “For $1.50 < x < … the company makes a loss; profit increases to a maximum of $… at x = …; then decreases.” (2018F-Q6(a) 1 mark per section.)
- Interpreting the derivative: “At t = …, [quantity] is increasing/decreasing at a rate of [value + units] per [unit of the independent variable].”
- Reports repeatedly point out that writing only calculations without saying what has been calculated loses marks (2018, 2019 reports), and answers must use accurate terminology (2025 report). State the name of the specific quantity, include units, and link it to the context.

**Past exam questions**: 2017A-Q15(b), 2017F-Q6(b)(ii), 2018F-Q6(a), 2019F-Q1(b), 2025A-Q9(c) (the maximum rate of increase is at the point of inflection: the point where the graph has its greatest gradient).
