import heapq
from collections import defaultdict, deque

def merge_sort(arr):
    arr = list(arr)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)



def _merge(a, b):
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
    out.extend(a[i:]); out.extend(b[j:])
    return out



def count_inversions(arr):
    return _count_inversions(arr)[1]



def _count_inversions(arr):
    arr = list(arr)
    if len(arr) <= 1:
        return arr, 0
    mid = len(arr) // 2
    left, invL = _count_inversions(arr[:mid])
    right, invR = _count_inversions(arr[mid:])
    merged, invSplit = _merge_count(left, right)
    return merged, invL + invR + invSplit



def _merge_count(a, b):
    out = []
    i = j = 0
    inv = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i]); i += 1
        else:
            out.append(b[j]); j += 1
            inv += len(a) - i
    out.extend(a[i:]); out.extend(b[j:])
    return out, inv



def closest_pair(points):
    """Divide & conquer closest pair of points (2D)."""
    pts = sorted(points, key=lambda p: p[0])
    return _closest(pts)



def _closest(pts):
    n = len(pts)
    if n <= 3:
        best = float("inf")
        pair = None
        for i in range(n):
            for j in range(i+1, n):
                d = _dist(pts[i], pts[j])
                if d < best:
                    best = d; pair = (pts[i], pts[j])
        return best, pair
    mid = n // 2
    midx = pts[mid][0]
    dl, pl = _closest(pts[:mid])
    dr, pr = _closest(pts[mid:])
    d = min(dl, dr)
    best_pair = pl if dl <= dr else pr
    # strip
    strip = [p for p in pts if abs(p[0]-midx) < d]
    strip.sort(key=lambda p: p[1])
    for i in range(len(strip)):
        for j in range(i+1, min(i+8, len(strip))):
            dd = _dist(strip[i], strip[j])
            if dd < d:
                d = dd; best_pair = (strip[i], strip[j])
    return d, best_pair


# ---------- Greedy ----------


def _dist(a, b):
    return ((a[0]-b[0])**2 + (a[1]-b[1])**2) ** 0.5



