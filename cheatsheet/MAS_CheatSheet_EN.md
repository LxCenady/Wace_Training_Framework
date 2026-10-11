# WACE Mathematics Specialist · Cheat Sheet (Patterns + Key Notes)

**General rules**: Principal argument −π < θ ≤ π · Write mathematical statements, not calculator language · When explaining, do not write "it"; state which quantity (e.g. "SD **of the sample mean**") · ln|…| include absolute value (may omit when the argument is always positive) · Indefinite integral + c · Rates of change with units · Expand brackets and guard against sign errors when copying (repeatedly flagged in yearly reports) · Memorise exact trigonometric values for special angles · When a question asks to prove / show, use algebra; "CAS says no solution" is not a proof · State the conclusion clearly

## 1 Complex numbers

**① Form conversion and operations**
- Division: multiply numerator and denominator by the conjugate of the denominator. Powers and roots: first write in r cis θ form, then use De Moivre ((√3 − i)⁵ = 32 cis(−5π/6) = −16√3 − 16i).
- ⚠ Third quadrant: the principal argument of −1 − i is −3π/4, not π/4, and cannot be written as 5π/4. Draw a diagram first to determine the quadrant.
- Given z = 3 + bi and tan θ = 2 ⇒ b = 6, r = 3√5.

**② Solve zⁿ = w** ★ appears every year
- Write w as R cis φ (1 mark for modulus, 1 mark for argument) → z = R^(1/n) cis((φ + 2kπ)/n), k = 0, …, n − 1 (1 mark for the general formula) → list **all** n roots within the range specified in the question, with adjacent roots separated by 2π/n.
- Example: z⁴ = −16i ⇒ 2 cis(−5π/8), 2 cis(−π/8), 2 cis(3π/8), 2 cis(7π/8).
- Roots of zⁿ = 1: equally spaced on the unit circle (2 marks for explanation: radius 1, equal spacing); product of all roots = (−1)ⁿ⁺¹; z⁴³ = 1 and z⁴⁷ = 1 have only the common root 1 (43 and 47 are coprime).
- zⁿ is a positive real number: n·arg z is an integer multiple of 2π (z = 4 cis(5π/6) ⇒ smallest n = 12).

**③ Complex roots of polynomials**
- "Show (z − α) is a factor": calculate P(α), **write out every term**, obtain 0 (key: not just the statement).
- Real coefficients ⇒ ᾱ is also a root ⇒ (z − α)(z − ᾱ) = z² − 2Re(α)z + |α|² → use division or compare coefficients to find the remaining factor → solve the quadratic.
- Example: P(2 + 4i) = 0 ⇒ factor z² − 4z + 20, remaining z² − 2z + 3 ⇒ z = 1 ± √2 i. ⚠ z² − 2z + 3 cannot be factorised as (z − 3)(z + 1) (2021 report).
- Given two complex roots, find the coefficients: each pair of conjugate roots gives a quadratic factor, then use the constant term to find the real root.

**④ Geometric meaning of multiplication**
- Template (1 mark each): "Multiplication by w = r cis θ dilates the modulus by a factor r and rotates anticlockwise by θ (clockwise by |θ| if θ < 0) about the origin." Multiplication by z⁻¹: take the reciprocal of the factor and reverse the direction of rotation.
- Find n for which zwⁿ lies in the second quadrant: each step rotates by arg w; when |w| = 1 there is a period, so give the full set of answers, e.g. n = 3 + 12k, 4 + 12k, 5 + 12k.

**⑤ Loci: sketch from equations**
- |z − a| = r: circle. |z − a| = |z − b|: perpendicular bisector of a and b. Arg(z − a) = θ: ray, with **open endpoint at a**.
- |z − a| + |z − b| = k: an ellipse when k is greater than |a − b|, **degenerates to a line segment when equal**.
- |z + 2| = |z − i| + √5 (difference equals the distance between the two points): ray starting from i, with **solid endpoint at i**.
- (z + i)·conj(z + i) = 2 ⇒ centre −i, radius √2; z − z̄ ≤ 6i ⇒ Im z ≤ 3.
- Marking points for graphs: key points or centre, position of boundaries, solid or dashed lines, shaded regions.

**⑥ Loci: write equations from graphs**: use only z, not x, y; circle ⇒ |z − c| ≤ r; sector ⇒ two Arg inequalities + one modulus inequality; find angles exactly using trigonometry.

