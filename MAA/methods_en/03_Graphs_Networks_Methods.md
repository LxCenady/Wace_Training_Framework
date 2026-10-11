# MAA · Graphs and Networks — Patterns and Solution Approaches

> Source: marking keys and exam reports for 23 past exam questions from 2016–2025 containing graph and network material, 96 sub-question tags (one sub-question may belong to several patterns; 91 distinct sub-questions after removing duplicates). 2019 has no marking key and is not included. Checked line by line by an independent reviewer; the record is in the Chinese review log `MAA/methods/` (01–03). Items still marked "(to be checked)" have their reasons given in the review log. The original questions and marking keys are not published with the repository; see the local `evidence/maa`.
> Numbering: `2023A-Q8(h)` = sub-question (h) of question 8 of the 2023 Calculator-assumed paper; `F` = Calculator-free. ★ = patterns ranked in roughly the top quarter by marks per sub-question: GRF3 (29 marks) is first, and GRF1 and GRF5 are joint second (28 marks each).
> Boundary with NDM (Network and Decision Mathematics): project critical paths, minimum spanning trees, maximum flow and similar topics belong to NDM and are not covered in this note.

## Marking-key reminders

- **Use terminology accurately**: syllabus terms such as simple, connected, bipartite, Eulerian, Hamiltonian and adjacency matrix are often misused. This point is repeated across many years' reports (the 2016 report; the 2017 and 2024 reports also give this advice to teachers).
- **Questions asking for an explanation or reasons are done poorly**: when a question uses "explain", "comment on" or "give reasons", the reasons are often incomplete (2016 report). The reasons must refer to specific properties of the graph, such as whether there are loops, whether there are multiple edges, or the number of odd vertices.
- **Directed graphs must show arrows** (2022 report). When marking out a route, use a bold pen (2020 report).
- **Write out the full check for Euler's formula**: the 2024 report names this point; a correct verification of Euler's rule is a weak area. First write the values of v, e and f, then substitute them to check.
- **Read the scale carefully when plotting points or drawing lines** (2017 and 2019 reports).
- **Network questions overall are done well**: the 2016 report says candidates answered network questions well; the 2025 report says question 3 (graphs and networks) was the best-performed question. However, many candidates did not know the calculator functions well and did not use them fully (2016 report).
- **Two-mark questions also need working shown** (common advice in the 2017, 2019 and 2020 reports): an answer with only the result and no working may earn no marks even if correct.

---

## Pattern 1: Graph types, degrees and construction ★

**Recognition**: The question asks whether a graph is a simple graph, whether it is connected, or whether it is bipartite; or asks for the minimum or maximum number of edges, the name of a complete graph, or the edges to add to make a graph connected or complete.

**Approach**
1. Simple graph: check for loops and multiple edges. Give two separate reasons, one for each; do not just say "it is not simple" without stating which kind of fault it has.
2. Bounds on the number of edges (for a simple connected graph with n vertices): at least n − 1 edges (a tree); at most n(n − 1)/2 edges (a complete graph). A complete graph is named directly from its definition.
3. Adding edges: to make a graph connected, first count the connected components; to make a graph complete, subtract the existing number of edges from n(n − 1)/2.
4. Bipartite graph: the vertices can be divided into two sets, with every edge joining the two sets. When drawing, keep the two sets clearly separate and draw only edges between the sets.
5. Bridge: an edge whose removal disconnects the graph. When a question asks which edge cannot be removed, it is looking for a bridge.

**Mark-earning points (typical key wording)**
- Edge-count questions: the maximum and the minimum each earn 1 mark (2017F-Q3(b)(i)); a single minimum value earns 1 mark (2017F-Q3(b)(ii)).
- Reasons questions: no loops and no multiple edges each earn 1 mark (2018F-Q5(a)(ii), 2021F-Q2(c), 2025F-Q3(a)).
- Bipartite graph: drawing two distinct sets of vertices with correct connections earns 2 marks (2024F-Q4(c)(ii)).
- Counting subgraphs: drawing 3, 6 or 9 correct qualifying subgraphs earns each band (2024F-Q5(d)). Note that the question asks for continuous paths, not arbitrary subgraphs.
- Three-word selection question: marks are banded by the number of correct selections and incorrect selections; full marks only if all correct ones are chosen and none extra (2025F-Q3(b)).

