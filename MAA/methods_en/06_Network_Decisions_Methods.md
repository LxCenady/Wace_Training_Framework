# MAA · Network and Decision Mathematics — Patterns and Solution Approaches

> Source: past exam questions from 2016–2025 (excluding 2019, which has no marking key) with sub-questions tagged NDM. These cover 37 questions and 15 patterns: 20 questions from the F paper (Calculator-free) and 17 from the A paper (Calculator-assumed). Pattern definitions are taken from `tools/catalogue_MAA.json`. Tags are drafts (draft_for_review); some have been checked. ★ marks the three patterns with the highest tagged marks (NDM10, NDM1, NDM6; about 20% of the 15 patterns).
> Figures and mark-earning points are taken from the Specific behaviours in the marking keys and are paraphrased; algorithm steps are general solution methods. The original questions and marking files are kept in the local ignored directory, and this document does not copy question stems.
> Review status: checked on 2026-10-11 by an independent reviewer against the original papers and keys (results in the Chinese review log `MAA/methods/审校记录.md`). No open review items remain in this file (2017A-Q8 is tagged only under FIN).

## Marking-key reminders

- **Arrows must be drawn on directed networks, including dummy activities** (2022 and 2023 reports): the 2022 report requires arrows on directed networks; the 2023 report goes further and requires dummy links to carry arrows too.
- **Capacities of cuts must be calculated by direction** (2018 report): the report stresses that the sum of capacities of a cut depends on the direction of each edge in a flow network. The 2025 report notes that explaining a cut in a maximum-flow diagram is a weak area.
- **List paths and flows clearly** (2016, 2017 reports): the 2016 report names the untidy layout of a maximum-flow answer; the 2017 report requires that 2-mark questions also show working, and an answer with only the result earns no marks. For a maximum-flow question, list each path with its flow, then add them up.
- **Use terms precisely** (2016, 2018, 2024 reports): network terms (spanning tree, cut, critical path, dummy link, etc.) must be used correctly. The 2016 report notes that network questions requiring a written explanation were answered poorly, while calculation questions were answered well.
- **Difficulty data**: 2016 report, the minimum spanning tree question (Q1) had a mean of 86.94%, the easiest question of that year; 2017 report, the Hungarian algorithm question (Q2) had a mean of 80.45%, the easiest question of that year; 2023 report, the Hungarian algorithm question (Q5) had a mean of 82.04%, also the easiest question of that year. The 2018 report says the maximum-flow question (Q17) was one of the hardest questions in the A paper.
- **Mark the chosen route on the network diagram** (2020 report): using a highlighter to mark the route or the chosen edges helps markers check the answer.
- **Note: the keywords for GRF and NDM overlap in the report index.** This note takes only passages whose context clearly belongs to network decision questions (minimum spanning trees, critical paths, maximum flow, the Hungarian algorithm). Passages on pure graph theory (Euler, Hamiltonian, etc.) are not used here.

---

## Pattern 1: Spanning trees and minimum spanning trees ★

**Recognition**: A connected weighted graph is given (cities, pipes, roads, etc.), and the question asks you to draw the tree that connects all vertices with the smallest total weight, or to find its total length. It may also ask you to demonstrate the working of Prim's algorithm.

**Steps**
1. Definition of a tree: connects all n vertices, contains no cycles, and has exactly n − 1 edges.
2. Prim's algorithm: choose a starting vertex; at each step add the edge of smallest weight that joins a selected vertex to an unselected one, provided it does not form a cycle, until all vertices are connected.
3. Mark the selected edges on the diagram (highlighted), and list the edge chosen at each step with its length.
4. Total length = sum of the weights of the selected edges, with units.
5. If the question requires the working of Prim's algorithm to be shown, record each step in a table (e.g. 2021A-Q15(a)).

**Mark-earning points (typical key wording)**: marks are banded by the number of correct edges chosen, e.g. stage marks for 3, 5 and 7 edges (2016F-Q1(b)); the tree is drawn complete; the length is correctly labelled; the total length the question asks for (2017F-Q6(b)(ii)); at least four correct edges drawn (2018F-Q1(a)).

