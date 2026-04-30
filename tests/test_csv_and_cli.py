from pathlib import Path

from graph_search.cli import main
from graph_search.csv_io import heuristic_for_goal, load_adjacency_matrix, load_heuristic_matrix


EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


def test_load_csv_examples_and_build_heuristic():
    graph = load_adjacency_matrix(EXAMPLES / "graph.csv")
    heuristics = load_heuristic_matrix(EXAMPLES / "h_sld.csv")
    heuristic = heuristic_for_goal(heuristics, "6")

    assert graph.path_cost(("1", "3", "5", "6")) == 33
    assert heuristic("4") == 13


def test_cli_astar_outputs_path_and_cost(capsys):
    exit_code = main(
        [
            str(EXAMPLES / "graph.csv"),
            str(EXAMPLES / "h_zero.csv"),
            "1",
            "6",
            "--strategy",
            "astar",
        ]
    )

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "1 3 5 6" in output
    assert "cost: 33" in output


def test_cli_invalid_node_returns_error(capsys):
    exit_code = main(
        [
            str(EXAMPLES / "graph.csv"),
            str(EXAMPLES / "h_zero.csv"),
            "99",
            "1",
            "--strategy",
            "bfs",
        ]
    )

    assert exit_code == 2
    assert "unknown start node" in capsys.readouterr().err
