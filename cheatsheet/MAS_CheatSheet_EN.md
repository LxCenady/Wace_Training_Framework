# WACE Mathematics Specialist · Cheat Sheet (Patterns + Notes)

**General rules**: principal argument −π < θ ≤ π · Write mathematical statements, not calculator language · When explaining, don't write "it"; state which quantity (e.g. "SD **of the sample mean**") · Add absolute value signs to ln|…| (can omit when the argument is always positive) · Indefinite integrals + c · Rates of change with units · Expand brackets and watch for sign errors when copying (repeatedly noted in yearly reports) · Memorise exact trigonometric values for special angles · When a question asks prove / show, use algebra; "CAS says no solution" is not a proof · State the conclusion clearly

## 1 Complex numbers

**① Form conversion and operations**
- Division: multiply the numerator and denominator by the conjugate of the denominator. Powers and roots: first write as r cis θ, then use De Moivre ((√3 − i)⁵ = 32 cis(−5π/6) = −16√3 − 16i).
- ⚠ Third quadrant: the principal argument of −1 − i is −3π/4, not π/4, and it cannot be written as 5π/4. Draw the diagram first to determine the quadrant.
- Given z = 3 + bi, tan θ = 2 ⇒ b = 6, r = 3√5.

**② Solving zⁿ = w** ★ appears every year
- Write w as R cis φ (modulus 1 mark, argument 1 mark) → z = R^(1/n) cis((φ + 2kπ)/n), k = 0, …, n − 1 (general formula 1 mark) → list **all** n roots within the range required by the question, spaced 2π/n apart.
- Example: z⁴ = −16i ⇒ 2 cis(−5π/8), 2 cis(−π/8), 2 cis(3π/8), 2 cis(7π/8).
- Roots of zⁿ = 1: equally spaced on the unit circle (explanation 2 marks: radius 1, equal spacing); product of all roots = (−1)ⁿ⁺¹; z⁴³ = 1 and z⁴⁷ = 1 have only the common root 1 (43 and 47 are coprime).
- zⁿ is a positive real number: n·arg z is an integer multiple of 2π (z = 4 cis(5π/6) ⇒ smallest n = 12).

**③ Complex roots of polynomials**
- "Show (z − α) is a factor": calculate P(α), **write out every term**, obtain 0 (key: not just the statement).
- Real coefficients ⇒ ᾱ is also a root ⇒ (z − α)(z − ᾱ) = z² − 2Re(α)z + |α|² → use division or compare coefficients to find the remaining factor → solve the quadratic.
- Example: P(2 + 4i) = 0 ⇒ factor z² − 4z + 20, remaining z² − 2z + 3 ⇒ z = 1 ± √2 i. ⚠ z² − 2z + 3 cannot be factorised as (z − 3)(z + 1) (2021 report).
- Given two complex roots, work backwards to find coefficients: the two conjugate pairs each give a quadratic factor, then use the constant term to find the real root.

**④ Geometric meaning of multiplication**
- Template (1 mark each): "Multiplication by w = r cis θ dilates the modulus by a factor r and rotates anticlockwise by θ (clockwise by |θ| if θ < 0) about the origin." Multiply by z⁻¹: take the reciprocal of the scale factor and reverse the direction of rotation.
- Find n such that zwⁿ lies in the second quadrant: rotate by arg w each time; if |w| = 1 there is a period, so give all answers, e.g. n = 3 + 12k, 4 + 12k, 5 + 12k.

**⑤ Loci: graph from equation**
- |z − a| = r: circle. |z − a| = |z − b|: perpendicular bisector of a and b. Arg(z − a) = θ: ray, with **open endpoint at a**.
- |z − a| + |z − b| = k: if k is greater than |a − b| it is an ellipse; **if equal it degenerates to a line segment**.
- |z + 2| = |z − i| + √5 (difference equals the distance between the two points): ray starting from i, with **closed endpoint at i**.
- (z + i)·conj(z + i) = 2 ⇒ centre −i, radius √2; z − z̄ ≤ 6i ⇒ Im z ≤ 3.
- Mark-earning points when drawing: key points or centre, boundary position, solid or dashed lines, shaded region.

**⑥ Loci: write equation from graph**: use only z, not x, y; circle ⇒ |z − c| ≤ r; sector ⇒ two Arg inequalities + one modulus inequality; find angles exactly using trigonometry.

