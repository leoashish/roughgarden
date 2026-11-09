package roughgarden

import (
	"container/heap"
	"math"
	"sort"

	"mlfromscratch/mat"
)

// ---------- Divide & Conquer ----------

func MergeSort(arr []int) []int {
	if len(arr) <= 1 {
		return append([]int(nil), arr...)
	}
	mid := len(arr) / 2
	left := MergeSort(arr[:mid])
	right := MergeSort(arr[mid:])
	return merge(left, right)
}

func merge(a, b []int) []int {
	out := make([]int, 0, len(a)+len(b))
	i, j := 0, 0
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] {
			out = append(out, a[i]); i++
		} else {
			out = append(out, b[j]); j++
		}
	}
	out = append(out, a[i:]...)
	out = append(out, b[j:]...)
	return out
}

func CountInversions(arr []int) int {
	_, inv := countInv(arr)
	return inv
}

func countInv(arr []int) ([]int, int) {
	if len(arr) <= 1 {
		return append([]int(nil), arr...), 0
	}
	mid := len(arr) / 2
	left, invL := countInv(arr[:mid])
	right, invR := countInv(arr[mid:])
	merged, invSplit := mergeCount(left, right)
	return merged, invL + invR + invSplit
}

func mergeCount(a, b []int) ([]int, int) {
	out := make([]int, 0, len(a)+len(b))
	i, j, inv := 0, 0, 0
	for i < len(a) && j < len(b) {
		if a[i] <= b[j] {
			out = append(out, a[i]); i++
		} else {
			out = append(out, b[j]); j++
			inv += len(a) - i
		}
	}
	out = append(out, a[i:]...)
	out = append(out, b[j:]...)
	return out, inv
}

type Point struct{ X, Y float64 }

func dist(a, b Point) float64 {
	return math.Hypot(a.X-b.X, a.Y-b.Y)
}

func ClosestPair(pts []Point) (float64, [2]Point) {
	sorted := append([]Point(nil), pts...)
	sort.Slice(sorted, func(i, j int) bool { return sorted[i].X < sorted[j].X })
	return closestRec(sorted)
}

func closestRec(pts []Point) (float64, [2]Point) {
	n := len(pts)
	if n <= 3 {
		best := math.Inf(1)
		var pair [2]Point
		for i := 0; i < n; i++ {
			for j := i + 1; j < n; j++ {
				d := dist(pts[i], pts[j])
				if d < best {
					best = d
					pair = [2]Point{pts[i], pts[j]}
				}
			}
		}
		return best, pair
	}
	mid := n / 2
	midx := pts[mid].X
	dl, pl := closestRec(pts[:mid])
	dr, pr := closestRec(pts[mid:])
	var d float64
	var bestPair [2]Point
	if dl <= dr {
		d, bestPair = dl, pl
	} else {
		d, bestPair = dr, pr
	}
	// strip
	var strip []Point
	for _, p := range pts {
		if math.Abs(p.X-midx) < d {
			strip = append(strip, p)
		}
	}
	sort.Slice(strip, func(i, j int) bool { return strip[i].Y < strip[j].Y })
	for i := 0; i < len(strip); i++ {
		for j := i + 1; j < len(strip) && j < i+8; j++ {
			dd := dist(strip[i], strip[j])
			if dd < d {
				d = dd
				bestPair = [2]Point{strip[i], strip[j]}
			}
		}
	}
	return d, bestPair
}

// ---------- Greedy ----------

type Edge struct{ W, U, V int }

func KruskalMST(n int, edges []Edge) ([]Edge, int) {
	se := append([]Edge(nil), edges...)
	sort.Slice(se, func(i, j int) bool { return se[i].W < se[j].W })
	parent := make([]int, n)
	for i := range parent {
		parent[i] = i
	}
	var find func(int) int
	find = func(x int) int {
		for parent[x] != x {
			parent[x] = parent[parent[x]]
			x = parent[x]
		}
		return x
	}
	var mst []Edge
	total := 0
	for _, e := range se {
		ru, rv := find(e.U), find(e.V)
		if ru != rv {
			parent[ru] = rv
			mst = append(mst, e)
			total += e.W
			if len(mst) == n-1 {
				break
			}
		}
	}
	return mst, total
}