**Common errors**: drawing a cycle; writing out the tree without showing the edge-selection process; forgetting units (metres or kilometres); omitting a connection the question requires to be included (2022A-Q14(b)(i) requires the connection to the main power supply to be counted); confusing a minimum spanning tree with a shortest path (shortest-path questions belong to GRF).

**Past questions**: 2016F-Q1(b), 2017F-Q6(b)(i), 2017F-Q6(b)(ii), 2018F-Q1(a), 2018F-Q1(b), 2020F-Q5(a)(i), 2020F-Q5(a)(ii), 2020F-Q5(b), 2021A-Q15(a), 2021A-Q15(b), 2021A-Q15(c), 2022A-Q14(a), 2022A-Q14(b)(i), 2022A-Q14(c), 2023A-Q11(d), 2024F-Q4(a), 2024F-Q4(c)(i), 2025A-Q11(a), 2025A-Q11(b), 2025A-Q11(c)(i), 2025A-Q11(d)

---

## Pattern 2: Minimum connector problem

**Recognition**: A context question asks you to connect locations (homes, facilities, stations) at the lowest total cost. A unit price is usually given, or the question asks whether a budget is enough.

**Steps**
1. Draw the locations as vertices, and the feasible connections as weighted edges.
2. Use the method in Pattern 1 to find the minimum spanning tree, and obtain the minimum total length.
3. If the question has a compulsory connection (e.g. a particular point must be connected), include it in the tree first (2022A-Q14(b)(i)).
4. Cost = total length × unit price (2022A-Q14(b)(ii)); to judge a budget, compare total cost with the budget and state the conclusion.
5. Changes in the situation (an edge becomes unavailable, or an edge's cost doubles): check again whether the tree changes. If an edge is replaced, write out the edge removed, the new edge added, and the change in total cost (2020F-Q5(b), 2022A-Q14(c)).

**Mark-earning points (typical key wording)**: total length correct, with units (2018F-Q1(b), 2022A-Q14(b)(i)); total cost and amount correct (2020F-Q5(a)(ii)); the conclusion matches the comparison (2021A-Q15(b)); the replaced edge and the change in cost are explained (2020F-Q5(b), 2021A-Q15(c), 2022A-Q14(c)).

**Common errors**: forgetting a compulsory connection; calculating cost from length without multiplying by the unit price; after a change, saying only that cost rises without giving the increase as a number; omitting units (metres, kilometres, dollars).

**Past questions**: 2016F-Q1(b), 2018F-Q1(a), 2018F-Q1(b), 2020F-Q5(a)(ii), 2020F-Q5(b), 2021A-Q15(b), 2021A-Q15(c), 2022A-Q14(b)(i), 2022A-Q14(b)(ii), 2022A-Q14(c), 2024F-Q4(b), 2025A-Q11(c)(ii), 2025A-Q11(d)

---

## Pattern 3: Project activity network construction

**Recognition**: An activity table is given (activity description, duration, immediate predecessors), and the question asks you to draw the project network, to write the immediate predecessors of an activity, or to explain the dashed lines in the diagram.

**Steps**
1. Nodes and arcs: nodes may represent events and arcs activities, with the activity name and duration written on each arc; use the convention set by the question consistently.
2. Connect in order: all the immediate predecessors of an activity point to it.
3. When the predecessors of two activities are not identical, or two activities share some predecessors, a dummy activity (duration 0, drawn as a dashed line) is needed to express the dependency.
4. Check: every activity appears in the diagram, there is one start and one end, and every edge has a direction.

**Mark-earning points (typical key wording)**: every edge has a task name, a duration and a direction (2024A-Q9(a), 2022F-Q7); dummy activities are correct (2024A-Q9(a) awards marks for two dummy activities separately; 2023F-Q4 requires at least one dummy activity; 2020A-Q16(a) requires the dashed connections to be correct); the table of immediate predecessors is complete (2023F-Q6(a), full marks only if all are listed); explaining the role of a dashed line (2021A-Q13(c)).

**Common errors**: dummy activities drawn too many times or missed; arrows not shown (both the 2022 and 2023 reports advise drawing arrows, including on dummy activities); immediate predecessors omitted where they connect through a dummy activity (2025A-Q10(a) awards two marks separately for the judgement of predecessors).

**Past questions**: 2017A-Q11(a), 2018F-Q6(a), 2020A-Q16(a), 2021A-Q13(a), 2021A-Q13(b), 2021A-Q13(c), 2022F-Q4(b), 2022F-Q7, 2023F-Q4, 2023F-Q6(a), 2023F-Q6(e), 2024A-Q9(a), 2025A-Q10(a)

---

## Pattern 4: Forward scan and earliest starting times

**Recognition**: In a project network, the question asks for the earliest starting time (ES) of an activity, which may need to be converted to a clock time or a date.

**Steps**
1. Record the project start time as 0, and calculate from left to right through the network.
2. For each activity: ES = the maximum of (ES + duration) over all immediate predecessors (take the largest, not the sum).
3. If the question gives a start clock time or an intermediate break, convert days or hours into clock times (an example is in the note under Pattern 5).

**Mark-earning points (typical key wording)**: the value is correct (2016F-Q2(b)(i)); the conversion to clock time is correct.

**Common errors**: taking the sum instead of the maximum; confusing time units (hours and days).

**Past questions**: 2016F-Q2(b)(i), 2017A-Q11(c)

> Note: Pattern 4 has only 2 tags, so this section is brief.

---

## Pattern 5: Backward scan and latest starting times

**Recognition**: The question asks for the latest starting time (LST) or latest finishing date of an activity.

**Steps**
1. The latest finish time of the project end = the project duration (the end time found from the forward scan).
2. For each activity: latest finish time = the minimum of the LST over all following activities (take the smallest); LST = latest finish time − duration.
3. If a date is required, first calculate the day number, then convert it into a calendar date (2022F-Q4(c) is done in two steps: first the number of days, then the date).

**Mark-earning points (typical key wording)**: LST values are correct (2016F-Q2(b)(ii), 2018F-Q6(d)(i), 2025A-Q10(c)); the number of days and the date are marked in two steps (2022F-Q4(c)). For 2018F-Q6(d)(ii), the stem says "earliest starting time", but the key's calculation is for the latest: the project duration is 9.5 hours (including a 30-minute break), the end is at 4 pm, and V must start before 1:30 pm. The stem and the key disagree; here it is recorded as LST, following the key.

**Common errors**: taking the maximum instead of the minimum in a backward scan; treating ES as LST; a date conversion off by one day.

**Past questions**: 2016F-Q2(b)(ii), 2017A-Q11(c), 2018F-Q6(d)(i), 2018F-Q6(d)(ii), 2022F-Q4(c), 2025A-Q10(c)

> Note: Pattern 5 has only 6 tags, so this section is brief.

---

## Pattern 6: Critical path and minimum project duration ★

**Recognition**: The question asks for the critical path, the critical activities or the minimum completion time, or asks about the effect on the project duration of a delay or a shortening of an activity.

**Steps**
1. Forward scan (Pattern 4) gives ES; backward scan (Pattern 5) gives LST.
2. Calculate the float of each activity = LST − ES; activities with float 0 are critical.
3. Critical path = the path from start to end made up of critical activities.
4. Minimum duration = the earliest finish time of the end vertex.
5. If the question requires it, write out the scan on the network (ES and LST marked at the nodes), then give the path and the duration (2023F-Q6(b), 2024A-Q9(b), 2025A-Q10(b)).
6. When activity times change, the scan must be redone: a new critical path may appear, and the duration does not necessarily change by the amount of the change.

**Mark-earning points (typical key wording)**: the critical path is correct (2016F-Q2(a), 2024A-Q9(b)); the duration is correct (as above); all critical activities are listed (2020A-Q16(b); listing fewer than all earns partial marks); the new duration and the new critical path after a delay (2016F-Q2(c), 2022F-Q4(d)); comparing the durations of two situations and choosing the plan that gives the shortest duration (2017A-Q11(d)).

**Common errors**: writing only the activity letters and not the full order of the path; when shortening an activity, looking at only one path and ignoring another that is also critical (2020A-Q16(e) key: B lies on both critical paths, BCE and BDG, so shortening B reduces the duration by 1 day; F is not a critical activity, so shortening it is ineffective; E lies on only one critical path, so D or G must also be shortened for it to be effective); the context of 2025A-Q10(e) shows that when several activities are shortened at once, the durations do not necessarily add up, and a rescan is needed to confirm.

**Past questions**: 2016F-Q2(a), 2016F-Q2(c), 2017A-Q11(b), 2017A-Q11(d), 2018F-Q6(b), 2018F-Q6(e), 2020A-Q16(b), 2020A-Q16(d), 2020A-Q16(e), 2021A-Q13(d), 2021A-Q13(f), 2021A-Q13(g), 2022F-Q4(a), 2022F-Q4(d), 2023F-Q6(b), 2024A-Q9(b), 2025A-Q10(b), 2025A-Q10(d)(ii), 2025A-Q10(e)(i), 2025A-Q10(e)(ii)

---

## Pattern 7: Float for non-critical activities

**Recognition**: The question asks for the float time of a non-critical activity, or the maximum delay that can occur without affecting the project duration; it may also ask for the meaning of float to be explained in context.

**Steps**
1. Float = LST − ES = latest finish time − earliest finish time.
2. Non-critical activities have float greater than 0; critical activities have float 0.
3. A delay no greater than the float does not change the duration; only the part of a delay beyond the float increases the duration. In the context of 2020A-Q16(d), a delay of 3 days with float 1 day increases the duration by 2 days.
4. If two activities lie on the same path, they share float: once one activity uses up float, the available float of the other reduces accordingly. The key for 2023F-Q6(d) requires the float of H to be found first (7 hours), and then D's ability to be delayed by 6 hours to be explained.
5. Explanation questions must be answered in context, stating the practical meaning of float (e.g. 2021A-Q13(e): how many days a task can be postponed without delaying the renovation).

**Mark-earning points (typical key wording)**: the float values are correct (2020A-Q16(c) awards marks separately for A, F and H; 2025A-Q10(d)(i)); when explaining why float is zero, state that these activities are on the critical path (2025A-Q10(d)(ii)); the change in duration caused by a delay (2020A-Q16(d)).

**Common errors**: writing a non-zero float for a critical activity; explanation questions answered with numbers only and no context (the 2025 report requires answers in context); ignoring the mutual effect of float on the same path.

**Past questions**: 2016F-Q2(b)(iii), 2017A-Q11(c), 2018F-Q6(c)(i), 2018F-Q6(c)(ii), 2020A-Q16(c), 2020A-Q16(d), 2020A-Q16(e), 2021A-Q13(e), 2021A-Q13(h), 2023F-Q6(c), 2023F-Q6(d), 2024A-Q9(c)(i), 2024A-Q9(c)(ii), 2024A-Q9(d), 2025A-Q10(d)(i), 2025A-Q10(d)(ii)

---

## Pattern 8: Maximum flow and minimum cut

**Recognition**: A directed capacitated network is given (pipes, roads, air routes, etc., with a capacity on each arc), and the question asks for the maximum flow that can pass (e.g. per minute or per hour), or the meaning of some nodes.

**Steps**
1. List all directed paths from the source (S) to the sink (T). For each path, mark its bottleneck (the smallest remaining capacity on the path) as the flow that can be allocated.
2. Allocate flow, reducing shared arcs by the capacity they use; add up the path flows to obtain the maximum flow.
3. Find a cut: divide the vertices into two parts, one containing S and one containing T. The capacity of the cut = the sum of the capacities of all arcs going from the S side to the T side (only arcs directed from the S side to the T side are counted).
4. If the maximum flow equals the capacity of some cut, that cut is a minimum cut, which verifies the maximum flow.
5. Units must be consistent: if the question asks for the hourly flow, multiply the per-minute value by 60 (2025A-Q13(d) requires both the per-minute and per-hour results to be written out).

**Mark-earning points (typical key wording)**: at least two path flows correct (2016A-Q9(a), 2017A-Q13(a)); all paths listed, and done systematically (2023A-Q11(a), 2022A-Q12(b)); the maximum flow value and units are correct (2017A-Q13(a), which requires the units given in the question); the minimum cut is drawn correctly (2016A-Q9(b), 2017A-Q13(b)).

**Common errors**: ignoring arc direction (the arrows determine how the cut capacity is calculated; the 2018 report specifically warns about this); a cut missing a vertex, or counting reverse arcs; path flow exceeding the remaining capacity of a shared arc; confusion of units (per minute and per hour); the 2025 report notes that explaining a cut in a maximum-flow diagram is a weak area.

**Past questions**: 2016A-Q9(a), 2016A-Q9(b), 2017A-Q13(a), 2017A-Q13(b), 2017A-Q13(c)(ii), 2018A-Q17(e)(ii), 2020A-Q15(b), 2020A-Q15(d), 2021A-Q16(c), 2021A-Q16(e), 2022A-Q12(b), 2023A-Q11(a), 2024F-Q3(b), 2024F-Q3(e), 2025A-Q13(d)

---

## Pattern 9: Represent an assignment problem

**Recognition**: The question gives feasible assignments between people and tasks (or machines), and asks you to draw a bipartite graph, to fill in an assignment matrix, or to draw a bipartite graph from an adjacency matrix.

**Steps**
1. On the left, place the people (or workers); on the right, the tasks (or machines). Edges show feasible assignments, labelled with weights (times, costs, outputs).
2. Matrix: rows correspond to the left side, columns to the right side, and entries are the weights of the corresponding pairs; infeasible positions are filled according to the convention stated.
3. If the numbers of rows and columns differ, add a column or row of zeros (dummy assignments) to make the matrix square, so that the Hungarian algorithm can be applied (see Pattern 10).
4. To draw a bipartite graph from an adjacency matrix, a position with a 1 means assignment is possible, and the corresponding edge is drawn (2021F-Q2(a)).

**Mark-earning points (typical key wording)**: matrix entries correct (2016F-Q3(a) is banded by the number of correct entries; 2020F-Q3(a)); edges and weights correct (2018F-Q4(a), 2023F-Q5(a)); the reason for adding a column or row of zeros (see Pattern 10).

**Common errors**: rows and columns swapped; infeasible entries missing from the matrix; applying the Hungarian algorithm to a non-square matrix without adding zeros; in 2023F-Q5(b), the key requires a column of zeros to be added, so pay attention to which objects (people or tasks) the added column corresponds to.

**Past questions**: 2016F-Q3(a), 2018F-Q4(a), 2020F-Q3(a), 2021F-Q2(a), 2023F-Q5(a), 2023F-Q5(b), 2025F-Q4(b)

---

## Pattern 10: Optimal assignment and Hungarian algorithm ★

**Recognition**: The question asks you to assign each person (or machine, or site) to a unique task so that the total time is shortest, or the total output (sales, production) is largest; the stem usually specifies the Hungarian algorithm.

**Steps**
1. For a maximisation problem: first subtract every element from a constant not less than all the elements (usually the largest value in the matrix), to convert the problem into minimisation. The keys for 2018F-Q4(c), 2020F-Q3(b), 2022F-Q6(a) and 2024A-Q12(a) all use this method.
2. Subtract the minimum of each row from that row.
3. Subtract the minimum of each column from that column.
4. Cover all the zeros with the fewest horizontal and vertical lines. If the number of lines equals the order of the matrix, go to step 5; otherwise take the minimum m among the uncovered elements, subtract m from each uncovered element, add m to each element at the intersection of two lines, and return to step 4.
5. Make a unique assignment among the zeros: take exactly one zero from each row and each column.
6. The total cost or total output of the assignment is found by adding the corresponding values in the original matrix, not in the adjusted matrix.

**Mark-earning points (typical key wording)**: each adjustment step is correct (row and column subtraction; taking the minimum of the uncovered elements and using it for the adjustment); 2016F-Q3(b) and 2022F-Q6(a) are marked step by step; the number of lines needed to cover the zeros is given (e.g. 3 lines; when the number of lines is less than the order, state that further adjustment is needed); the assignment is correct (2016F-Q3(b), 2025F-Q4(c)); the total is correct and uses the original matrix values (2024A-Q12(c), 2025F-Q4(a)).

**Common errors**: forgetting the conversion in a maximisation problem; using the wrong minimum in row or column subtraction; misjudging the number of covering lines; an assignment that is not unique; using the adjusted values to find the total; the assignment should be given in table form (2024A-Q12(b)). 2017F-Q2(b)(ii) asks why an assignment cannot yet be made; the answer is that the number of covering lines is less than the order.

**Past questions**: 2016F-Q3(b), 2017F-Q2(a), 2017F-Q2(b)(i), 2017F-Q2(b)(ii), 2017F-Q2(c), 2018F-Q4(b), 2018F-Q4(c), 2020F-Q3(b), 2020F-Q3(c), 2021F-Q2(d), 2021F-Q2(e), 2022F-Q6(a), 2022F-Q6(b), 2023F-Q5(c), 2023F-Q5(d), 2024A-Q12(a), 2024A-Q12(b), 2024A-Q12(c), 2024A-Q12(d), 2025F-Q4(a), 2025F-Q4(c)

---

## Pattern 11: Flow conservation and feasible flow assignment

**Recognition**: The question shows the flows on each arc of a capacitated network, and asks you to complete the unknown flows (x, y, z) or to identify which arcs are at full capacity.

**Steps**
1. Node conservation: at each intermediate node, inflow = outflow.
2. The flow on each arc does not exceed its capacity; when the flow equals the capacity, the arc is at full capacity.
3. Total outflow from the source S = total inflow to the sink T = network flow.
4. Use the conservation relationships to write equations for the unknowns, and explain why the value holds (2018A-Q17(b)(i) requires the basis for the value of x to be explained).

**Mark-earning points (typical key wording)**: the reason for conservation (2018A-Q17(b)(i)); calculation of the unknown (2018A-Q17(b)(ii)); all arcs at full capacity listed (2018A-Q17(c)); the network flow value is correct (2018A-Q17(d)); labelling is correct (2016A-Q9(c), 2020A-Q15(c), 2021A-Q16(d)); the flow through C is correct (2016A-Q9(d)).

**Common errors**: writing capacity as flow in the labels; missing an arc; flow direction inconsistent with the arrow; checking only one end (the outflow from S) and forgetting to check against the inflow to T.

**Past questions**: 2016A-Q9(c), 2016A-Q9(d), 2018A-Q17(b)(i), 2018A-Q17(b)(ii), 2018A-Q17(c), 2018A-Q17(d), 2020A-Q15(c), 2021A-Q16(d), 2024F-Q3(d)

---

## Pattern 12: Cut capacity and flow upper bounds

**Recognition**: The question asks for the capacity of a cut, asks you to show that a number (such as x) follows from the capacity of a cut, or asks you to verify the maximum flow by identifying a minimum cut. It may also ask which arc upgrade would increase the maximum flow.

**Steps**
1. Calculate the capacity of a cut from its definition: the sum of capacities of all arcs from the S side to the T side (reverse arcs are not counted).
2. The flow in any feasible flow does not exceed the capacity of any cut; so the capacity of a cut gives an upper bound on the maximum flow.
3. If the capacity of some cut equals the value of the maximum flow, that cut is a minimum cut, and the maximum flow is verified.
4. Explanation questions: when the capacity of one arc changes, only arcs on the minimum cut affect the maximum flow (questions such as 2017A-Q13(c) choose a road on this basis).

**Mark-earning points (typical key wording)**: interpreting the cut correctly, writing an equation and finding x (2020A-Q15(a)); all three cut capacities calculated (2018A-Q17(a)); the minimum cut drawn correctly (2016A-Q9(b), 2017A-Q13(b), 2021A-Q16(e), 2022A-Q12(c), 2023A-Q11(b), 2024F-Q3(c), 2025A-Q13(e)); explaining the cut (2025A-Q13(c)(ii)); arcs that can increase the flow (2017A-Q13(c)(i), (ii); the augmenting-path example is under Pattern 14).

**Common errors**: counting reverse arcs when calculating the cut; an incomplete division of the vertices (a vertex left without assignment to a side); in 2025A-Q13(f) (1 mark), the key requires an explanation of why cut 3 is not valid: the reason is that cut 3 does not separate the sink (H) from the source (A), so it does not satisfy the definition of a cut. The 2025 report notes that explaining cuts in a maximum-flow diagram is a weak area.

**Past questions**: 2016A-Q9(b), 2017A-Q13(b), 2017A-Q13(c)(i), 2017A-Q13(c)(ii), 2018A-Q17(a), 2018A-Q17(e)(ii), 2020A-Q15(a), 2020A-Q15(b), 2020A-Q15(d), 2021A-Q16(a)(i), 2021A-Q16(a)(ii), 2021A-Q16(e), 2022A-Q12(c), 2023A-Q11(b), 2024F-Q3(c), 2024F-Q3(e), 2025A-Q13(c)(i), 2025A-Q13(c)(ii), 2025A-Q13(e), 2025A-Q13(f)

---

## Pattern 13: Path bottlenecks and path-flow allocation

**Recognition**: The question asks you to list several paths and give the flow each path can carry, then add them to obtain the maximum flow; or asks for the maximum flow along a particular path.

**Steps**
1. List systematically all paths from S to T (start with the arcs leaving S, then expand layer by layer, to avoid missing any).
2. The maximum flow on each path = the smallest capacity on the path (taking into account the part already used by earlier paths).
3. Allocate in order: after allocating a path, subtract the capacity it uses from the shared arcs, then deal with the next path.
4. Add all the path flows to get the total flow; check against the cut capacities (Pattern 12).
5. Convert units (e.g. from per minute to per hour).

**Mark-earning points (typical key wording)**: at least two paths and their flows correct (2016A-Q9(a), banded by the number of correct paths); all paths listed (2022A-Q12(b), 2023A-Q11(a), 2024F-Q3(b)); total flow and units correct (2017A-Q13(a)); for 2021A-Q16(b), the maximum flow of each of two specified paths is marked separately; 2025A-Q13(d) requires the path, its length, and the per-minute and per-hour totals.

**Common errors**: missing paths; not subtracting the capacity of shared arcs, so the allocation exceeds capacity; forgetting unit conversion; paths not written out in full (each vertex from S to T should be listed).

**Past questions**: 2016A-Q9(a), 2017A-Q13(a), 2020A-Q15(b), 2020A-Q15(d), 2021A-Q16(b), 2021A-Q16(c), 2022A-Q12(b), 2023A-Q11(a), 2024F-Q3(b), 2025A-Q13(d)

---

## Pattern 14: Augmenting paths and residual capacities

**Recognition**: The question asks you to add a further flow to an existing flow, and to list the pipe sequence that can be used; or asks in which segment an upgrade increases the total flow the most.

**Steps**
1. From the current feasible flow, find a path from S to T on which every arc still has spare capacity (spare = capacity − current flow).
2. The flow that can be added = the smallest spare capacity on the path.
3. Update the flow and spare capacity on each arc, and repeat until no augmenting path exists; the flow is then maximal.
4. Only if an arc on the minimum cut is upgraded can the maximum flow increase; which segment to upgrade and by how much must be judged from the spare capacities and the cut capacities together (see Patterns 8 and 12).

**Mark-earning points (typical key wording)**: the path is correct (2018A-Q17(e)(i)); the right arcs are chosen and justified (2022A-Q12(d) requires reasons); the correct increment and new maximum flow (see Pattern 8).

**Common errors**: spare capacity not reduced; choosing an arc not on the bottleneck for upgrade; only giving the arcs without the reason.

**Past questions**: 2016A-Q9(e), 2018A-Q17(e)(i), 2022A-Q12(d)

> Note: Pattern 14 has only 3 tags, so this section is brief. In the catalogue, this pattern's syllabus status is "related".

---

## Pattern 15: Sources, sinks and intermediate nodes in flow networks

**Recognition**: A directed flow network is given (such as a cooling circuit or a water supply system), and the question asks you to identify the source and sink, or to count the intermediate nodes.

**Steps**
1. Source: a node with outgoing arcs only and no incoming arcs.
2. Sink: a node with incoming arcs only and no outgoing arcs.
3. The remaining nodes are intermediate nodes; in context questions, count the objects in the question (e.g. machines).

**Mark-earning points (typical key wording)**: all sources and sinks correct (2024F-Q3(a), 2025A-Q13(a)); the number of intermediate nodes (2025A-Q13(b)).

**Common errors**: ignoring the arrow direction; confusing a "source" in the situation (such as a supply facility) with a source node in the network.

**Past questions**: 2022A-Q12(a)(i), 2022A-Q12(a)(ii), 2024F-Q3(a), 2025A-Q13(a), 2025A-Q13(b)

> Note: Pattern 15 has only 5 tags, so this section is brief. In the catalogue, this pattern's syllabus status is "related".
