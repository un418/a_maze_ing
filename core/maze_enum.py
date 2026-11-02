"""Enums shared by the generator, the solver and the renderer."""

from enum import Enum, IntFlag, auto


class Dir(IntFlag):
    """Wall bit of each direction in a cell's 4-bit `wall` mask.

    A set bit means the wall is closed on that side.
    """
    N = 1  # 0b0001
    E = 2  # 0b0010
    S = 4  # 0b0100
    W = 8  # 0b1000
    # max (all close) = 15


class OppDir(Enum):
    """Opposite direction name, to update the neighbour's wall."""
    N = "S"
    E = "W"
    S = "N"
    W = "E"


class Step(Enum):
    """(dx, dy) offset to move one cell (y grows downward)."""
    N = (0, -1)
    E = (+1, 0)
    S = (0, +1)
    W = (-1, 0)


class CellState(Enum):
    """Solver marks on a cell, used by the renderer to colour it."""
    SOLVER_VISITED = auto()
    DEAD_END = auto()
