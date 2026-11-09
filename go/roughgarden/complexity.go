package roughgarden

// SolveSAT DPLL. clauses: [][]int, numVars int. Returns []bool or nil.
func SolveSAT(clauses [][]int, numVars int) []bool {
	assign := make([]int, numVars+1) // 0 unassigned, 1 true, -1 false

	unitPropagate := func() bool {
		changed := true
		for changed {
			changed = false
			for _, c := range clauses {
				unassigned := []int{}
				val := false
				for _, lit := range c {
					varr := lit
					if varr < 0 {
						varr = -varr
					}
					if assign[varr] == 0 {
						unassigned = append(unassigned, lit)
					} else {
						if (lit > 0 && assign[varr] == 1) || (lit < 0 && assign[varr] == -1) {
							val = true
						}
					}
				}
				if val {
					continue
				}
				if len(unassigned) == 0 {
					return false
				}
				if len(unassigned) == 1 {
					lit := unassigned[0]
					varr := lit
					if varr < 0 {
						varr = -varr
					}
					if lit > 0 {
						assign[varr] = 1
					} else {
						assign[varr] = -1
					}
					changed = true
				}
			}
		}
		return true
	}

	backtrack := func() int {
		for v := 1; v <= numVars; v++ {
			if assign[v] == 0 {
				return v
			}
		}
		return 0
	}

	var dpll func() bool
	dpll = func() bool {
		if !unitPropagate() {
			return false
		}
		v := backtrack()
		if v == 0 {
			return true
		}
		assign[v] = 1
		if dpll() {
			return true
		}
		assign[v] = -1
		if dpll() {
			return true
		}
		assign[v] = 0
		return false
	}

	if !dpll() {
		return nil
	}
	out := make([]bool, numVars)
	for v := 1; v <= numVars; v++ {
		out[v-1] = assign[v] == 1
	}
	return out
}

// IsIndependentSet checks if S is independent in graph (adjacency sets).
func IsIndependentSet(adj map[int]map[int]bool, S []int) bool {
	set := map[int]bool{}
	for _, u := range S {
		set[u] = true
	}
	for _, u := range S {
		for _, v := range S {
			if u != v && adj[u][v] {
				return false
			}
		}
	}
	return true
}
