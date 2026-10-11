# GRF · Graphs and networks 图与网络 (Unit 3.3)

Bank: `<ROOT>\MAA\topics\03_Graphs_Networks.md` / `.pdf`. 23 questions with GRF parts in 2016–2025 (no 2019 key), about 167 tagged marks (12% of the total). 17 of these are Calculator-free and 6 Calculator-assumed. This is the most reliable calculator-free topic: candidates do well on the calculations and lose marks on the wording of reasons.

Scope boundary: critical paths, minimum spanning trees, maximum flow and assignment belong to NDM (see `06_Network_Decisions.md`).

## Scope
- Graph types and terms: simple, connected, bipartite, complete, bridge, degree, loops, multiple edges.
- Adjacency matrices (undirected, directed, weighted) and counting routes with matrix powers.
- Planar graphs and Euler's formula v − e + f = 2; redrawing with no crossings.
- Shortest path in a weighted network, with routes and lengths or costs.
- Euler trails and circuits (odd-vertex counting); Hamiltonian paths and cycles.
- Drawing a network from its adjacency matrix.
- Terminology: walk, trail, path, closed walk, cycle.
- Shortest journey that visits every vertex.

## How SCSA asks it
- Graph types, edge counts and reasons (Calculator-free): 2017 CF Q3, 2021 CF Q2, 2025 CF Q3.
- Adjacency matrices and counting routes: 2016 CF Q1(a), 2018 CF Q5, 2023 CF Q2.
- Planar graphs, Euler's formula and redrawing: 2016 CF Q5, 2017 CF Q3, 2022 CF Q1(c), 2024 CF Q5.
- Euler and Hamiltonian questions in a context such as an inspection route or a delivery round: 2016 CA Q14, 2022 CF Q1(b), (d), 2024 CF Q4, 2024 CF Q5.
- Shortest path in a directed or weighted network, with a cost formula or a road change: 2018 CF Q2(c), 2020 CA Q13, 2023 CA Q11(c), 2025 CF Q3(c)–(d).

## Patterns

| code | pattern | questions / marks (2016–25) | median part marks (range) | CF / CA parts | key past refs |
|---|---|---|---|---|---|
| GRF1 | 图的类型、顶点度数与构造 Graph types, degrees and construction | 9 / 28 | 1 (1–3) | 18 / 0 | 2017 CF Q3(b)(i)–(iii); 2021 CF Q2(c); 2025 CF Q3(a)–(b) |
| GRF2 | 邻接矩阵与多阶段路径计数 Adjacency matrices and multistage counts | 6 / 22 | 2 (1–3) | 11 / 2 | 2016 CF Q1(a); 2018 CF Q5(b)(i); 2023 CF Q2(a)–(c) |
| GRF3 | 平面图与欧拉公式 Planar graphs and Euler formula | 10 / 29 | 2 (1–3) | 12 / 3 | 2016 CA Q14(a); 2017 CF Q3(a)(i)–(ii); 2022 CF Q1(c); 2023 CA Q12(a)–(b) |
| GRF4 | 加权图最短路径 Shortest path in a weighted graph | 7 / 25 | 3 (2–3) | 6 / 6 | 2018 CF Q2(c); 2020 CA Q13(b)–(c); 2023 CA Q11(c); 2025 CF Q3(c)–(d) |
| GRF5 | 欧拉迹与欧拉回路判定及构造 Euler trails and circuits | 13 / 28 | 2 (1–3) | 15 / 2 | 2017 CF Q7(a)(i)–(ii); 2018 CF Q5(c); 2022 CA Q10(a); 2024 CF Q4(d) |
| GRF6 | 哈密顿路径与回路判定 Hamiltonian paths and cycles | 9 / 22 | 2 (1–3) | 7 / 7 | 2016 CA Q14(c)–(d); 2017 CF Q3(a)(iii); 2021 CF Q5(c)(i); 2024 CF Q5(c) |
| GRF7 | 由邻接矩阵还原网络图 Construct a graph from an adjacency matrix (related) | 3 / 11 | 3 (2–3) | 2 / 2 | 2016 CA Q15(a)–(b)(i); 2020 CF Q6(d) |
| GRF8 | 游走、迹、路径与闭合路线术语 Walk, trail, path and closed-walk terminology | 4 / 6 | 1.5 (1–2) | 2 / 2 | 2016 CA Q14(b); 2018 CF Q2(b); 2022 CA Q10(b)(i) |
| GRF9 | 访问所有顶点的最短行程 Shortest journey visiting every vertex (related) | 3 / 9 | 3 (3) | 1 / 0 | 2017 CF Q6(a); see the GRF9 caveat in SKILL.md |

