# WACE Mathematics Applications · Cheat Sheet (Patterns + Notes)

**General rules**: formulas on the formula sheet are not repeated · interpretations state "which quantity + units + direction + context" · two-mark questions need working · draw with a ruler, label scales and arrows (directed networks, dummy activities) · CA: write the inputs (N, I, PV, PMT, FV, P/Y, C/Y, or regression or matrix expression) and key output, not keystrokes · discrete quantities (people, periods, weeks): "at least" rounds up, "latest / maximum" rounds down · money to the cent unless told otherwise

## 1 Bivariate data analysis (BIV)

**① Two-way tables and percentages** ★
- Check row and column totals against each other; a missing cell = total minus known cells.
- Percentages follow the explanatory variable: explanatory in rows ⇒ row percentages; in columns ⇒ column percentages. Each % = cell ÷ group total × 100.
- Compare association: "In group A, X is a%, versus b% in group B, c percentage points higher", then the direction in context. Comparing counts, or the wrong groups, loses marks.
- Maximum rate in a multi-way table: fix the base, compare rates within each dimension.

**② Scatterplots and r** ★
- Describe direction (positive/negative), form (linear, or "non-linear" if clearly curved) and strength (weak / moderate / strong, quoting r).
- r has the sign of the slope. If only r² is given, r = ±√r² with the sign from the slope.
- r measures linear association only. In context, name both variables.
- Strong r does not prove causation: name a confounding variable, reverse causation or chance, with a factor from the context.

**③ Least-squares line** ★
- Read a and b from the statistics mode; write ŷ = a + bx with the question's variable names (y response, x explanatory); round as asked.
- Drawing: two x values, two calculated y values, plotted and joined with a ruler; label the two points. The line must span the data and pass near key points.
- Slope: "for each extra 1 unit of x (units), y is predicted to increase (or decrease) on average by |b| (units)". Use "decrease" if b is negative.
- Intercept: predicted y at x = 0; meaningless if x = 0 is unrealistic or outside the data.
- r²: "about r² × 100% of the variation in y is explained by the linear relationship with x"; unexplained = 1 − r².

**④ Prediction and extrapolation** ★
- Check variable coding (e.g. year ⇒ n) before substituting.
- Inside the data range (interpolation) with strong r ⇒ reliable; outside (extrapolation) ⇒ unreliable; moderate r ⇒ "may not be valid".
- With several predictors choose the strongest r, and give the reason.

**⑤ Residuals and residual plots** ★
- Residual = observed − predicted; negative means the observed value is below prediction.
- Plot: explanatory variable on the horizontal axis, residuals vertical, zero line drawn, points to scale.
- Random scatter around zero ⇒ linear model suitable; curve, funnel or trend ⇒ not suitable. Justify with the pattern, not r alone.

**⑥ Roles and conclusions**
- The explanatory variable explains or predicts; the response is what is explained. Use time order or who sets the variable.
- "Does it prove …?" ⇒ No: not every interval reflects the truth, and chance cannot be excluded.

⚠ Common errors: r² for r; intercept and slope swapped; variable names not from the question; residual sign reversed; "high/low" without comparison to the prediction.

## 2 Sequences: growth and decay (SEQ)