**⑦ Maximum and minimum values on a locus**
- Distance from a point on a circle to c: maximum d + r, minimum |d − r| (d = distance from the centre to c). Nearest point on a ray: drop a perpendicular.
- The maximum argument occurs at the tangent: first use sin θ = r/d to find the angle between the tangent and the line to the centre, then add the argument of the centre, paying attention to the range specified in the question.

**⑧ Vectors and geometric methods**
- z + r (sum of two equal-length vectors) forms a rhombus ⇒ arg(z + r) = θ/2; z − k forms a triangle, use the sine or cosine rule.
- Regular hexagon: first check where the centre is. When the centre is at the origin, the vertices have equal modulus and arguments differ by π/3; in 2025F-Q7 z₀ is at the origin, the moduli are r, √3r, 2r, √3r, r respectively, and the product is 6r⁵.
- Trick: Σ n·iⁿ in groups of 4 terms, each group sums to 2 − 2i; take modulus of (a + bi)³ ⇒ (a² + b²)³ = |…|².

## 2 Functions and graphs

**① Domain of composite functions** ★ most frequently mentioned (6 years)
- f(g(x)) is defined ⇔ x ∈ dom g **and** g(x) ∈ dom f. After substituting, don't simplify first; each restriction usually earns 1 mark.
- Sources of restrictions: denominator ≠ 0; expression under a square root ≥ 0; **when the square root is in the denominator > 0**; argument of ln > 0.
- Example: f = 1 − √(x − 4), g = 1/x² ⇒ 1/x² ≥ 4 ⇒ −½ ≤ x ≤ ½ and x ≠ 0. f = √(4 − x), g = 1/x² ⇒ x ≤ −½ or x ≥ ½.
- ⚠ √(x²) = |x|, so f(h(g(x))) is not necessarily equal to f(x).

**② Inverse functions**
- Exists ⇔ one-to-one (horizontal line test); otherwise restrict the domain; for the "largest possible domain", go up to the vertex.
- Method: swap x and y (1 mark) → solve for y → the sign is determined by **ran f⁻¹ = dom f**; dom f⁻¹ = ran f.
- The graphs are symmetric about y = x; mark the corresponding endpoints (a, b) ↔ (b, a). Whether f⁻¹(−1) is defined: first check whether −1 is in ran f.
- Inverse trigonometric functions: x = 2 tan y ⇒ y′ = 2/(4 + x²) (use implicit differentiation, then use 1 + tan²y to change to x).
- Explaining "g is not one-to-one": "because g(1) = g(−1) = 1", don't write "it is many to one".

**③ Graphing y = 1/f(x)** ★ often tested in CF
- Zero of f ⇒ vertical asymptote; as x → ±∞, f → ±∞ ⇒ horizontal asymptote y = 0.
- Vertical asymptote of f at x = b ⇒ 1/f has an open point at (b, 0) (range excludes 0); horizontal asymptote of f at y = c (c ≠ 0) ⇒ y = 1/c.
- Local maximum (a, m) ↔ local minimum (a, 1/m); points where f = ±1 stay fixed; sign does not change; an open point of f at (a, b) ⇒ an open point of 1/f at (a, 1/b); if b = 0 it becomes a one-sided asymptote.
- Find the range: read from the graph of 1/f, noting values that are not included.

**④ Absolute value functions**
- |f(x)|: reflect the part below the x-axis above the x-axis; f(|x|): keep the right half and mirror it to the left; f(−|x|): keep the left half and mirror it to the right.
- Number of solutions of |f(x)| = k: use the horizontal line y = k to intersect; check endpoint k separately; you can draw the number-of-solutions function N(k).
- The solution set of |x + 1| + |x + a| = k is an interval ⇒ the flat-bottom interval of the sum of two absolute values is the solution set (a = 3, k = 2).
- Determine y = a|x − b| + c from the graph: the vertex gives b and c, the gradient gives a.

