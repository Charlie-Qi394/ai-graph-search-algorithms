"""BFS, DFS, Greedy Best-First Search and A* implementations."""

from __future__ import annotations

from collections import deque
from heapq import heappop, heappush
from itertools import count
from typing import Callable, Literal

from graph_search.models import Graph, SearchResult

Heuristic = Callable[[str], float]
Strategy = Literal["bfs", "dfs", "greedy", "astar"]


def _validate_nodes(graph: Graph, start: str, goal: str) -> None:
    if not graph.has_node(start):
        raise ValueError(f"unknown start node: {start}")
    if not graph.has_node(goal):
        raise ValueError(f"unknown goal node: {goal}")


def breadth_first_search(graph: Graph, start: str, goal: str) -> SearchResult | None:
    """Find a path with the fewest edges."""
    _validate_nodes(graph, start, goal)
    frontier = deque([(start, (start,))])
    visited: set[str] = set()
    expanded = 0

    while frontier:
        node, path = frontier.popleft()
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return SearchResult(path=path, cost=graph.path_cost(path), expanded=expanded)
        for neighbor, _ in graph.neighbors(node):
            if neighbor not in visited:
                frontier.append((neighbor, path + (neighbor,)))
    return None


def depth_first_search(graph: Graph, start: str, goal: str) -> SearchResult | None:
    """Find a depth-first path."""
    _validate_nodes(graph, start, goal)
    frontier = [(start, (start,))]
    visited: set[str] = set()
    expanded = 0

    while frontier:
        node, path = frontier.pop()
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return SearchResult(path=path, cost=graph.path_cost(path), expanded=expanded)
        for neighbor, _ in reversed(graph.neighbors(node)):
            if neighbor not in visited:
                frontier.append((neighbor, path + (neighbor,)))
    return None


def greedy_best_first_search(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Heuristic,
) -> SearchResult | None:
    """Find a path by expanding the lowest heuristic estimate first."""
    _validate_nodes(graph, start, goal)
    sequence = count()
    frontier = [(heuristic(start), next(sequence), start, (start,))]
    visited: set[str] = set()
    expanded = 0

    while frontier:
        _, _, node, path = heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        expanded += 1
        if node == goal:
            return SearchResult(path=path, cost=graph.path_cost(path), expanded=expanded)
        for neighbor, _ in graph.neighbors(node):
            if neighbor not in visited:
                heappush(frontier, (heuristic(neighbor), next(sequence), neighbor, path + (neighbor,)))
    return None


def a_star_search(
    graph: Graph,
    start: str,
    goal: str,
    heuristic: Heuristic,
) -> SearchResult | None:
    """Find the lowest-cost path using f(n) = g(n) + h(n)."""
    _validate_nodes(graph, start, goal)
    sequence = count()
    frontier = [(heuristic(start), next(sequence), 0.0, start, (start,))]
    best_cost: dict[str, float] = {start: 0.0}
    expanded = 0

    while frontier:
        _, _, cost_so_far, node, path = heappop(frontier)
        if cost_so_far > best_cost.get(node, float("inf")):
            continue
        expanded += 1
        if node == goal:
            return SearchResult(path=path, cost=cost_so_far, expanded=expanded)
        for neighbor, edge_cost in graph.neighbors(node):
            candidate_cost = cost_so_far + edge_cost
            if candidate_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = candidate_cost
                priority = candidate_cost + heuristic(neighbor)
                heappush(frontier, (priority, next(sequence), candidate_cost, neighbor, path + (neighbor,)))
    return None


def search(
    graph: Graph,
    start: str,
    goal: str,
    strategy: Strategy,
    heuristic: Heuristic | None = None,
) -> SearchResult | None:
    """Dispatch to one of the supported graph search algorithms."""
    if strategy == "bfs":
        return breadth_first_search(graph, start, goal)
    if strategy == "dfs":
        return depth_first_search(graph, start, goal)
    if strategy == "greedy":
        if heuristic is None:
            raise ValueError("greedy search requires a heuristic")
        return greedy_best_first_search(graph, start, goal, heuristic)
    if strategy == "astar":
        if heuristic is None:
            raise ValueError("A* search requires a heuristic")
        return a_star_search(graph, start, goal, heuristic)
    raise ValueError(f"unknown search strategy: {strategy}")