**⑦ Extrema on loci**
- Distance from a point on a circle to c: maximum d + r, minimum |d − r| (d = distance from the centre to c). Nearest point on a ray: draw a perpendicular.
- Maximum argument occurs at the tangent: first use sin θ = r/d to find the angle between the tangent and the line to the centre, then add the argument of the centre, noting the range specified in the question.

**⑧ Vectors and geometric methods**
- z + r (sum of two equal-length vectors) forms a rhombus ⇒ arg(z + r) = θ/2; z − k forms a triangle, use the sine or cosine rule.
- Regular hexagon: first check where the centre is. When centred at the origin, all vertices have equal modulus and arguments differ by π/3; in 2025F-Q7, z₀ is at the origin, the moduli are r, √3r, 2r, √3r, r in order, and the product is 6r⁵.
- Trick: Σ n·iⁿ groups into sets of 4 terms, each group sums to 2 − 2i; taking the modulus of (a + bi)³ ⇒ (a² + b²)³ = |…|².

## 2 Functions and graphs

**① Domain of composite functions** ★ most frequently flagged (6 years)
- f(g(x)) is defined ⇔ x ∈ dom g **and** g(x) ∈ dom f. After substituting, do not simplify first; each restriction usually earns 1 mark.
- Sources of restrictions: denominator ≠ 0; expression under a square root ≥ 0; **when the square root is in the denominator, > 0**; argument of ln > 0.
- Example: f = 1 − √(x − 4), g = 1/x² ⇒ 1/x² ≥ 4 ⇒ −½ ≤ x ≤ ½ and x ≠ 0. f = √(4 − x), g = 1/x² ⇒ x ≤ −½ or x ≥ ½.
- ⚠ √(x²) = |x|, so f(h(g(x))) is not necessarily equal to f(x).

**② Inverse functions**
- Exists ⇔ one-to-one (horizontal line test); otherwise restrict the domain, with the "largest possible domain" taken up to the vertex.
- Method: swap x and y (1 mark) → solve for y → the ± sign is determined by **ran f⁻¹ = dom f**; dom f⁻¹ = ran f.
- Graph is symmetric about y = x, mark the corresponding endpoints (a, b) ↔ (b, a). Whether f⁻¹(−1) is defined: first check whether −1 is in ran f.
- Inverse trigonometric functions: x = 2 tan y ⇒ y′ = 2/(4 + x²) (use implicit differentiation, then use 1 + tan²y to convert to x).
- Explain "g is not one-to-one": "because g(1) = g(−1) = 1"; do not write "it is many to one".

**③ Sketching y = 1/f(x)** ★ often examined in CF
- Zeros of f ⇒ vertical asymptotes; as x → ±∞, f → ±∞ ⇒ horizontal asymptote y = 0.
- Vertical asymptote of f at x = b ⇒ 1/f has an open point at (b, 0) (range excludes 0); horizontal asymptote of f at y = c (c ≠ 0) ⇒ y = 1/c.
- Local maximum (a, m) ↔ local minimum (a, 1/m); points where f = ±1 are fixed; sign does not change; open point of f at (a, b) ⇒ open point of 1/f at (a, 1/b), when b = 0 it becomes a one-sided asymptote.
- Find the range: read from the graph of 1/f, noting values that are not attained.

**④ Absolute value functions**
- |f(x)|: reflect the part below the x-axis above the x-axis; f(|x|): keep the right half and mirror it to the left; f(−|x|): keep the left half and mirror it to the right.
- Number of solutions to |f(x)| = k: intersect with the horizontal line y = k, check the endpoint k separately; you can sketch the number-of-solutions function N(k).
- The solution set of |x + 1| + |x + a| = k is an interval ⇒ the flat section of the sum of two absolute values is the solution set (a = 3, k = 2).
- Determine y = a|x − b| + c from the graph: the vertex gives b and c, the gradient gives a.