**⑤ Rational functions: determine parameters from graph / sketch graph**
- Zero ↔ factor of numerator; vertical asymptote ↔ factor of denominator; horizontal asymptote = ratio of leading coefficients; oblique asymptote = quotient from polynomial division (x − 1 − 3/(x + 1) ⇒ y = x − 1).
- Repeated factor: in the numerator ⇒ graph touches the x-axis but does not cross; in the denominator ⇒ both sides of the asymptote have the same sign (both tend to −∞).
- Write the reason (1 mark): "c = 3 since x = 3 is a vertical asymptote". A quadratic with no zeros of the form a(x − 3)² + c requires a and c to have the same sign.
- Sketching checklist (1 mark each): x-intercept, y-intercept, vertical asymptote, horizontal or oblique asymptote, turning point (mark if present), behaviour on either side of the asymptote. First check for cancelled factors (holes).

## 3 Three-dimensional vectors and systems of linear equations

**① Systems of linear equations** ★ Appeared in CF in 7 out of 10 years
- Three elimination steps (1 mark each): use two pairs of equations to eliminate the same variable → solve for one variable → back-substitute.
- With a parameter: reduce to (k − 2)z = c − 5 ⇒ k ≠ 2: unique solution (c arbitrary); k = 2 and c ≠ 5: no solution; k = 2 and c = 5: infinitely many solutions.
- ⚠ **For infinitely many solutions, write the solution set** (2022 report: many people stop after writing "infinitely many solutions"), expressing it using a parameter or relationships between variables. Example: z = t ⇒ y = t − 1, x = (11 − 3t)/2, i.e. r = (11/2, −1, 0) + t(−3/2, 1, 1).
- Geometric interpretation: unique solution = three planes intersect at a point; one parameter = intersect in a line (two planes may coincide; both points must be written); two parameters = three planes coincide; no solution = there are parallel planes, **or** the three planes intersect pairwise in three parallel lines (triangular prism, 2020F-Q4). First check whether the normal vectors are proportional.

**② Equations of planes**
- Parametric form r = a + λu + μv ⇒ n = u × v (write each component of the cross product clearly) ⇒ r·n = a·n, i.e. ax + by + cz = k.
- Through three points: cross product of two edge vectors; z = 2x + y + 4 ⇒ n = (2, 1, −1).
- Contains line L and is perpendicular to plane 1 ⇒ n₂ = d_L × n₁; contains two intersecting lines ⇒ n = d₁ × d₂.

**③ Intersections, angles, distances**
- Line and plane: substitute r = a + λd, solve for λ, write down the point (3 marks). Line and sphere: obtain a quadratic equation in λ; two solutions, tangent, no intersection; or compare the distance from the centre of the sphere to the line with the radius.
- Two lines: equate components, use two equations to solve for λ, μ, **substitute into the third to check**; if it does not hold, they do not intersect, and this step is the proof.
- Point on a plane closest to point L: construct a line through L along the normal vector and find its intersection with the plane.
- Line-plane angle: sin θ = |d·n|/(|d||n|). Distance from a point to a plane = |n·(P − A)|/|n|, where A is any point on the plane; this formula is not on the formula sheet, so when used include a derivation or use the normal method. Volume of a parallelepiped = |c·(a × b)|.

**④ Spheres**: complete the square for the general form, e.g. x² + y² + z² − 4x + 2y − 6z + 5 = 0 ⇒ |r − (2, −1, 3)| = 3; endpoints of a diameter ⇒ centre is the midpoint (report: often miscalculated); tangent to a plane ⇒ radius = distance from the centre to the plane; passes through all vertices of a rectangular prism ⇒ centre is the midpoint of the space diagonal.

**⑤ Vector proofs** (in both CF and CA): express the required vectors in terms of basis vectors → expand the dot product (key: get 4 terms) → use the given conditions (square ⇒ a·b = 0, |a| = |b|) → conclude. Marks are awarded for notation.

**⑥ Applications**: reflection ⇒ the sum of the unit vectors B→S and B→R ∥ n; the steepest downhill direction on a slope lies in the slope plane and is perpendicular to the horizontal line; for distance problems involving moving objects, see the next section.

## 4 Vector calculus and motion (CA paper only)

**① Differentiation**: v = r′, a = v′, differentiate component by component; speed |v|; draw vectors on the graph (start at the position at that time). Constant speed ≠ constant velocity (direction is changing); you must write that sin² + cos² = 1 was used (1 mark).

