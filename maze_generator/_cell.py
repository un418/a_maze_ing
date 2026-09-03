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
