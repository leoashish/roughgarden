import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.roughgarden.algorithms import (merge_sort, count_inversions, closest_pair,
    mst_kruskal, knapsack_01, edit_distance, dijkstra, bellman_ford, max_flow,
    weighted_interval_scheduling)
from src.roughgarden.complexity import solve_sat
from src.roughgarden.game_theory import find_pure_nash, vickrey_auction, pigou_price_of_anarchy


def test_merge_sort():
    assert merge_sort([3,1,4,1,5,9,2,6]) == sorted([3,1,4,1,5,9,2,6])


def test_inversions():
    assert count_inversions([2,4,1,3,5]) == 3


def test_kruskal():
    edges = [(1,0,1),(2,1,2),(3,0,2)]
    mst, w = mst_kruskal(3, edges)
    assert w == 3


def test_knapsack():
    assert knapsack_01([2,3,4,5],[3,4,5,6],8) == 10


def test_edit_distance():
    assert edit_distance("kitten","sitting") == 3


def test_dijkstra():
    adj = {0:[(1,4),(2,1)],1:[(3,1)],2:[(1,2),(3,5)],3:[]}
    # convert to expected format: dict node -> list (neighbor,weight)
    adj2 = {0:[(1,4),(2,1)],1:[(3,1)],2:[(1,2),(3,5)],3:[]}
    d = dijkstra(adj2, 0)
    assert d[3] == 4


def test_bellman_ford():
    edges = [(0,1,4),(0,2,1),(2,1,2),(1,3,1),(2,3,5)]
    d = bellman_ford(edges, 4, 0)
    assert d is not None and d[3] == 4


def test_max_flow():
    cap = {(0,1):10,(0,2):10,(1,2):2,(1,3):4,(1,4):8,(2,4):9,(3,5):10,(4,5):10}
    assert max_flow(cap,0,5) == 14
    assert max_flow(cap,0,5) > 0


def test_sat():
    clauses = [[1,2],[-1,3],[ -2,-3]]
    res = solve_sat(clauses,3)
    assert res is not None


def test_nash():
    A = [[[3,3],[0,5]],[[5,0],[1,1]]]
    ne = find_pure_nash(A)
    assert (1,1) in ne


def test_vickrey():
    w,p = vickrey_auction([10,15,8])
    assert w == 1 and p == 10


def test_pigou():
    ne,opt,poa = pigou_price_of_anarchy()
    assert abs(poa-4/3) < 1e-9
