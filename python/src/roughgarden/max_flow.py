import heapq
from collections import defaultdict, deque

def max_flow(capacity, s, t):
    """capacity: dict (u,v)->cap. Returns max flow."""
    from collections import defaultdict, deque
    # build residual
    cap = defaultdict(lambda: defaultdict(float))
    for (u, v), c in capacity.items():
        cap[u][v] += c
        if cap[v][u] is None:
            cap[v][u] = 0.0  # ensure key
    # adjacency
    nodes = set()
    for (u, v) in capacity:
        nodes.add(u); nodes.add(v)
    adj = defaultdict(set)
    for (u, v) in capacity:
        adj[u].add(v); adj[v].add(u)

    flow = 0.0
    while True:
        # BFS
        parent = {s: None}
        q = deque([s])
        found = False
        while q:
            u = q.popleft()
            if u == t:
                found = True
                break
            for v in adj[u]:
                if v not in parent and cap[u][v] > 1e-9:
                    parent[v] = u
                    q.append(v)
        if not found:
            break
        # bottleneck
        aug = float("inf")
        v = t
        while parent[v] is not None:
            u = parent[v]
            aug = min(aug, cap[u][v])
            v = u
        v = t
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= aug
            cap[v][u] += aug
            v = u
        flow += aug
    return flow