**② Integrating to find r(t)**
- Integrate component by component, add a **constant vector**, and use r(0) to determine each component (2018 report: many people do not write this clearly).
- Gravity + wind: a = (0, −9.8) ⇒ r = ((70cos θ + w)t, 70 sin θ·t − 4.9t²); range: set y = 0, solve for t, then substitute into x.
- Horizontal drag + vertical lift: x′ = 32e^(−0.05t), h″ = s − 9.8; use the given r to find s. For landing angle, use the angle between the velocity vector and the slope.

**③ Eliminating the parameter to get the Cartesian equation** ★
- sin² + cos² = 1 ⇒ circle or ellipse; double-angle formulas directly give a relationship between x and y ⇒ a segment of a parabola; first convert to the same angle then use sin² + cos² ⇒ general curve (e.g. figure eight); (eᵗ + e⁻ᵗ)² − (eᵗ − e⁻ᵗ)² = 4 ⇒ x² − y² = 4; x is linear in t ⇒ solve directly for t and substitute into y.
- ⚠ **State the range of values**, derived from the range of t; often both x and y must be restricted: x ≥ 2 **and y ≥ 0** (writing only x ≥ 2 loses marks); 1 ≤ x ≤ e³.

**④ Distance travelled and displacement**
- Distance travelled = ∫ₐᵇ √(ẋ² + ẏ²) dt; first determine the start and end times: the time for one lap = the least common multiple of the periods of the components (2π, 4π, 6π have all been examined), or find t from the coordinates.
- Explanation: ∫₀¹ v dt = "the change in displacement (position vector) during the first second"; ∫|v| dt = distance travelled. The 2025 report specifically identified confusion between these two. Draw the displacement vector on the graph: from r(a) to r(b).

**⑤ Closest distance and relative position**
- Same time parameter: relative position d(t) = r_P − r_Q (order matters when asked for relative position, 1 mark); closest ⇔ d(t)·(v_P − v_Q) = 0; "how long within 50 m" ⇒ solve |d(t)| < 50.
- Speed and departure time are both adjustable ⇒ shortest distance between two lines: use independent parameters λ, μ, and make PQ perpendicular to both d₁ and d₂.
- Angle of descent = |90° − φ| (φ is the angle between the velocity and k), or use sin⁻¹(|v_z|/|v|) directly.

## 5 Integration techniques and applications

**① Definite integrals with a given substitution** ★ CF almost every year (4–7 marks)
- Five steps (1 mark each): find dx from the substitution → **change the limits** → convert the integrand completely into the new variable and simplify → integrate → substitute to get the exact value.
- Trigonometric substitution: for √(a² − x²) use x = a sin θ; for x² + a² use x = a tan θ. Example: ∫₀^√3 √(1 − x²/4) dx, x = 2 sin θ ⇒ ∫₀^(π/3) 2cos²θ dθ = π/3 + √3/4.
- Indefinite integral version (∫x(1 + x)ⁿ dx): do not change the limits; back-substitute into x at the end. ⚠ Simplifying after substitution is often incorrect (2020, 2023 reports).

**② Trigonometric identities**: cos² = ½(1 + cos 2x); sin² = ½(1 − cos 2x); (sin x + cos x)² = 1 + sin 2x; product-to-sum 2 sin A cos B = sin(A + B) + sin(A − B); tan² = sec² − 1.

**③ Partial fractions** ★ CF high frequency
- Forms: distinct linear factors A/(x − a) + B/(x − b); repeated root A/(x + 1) + B/(x + 1)²; irreducible quadratic (Bx + C)/(x² + 2). When the question specifies the form, write it as given.
- After putting over a common denominator, equate numerators (1 mark) → substitute special values or compare coefficients to find the constants (1 mark) → integrate term by term: ln|x − a|, −B/(x + 1), when the numerator is the derivative of the denominator use ln|quadratic|, q/(x² + 4) → (q/2)tan⁻¹(x/2) → write + c.
- Example: 1/(x² − 1) ⇒ ½ ln|(x − 1)/(x + 1)| + c; (5x + 3)/(x + 1)² = 5/(x + 1) − 2/(x + 1)². If no hint is given, factorise the denominator yourself first (1 mark).

**④ Area**
- First find intersection points and points of tangency; when writing the curve as x = g(y) is more convenient, integrate with respect to y (key: marks are given for both methods).
- Symmetry: for an ellipse or a shape symmetric about the coordinate axes, multiply by a factor; circular segment: the difference between the upper and lower branches is 2√(…).
- A definite integral can be interpreted as a geometric area (triangle, trapezium). Comparing a numerical area with πr² can determine whether the curve is a circle.

