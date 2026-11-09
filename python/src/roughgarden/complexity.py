"""Complexity theory: SAT solving and NP-completeness reductions (Roughgarden)."""

# ---------- SAT / DPLL ----------

def solve_sat(clauses, num_vars):
    """DPLL SAT solver. clauses: list of lists of ints (positive/negative literals).
    Returns assignment list (1-based, True/False) or None."""
    # assignment: 0 unassigned, 1 True, -1 False
    assign = [0] * (num_vars + 1)

    def unit_propagate(clauses, assign):
        changed = True
        while changed:
            changed = False
            for c in clauses:
                # evaluate clause
                unassigned = []
                val = False
                for lit in c:
                    var = abs(lit)
                    if assign[var] == 0:
                        unassigned.append(lit)
                    else:
                        if (lit > 0 and assign[var] == 1) or (lit < 0 and assign[var] == -1):
                            val = True
                if val:
                    continue
                if len(unassigned) == 0:
                    return False  # conflict
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    var = abs(lit)
                    assign[var] = 1 if lit > 0 else -1
                    changed = True
        return True

    def backtrack(assign):
        # find unassigned var
        for v in range(1, num_vars + 1):
            if assign[v] == 0:
                return v
        return None

    def dpll(clauses, assign):
        if not unit_propagate(clauses, assign):
            return False
        v = backtrack(assign)
        if v is None:
            return True
        # try True
        assign[v] = 1
        if dpll(clauses, assign):
            return True
        # try False
        assign[v] = -1
        if dpll(clauses, assign):
            return True
        assign[v] = 0
        return False

    if dpll(clauses, assign):
        return [assign[v] == 1 for v in range(1, num_vars + 1)]
    return None


# ---------- Reductions ----------

def is_independent_set(graph, S):
    """graph: dict node->set neighbors. S subset nodes."""
    S = set(S)
    for u in S:
        for v in S:
            if u != v and v in graph.get(u, set()):
                return False
    return True


def reduce_3sat_to_independent_set(clauses):
    """Standard reduction: each literal becomes a node; edges between
    conflicting literals in same clause and complementary literals.
    Returns (graph, k) where k = number of clauses."""
    # Nodes: (clause_idx, literal_idx)
    nodes = []
    for ci, c in enumerate(clauses):
        for li, lit in enumerate(c):
            nodes.append((ci, li, lit))
    node_id = {n: i for i, n in enumerate(nodes)}
    graph = {i: set() for i in range(len(nodes))}
    # edges within same clause (all pairs)
    from collections import defaultdict
    by_clause = defaultdict(list)
    for n in nodes:
        by_clause[n[0]].append(n)
    for ci, ns in by_clause.items():
        for a in range(len(ns)):
            for b in range(a+1, len(ns)):
                ia, ib = node_id[ns[a]], node_id[ns[b]]
                graph[ia].add(ib); graph[ib].add(ia)
    # edges between complementary literals across clauses
    for i, n1 in enumerate(nodes):
        for j, n2 in enumerate(nodes):
            if i < j and n1[2] == -n2[2]:
                graph[i].add(j); graph[j].add(i)
    k = len(clauses)
    return graph, k, nodes


def vertex_cover_bruteforce(graph, k):
    """Brute force vertex cover of size <= k."""
    nodes = list(graph.keys())
    from itertools import combinations
    for size in range(k + 1):
        for S in combinations(nodes, size):
            Sset = set(S)
            ok = True
            for u in nodes:
                for v in graph.get(u, set()):
                    if u < v and not (u in Sset or v in Sset):
                        ok = False; break
                if not ok:
                    break
            if ok:
                return list(S)
    return None