**Common errors**
- Confusing connected with complete, leading to wrong edge counts when adding edges.
- Giving only the edge in a bridge question, without its name (2021F-Q3(d)(ii) carries a separate mark).
- For 2024F-Q5(a)(ii), which asks what else the planar graph shows, the key answer is "connected", which is the premise for Euler's formula. The question and key are consistent.

**Past questions**: 2017F-Q3(b)(i), 2017F-Q3(b)(ii), 2017F-Q3(b)(iii), 2018F-Q5(a)(ii), 2018F-Q5(b)(ii), 2020F-Q2(a)(i), 2020F-Q2(a)(ii), 2020F-Q2(b)(i), 2021F-Q2(b)(ii), 2021F-Q2(c), 2021F-Q3(d)(i), 2021F-Q3(d)(ii), 2022F-Q1(a), 2024F-Q4(c)(ii), 2024F-Q5(a)(ii), 2024F-Q5(d), 2025F-Q3(a), 2025F-Q3(b) (multi-label)

---

## Pattern 2: Adjacency matrices and multistage counts

**Recognition**: An adjacency matrix is given, or the question asks you to write one out; the question asks for the number of one-step routes from a vertex, the number of two-step one-way routes, the number of routes of a given length, or the meaning of a row or column of the matrix.

**Approach**
1. Writing the matrix: an undirected graph's matrix is symmetric; for a directed graph, put a 1 in the position matching the arrow's direction; for a weighted network, enter the edge weight; no edge gives 0.
2. Reading the matrix: the sum of row i (or column i) gives the number of connections to that vertex (2020F-Q6(c)); a non-zero entry on the diagonal represents a loop.
3. Number of one-step routes: the number of non-zero entries in a row (2016A-Q15(b)(ii)).
4. Number of multi-step routes: in the nth power of the matrix, the (i, j) entry is the number of routes from i to j of exactly n steps, including return routes (2016A-Q15(b) distinguishes return routes from one-way routes in its stem).
5. Perform matrix powers on the calculator (CAS or matrix function), and write out the matrix or expression used.

**Mark-earning points (typical key wording)**
- Filling in the matrix is banded by the number of correct elements: at least 12, at least 16, all correct (2023F-Q2(a), 3 marks); 2016F-Q1(a) is banded similarly by about 12 and all 18.
- Listing routes: at least 3 listed, or all listed (2016A-Q15(b)(iii): 6 routes in total; 2023F-Q2(c): from G there are 5 open paths of length 2, not counting loops).
- Interpreting matrix entries: state the value first, then what it represents (2018F-Q5(b)(i), 2 marks).
- Identifying an undirected graph: state that the matrix is symmetric about the main diagonal (2023F-Q2(b)).

**Common errors**
- Counting or missing return routes (A → B → A) when a one-way route is asked for.
- Routes that pass through a loop, or are not open paths (start and end different, with no vertex revisited).
- Missing the direction of a directed edge (the explanation in 2018F-Q5(a)(i) must state the reason the matrix is not symmetric).

**Past questions**: 2016A-Q15(b)(ii), 2016A-Q15(b)(iii), 2016F-Q1(a), 2018F-Q2(a), 2018F-Q5(a)(i), 2018F-Q5(b)(i), 2020F-Q6(a), 2020F-Q6(b), 2020F-Q6(c), 2020F-Q6(e), 2023F-Q2(a), 2023F-Q2(b), 2023F-Q2(c)

---

## Pattern 3: Planar graphs and Euler formula ★