func Huffman(freqs map[string]int) (map[string]string, int) {
	type node struct {
		freq int
		syms []string
	}
	pq := &huffHeap{}
	for sym, f := range freqs {
		heap.Push(pq, node{freq: f, syms: []string{sym}})
	}
	cost := 0
	for pq.Len() > 1 {
		a := heap.Pop(pq).(node)
		b := heap.Pop(pq).(node)
		merged := node{freq: a.freq + b.freq, syms: append(append([]string{}, a.syms...), b.syms...)}
		heap.Push(pq, merged)
		cost += a.freq + b.freq
	}
	// codes
	codes := map[string]string{}
	if pq.Len() == 1 {
		n := heap.Pop(pq).(node)
		if len(n.syms) == 1 {
			codes[n.syms[0]] = "0"
		} else {
			// simple: assign 0/1 (not full tree, but cost already computed)
			for i, s := range n.syms {
				if i == 0 {
					codes[s] = "0"
				} else {
					codes[s] = "1"
				}
			}
		}
	}
	return codes, cost
}

type huffHeap []struct {
	freq int
	syms []string
}

func (h huffHeap) Len() int            { return len(h) }
func (h huffHeap) Less(i, j int) bool  { return h[i].freq < h[j].freq }
func (h huffHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *huffHeap) Push(x interface{}) { *h = append(*h, x.(struct {
	freq int
	syms []string
})) }
func (h *huffHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func WeightedIntervalScheduling(jobs [][3]int) int {
	// jobs: (start, finish, weight)
	js := append([][3]int(nil), jobs...)
	sort.Slice(js, func(i, j int) bool { return js[i][1] < js[j][1] })
	n := len(js)
	p := make([]int, n)
	for i := 0; i < n; i++ {
		p[i] = -1
		for j := i - 1; j >= 0; j-- {
			if js[j][1] <= js[i][0] {
				p[i] = j
				break
			}
		}
	}
	dp := make([]int, n+1)
	for i := 1; i <= n; i++ {
		wi := js[i-1][2]
		pi := p[i-1]
		incl := wi
		if pi >= 0 {
			incl += dp[pi+1]
		}
		excl := dp[i-1]
		if incl > excl {
			dp[i] = incl
		} else {
			dp[i] = excl
		}
	}
	return dp[n]
}

// ---------- DP ----------

func Knapsack01(weights, values []int, capacity int) int {
	n := len(weights)
	dp := make([][]int, n+1)
	for i := range dp {
		dp[i] = make([]int, capacity+1)
	}
	for i := 1; i <= n; i++ {
		for c := 0; c <= capacity; c++ {
			dp[i][c] = dp[i-1][c]
			if weights[i-1] <= c {
				v := dp[i-1][c-weights[i-1]] + values[i-1]
				if v > dp[i][c] {
					dp[i][c] = v
				}
			}
		}
	}
	return dp[n][capacity]
}

func EditDistance(a, b string) int {
	m, n := len(a), len(b)
	dp := make([][]int, m+1)
	for i := range dp {
		dp[i] = make([]int, n+1)
	}
	for i := 0; i <= m; i++ {
		dp[i][0] = i
	}
	for j := 0; j <= n; j++ {
		dp[0][j] = j
	}
	for i := 1; i <= m; i++ {
		for j := 1; j <= n; j++ {
			cost := 1
			if a[i-1] == b[j-1] {
				cost = 0
			}
			dp[i][j] = min3(dp[i-1][j]+1, dp[i][j-1]+1, dp[i-1][j-1]+cost)
		}
	}
	return dp[m][n]
}

func min3(a, b, c int) int {
	if a < b {
		if a < c {
			return a
		}
		return c
	}
	if b < c {
		return b
	}
	return c
}

// ---------- Shortest Paths ----------

func Dijkstra(adj map[int][]struct {
	To int
	W  float64
}, src int) map[int]float64 {
	dist := map[int]float64{src: 0}
	pq := &dijkHeap{}
	heap.Push(pq, dijkNode{dist: 0, node: src})
	for pq.Len() > 0 {
		cur := heap.Pop(pq).(dijkNode)
		if cur.dist > dist[cur.node] {
			continue
		}
		for _, e := range adj[cur.node] {
			nd := cur.dist + e.W
			if d, ok := dist[e.To]; !ok || nd < d {
				dist[e.To] = nd
				heap.Push(pq, dijkNode{dist: nd, node: e.To})
			}
		}
	}
	return dist
}

type dijkNode struct {
	dist float64
	node int
}

type dijkHeap []dijkNode

func (h dijkHeap) Len() int            { return len(h) }
func (h dijkHeap) Less(i, j int) bool  { return h[i].dist < h[j].dist }
func (h dijkHeap) Swap(i, j int)       { h[i], h[j] = h[j], h[i] }
func (h *dijkHeap) Push(x interface{}) { *h = append(*h, x.(dijkNode)) }
func (h *dijkHeap) Pop() interface{} {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[:n-1]
	return x
}

func BellmanFord(edges [][3]int, n, src int) ([]float64, bool) {
	INF := math.Inf(1)
	dist := make([]float64, n)
	for i := range dist {
		dist[i] = INF
	}
	dist[src] = 0
	for iter := 0; iter < n-1; iter++ {
		updated := false
		for _, e := range edges {
			u, v, w := e[0], e[1], e[2]
			if dist[u] != INF && dist[u]+float64(w) < dist[v] {
				dist[v] = dist[u] + float64(w)
				updated = true
			}
		}
		if !updated {
			break
		}
	}
	for _, e := range edges {
		u, v, w := e[0], e[1], e[2]
		if dist[u] != INF && dist[u]+float64(w) < dist[v] {
			return dist, true // negative cycle
		}
	}
	return dist, false
}

// ---------- Max Flow (Edmonds-Karp) ----------

func MaxFlow(cap map[[2]int]float64, s, t int) float64 {
	// residual
	res := map[int]map[int]float64{}
	adj := map[int]map[int]bool{}
	addNode := func(u int) {
		if res[u] == nil {
			res[u] = map[int]float64{}
		}
		if adj[u] == nil {
			adj[u] = map[int]bool{}
		}
	}
	for uv, c := range cap {
		u, v := uv[0], uv[1]
		addNode(u); addNode(v)
		res[u][v] += c
		if _, ok := res[v][u]; !ok {
			res[v][u] = 0
		}
		adj[u][v] = true
		adj[v][u] = true
	}
	flow := 0.0
	for {
		// BFS
		parent := map[int]int{}
		visited := map[int]bool{s: true}
		q := []int{s}
		found := false
		for len(q) > 0 {
			u := q[0]; q = q[1:]
			if u == t {
				found = true
				break
			}
			for v := range adj[u] {
				if !visited[v] && res[u][v] > 1e-9 {
					visited[v] = true
					parent[v] = u
					q = append(q, v)
				}
			}
		}
		if !found {
			break
		}
		// bottleneck
		aug := math.Inf(1)
		v := t
		for v != s {
			u := parent[v]
			if res[u][v] < aug {
				aug = res[u][v]
			}
			v = u
		}
		v = t
		for v != s {
			u := parent[v]
			res[u][v] -= aug
			res[v][u] += aug
			v = u
		}
		flow += aug
	}
	return flow
}
var _ = mat.NewMatrix
