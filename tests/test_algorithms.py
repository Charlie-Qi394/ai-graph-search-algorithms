from graph_search.algorithms import (
    a_star_search,
    breadth_first_search,
    depth_first_search,
    greedy_best_first_search,
)
from graph_search.models import Graph


def sample_graph() -> Graph:
    return Graph(
        {
            "A": {"B": 1, "C": 4},
            "B": {"D": 2, "E": 8},
            "C": {"D": 1},
            "D": {"E": 3},
            "E": {},
            "Z": {},
        }
    )


def test_bfs_finds_fewest_edges():
    result = breadth_first_search(sample_graph(), "A", "E")

    assert result is not None
    assert result.path == ("A", "B", "E")
    assert result.cost == 9


def test_dfs_returns_a_valid_path():
    graph = sample_graph()
    result = depth_first_search(graph, "A", "E")

    assert result is not None
    assert result.path[0] == "A"
    assert result.path[-1] == "E"
    assert graph.path_cost(result.path) == result.cost


def test_a_star_finds_lowest_cost_path():
    graph = sample_graph()
    heuristic = {"A": 4, "B": 4, "C": 2, "D": 1, "E": 0, "Z": 99}.__getitem__

    result = a_star_search(graph, "A", "E", heuristic)

    assert result is not None
    assert result.path == ("A", "B", "D", "E")
    assert result.cost == 6


def test_greedy_uses_heuristic_priority():
    graph = sample_graph()
    heuristic = {"A": 4, "B": 1, "C": 5, "D": 2, "E": 0, "Z": 99}.__getitem__

    result = greedy_best_first_search(graph, "A", "E", heuristic)

    assert result is not None
    assert result.path == ("A", "B", "E")


def test_unreachable_goal_returns_none():
    assert breadth_first_search(sample_graph(), "A", "Z") is None