**⑤ Volumes of solids of revolution** ★ CA high frequency
- About the x-axis π∫y² dx; about the y-axis π∫x² dy (first express x² as a function of y); between two curves π∫(R² − r²), ⚠ not π∫(R − r)².
- The integral expression must include π, the limits, and dx or dy (the limits + notation together give 1 mark).
- Context: depth when filled to 80% ⇒ set ∫₀ʰ πx² dy = 0.8V and solve for h; filling rate dV/dt = (dV/dh)(dh/dt); increment δh ≈ δV ÷ πx²|_(y=h); annulus R, r = 3 ± √(4 − y²).

## 6 Rates of Change and Differential Equations

**① Implicit Differentiation**
- Differentiate both sides with respect to x; for terms containing y, multiply by y′; use the product and chain rules as usual. If the question says not to solve for y′, don't; substitute the point directly to evaluate.
- Horizontal tangents: set numerator = 0, solve simultaneously with the original equation; second derivative: differentiate the expression already found again, substitute x, y, y′.

**② Related Rates** ★
- Write a relationship (eliminate extra variables if necessary; you can also keep two variables and differentiate implicitly) → differentiate with respect to t → substitute the values **at that instant** (often find θ, h first) → include units.
- Example: regular hexagon A = (3√3/2)s², s = 4, ds/dt = 0.5 ⇒ dA/dt = 6√3 ≈ 10.39 cm²/s. A lighthouse makes 3 revolutions per minute ⇒ dθ/dt = π/10 rad/s.
- Circular motion (Ferris wheel, merry-go-round): dθ/dt = 2π/T; use cosine rule s² = 89 − 80cos θ or y = R sin(θ + α); differentiate implicitly with respect to t; to find the maximum ds/dt, differentiate again (geometrically, this is when PC is tangent to the circle). ⚠ Height above ground = height relative to centre + R.

**③ Slope Fields**
- Substitute a point to find the slope (1 mark); infer the equation from the field: see whether the slope depends only on x or only on y, where it is 0 and where it is undefined.
- Sketch the solution curve: pass through the specified point, follow the short line segments, mark symmetry; where the denominator is 0 and the numerator ≠ 0 the tangent is vertical, and the curve turns back there; where the slope is 0 there is a horizontal tangent; **where the slope is greatest is a point of inflection** (2025A-Q16 point of inflection at (3, −1)).

**④ Separation of Variables**
- Write as ∫g(y)dy = ∫f(x)dx (1 mark) → integrate, add only one constant, put absolute value around ln → substitute initial values → write in explicit form.
- dP/dt = kP ⇒ P = P₀eᵏᵗ. ⚠ “instantaneous growth rate is 10%” means dP/dt = 0.1P (P₀ = 30000e^(−4.5) ≈ 333), not multiplying by 1.1 each year (≈ 412).
- Example: dh/dt = −1/(100h) ⇒ h² = h₀² − t/50; dv/dt = −9.8 − 2v ⇒ v = 4.9(e^(−2t) − 1); for depth, integrate v again.

**⑤ Logistic Growth** ★
- dP/dt = rP(k − P) ⇔ P = k/(1 + Ae^(−rkt)): carrying capacity = the non-zero P that makes dP/dt = 0; **growth is fastest when P = k/2**, maximum growth rate = r(k/2)².
- ⚠ Letters depend on the question (in some questions k is the proportionality constant; in others it is written as (1/r)P(k − P)). Example: P = 18000/(10.25e^(−0.15t) + 1) ⇒ carrying capacity 18000, maximum growth rate 0.15 × 9000 × ½ = 675 horses/year.
- Sketching: k/2 < P₀ < k ⇒ concave down throughout, no point of inflection; P₀ > k ⇒ decreasing towards k; changing the carrying capacity ⇒ new point of inflection and asymptote.
- Explanation: when P < k/2 the growth rate increases as P increases; when P > k/2 it decreases and approaches k. For equations that are not logistic (e.g. 0.001(100 − P)²), analyse the change in slope directly.

