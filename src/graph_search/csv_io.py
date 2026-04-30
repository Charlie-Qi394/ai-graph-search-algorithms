"""CSV parsing helpers for graph search examples."""

from __future__ import annotations

import csv
from pathlib import Path

from graph_search.models import Graph


def load_adjacency_matrix(path: str | Path, labels: list[str] | None = None) -> Graph:
    """Load a weighted graph from a CSV adjacency matrix."""
    rows = _read_csv(path)
    if not rows:
        raise ValueError("graph CSV is empty")
    width = len(rows)
    if any(len(row) != width for row in rows):
        raise ValueError("graph CSV must be a square matrix")

    node_labels = labels or [str(index + 1) for index in range(width)]
    if len(node_labels) != width:
        raise ValueError("label count must match graph size")

    adjacency: dict[str, dict[str, float]] = {label: {} for label in node_labels}
    for row_index, row in enumerate(rows):
        source = node_labels[row_index]
        for col_index, value in enumerate(row):
            if value == "":
                continue
            adjacency[source][node_labels[col_index]] = float(value)
    return Graph(adjacency)


def load_heuristic_matrix(path: str | Path, labels: list[str] | None = None) -> dict[str, dict[str, float]]:
    """Load a heuristic matrix keyed as heuristics[node][goal]."""
    rows = _read_csv(path)
    if not rows:
        raise ValueError("heuristic CSV is empty")
    width = len(rows)
    if any(len(row) != width for row in rows):
        raise ValueError("heuristic CSV must be a square matrix")

    node_labels = labels or [str(index + 1) for index in range(width)]
    if len(node_labels) != width:
        raise ValueError("label count must match heuristic size")

    matrix: dict[str, dict[str, float]] = {}
    for row_index, row in enumerate(rows):
        source = node_labels[row_index]
        matrix[source] = {}
        for col_index, value in enumerate(row):
            matrix[source][node_labels[col_index]] = float(value or 0)
    return matrix


def heuristic_for_goal(matrix: dict[str, dict[str, float]], goal: str):
    """Create a heuristic function for a selected goal node."""
    if goal not in next(iter(matrix.values())):
        raise ValueError(f"unknown heuristic goal: {goal}")

    def heuristic(node: str) -> float:
        try:
            return matrix[node][goal]
        except KeyError as exc:
            raise ValueError(f"missing heuristic for node {node!r} and goal {goal!r}") from exc

    return heuristic


def _read_csv(path: str | Path) -> list[list[str]]:
    with Path(path).open(newline="", encoding="utf-8-sig") as handle:
        return [[cell.strip() for cell in row] for row in csv.reader(handle)]