**Recognition**: The question asks you to use Euler's formula to verify something, to find the number of edges from the number of faces and vertices, to redraw a graph as a planar graph (edges do not cross), or asks how many regions (faces) the planar graph has.

**Approach**
1. Euler's formula: for a connected planar graph, v − e + f = 2. To verify, first write the numerical values of v, e and f, then substitute and check.
2. Finding the number of edges from the formula: e = v + f − 2. For example, a planar graph with 5 faces and 5 vertices: 5 − e + 5 = 2, giving e = 8 (the same as the setup of 2017F-Q3(a)(i)).
3. Verifying connectivity: the approach in 2016A-Q14(a) is to use Euler's formula to check whether the given network is connected; the key is to calculate v, e and f first and substitute them correctly.
4. Redrawing as a planar graph: reroute the crossing edges around the outside or inside so that no edges cross, keeping all vertices and edges (2023A-Q12(a)); when redrawing, each redrawn edge earns marks separately (2016F-Q5(a)(ii), (iii) are marked by edge).
5. Adding edges to limit the number of regions (2020F-Q2(a)(iii)): Euler's formula gives the total number of edges needed (for 5 vertices and 4 regions, e = 7), then subtract the existing edges to obtain the number of edges to add.

**Mark-earning points (typical key wording)**
- Correctly give the values of v, e and f, and check with Euler's formula: one mark each (2016A-Q14(a), 2024F-Q5(a)(i)).
- Finding the number of edges: write Euler's formula and solve correctly for e (2017F-Q3(a)(i), 2 marks).
- Drawing a planar graph: the drawn graph has the correct numbers of vertices, edges and faces, and has no crossings (2017F-Q3(a)(ii)).
- Adding edges: state the total number of edges first, then the number of edges to add (2020F-Q2(a)(iii)).

**Common errors**
- Forgetting that f includes the external region (the outside region must also be counted).
- Writing only "verified" without the substitution showing LHS = RHS (2022F-Q1(c) requires both sides of the equation to be written).
- Calling a non-planar graph planar without indicating the redrawn graph.
- The 2024 report notes that correctly verifying Euler's formula is a weak area.

**Past questions**: 2016A-Q14(a), 2016F-Q5(a)(i), 2016F-Q5(a)(ii), 2016F-Q5(a)(iii), 2016F-Q5(b), 2017F-Q3(a)(i), 2017F-Q3(a)(ii), 2020F-Q2(a)(iii), 2021F-Q2(b)(i), 2021F-Q3(a), 2022F-Q1(c), 2023A-Q12(a), 2023A-Q12(b), 2024F-Q5(a)(i), 2025F-Q3(b) (multi-label)

---

## Pattern 4: Shortest path in a weighted graph

**Recognition**: A weighted network is given (numbers on the edges are distances, times or costs), and the question asks for the shortest route from A to B and its length, time or cost; or asks how the shortest route changes after a road is added or shortened.

**Approach**
1. Label the network (working must appear on the network): starting from the start vertex, label each vertex with the shortest distance to it, working forward until the end vertex is reached.
2. Trace back from the end vertex along the labels, and write out the complete sequence of vertices (the route).
3. Write the total length. Convert units: in 2021F-Q5(a), the edge lengths are in hundreds of metres, so a path of 22 must be converted to 2200 m.
4. Cost questions: cost = fixed charge + unit rate × distance (2023A-Q11(c): first find the shortest distance, then substitute into the cost formula).
5. Questions with a stop along the way or a required intermediate point (2025F-Q3(d)): the key first finds the shortest journey passing through F, K–J–E–D–F–D–C–B, which takes 28 minutes; then adds a 45-minute stop, for a total of 73 minutes. Write the route in full.
6. Questions about altering a road (2020A-Q13(c)): let the length of the new road be a variable, compare the length of the route through it with the original route, set up an inequality, and find the range of the reduction.

