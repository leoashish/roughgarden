# Tim Roughgarden: Algorithms, Complexity, Game Theory — Notes

## Algorithms (CS161 / Algorithms Illuminated)

### Divide & Conquer
- **Merge sort**: split, recurse, merge. O(n log n).
- **Inversion count**: count pairs i<j with a_i > a_j via merge sort. O(n log n).
- **Closest pair**: split by x, recurse, check strip. O(n log n).

### Greedy
- **MST (Kruskal)**: sort edges, union-find, add if no cycle. Correct by cut property.
- **Huffman**: combine two smallest frequencies; optimal prefix code (exchange argument).
- **Weighted interval scheduling**: DP with p(i) (last compatible job). O(n log n).

### Dynamic Programming
- **0/1 Knapsack**: dp[i][c] = max(dp[i-1][c], dp[i-1][c-w_i]+v_i).
- **Edit distance**: Levenshtein DP.
- **Optimal BST / sequence alignment**.

### Shortest Paths
- **Dijkstra**: non-negative weights, greedy with priority queue. O(m log n).
- **Bellman-Ford**: handles negative edges, detects negative cycles. O(mn).

### Max Flow
- **Edmonds-Karp** (BFS Ford-Fulkerson): O(V E²). Min-cut max-flow theorem.

## Complexity Theory

### P vs NP
- P: polynomial-time solvable. NP: polynomial-time verifiable.
- NP-complete: in NP and NP-hard (all NP reduce to it).
- **Cook-Levin**: SAT is NP-complete.

### Reductions
- 3-SAT → Independent Set (literal nodes, clause edges, complement edges).
- Independent Set ↔ Vertex Cover ↔ Set Cover (approximation).

### SAT Solving
- **DPLL**: unit propagation + branching + backtracking.

## Game Theory (Algorithmic)

### Nash Equilibrium
- Pure NE: best-response profile.
- Mixed NE: 2x2 via indifference equations.
- **Minimax theorem**: zero-sum games have value; solved by LP.

### Auctions
- **Vickrey (second-price)**: truthful, efficient.
- **VCG**: generalizes Vickrey; payment = externality.

### Price of Anarchy
- **Pigou**: NE cost / OPT cost = 4/3 (with linear cost).
- **Braess paradox**: adding an edge can worsen equilibrium.

### Mechanism Design
- Truthful mechanisms, VCG, revenue equivalence.

## Math (from ML README_MATH)

### 18. Roughgarden-style Algorithms
Divide & Conquer: merge sort, inversion count, closest pair. Greedy: Kruskal MST, Huffman, weighted interval scheduling. DP: 0/1 knapsack, edit distance. Shortest paths: Dijkstra, Bellman-Ford. Max flow: Edmonds-Karp.

### 19. Complexity Theory
P vs NP, NP-completeness, reductions (3-SAT -> Independent Set). DPLL SAT solver.

### 20. Algorithmic Game Theory
Pure/mixed Nash, minimax, Vickrey/VCG auctions, price of anarchy (Pigou 4/3).
