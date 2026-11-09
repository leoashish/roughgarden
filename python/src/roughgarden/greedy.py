import heapq
from collections import defaultdict, deque

def mst_kruskal(n, edges):
    """Kruskal MST. edges: (w,u,v)."""
    edges = sorted(edges)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
        return True

    mst = []
    total = 0
    for w, u, v in edges:
        if union(u, v):
            mst.append((w, u, v))
            total += w
            if len(mst) == n - 1:
                break
    return mst, total



def huffman(freqs):
    """Huffman coding. freqs: dict symbol->freq. Returns (code dict, total cost)."""
    import heapq as hq
    heap = []
    for sym, f in freqs.items():
        hq.heappush(heap, (f, [sym]))
    # We'll track merges; simpler: standard
    heap = [(f, [sym]) for sym, f in freqs.items()]
    hq.heapify(heap)
    # store tree as merges
    # Build codes via repeated merge
    # We'll just compute cost
    if len(heap) == 1:
        return {heap[0][1][0]: "0"}, heap[0][0]
    # merge
    nodes = list(heap)
    # Use algorithm: combine two smallest
    hq.heapify(nodes)
    cost = 0
    # We need codebook; do standard
    # Reimplement with tree
    class Node:
        __slots__ = ("freq", "syms", "left", "right", "sym")
    # easier: use dict of codes via priority of lists
    # Standard:
    pq = [(f, [sym]) for sym, f in freqs.items()]
    hq.heapify(pq)
    # We'll build a merge tree stored as nested tuples
    while len(pq) > 1:
        f1, s1 = hq.heappop(pq)
        f2, s2 = hq.heappop(pq)
        hq.heappush(pq, (f1+f2, [s1, s2]))
        cost += f1 + f2
    # codes: traverse
    codes = {}

    def traverse(node, prefix):
        if isinstance(node, str) or (not isinstance(node, list)):
            # leaf symbol
            codes[node] = prefix if prefix else "0"
            return
        # node is list [left, right] maybe
        if len(node) == 2 and not isinstance(node[0], list) and not isinstance(node[1], list):
            # two symbols
            codes[node[0]] = prefix + "0"
            codes[node[1]] = prefix + "1"
            return
        # general
        if isinstance(node[0], list):
            traverse(node[0], prefix + "0")
        else:
            codes[node[0]] = prefix + "0"
        if isinstance(node[1], list):
            traverse(node[1], prefix + "1")
        else:
            codes[node[1]] = prefix + "1"

    root = pq[0][1]
    if isinstance(root, list) and len(root) == 2:
        traverse(root, "")
    else:
        codes[root[0] if isinstance(root, list) else root] = "0"
    return codes, cost



def weighted_interval_scheduling(jobs):
    """jobs: list of (start, finish, weight). Returns max weight subset non-overlapping."""
    jobs = sorted(jobs, key=lambda j: j[1])
    n = len(jobs)
    # p(i) = largest j < i with finish_j <= start_i
    p = [-1] * n
    for i in range(n):
        for j in range(i-1, -1, -1):
            if jobs[j][1] <= jobs[i][0]:
                p[i] = j
                break
    # DP
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        wi = jobs[i-1][2]
        pi = p[i-1]
        incl = wi + (dp[pi+1] if pi >= 0 else 0)
        excl = dp[i-1]
        dp[i] = max(incl, excl)
    return dp[n]


# ---------- Dynamic Programming ----------


