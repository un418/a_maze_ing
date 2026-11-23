"""Maze solvers."""

from ._bfs import BFSsolver
from ._dead_end_solver import DeadEndSolver

__all__ = [
    "DeadEndSolver",
    "BFSsolver",
]
