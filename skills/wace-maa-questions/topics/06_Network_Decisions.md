# NDM · Network and decision mathematics 网络与决策数学 (Unit 4.3)

Bank: `<ROOT>\MAA\topics\06_Network_Decisions.md` / `.pdf`. 37 questions with NDM parts in 2016–2025 (no 2019 key), about 310 tagged marks (23% of the total, the largest topic). 20 of these are Calculator-free and 17 Calculator-assumed. It supplies about a third of the calculator-free questions (20 of 56), with GRF and BIV making up most of the rest.

Scope boundary: basic graph properties, Euler and Hamiltonian routes and shortest paths belong to GRF (see `03_Graphs_Networks.md`).

## Scope
- Spanning trees and the minimum spanning tree (Prim, or by inspection); minimum connector problems with cost.
- Project networks: activity tables, activity-on-arc diagrams with dummy activities, forward and backward scans, earliest and latest times, floats, critical path, minimum duration.
- Maximum flow and minimum cut: paths and their flows, cut capacities, flow conservation, augmenting paths, sources and sinks.
- Assignment problems: bipartite graphs, cost or time matrices, the Hungarian algorithm for minimising and maximising.

## How SCSA asks it
- Minimum spanning tree and minimum connector questions in a local context (sprinklers, pipes, power, roads): 2016 CF Q1, 2018 CF Q1, 2022 CA Q14, 2025 CA Q11.
- Project scheduling: 2016 CF Q2, 2022 CF Q4, 2023 CF Q6, 2024 CA Q9, 2025 CA Q10.
- Assignment and the Hungarian algorithm (workers to jobs, sales representatives to territories): 2017 CF Q2, 2020 CF Q3, 2022 CF Q6, 2024 CA Q12, 2025 CF Q4.
- Maximum flow, cuts and conservation in a water or factory network: 2016 CA Q9, 2018 CA Q17, 2021 CA Q16, 2023 CA Q11, 2025 CA Q13.

## Patterns

| code | pattern | questions / marks (2016–25) | median part marks (range) | CF / CA parts | key past refs |
|---|---|---|---|---|---|
| NDM1 | 生成树与最小生成树 Spanning trees and minimum spanning trees | 9 / 48 | 2 (1–5) | 10 / 11 | 2016 CF Q1(b); 2018 CF Q1(a)–(b); 2024 CF Q4(a); 2025 CA Q11(a)–(c)(i) |
| NDM2 | 最小连接方案 Minimum connector problem | 7 / 24 | 2 (1–5) | 5 / 6 | 2020 CF Q5(a)(ii), (b); 2022 CA Q14(b)(i)–(c); 2025 CA Q11(c)(ii), (d) |
| NDM3 | 项目活动网络建模 Project activity network construction | 10 / 32 | 3 (1–4) | 6 / 7 | 2023 CF Q4; 2023 CF Q6(a), (e); 2024 CA Q9(a) |
| NDM4 | 正向扫描与最早开始时间 Forward scan and earliest starting times | 5 / 10 | 2 (1–3) | 1 / 1 | 2016 CF Q2(b)(i); 2017 CA Q11(c); 2020 CA Q16(b) |
| NDM5 | 反向扫描与最迟开始时间 Backward scan and latest starting times | 7 / 13 | 1 (1–3) | 4 / 2 | 2016 CF Q2(b)(ii); 2018 CF Q6(d)(i); 2022 CF Q4(c); 2025 CA Q10(c) |
| NDM6 | 关键路径与最短项目工期 Critical path and minimum project duration | 9 / 46 | 2 (1–3) | 7 / 13 | 2016 CF Q2(a), (c); 2022 CF Q4(a), (d); 2024 CA Q9(b); 2025 CA Q10(b) |
| NDM7 | 非关键活动浮时 Float for non-critical activities | 9 / 35 | 2 (1–3) | 6 / 13 | 2020 CA Q16(c)–(e); 2023 CF Q6(c)–(d); 2025 CA Q10(d)(i)–(ii) |
| NDM8 | 最大流与最小割 Maximum flow and minimum cut | 9 / 35 | 2 (1–4) | 1 / 14 | 2016 CA Q9(a)–(b); 2023 CA Q11(a); 2025 CA Q13(d) |
| NDM9 | 分配问题的二分图、表格或矩阵表示 Represent an assignment problem | 6 / 13 | 2 (1–2) | 7 / 0 | 2016 CF Q3(a); 2023 CF Q5(a)–(b); 2025 CF Q4(b) |
| NDM10 | 最优分配与匈牙利算法 Optimal assignment and Hungarian algorithm | 9 / 59 | 2 (1–6) | 17 / 4 | 2017 CF Q2(a)–(c); 2022 CF Q6(a)–(b); 2024 CA Q12(a)–(d); 2025 CF Q4(a), (c) |
| NDM11 | 流量守恒与可行流配置 Flow conservation and feasible flow assignment (related) | 5 / 14 | 2 (1–2) | 1 / 8 | 2018 CA Q17(b)(i)–(ii); 2024 CF Q3(d) |
| NDM12 | 割容量与流量上界 Cut capacity and flow upper bounds | 9 / 28 | 1 (1–3) | 1 / 19 | 2018 CA Q17(a); 2020 CA Q15(a); 2025 CA Q13(c)(i)–(ii) |
| NDM13 | 路径瓶颈与路径流量分配 Path bottlenecks and path-flow allocation (related) | 8 / 31 | 3 (2–4) | 1 / 9 | 2016 CA Q9(a); 2021 CA Q16(b); 2022 CA Q12(b) |
| NDM14 | 增广路径与剩余容量 Augmenting paths and residual capacities (related) | 3 / 5 | 2 (1–2) | 1 / 2 | 2018 CA Q17(e)(i); 2024 CF Q3(e) |
| NDM15 | 流量网络源汇与中间节点识别 Sources, sinks and intermediate nodes in flow networks (related) | 2 / 5 | 2 (1–2) | 1 / 2 | 2024 CF Q3(a); 2025 CA Q13(a)–(b) |