**Mark-earning points (typical key wording)**
- Route and length are marked separately: route correct 1 mark, length correct 1 mark (2018F-Q2(c), 2022A-Q10(c), 2024F-Q4(e)).
- The working needs a systematic labelling (2024F-Q4(e); 2020A-Q13(b) requires the method to be shown on the diagram).
- Cost questions are marked in three separate steps: shortest route, shortest distance, lowest cost (2023A-Q11(c)).
- Road-alteration question: compare the route A–C–H through the new road CH with the original shortest route ACFH (44 km). The key concludes that the reduction must be greater than 4 km and less than 26 km (2020A-Q13(c), 3 marks).

**Common errors**
- Writing only the length without the route, or only the route without the length.
- Ignoring arrow directions in a directed graph, so that the route is not travelable (2018F-Q2(c) is a directed graph).
- Forgetting unit conversion (hundreds of metres, kilometres, minutes, dollars).
- The 2020 report advises marking routes in a bold pen so that they are not confused.

**Past questions**: 2018F-Q2(c), 2020A-Q13(b), 2020A-Q13(c), 2021F-Q5(a), 2021F-Q5(c)(ii), 2022A-Q10(c), 2023A-Q11(c), 2024F-Q4(e), 2025F-Q3(c), 2025F-Q3(d)

---

## Pattern 5: Euler trails and circuits ★

**Recognition**: The question asks whether a graph is Eulerian or semi-Eulerian, with reasons; asks whether a route can traverse every edge exactly once; asks for a feasible route, for an edge to add to make a route feasible, or for suggested stopping points or start points.

