# AI Graph Search Algorithms

## Overview
This repository implements core graph search algorithms used in introductory artificial intelligence:

- Breadth-First Search
- Depth-First Search
- Greedy Best-First Search
- A* Search

The project is a sanitized portfolio version of algorithmic AI coursework. It is written as a small reusable Python package with a command-line interface, CSV examples and automated tests.

## What It Demonstrates
- Graph parsing from CSV adjacency matrices.
- Heuristic parsing from CSV matrices.
- Uninformed search versus heuristic-guided search.
- A* path-cost optimization.
- CLI design, validation and pytest coverage.

## Algorithms
Breadth-First Search explores by depth and is useful for finding the shortest path by edge count in unweighted graphs.

Depth-First Search follows one branch deeply before backtracking. It is memory-light but does not guarantee an optimal path.

Greedy Best-First Search expands nodes with the lowest heuristic estimate to the goal. It can be fast, but it does not guarantee the lowest-cost path.

A* Search uses `f(n) = g(n) + h(n)`, where `g(n)` is the path cost so far and `h(n)` is the heuristic estimate. With an admissible heuristic, A* returns an optimal lowest-cost path.

## How To Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
pytest
```

Run the CLI:
```bash
python -m graph_search.cli examples/graph.csv examples/h_zero.csv 1 6 --strategy astar
python -m graph_search.cli examples/graph.csv examples/h_sld.csv 1 6 --strategy greedy
```

Example output:
```text
1 3 5 6
cost: 33
```

## CSV Format
The graph CSV is an adjacency matrix. Empty cells mean no edge.

```csv
,10,7,,,
10,,11,9,,
7,11,,11,15,
,9,11,,5,16
,,15,5,,11
,,,16,11,
```

The heuristic CSV is a matrix where row `i`, column `j` gives a heuristic estimate from node `i` to goal node `j`.

Node labels in the CLI are 1-based to make CSV examples easier to read. The Python package uses the labels exactly as loaded.

## Repository Structure
```text
ai-graph-search-algorithms/
  README.md
  academic-integrity.md
  pyproject.toml
  examples/
    graph.csv
    h_sld.csv
    h_zero.csv
  src/
    graph_search/
      algorithms.py
      cli.py
      csv_io.py
      models.py
  tests/
```

## Academic Integrity
This repository excludes assignment briefs, answer sheets, submitted documents, student identifiers and course-specific wording. It is reconstructed as a general-purpose portfolio project.