**⑤ Rational functions: determine parameters from graphs / sketch graphs**
- Zeros ↔ factors of the numerator; vertical asymptotes ↔ factors of the denominator; horizontal asymptote = ratio of leading coefficients; oblique asymptote = quotient from polynomial division (x − 1 − 3/(x + 1) ⇒ y = x − 1).
- Repeated factor: in the numerator ⇒ graph touches but does not cross the x-axis; in the denominator ⇒ both sides of the asymptote have the same sign (both tend to −∞).
- Give a reason (1 mark): "c = 3 since x = 3 is a vertical asymptote". A quadratic with no zeros, a(x − 3)² + c, requires a and c to have the same sign.
- Sketch checklist (1 mark each): x-intercept, y-intercept, vertical asymptote, horizontal or oblique asymptote, turning points (mark if present), behaviour on each side of asymptotes. First check for any cancelled factor (hole).

## 3 Three-dimensional vectors and systems of linear equations

**① Systems of linear equations** ★ appeared in CF in 7 of the last 10 years
- Three elimination steps (1 mark each): use two pairs of equations to eliminate the same variable → solve for one variable → back-substitute.
- With parameters: reduce to (k − 2)z = c − 5 ⇒ k ≠ 2: unique solution (c arbitrary); k = 2 and c ≠ 5: no solution; k = 2 and c = 5: infinitely many solutions.
- ⚠ **For infinitely many solutions, write the solution set** (2022 report: many stopped after writing “infinitely many solutions”), express it using a parameter or relationships between variables. Example: z = t ⇒ y = t − 1, x = (11 − 3t)/2, i.e. r = (11/2, −1, 0) + t(−3/2, 1, 1).
- Geometric interpretation: unique solution = three planes intersect at a point; one parameter = intersect in a line (possibly two planes coincide; both points must be written); two parameters = three planes coincide; no solution = there are parallel planes, **or** the three planes intersect pairwise to form three parallel lines (triangular prism, 2020F-Q4). First check whether the normal vectors are proportional.

**② Plane equations**
- Parametric form r = a + λu + μv ⇒ n = u × v (write each component of the cross product clearly) ⇒ r·n = a·n, i.e. ax + by + cz = k.
- Through three points: cross product of two edge vectors; z = 2x + y + 4 ⇒ n = (2, 1, −1).
- Contains line L and is perpendicular to plane 1 ⇒ n₂ = d_L × n₁; contains two intersecting lines ⇒ n = d₁ × d₂.

**③ Intersections, angles, distances**
- Line and plane: substitute r = a + λd, solve for λ, write the point (3 marks). Line and sphere: obtain a quadratic equation in λ, two solutions, tangent, no intersection; or compare the distance from the centre of the sphere to the line with the radius.
- Two lines: set components equal, use two equations to solve for λ, μ, **substitute into the third to check**; if it does not hold, they do not intersect, and this step is the proof.
- Closest point on a plane to point L: draw a line through L along the normal vector, find its intersection with the plane.
- Angle between line and plane: sin θ = |d·n|/(|d||n|). Distance from point to plane = |n·(P − A)|/|n|, where A is any point on the plane; this formula is not on the formula sheet, so if used, include the derivation or use the normal method instead. Volume of parallelepiped = |c·(a × b)|.

**④ Spheres**: complete the square on the general form, e.g. x² + y² + z² − 4x + 2y − 6z + 5 = 0 ⇒ |r − (2, −1, 3)| = 3; endpoints of a diameter ⇒ centre is the midpoint (report: often calculated incorrectly); tangent to a plane ⇒ radius = distance from centre to plane; passes through all vertices of a rectangular prism ⇒ centre is the midpoint of a space diagonal.

**⑤ Vector proofs** (in both CF and CA): express the required vector in terms of basis vectors → expand the dot product (key: get 4 terms) → use given conditions (square ⇒ a·b = 0, |a| = |b|) → state conclusion. Marks for notation.

**⑥ Applications**: reflection ⇒ the sum of the unit vectors B→S and B→R is ∥ n; the steepest descent direction on a slope lies in the slope plane and is perpendicular to the horizontal line; for distance problems involving moving objects, see the next section.

## 4 Vector calculus and motion (only in CA paper)

**① Differentiation**: v = r′, a = v′, differentiate component by component; speed |v|; draw vectors on the diagram (with the start point at the position at that time). Constant speed ≠ uniform velocity (direction is changing); write that sin² + cos² = 1 was used (1 mark).