**⑥ Velocity as a Function of Displacement v = f(x)** ★★ named three times in the report
- a = dv/dt = v·dv/dx = d(½v²)/dx. ⚠ dv/dx itself is not acceleration. Example: v = −0.2x ⇒ a = 0.04x; v = x/8 ⇒ a = x/64.
- x(t): dx/dt = v(x), separate variables, substitute the initial position. Example: v = x/8, x(0) = 192 ⇒ x = 192e^(t/8).
- To decide SHM: only a = −n²(x − c) (proportional to displacement and opposite in direction) qualifies; a = 0.04x is not.

**⑦ Simple Harmonic Motion SHM**
- ẍ = −n²x ⇒ x = A cos(nt + φ); T = 2π/n; v_max = An; v² = n²(A² − x²).
- Determine A and phase: x(0) = 0 and v(0) > 0 ⇒ A sin(nt); if no direction is given, both ±A sin receive marks; n = 2, x(0) = −1, v(0)² = 32 ⇒ A = 3.
- Distance travelled: 4A per period, 2A per half-period; if less than half a period and the starting point is not at the equilibrium position or an endpoint, use ∫|v| dt. Damping: A = A₀e^(−kt); A < 0.01 is treated as stopped.

**⑧ Increment Formula**: δy ≈ (dy/dx)δx; δN ≈ (dN/dt)·δt (dN/dt is given directly by the equation; watch the time units).

## 7 Statistical Inference (only in the CA paper)

**① Distribution and Probability of X̄** ★
- “By the CLT, since n is large, X̄ is approximately normal with mean μ and SD σ/√n” (normal, mean, standard deviation, 3 marks in total). If the population is normal, this holds for any n.
- Population not normal (uniform, exponential, skewed): same method; if asked “does the answer change?”, answer no + CLT reason.
- Sum question: total of 50 observations < 8.96 kL ⇔ X̄ < 179.2 L. Sketch the distribution of X̄: a narrow bell shape centred at μ, width about ±3σ/√n; mark the probability region if required.

**② Finding Sample Size**
- First sketch to decide whether it is two-tailed, one-tailed or half-interval, then find the critical z: P(|X̄ − μ| < d) = 0.98 ⇒ z = 2.326; P(X̄ > 25) = 0.03 ⇒ z = 1.881; P(0 < Z < k) = 0.4 ⇒ k = 1.282.
- n = (zσ/d)²: when “at least” is required, round up (304.3 ⇒ 305, 600.25 ⇒ 601); when working backwards from an interval to n, take the nearest integer (differences caused by using z = 2.576 and 2.58 are both accepted by the key).

**③ Confidence Intervals**
- x̄ ± z·s/√n. Work backwards: midpoint = x̄; half-width = z·σ_X̄ (150 ≤ μ ≤ 200 ⇒ σ_X̄ = 25/1.96 = 12.76); find s from the width and n.
- Changing sample size: width ∝ 1/√n (n × 16 ⇒ width becomes 1/4); 2n ⇒ standard error divided by √2.

**④ Interpreting Confidence Intervals** ★ must memorise (state True / False first, then give a reason)
- μ is fixed but unknown; a particular interval either contains μ or it does not, **and you cannot know which**.
- 95% means that under repeated sampling about 95% of intervals contain μ, **not** “the probability that μ lies in this interval is 95%”.
- The next sample mean will not necessarily fall in the interval; a single individual even less so (the variation in individuals is far greater than the variation in sample means).
- A wider interval does not mean it is more likely to contain μ; 10 out of 50 intervals being on the low side is normal variation; but a large number of intervals not containing μ (far more than 5%, e.g. 298 out of 500) is evidence, although you still cannot determine the cause.
- Copying the same sample once to make up 2n is not a new random sample, and the interval does not truly become narrower; combining two independent random samples is acceptable and gives higher precision.
- Intervals from different sample sizes cannot be compared directly in this way; a lower sample mean alone also cannot show that the new method is better.

**⑤ Using an Interval to Test a Claim**: construct a μ interval for the new sample (e.g. 182.5 ± 1.96 × 15/6 = (177.6, 187.4)) → whether the claimed value 175 lies in the interval → draw a conclusion. You can only draw a conclusion about whether the means are different; you cannot infer the source of the sample.

**⑥ Factors Affecting Precision**: increasing n ⇒ σ_X̄ decreases, the interval becomes narrower, and the tail probability on the side away from μ decreases; increasing the confidence level ⇒ the interval becomes wider; increasing σ (or s) ⇒ the interval becomes wider.