## Method in brief

- **GRF1.** Simple: check for loops and for multiple edges, and give each fault its own reason. A connected graph on n vertices has at least n − 1 edges (a tree) and a complete graph has n(n − 1)/2. To make a graph connected, count its components first. To make it complete, subtract the existing edges from n(n − 1)/2. Bipartite: split the vertices into two sets, and draw only edges between the sets. A bridge is an edge whose removal disconnects the graph.
- **GRF2.** Undirected matrices are symmetric. For a directed graph, a 1 goes where the arrow points. Weights go in the matrix for weighted networks, and a loop shows as a non-zero diagonal entry. One-step routes from a vertex = the non-zero entries in its row. Routes of length n: the (i, j) entry of the nth power, counting returns. Use the calculator's matrix power and write the expression you used.
- **GRF3.** For a connected planar graph, v − e + f = 2. Write the values of v, e and f first, then substitute. Remember the outside face. Number of edges from the formula: e = v + f − 2. Redraw crossing edges around the outside or inside so that no edges cross, keeping every vertex and edge.
- **GRF4.** Label the network from the start vertex: each vertex gets the shortest distance to it and its predecessor. Trace back from the end vertex to write the route, then give the total with units. Cost questions: cost = fixed charge + rate × distance. For a changed road, let its length be a variable, compare the route through it with the original, and solve the inequality. Obey arrow directions.
- **GRF5.** Confirm connectivity first. Count odd vertices: none gives an Eulerian circuit (closed, back at the start); exactly two gives a semi-Eulerian trail from one odd vertex to the other; four or more gives neither. To make a route possible, add an edge between two odd vertices, and check that it is sensible in context.
- **GRF6.** A Hamiltonian cycle visits every vertex exactly once and returns to the start. A Hamiltonian path visits every vertex exactly once and does not return. Build the route by moving between adjacent vertices and checking for repeats. Name it as a cycle or a path, and say whether it is Hamiltonian.
- **GRF7.** Rows and columns are the vertices in the same order. A non-zero entry is an edge; an entry of 2 is a double edge; a diagonal entry is a loop. Symmetry about the main diagonal shows the graph is undirected; draw each edge once.
- **GRF8.** Walk: vertices and edges may repeat. Trail: no edge repeated. Path: no vertex repeated. Closed walk: start equals end. Cycle: a closed path. Check edges for repeats first, then vertices.
- **GRF9.** When the stem allows repeats, list the feasible routes, total the weights, and choose the smallest. State the full route, its total, and check the end vertex. If the stem says every vertex is visited once, it is a Hamiltonian question (GRF6), not GRF9.

## Writing tips
- Reasons must refer to a property of the graph: loops, multiple edges, the number of odd vertices, or whether v − e + f = 2 holds. "It is not simple" with no reason earns no mark.
- Use terms precisely. Eulerian (each edge once, back at the start) is not Hamiltonian (each vertex once).
- Verify Euler's formula with the numbers written out, not just "verified".
- Routes on a drawn network: mark them boldly, and show the arrows on directed graphs.
- Calculator-free networks: keep to up to about 8 vertices, and let every answer be checked by hand.