**② Integrate to find r(t)**
- Integrate component by component, add a **constant vector**, use r(0) to determine each component (2018 report: many wrote this unclearly).
- Gravity + wind: a = (0, −9.8) ⇒ r = ((70cos θ + w)t, 70 sin θ·t − 4.9t²); range: set y = 0, solve for t, then substitute into x.
- Horizontal drag + vertical lift: x′ = 32e^(−0.05t), h″ = s − 9.8, find s from the given r. For the landing angle, use the angle between the velocity vector and the slope.

**③ Eliminate the parameter to get a Cartesian equation** ★
- sin² + cos² = 1 ⇒ circle or ellipse; double-angle formulas directly give the relationship between x and y ⇒ a segment of a parabola; first convert to the same angle and then use sin² + cos² ⇒ general curve (e.g. a figure “8” shape); (eᵗ + e⁻ᵗ)² − (eᵗ − e⁻ᵗ)² = 4 ⇒ x² − y² = 4; x is linear in t ⇒ solve directly for t and substitute into y.
- ⚠ **Write the range of values**, derive it from the range of t; often both x and y need restrictions: x ≥ 2 **and y ≥ 0** (writing only x ≥ 2 loses marks); 1 ≤ x ≤ e³.

**④ Distance travelled and displacement**
- Distance travelled = ∫ₐᵇ √(ẋ² + ẏ²) dt; first determine the start and end times: time for one lap = least common multiple of the periods of the components (2π, 4π, 6π have all been tested), or find t from the coordinates.
- Explanation: ∫₀¹ v dt = “the change in displacement (position vector) during the first second”; ∫|v| dt = distance travelled. The 2025 report specifically names confusion between these two. Draw the displacement vector on the diagram: from r(a) to r(b).

**⑤ Closest distance and relative position**
- Same time parameter: relative position d(t) = r_P − r_Q (when asked for relative position, the order must be correct, 1 mark); closest ⇔ d(t)·(v_P − v_Q) = 0; “how long within 50 m” ⇒ solve |d(t)| < 50.
- Both speed and departure time can be adjusted ⇒ shortest distance between two lines: use independent parameters λ, μ, make PQ perpendicular to both d₁ and d₂.
- Angle of descent = |90° − φ| (φ is the angle between the velocity and k), or use sin⁻¹(|v_z|/|v|) directly.

## 5 Integration techniques and applications

**① Definite integrals with a given substitution** ★ almost every year in CF (4–7 marks)
- Five steps (1 mark each): find dx from the substitution → **change the limits** → convert the integrand completely to the new variable and simplify → integrate → substitute to get the exact value.
- Trigonometric substitution: for √(a² − x²) use x = a sin θ; for x² + a² use x = a tan θ. Example: ∫₀^√3 √(1 − x²/4) dx, x = 2 sin θ ⇒ ∫₀^(π/3) 2cos²θ dθ = π/3 + √3/4.
- Indefinite integral version (∫x(1 + x)ⁿ dx): do not change the limits; substitute back to x at the end. ⚠ Simplifying after substitution is often where errors occur (2020, 2023 reports).

**② Trigonometric identities**: cos² = ½(1 + cos 2x); sin² = ½(1 − cos 2x); (sin x + cos x)² = 1 + sin 2x; product-to-sum 2 sin A cos B = sin(A + B) + sin(A − B); tan² = sec² − 1.

**③ Partial fractions** ★ high frequency in CF
- Forms: distinct linear factors A/(x − a) + B/(x − b); repeated root A/(x + 1) + B/(x + 1)²; irreducible quadratic (Bx + C)/(x² + 2). When the question specifies the form, write it as given.
- After putting over a common denominator, equate numerators (1 mark) → substitute special values or compare coefficients to find the constants (1 mark) → integrate term by term: ln|x − a|, −B/(x + 1), if the numerator is the derivative of the denominator then ln|quadratic|, q/(x² + 4) → (q/2)tan⁻¹(x/2) → write + c.
- Example: 1/(x² − 1) ⇒ ½ ln|(x − 1)/(x + 1)| + c; (5x + 3)/(x + 1)² = 5/(x + 1) − 2/(x + 1)². If no hint is given, first factorise the denominator yourself (1 mark).

**④ Area**
- First find intersection points and tangent points; when writing the curve as x = g(y) is more convenient, integrate with respect to y (key: marks are given for both methods).
- Symmetry: for an ellipse, or a shape symmetric about a coordinate axis, multiply by a factor; circular segment: difference between the upper and lower branches 2√(…).
- A definite integral can be interpreted as a geometric area (triangle, trapezium). Compare the numerical area with πr² to determine whether a curve is a circle.

