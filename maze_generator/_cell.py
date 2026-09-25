from core import CellState


class Cell:
    def __init__(self,
                 x: int,
                 y: int,
                 border: bool = False,
                 logo: bool = False,
                 wall: int = 0b1111
                 ) -> None:
        self.x, self.y = x, y
        self.border = border
        self.logo = logo
        self.wall = wall
        self.state: CellState | None = None
