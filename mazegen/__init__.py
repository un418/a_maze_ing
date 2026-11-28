"""A standalone library to generate and solve mazes."""

from ._maze_generator import MazeGenerator
from .generator import MazeLogoError
from .solver import SolverError

__all__ = ["MazeGenerator", "MazeLogoError", "SolverError"]