**Approach**
1. First confirm the graph is connected (Euler's results apply only to connected graphs).
2. Count the odd vertices:
   - 0 odd vertices: Eulerian; there is a closed Eulerian circuit that returns to the start.
   - 2 odd vertices: semi-Eulerian; there is an Euler trail, whose start and end are the two odd vertices.
   - 4 or more: neither Eulerian nor semi-Eulerian (the conclusion of 2024F-Q4(d) is neither).
3. Making the graph semi-Eulerian or Eulerian: add an edge between two odd vertices (2018F-Q5(c)(i)); after adding it, check that the edge is not a bridge (requirement of 2017F-Q7(a)(ii)).
4. Writing the route: a route that does not return to the start must start at one of the two odd vertices (in 2022F-Q1(d), the key accepts D as the stopping point, on the basis that the route does not need to return to the stopping point).
5. Naming the route: closed (returning to the start) is a circuit; not closed is a trail. The key for 2021F-Q3(c) is "semi-Eulerian trail" (the route in the question traverses each edge once, with different start and end points).
6. When explaining the conclusion, state the number of odd vertices, e.g. the graph has two odd vertices, so it is semi-Eulerian.

**Mark-earning points (typical key wording)**
- A judgement plus a reason, each as an item, e.g. "semi-Eulerian, because there are two odd vertices" (2022F-Q1(b), 2 marks).
- With 0 odd vertices, state "yes" and give the reason (2022A-Q10(a)).
- State the number of odd vertices (2023A-Q12(c); 2024F-Q5(b) requires counting the odd and even vertices).
- Edge-adding question: draw the added edge correctly, and explain why the route can now traverse every edge (2018F-Q5(c)(i), (ii)).
- Context question: the route must fit the situation (e.g. a parking stop or an inspection route), and the mathematical basis is written out (2022F-Q1(d)).

**Common errors**
- Answering only yes or no, without giving the number of odd vertices as the reason.
- Confusing Eulerian (each edge once, returning to the start) with Hamiltonian (each vertex once) (see Pattern 6).
- Forgetting to check connectivity.
- Assuming a graph with two odd vertices can be closed.
- 2025F-Q3(b) is a multi-label sub-question; the scoring rule for the three terms is given under Pattern 1.

**Past questions**: 2016F-Q5(c), 2017F-Q3(a)(iv), 2017F-Q7(a)(i), 2017F-Q7(a)(ii), 2018F-Q5(c)(i), 2018F-Q5(c)(ii), 2020F-Q2(b)(ii), 2021F-Q3(b), 2021F-Q3(c), 2022A-Q10(a), 2022F-Q1(b), 2022F-Q1(d), 2023A-Q12(c), 2023F-Q2(d), 2024F-Q4(d), 2024F-Q5(b), 2025F-Q3(b) (multi-label)

---

## Pattern 6: Hamiltonian paths and cycles

**Recognition**: The question asks whether a route can pass through every vertex exactly once (Hamiltonian), asks for such a route, or asks for the type of route (path or cycle).

**Approach**
1. Hamiltonian cycle: passes through every vertex exactly once and returns to the start (closed).
2. Hamiltonian path: passes through every vertex exactly once, but does not return to the start (end differs from start).
3. Finding a route: starting from the given vertex, move to adjacent vertices in turn, checking that no vertex is repeated; the route answer is written as a sequence of vertex letters (2017F-Q3(a)(iii)).
4. Naming: first check whether the route is closed, then whether each vertex is visited exactly once (the key for 2021F-Q5(c)(i) requires both cycle and Hamiltonian to be written).
5. For several plans on the same graph (e.g. Plans P, Q, R), check each one in turn for closure and for visiting each vertex exactly once (2020F-Q2(b)(iii)).
6. Drawing the route on the graph: the start must be marked, and each vertex is visited only once (2016A-Q14(d)).

**Mark-earning points (typical key wording)**
- The route passes through all vertices, with each vertex visited only once (2016A-Q14(d), 2024F-Q5(c)).
- The route is closed (start and end are the same) (2024F-Q5(c) also asks for the statement that the path is closed).
- Two properties, one mark each (2016A-Q14(c): the key gives "every vertex except the start and end is visited once" and "start and end are the same (closed)").
- Naming: cycle and Hamiltonian are each marked (2021F-Q5(c)(i), 2022A-Q10(b)(i)).
- Requirement for the end of a Hamiltonian path: the end must differ from the start (2018F-Q2(d)).

**Common errors**
- Revisiting a vertex (this breaks the definition of Hamiltonian; note that the shortest journey in Pattern 9 allows repetition).
- Calling a Hamiltonian path a cycle, forgetting that it is not closed.

**Past questions**: 2016A-Q14(c), 2016A-Q14(d), 2017F-Q3(a)(iii), 2018F-Q2(d), 2020F-Q2(b)(iii), 2021F-Q5(c)(i), 2021F-Q5(c)(ii) (also GRF4), 2022A-Q10(b)(i) (also GRF8), 2023A-Q12(d)(i), 2023A-Q12(d)(ii), 2024F-Q5(c), 2025F-Q3(b) (multi-label)

---

## Pattern 7: Construct a graph from an adjacency matrix

**Recognition**: An adjacency matrix is given, and the question asks you to draw the corresponding network; or asks which feature of the matrix shows that the network is undirected.

**Approach**
1. The rows and columns of the matrix correspond to the same set of vertices; place the points in the order given.
2. Non-zero entries represent edges: an entry of 1 is drawn as one edge; an entry of 2 is drawn as two multiple edges; a non-zero diagonal entry is drawn as a loop.
3. For an undirected network, the matrix is symmetric about the main diagonal, so each edge appears twice in the matrix. Count it only once when drawing (use the upper or lower triangle).
4. Identifying undirected: check whether the matrix is symmetric about the main diagonal (2016A-Q15(b)(i)).

**Mark-earning points (typical key wording)**
- Banded by the number of correctly drawn edges: at least 3, at least 6, all 9 (2016A-Q15(a), 3 marks).
- Stating the symmetry and the main diagonal (2016A-Q15(b)(i), 2 marks).
- For a planar graph drawing: correct connections, the loop is drawn, and the graph is planar, each marked separately (2017F-Q7(b)).
- Completing a network: add the missing edges from the matrix, including multiple edges (2020F-Q6(d)).

**Common errors**
- For a symmetric matrix, drawing each edge twice, which produces multiple edges.
- Missing the loops on the diagonal.

**Past questions**: 2016A-Q15(a), 2016A-Q15(b)(i), 2017F-Q7(b), 2020F-Q6(d)

(This pattern has only 4 sub-questions, so its conclusions are thin.)

---

## Pattern 8: Walk, trail, path and closed-walk terminology

**Recognition**: The question asks you to explain route terms such as closed walk, trail, path or cycle, or to judge which category a route falls into.

**Approach**
1. Walk: edges and vertices on the route may both be repeated.
2. Trail: a walk in which each edge is used only once (vertices may be repeated).
3. Path: each vertex is used only once (edges are then also not repeated).
4. Closed walk: a walk whose start and end are the same. Cycle: a closed path.
5. To judge a route, check edges for repetition first, then check vertices for repetition.

**Mark-earning points (typical key wording)**
- Explaining a trail: first say that it is a walk, then say that no edge is repeated (2018F-Q2(b), 2 marks).
- Explaining a closed walk: state that the start and end are the same (2016A-Q14(b)).
- Judging the type of route (2022A-Q10(b)(i), also in Pattern 6); from a given route length, deduce an open path (2021F-Q5(b); the key only requires the correct route to be written).

**Common errors**
- Calling a trail a path (a trail allows repeated vertices).
- Saying only that the route returns to the start, without stating that each edge is traversed once.

**Past questions**: 2016A-Q14(b), 2018F-Q2(b), 2021F-Q5(b), 2022A-Q10(b)(i) (multi-label, also in Pattern 6)

---

## Pattern 9: Shortest journey visiting every vertex

**Recognition**: Starting from a given vertex, visit all vertices and end at a given vertex; the question asks for the shortest time or distance and the route.

**Approach**
1. Check whether the question allows vertices to be revisited. The stem of 2017F-Q6(a) explicitly allows the same town to be passed more than once, so the complete total weight of each feasible route is what is compared.
2. List the feasible routes, calculate the total weight of each, and take the smallest.
3. Write out the complete route (the sequence of vertices) and the shortest total time (or total distance).
4. Check that the end vertex meets the question's requirements.

**Mark-earning points (typical key wording)**
- Listing a route that visits all vertices, listing the shortest route, and giving the shortest time: each is worth 1 mark (2017F-Q6(a)).
- 2022A-Q10(b)(ii): the key route is CBAGHFEDC (starting and ending at C, with each other vertex visited once), length 47, distance 4700 m; each of the three items is worth 1 mark.
- 2020A-Q13(a): give a route visiting all vertices, identify the correct route, and give the length (1 mark each).

**Common errors**
- The routes in the keys for 2020A-Q13(a) and 2022A-Q10(b)(ii) do not revisit any vertex (the former is a Hamiltonian path, the latter a Hamiltonian cycle), which does not match this pattern's definition of allowing repetition. By definition they belong to GRF6 (the length part can also be classed under GRF4). Their tag is GRF9; this is a labelling matter recorded in the review log, and this note has not changed the tag (to be checked).
- Giving only the route, without the total weight.
- Wrong end vertex (the question requires finishing at a specific vertex).

**Past questions**: 2017F-Q6(a) (the only sub-question in this pattern that explicitly allows repetition), 2020A-Q13(a) (to be checked, see above), 2022A-Q10(b)(ii) (to be checked, see above)

---

## Items to be checked

- Pattern 9: the tags for 2020A-Q13(a) and 2022A-Q10(b)(ii) are GRF9, but their keys require that no vertex is revisited, so they should be read as GRF6. The labels are set by the labeller; this note has not changed them, pending review.
- The following entries have been checked against the original key and their text has already been revised: 2024F-Q5(a)(ii) (Pattern 1), 2025F-Q3(d) (Pattern 4), 2020A-Q13(c) (Pattern 4), 2021F-Q3(c) (Pattern 5), 2016A-Q14(c) (Pattern 6); see the review log for details.
