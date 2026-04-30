"""Core graph search data models."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    """Result returned by a graph search algorithm."""

    path: tuple[str, ...]
    cost: float
    expanded: int


class Graph:
    """Directed weighted graph with deterministic neighbor ordering."""

    def __init__(self, adjacency: dict[str, dict[str, float]]) -> None:
        if not adjacency:
            raise ValueError("graph must contain at least one node")
        self._adjacency = {
            str(node): {str(neighbor): float(cost) for neighbor, cost in edges.items()}
            for node, edges in adjacency.items()
        }
        for node, edges in self._adjacency.items():
            for neighbor, cost in edges.items():
                if cost < 0:
                    raise ValueError("negative edge costs are not supported")
                self._adjacency.setdefault(neighbor, {})

    @property
    def nodes(self) -> tuple[str, ...]:
        return tuple(self._adjacency.keys())

    def has_node(self, node: str) -> bool:
        return node in self._adjacency

    def neighbors(self, node: str) -> tuple[tuple[str, float], ...]:
        if node not in self._adjacency:
            raise KeyError(f"unknown node: {node}")
        return tuple(self._adjacency[node].items())

    def path_cost(self, path: tuple[str, ...] | list[str]) -> float:
        if len(path) <= 1:
            return 0.0
        total = 0.0
        for source, target in zip(path, path[1:]):
            try:
                total += self._adjacency[source][target]
            except KeyError as exc:
                raise ValueError(f"invalid path edge: {source!r} -> {target!r}") from exc
        return total
