# Roughgarden: Algorithms, Complexity, and Game Theory

This folder collects Tim Roughgarden-style material (algorithms, complexity
theory, algorithmic game theory) that is **not** part of "ML from scratch"
but is useful foundational CS.

## Layout

```
roughgarden/
├── python/   # Python implementations + tests + notes
│   ├── src/roughgarden/   # algorithms, complexity, game_theory modules
│   ├── tests/
│   └── docs/roughgarden_notes.md
└── go/       # Go port
    └── roughgarden/
```

## Python

```bash
cd roughgarden/python
PYTHONPATH=. python -m pytest -q
```

Modules:
- `algorithms.py`: divide & conquer (merge sort, inversions, closest pair),
  greedy (Kruskal MST, Huffman, weighted interval scheduling), DP (knapsack,
  edit distance), shortest paths (Dijkstra, Bellman-Ford), max flow (Edmonds-Karp).
- `complexity.py`: DPLL SAT solver, independent-set reduction.
- `game_theory.py`: pure/mixed Nash, Vickrey auction, Pigou price of anarchy.

## Go

```bash
cd roughgarden/go
go build ./...
```

## Notes
See `python/docs/roughgarden_notes.md` for lecture notes and math.
EOF