## Method in brief

- **NDM1.** A tree on n vertices has n − 1 edges and no cycles. Prim: start at a vertex and repeatedly add the cheapest edge that joins a chosen vertex to an unchosen one without forming a cycle. Mark the chosen edges on the diagram, list them in the order chosen, and give the total with units.
- **NDM2.** Build the minimum spanning tree on the feasible connections. Include any compulsory connection first. Cost = total length × unit price (or a fixed cost plus the rate, as stated). For a changed connection, state the edge removed, the edge added, the new total, and the change in cost as a number.
- **NDM3.** Activities are arcs with a name, a duration and a direction; events are nodes. Where two activities share some predecessors but not all, add a dummy activity (duration 0, dashed, with an arrow). Check that every activity appears once, that there is one start and one end, and that every arc has an arrow, including dummies. Write the immediate predecessors as a table if asked.
- **NDM4.** Forward pass: start at 0; for each activity, earliest start = the largest earliest finish among its immediate predecessors (the maximum, not the sum). Convert to clock times or dates if the stem asks.
- **NDM5.** Backward pass: latest finish of the end = project duration. For each activity, latest finish = the smallest latest start among its successors; latest start = latest finish − duration. Give dates by counting days first, then converting.
- **NDM6.** Float = latest start − earliest start. Activities with zero float are critical; the critical path runs from start to end through them. Minimum duration = earliest finish of the end node. If an activity time changes, rescan the whole network: a new critical path may appear, and the duration does not always change by the full amount. When two critical paths exist, shortening one activity may not shorten the project.
- **NDM7.** A delay no bigger than the float does not change the project duration; only the part beyond the float does. Floats on the same path are shared: after one activity uses some float, the others have less. Explanations give the practical meaning in context (days a task can be postponed without delaying the job).
- **NDM8.** Cut capacity = sum of the capacities of the arcs that go from the source side to the sink side (arcs going back are not counted). Each path's flow is at most the cut capacity of any cut, so a cut gives an upper bound. If a flow equals a cut capacity, the flow is maximum and the cut is minimum. Units: convert per minute to per hour when asked.
- **NDM9.** Bipartite graph or matrix: rows are one set (people), columns the other (tasks). Entries are weights for feasible pairs; infeasible pairs are left out or marked by the convention stated. For a non-square matrix, add a dummy row or column of zeros before using the Hungarian algorithm, and say which objects it stands for.
- **NDM10.** Minimising: row reduction (subtract each row's minimum), column reduction, then cover all zeros with the fewest lines. If the lines equal the matrix order, make the unique assignment; otherwise subtract the smallest uncovered value from uncovered entries and add it at the intersections of two lines, and repeat. Maximising: subtract every entry from a constant at least as large as the largest entry, then minimise. The total cost or output is found from the original matrix.
- **NDM11.** Conservation: at each intermediate node, inflow = outflow. Each arc's flow is at most its capacity. Outflow from the source = inflow to the sink = network flow. Use these equations to find unknown flows and state why the value holds.
- **NDM12.** Cut capacity by definition (source side to sink side only). The capacity of any cut is an upper bound on the maximum flow. Increasing an arc raises the maximum flow only if it lies on a minimum cut. A set of vertices is a valid cut only if it separates the source from the sink.
- **NDM13.** List all paths from S to T systematically, layer by layer. Each path's flow = the smallest remaining capacity on it. Allocate in turn, subtracting the used capacity from the shared arcs, and add the path flows.
- **NDM14.** Augmenting path: a path from S to T on which every arc has spare capacity (capacity minus current flow). Add the smallest spare capacity on it, update, and repeat until no such path exists. The flow is then maximal.
- **NDM15.** Source: arcs leave it but none enter it. Sink: arcs enter but none leave. Everything else is intermediate. In a context question, count the items the question names (for example, machines).

## Writing tips
- Arrows are required on directed networks, including dummy activities. The 2022 and 2023 examiners' reports both name missing arrows as a lost-mark point.
- Show each stage of the algorithm: the reduced matrix, the lines, and the assignment. Mark routes and chosen edges clearly on the diagram (a bold or highlighted route is easier to check).
- For maximum flow: list every path with its flow, add them, and check against a cut.
- Explain cuts and conservation in words that name the arcs and the source and sink. This is a weak area in the reports.
- Keep the calculator-free networks to a manageable size: a project of up to about 10 activities, assignment matrices up to 4 × 4 (or 5 × 5 with simple numbers), and flow networks with up to about 8 arcs.
- Calculator-assumed networks may be larger, but the working for each step (the path, the cut, the ES or LS values) is still needed.