**⑤ Volumes of solids of revolution** ★ high frequency in CA
- About the x-axis π∫y² dx; about the y-axis π∫x² dy (first write x² as a function of y); between two curves π∫(R² − r²), ⚠ not π∫(R − r)².
- The integral expression must include π, the limits, and dx or dy (limits + notation together give 1 mark).
- Contexts: depth when 80% full ⇒ set ∫₀ʰ πx² dy = 0.8V and solve for h; filling rate dV/dt = (dV/dh)(dh/dt); increment δh ≈ δV ÷ πx²|_(y=h); annulus R, r = 3 ± √(4 − y²).

## 6 Rates of Change and Differential Equations

**① Implicit differentiation**
- Differentiate both sides with respect to x; terms containing y are multiplied by y′; use the usual product and chain rules. When the question says not to solve for y′, don't solve it—substitute the point directly to evaluate.
- Horizontal tangent: set numerator = 0 and solve simultaneously with the original equation; second derivative: differentiate the expression already found again, then substitute x, y, y′.

**② Related rates** ★
- Write the relation (eliminate redundant variables if necessary; you can also keep two variables and differentiate implicitly) → differentiate with respect to t → substitute the values **at that instant** (often find θ, h first) → include units.
- Example: regular hexagon A = (3√3/2)s², s = 4, ds/dt = 0.5 ⇒ dA/dt = 6√3 ≈ 10.39 cm²/s. Lighthouse makes 3 revolutions per minute ⇒ dθ/dt = π/10 rad/s.
- Circular motion (Ferris wheel, merry-go-round): dθ/dt = 2π/T; use the cosine rule s² = 89 − 80cos θ or y = R sin(θ + α); differentiate implicitly with respect to t; find the maximum of ds/dt by differentiating again (geometrically when PC is tangent to the circle). ⚠ Height above ground = height relative to the centre + R.

**③ Slope fields**
- Substitute points to find slopes (1 mark); infer the equation from the field: see whether the slope changes only with x or only with y, where it is 0, and where it is undefined.
- Draw solution curves: pass through the given point, follow the short line segments, mark symmetry; where denominator = 0 and numerator ≠ 0, the tangent is vertical and the curve turns back there; where slope = 0 there is a horizontal tangent; **the point of maximum slope is a point of inflection** (2025A-Q16 point of inflection at (3, −1)).

**④ Separation of variables**
- Write as ∫g(y)dy = ∫f(x)dx (1 mark) → integrate, add only one constant, put absolute value signs around the ln argument → substitute the initial condition → write in explicit form.
- dP/dt = kP ⇒ P = P₀eᵏᵗ. ⚠ "instantaneous growth rate is 10%" is dP/dt = 0.1P (P₀ = 30000e^(−4.5) ≈ 333); it cannot be treated as 1.1 times per year (≈ 412).
- Example: dh/dt = −1/(100h) ⇒ h² = h₀² − t/50; dv/dt = −9.8 − 2v ⇒ v = 4.9(e^(−2t) − 1); depth must then be found by integrating v again.

**⑤ Logistic growth** ★
- dP/dt = rP(k − P) ⇔ P = k/(1 + Ae^(−rkt)): carrying capacity = the non-zero P that makes dP/dt = 0; **fastest growth occurs when P = k/2**, maximum growth rate = r(k/2)².
- ⚠ Letters depend on the question (in some questions k is the proportionality constant; in others it is written as (1/r)P(k − P)). Example: P = 18000/(10.25e^(−0.15t) + 1) ⇒ carrying capacity 18000, maximum growth rate 0.15 × 9000 × ½ = 675 horses/year.
- Sketching: k/2 < P₀ < k ⇒ concave down throughout, no point of inflection; P₀ > k ⇒ decreasing towards k; changing the carrying capacity ⇒ new point of inflection and asymptote.
- Explanation: when P < k/2, the growth rate increases with P; when P > k/2, it decreases and approaches k. For equations that are not logistic (e.g. 0.001(100 − P)²), analyse the change in slope directly.

