from enum import Enum, IntFlag, auto


class Dir(IntFlag):
    N = 1  # 0b0001
    E = 2  # 0b0010
    S = 4  # 0b0100
    W = 8  # 0b1000
    # max (all close) = 15


class OppDir(Enum):
    N = "S"
    E = "W"
    S = "N"
    W = "E"


class Step(Enum):
    N = (0, -1)
    E = (+1, 0)
    S = (0, +1)
    W = (-1, 0)


class CellState(Enum):
    SOLVER_VISITED = auto()
    DEAD_END = auto()