**① Indices and starting values** (formula sheet uses T₁ = a; follow the question's indexing)
- Every recurrence states its starting value and whether it is T₀ or T₁.
- "nth term rule" ⇒ explicit rule; "how each period changes" ⇒ recurrence.

**② Arithmetic and geometric** ★
- Arithmetic: d (value and sign, negative when decreasing); with the intercept write Tₙ = dn + c, naming gradient d and intercept c.
- Geometric: decrease of x% ⇒ r = 1 − x% (14% ⇒ 0.86, not 0.14); r from the ratio of consecutive terms; average rate of decrease = 1 − r.
- "First time reaching a value": solve, take the smallest integer period ("at least / first" rounds up), and state the full result (which week, end of which year).

**③ Cumulative totals (not on the formula sheet)**
- Arithmetic sum Sₙ = n(T₁ + Tₙ)/2; geometric sum Sₙ = T₁(1 − rⁿ)/(1 − r).
- Cumulative total = sum of terms + initial amount. Compare two plans by finding each date of reaching the target.
- Off-by-one term counts are a common error.

**④ First-order recurrence Tₙ₊₁ = aTₙ + b** ★
- a = proportion kept per period (1 − loss rate); b = fixed change per period, with units consistent with T.
- Steady state: S = b/(1 − a), valid when |a| < 1; set Tₙ₊₁ = Tₙ = S; compare the value with the threshold (does it run out, reach the target?).
- Withdrawal that keeps the population stable = growth at steady state; round discrete quantities (fish) down.
- From three consecutive terms: solve two equations for a and b.
- After a change point use the new a and b, starting from the value at that time.
- Graphs: plot points only, not joined; use the required interval.

⚠ Common errors: r and 1 − r confused; index shift; wrong steady-state equation; convergence not checked; old parameters after a change point; wrong rounding direction.

## 3 Graphs and networks (GRF)

**① Terms and properties** ★
- Simple: no loops, no multiple edges (give the two reasons separately). Complete Kₙ has n(n − 1)/2 edges. Tree: connected, no cycles, n − 1 edges.
- Bipartite: two sets, every edge joins them; draw the sets clearly separated.
- Bridge: removal disconnects the graph; "which edge cannot be deleted" ⇒ find the bridge.
- Walk ⊃ trail (no repeated edges) ⊃ path (no repeated vertices). Closed walk: start = end. Cycle: closed path.
- Keep Eulerian (every edge once) and Hamiltonian (every vertex once) apart.

**② Adjacency matrices** ★
- Undirected: symmetric. Directed: follow arrows, usually not symmetric. Weighted: enter weights. Non-zero diagonal = loop.
- Non-zero entries in row i = one-step routes from i. The (i, j) entry of Mⁿ = routes from i to j of exactly n steps, including back-and-forth routes.
- List routes fully (at least 3, or all, earn marks). Open path: different start and end, no repeated vertex.
- From a matrix: 1 = one edge, 2 = double edge, non-zero diagonal = loop; undirected edges counted once.

**③ Euler's formula and planar graphs** ★
- v + f − e = 2 (formula sheet). Verify by writing v, e, f (f includes the outside region), then LHS = RHS. Rearrange for e or f.
- Redrawn planar graph: no crossings, all vertices and edges kept; each redrawn edge can earn marks.
- Edges needed for a set number of regions: Euler gives total edges, subtract those present.

**④ Eulerian conditions** ★
- Confirm connectivity. Odd-degree vertices: 0 ⇒ Eulerian (circuit returns to start); 2 ⇒ semi-Eulerian (trail from one odd vertex to the other); 4 or more ⇒ neither.
- To make it traversable, add an edge between the two odd vertices; write the route.
- Context routes (inspection, delivery): start or park at an odd vertex, because the route need not return.
- State the number of odd vertices in the explanation.

**⑤ Hamiltonian routes** ★
- Every vertex exactly once. Hamiltonian cycle returns to start; Hamiltonian path ends elsewhere. Write the vertex sequence and name it.
- If repeats are not allowed, do not repeat vertices.

**⑥ Shortest route (weighted graph)** ★
- Working on the network: label each vertex with its shortest distance from the start until the finish; backtrack to write the vertex sequence. Route and length are marked separately.
- Follow arrows on directed graphs; convert units (hundreds of metres to metres, minutes, dollars).
- Cost = fixed charge + unit price × distance. Stopping midway = journey time + stop time.
- New road of length x: compare the route through it with the original shortest route, solve the inequality for x.

**⑦ Shortest journey visiting all vertices**
- List feasible routes (compare full totals if repeats are allowed); pick the minimum. Write route, total and end vertex.

⚠ Common errors: connected confused with complete; "not simple" without naming loops or multiple edges; arrows ignored; length without route (or reverse); edge named but not the type in a bridge question; "verified" with no substitution in Euler checks.

## 4 Time series analysis (TSI)

**① Moving averages** ★
- Odd window (3, 5): average placed at the middle period.
- Even window (4, 6): centred; halve the first and last values, divide by the window length, place at the middle; write "centred".
- Window = period: quarters 4; five-day week 5; six-day week 6; seven-day week 7.
- Purpose: smooths short-term and seasonal variation to show the trend.

**② Seasonal indices (average percentage method)** ★
- % = actual ÷ seasonal average (centred moving average) × 100. Average each season's %, then normalise to mean 100% (quarterly indices sum to 400%; five-day week sums to 500%).
- Use decimals (110.76% ⇒ 1.1076); never multiply or divide percentages directly.
- Missing table entry = normalised total minus the other entries.
- Index > 1: above average; < 1: below. Name the season or day and the percentage above or below.

**③ Deseasonalising** ★
- Deseasonalised value = actual ÷ index (decimal). Reseasonalise: deseasonalised × index.
- Watch multiply/divide direction and units (hundreds of dollars vs dollars); round last.

**④ Time coding and linear trend** ★
- Least-squares line on deseasonalised data: y = a + bt, with the question's variable names.
- Coding: quarters consecutive; daily data with k days a week: t = (week − 1) × k + day within week. Example: Mon–Fri, Friday of week 4 ⇒ t = 3 × 5 + 5 = 20; Tue–Sun (6 days), Thursday of week 4 ⇒ t = 3 × 6 + 3 = 21.
- Slope sign: positive = growth, negative = decline; state the average change per period with units.
- Trend line: two points at chosen t values, joined with a ruler; mark the intercept.

**⑤ Forecasts and reliability** ★
- Deseasonalised forecast = a + bt; actual forecast = that × matching index; round as asked.
- Forecast beyond the data ⇒ extrapolation ⇒ "unreliable", with the reason.

**⑥ Description and decisions**
- Trend (slope direction, in context) and seasonality (high and low seasons with index values).
- Staff leave or similar decisions: choose the lowest index season and quote it.
- Long-term prospects: quote the slope, not just the graph.

⚠ Common errors: indices as percentages; even window not centred or ends not halved; off-by-one t; regression on raw data; extrapolation called reliable; moving averages in the wrong period.

## 5 Loans, investments and annuities (FIN)

**① Interest and recurrence** (compound and effective-rate formulas are on the sheet)
- Rate per period = annual rate ÷ periods per year; periods = years × periods per year.
- Recurrence: Aₙ₊₁ = (1 + r)Aₙ ± d (+ deposits, − repayments); always state A₀.
- Nominal rate = rate per period × periods per year (not the effective rate). Rate per period from growth factor = factor − 1.
- Plans: at the same nominal rate, more frequent compounding gives a higher effective rate. Investments: higher effective rate; loans: lower. Daily compounding: m = 365.

**② Financial solver (TVM)** ★
- Write each input: N (payments, not years), I (nominal annual rate), PV, PMT, FV, P/Y, C/Y (equal ⇒ interest per payment). BEG for start-of-period payments, END for end-of-period (check wording).
- Signs: opposite directions have opposite signs; loan cleared ⇒ FV = 0; savings target ⇒ FV opposite the deposit sign.
- N as a decimal: round as asked (up to be fully repaid, down for "maximum"), then apply the final-payment method.
- PMT: use the question's term and precision, usually rounded up to the cent.
- I: enter N, PV, PMT, FV; solve; state and convert.

**③ Repayment table and totals** ★
- Interest = r × opening balance; closing = opening × (1 + r) − R; every column correct.
- Balance after N full periods = Bₙ. Final payment = Bₙ × (1 + r). Total repaid = N × R + final. Total interest = total repaid − principal; total cost adds the deposit.
- Keep decimals in r and balances; do not substitute a rounded rate (the final payment can change markedly).
- If each payment is no more than that period's interest, the balance never falls and the loan is never repaid: state this.

**④ Withdrawals, perpetuities and rates** ★
- Withdrawal annuity: Aₙ₊₁ = (1 + r)Aₙ − P. Monthly interest with yearly withdrawals: first find the effective annual rate.
- Largest withdrawal that keeps capital from falling = interest per period = r × PV.
- Years the money lasts: solver with PV, PMT, I, FV = 0; take the decimal N, then round.
- Perpetuity: PV = PMT ÷ rate per period; PMT = PV × rate per period. Annuity to perpetuity: balance at change point becomes the new PV.
- Use the rate per payment period; never divide the annual rate by the number of payments.

⚠ Common errors: annual rate used per period; P/Y and C/Y not matched; N in years; same sign for deposits and withdrawals; final interest forgotten; largest withdrawal taken as a fraction of principal; two-mark answers without inputs.

## 6 Network and decision mathematics (NDM)

**① Spanning trees and Prim's algorithm** ★
- Spanning tree: all vertices, no cycles, exactly n − 1 edges.
- Prim: from any vertex, add the cheapest edge joining the chosen set to a new vertex without a cycle; list edges in order with lengths; highlight on the diagram; total with units.
- Compulsory links (e.g. main supply) are included first.

**② Minimum connector problems**
- Cost = total length × unit price; compare with budget; state the conclusion.
- Changed or unavailable edge: state the edge removed, the edge added, the change in cost, and whether the tree changes.

**③ Project networks** ★
- Activity names and durations on arrows; all arrows directed; all immediate predecessors point to the activity.
- Dummy activities (duration 0, dashed) express dependencies that cannot be shown otherwise; dummy links need arrows too.
- Complete precedence table; a missing predecessor loses marks.

**④ Scans, float and critical path** ★
- Forward scan: ES = largest of (ES + duration) over predecessors (not the sum). ES of the finish = minimum completion time.
- Backward scan: LST = smallest LST of successors − duration. LST of the finish = completion time.
- Float = LST − ES. Zero float = critical. Critical path: start to finish through critical activities only; write the full sequence.
- Delay ≤ float leaves completion time unchanged; floats are shared along a path.
- After shortening or delaying, rescan: the critical path may change. Shortening non-critical activities does not help.
- Convert days or hours to clock times or dates.

**⑤ Maximum flow and minimum cut** ★
- List all S → T paths systematically; each path carries its smallest remaining capacity; allocate in order, reducing shared arcs; total = maximum flow.
- Cut capacity = arcs from the S side to the T side only (backward arcs excluded). The cut must separate S from T. Maximum flow = a cut's capacity ⇒ that cut is minimum and verifies the maximum.
- Conservation: flow in = flow out at intermediate nodes; out of S = into T; flow = capacity ⇒ saturated.
- Units: per minute × 60 = per hour.
- Augmenting path: add flow along residual capacity; only arcs on the minimum cut can raise the maximum flow.

**⑥ Assignment and the Hungarian algorithm** ★
- Bipartite: workers vs tasks; rows = workers, columns = tasks; infeasible cells as stated; pad with zeros to make a square matrix.
- Maximising: subtract each entry from the largest entry.
- Subtract each row minimum; then each column minimum.
- Cover all zeros with the fewest lines. Lines = order ⇒ assign using a unique zero per row and column. Fewer lines ⇒ subtract the smallest uncovered entry m from uncovered entries, add m at crossings, and repeat covering.
- Total cost or profit uses the original matrix, not the adjusted one.

⚠ Common errors: maximisation not converted; wrong line count; sum taken instead of maximum (ES); non-zero float on a critical activity; backward arcs in a cut; non-unique assignment; arrows missing on directed networks; per minute vs per hour.
