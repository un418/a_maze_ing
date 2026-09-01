from enum import IntFlag


class Cell:
    def __init__(self,
                 x: int,
                 y: int,
                 border: bool = False,
                 logo: bool = False
                 ) -> None:
        self.x, self.y = x, y
        self.border = border
        self.logo = logo
        self.wall: int = 0b1111


class Dir(IntFlag):
    N = 1  # 0b0001
    E = 2  # 0b0010
    S = 4  # 0b0100
    W = 8  # 0b1000
    # max (all close) = 15
