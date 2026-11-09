package roughgarden

// FindPureNash for 2-player game given payoff matrix [a1][a2] -> [u1,u2].
func FindPureNash(payoff [][][]float64) [][2]int {
	n1 := len(payoff)
	n2 := len(payoff[0])
	var res [][2]int
	for a1 := 0; a1 < n1; a1++ {
		for a2 := 0; a2 < n2; a2++ {
			u1 := payoff[a1][a2][0]
			u2 := payoff[a1][a2][1]
			best1 := payoff[0][a2][0]
			for a1p := 1; a1p < n1; a1p++ {
				if payoff[a1p][a2][0] > best1 {
					best1 = payoff[a1p][a2][0]
				}
			}
			best2 := payoff[a1][0][1]
			for a2p := 1; a2p < n2; a2p++ {
				if payoff[a1][a2p][1] > best2 {
					best2 = payoff[a1][a2p][1]
				}
			}
			if u1 == best1 && u2 == best2 {
				res = append(res, [2]int{a1, a2})
			}
		}
	}
	return res
}

// VickreyAuction returns winner index and price.
func VickreyAuction(bids []float64) (int, float64) {
	if len(bids) == 0 {
		return -1, 0
	}
	order := make([]int, len(bids))
	for i := range order {
		order[i] = i
	}
	for i := 1; i < len(order); i++ {
		for j := i; j > 0 && bids[order[j-1]] < bids[order[j]]; j-- {
			order[j-1], order[j] = order[j], order[j-1]
		}
	}
	winner := order[0]
	price := 0.0
	if len(order) > 1 {
		price = bids[order[1]]
	}
	return winner, price
}

// PigouPoA returns NE cost, OPT cost, PoA.
func PigouPoA() (float64, float64, float64) {
	return 1.0, 0.75, 1.0 / 0.75
}
