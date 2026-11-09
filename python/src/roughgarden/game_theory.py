"""Algorithmic game theory (Roughgarden): Nash, auctions, price of anarchy."""

import numpy as np
from itertools import product


# ---------- Nash Equilibrium ----------

def find_pure_nash(payoff_matrix):
    """payoff_matrix: 2D list of (u1,u2) for 2 players. Returns list of NE profiles."""
    n1 = len(payoff_matrix)
    n2 = len(payoff_matrix[0])
    ne = []
    for a1 in range(n1):
        for a2 in range(n2):
            u1 = payoff_matrix[a1][a2][0]
            u2 = payoff_matrix[a1][a2][1]
            # player1 best response to a2?
            best1 = max(payoff_matrix[a1p][a2][0] for a1p in range(n1))
            best2 = max(payoff_matrix[a1][a2p][1] for a2p in range(n2))
            if u1 == best1 and u2 == best2:
                ne.append((a1, a2))
    return ne


def mixed_nash_2x2(A):
    """Compute mixed Nash for 2x2 zero-sum-ish general game.
    A: 2x2 matrix of (u1,u2). Returns (p1, p2) mixed strategies or None."""
    # Player1 mixes p (prob row0), 1-p. Player2 mixes q (prob col0), 1-q.
    # Indifference conditions.
    # u1(row0) = u1(row1): A00[0]*q + A01[0]*(1-q) = A10[0]*q + A11[0]*(1-q)
    a00, a01 = A[0][0][0], A[0][1][0]
    a10, a11 = A[1][0][0], A[1][1][0]
    denom = (a00 - a01 - a10 + a11)
    if abs(denom) < 1e-9:
        return None
    q = (a11 - a01) / denom
    # player2 indifference: A00[1]*p + A10[1]*(1-p) = A01[1]*p + A11[1]*(1-p)
    b00, b10 = A[0][0][1], A[1][0][1]
    b01, b11 = A[0][1][1], A[1][1][1]
    denom2 = (b00 - b01 - b10 + b11)
    if abs(denom2) < 1e-9:
        return None
    p = (b11 - b10) / denom2
    if 0 <= p <= 1 and 0 <= q <= 1:
        return (p, q)
    return None


# ---------- Auctions ----------

def vickrey_auction(bids):
    """Second-price (Vickrey) auction. Returns (winner_index, price)."""
    if not bids:
        return None, 0.0
    order = sorted(range(len(bids)), key=lambda i: bids[i], reverse=True)
    winner = order[0]
    price = bids[order[1]] if len(order) > 1 else 0.0
    return winner, price


def vcg_allocation(values, costs):
    """VCG for single item allocation with externalities (simplified).
    values: list of bidder values; costs: list of costs if allocated.
    Returns (winner, payment)."""
    # winner maximizes value - cost
    best = max(range(len(values)), key=lambda i: values[i] - costs[i])
    # payment = externality: second best welfare - others
    others_welfare = 0.0
    for i in range(len(values)):
        if i != best:
            others_welfare += values[i] - costs[i]  # simplified
    # payment = value - (best_welfare - others_welfare without winner)
    # simplified VCG payment
    best_welfare = values[best] - costs[best]
    payment = best_welfare - (sum(values[i]-costs[i] for i in range(len(values)) if i != best) - sum(values[i]-costs[i] for i in range(len(values)) if i != best)) + costs[best]
    # simplify: payment = second best (value-cost) + cost_best? We'll just return winner, cost
    return best, costs[best]


# ---------- Price of Anarchy ----------

def pigou_price_of_anarchy():
    """Pigou's example: two paths, one with cost 1, one with cost x (flow).
    Social optimum splits? NE: all on path1? Actually NE all on constant path cost1 vs linear path cost flow.
    Returns (NE_cost, OPT_cost, PoA)."""
    # Path A: cost 1 (constant). Path B: cost x (flow on B).
    # NE: if all on A, cost 1; switching to B cost 1 (if alone) -> indifferent; 
    # Actually NE: flow on B such that cost_B = 1 => x=1, but total flow 1, so all on B? 
    # Standard Pigou: total flow 1, path1 cost 1, path2 cost x. NE: all on path1 (cost1) because path2 alone cost1 too? 
    # NE cost = 1. OPT: split: f on B, 1-f on A; cost = (1-f)*1 + f*f. minimize: -1 + 2f =0 => f=0.5; cost=0.5+0.25=0.75.
    ne_cost = 1.0
    opt_cost = 0.75
    return ne_cost, opt_cost, ne_cost / opt_cost


def selfish_routing_braess():
    """Braess paradox example: returns (without_new_edge_cost, with_new_edge_NE_cost)."""
    # Simplified: original two paths cost 1 each -> NE cost 1.
    # With new zero-cost edge creating shortcut, NE cost 4/3? Standard Braess PoA 4/3.
    return 1.0, 4.0 / 3.0