**⑥ Velocity as a function of displacement v = f(x)** ★★ flagged in reports three times
- a = dv/dt = v·dv/dx = d(½v²)/dx. ⚠ dv/dx itself is not acceleration. Example: v = −0.2x ⇒ a = 0.04x; v = x/8 ⇒ a = x/64.
- x(t): dx/dt = v(x), separate variables, substitute the initial position. Example: v = x/8, x(0) = 192 ⇒ x = 192e^(t/8).
- Test for SHM: only a = −n²(x − c) (proportional to displacement and in the opposite direction) qualifies; a = 0.04x is not.

**⑦ Simple harmonic motion (SHM)**
- ẍ = −n²x ⇒ x = A cos(nt + φ); T = 2π/n; v_max = An; v² = n²(A² − x²).
- Determine A and the phase: x(0) = 0 and v(0) > 0 ⇒ A sin(nt); if no direction is given, both ±A sin are accepted; n = 2, x(0) = −1, v(0)² = 32 ⇒ A = 3.
- Distance travelled: 4A per period, 2A per half-period; for less than half a period and when the starting point is not at equilibrium or an endpoint, use ∫|v| dt. Damping: A = A₀e^(−kt); treat A < 0.01 as stopped.

**⑧ Small increments formula**: δy ≈ (dy/dx)δx; δN ≈ (dN/dt)·δt (dN/dt is given directly by the equation; watch the time units).

## 7 Statistical Inference (CA paper only)

**① Distribution and probability of X̄** ★
- "By the CLT, since n is large, X̄ is approximately normal with mean μ and SD σ/√n" (normal, mean, standard deviation worth 3 marks in total). If the population is normal, this holds for any n.
- If the population is not normal (uniform, exponential, skewed): the method is the same; when asked "does the answer change?", answer no + CLT reason.
- Sum question: 50 times with a total < 8.96 kL ⇔ X̄ < 179.2 L. Draw the distribution of X̄: a narrow bell shape centred at μ, width about ±3σ/√n; shade the probability region when required.

**② Finding the sample size**
- First draw a diagram to decide whether it is two-tailed, one-tailed or a half-interval, then find the critical z: P(|X̄ − μ| < d) = 0.98 ⇒ z = 2.326; P(X̄ > 25) = 0.03 ⇒ z = 1.881; P(0 < Z < k) = 0.4 ⇒ k = 1.282.
- n = (zσ/d)²: when "at least" is required, round up (304.3 ⇒ 305, 600.25 ⇒ 601); when finding n from an interval, take the nearest integer (differences caused by using z = 2.576 and z = 2.58 are both accepted in the key).

**③ Confidence intervals**
- x̄ ± z·s/√n. Reverse-engineer: midpoint = x̄; half-width = z·σ_X̄ (150 ≤ μ ≤ 200 ⇒ σ_X̄ = 25/1.96 = 12.76); find s from the width and n.
- Changing sample size: width ∝ 1/√n (n × 16 ⇒ width becomes 1/4); 2n ⇒ standard error divided by √2.

**④ Interpreting confidence intervals** ★ must memorise (state True / False first, then give a reason)
- μ is fixed but unknown; a particular interval either contains μ or does not, and **you cannot know which**.
- 95% means that in repeated sampling about 95% of intervals contain μ, **not** "the probability that μ lies in this interval is 95%".
- The next sample mean does not necessarily lie in the interval; a single individual even less so (variation between individuals is much greater than variation in sample means).
- A wider interval does not mean it is more likely to contain μ; 10 out of 50 intervals being too low is normal variation; but a large number of intervals not containing μ (far more than 5%, e.g. 298 out of 500) is evidence, although it still does not prove the cause.
- Copying the same sample to make 2n is not a new random sample, and the interval does not really become narrower; combining two independent random samples is acceptable and gives greater precision.
- Intervals from different sample sizes cannot be compared directly in this way; a lower sample mean alone does not show the new method is better.

**⑤ Using an interval to test a claim**: construct the μ interval for the new sample (e.g. 182.5 ± 1.96 × 15/6 = (177.6, 187.4)) → is the claimed value 175 in the interval? → draw a conclusion. You can only conclude whether the means differ; you cannot infer the source of the sample.

**⑥ Factors affecting precision**: increasing n ⇒ σ_X̄ decreases, the interval becomes narrower, and the tail probability on one side far from μ becomes smaller; increasing the confidence level ⇒ the interval becomes wider; increasing σ (or s) ⇒ the interval becomes wider.
