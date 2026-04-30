"""Command-line interface for graph search examples."""

from __future__ import annotations

import argparse
import sys

from graph_search.algorithms import Strategy, search
from graph_search.csv_io import heuristic_for_goal, load_adjacency_matrix, load_heuristic_matrix


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run graph search over CSV adjacency matrices.")
    parser.add_argument("graph_csv", help="Path to graph adjacency matrix CSV.")
    parser.add_argument("heuristic_csv", help="Path to heuristic matrix CSV.")
    parser.add_argument("start", help="Start node label.")
    parser.add_argument("goal", help="Goal node label.")
    parser.add_argument(
        "--strategy",
        choices=["bfs", "dfs", "greedy", "astar"],
        default="astar",
        help="Search strategy to run.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        graph = load_adjacency_matrix(args.graph_csv)
        heuristics = load_heuristic_matrix(args.heuristic_csv)
        heuristic = heuristic_for_goal(heuristics, args.goal)
        result = search(graph, args.start, args.goal, args.strategy, heuristic)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if result is None:
        print("no path")
        return 1

    print(" ".join(result.path))
    print(f"cost: {result.cost:g}")
    print(f"expanded: {result.expanded}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
