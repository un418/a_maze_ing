from ._cell import Cell


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.x_max = width - 1
        self.y_max = height - 1
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)]

    def pregen(self) -> None:
        """define constraint before generating maze"""
        self.grid = [
            [Cell(x, y,
                  border=(y == 0 or x == 0 or
                          y == self.y_max or x == self.x_max))
             for x in range(self.width)]
            for y in range(self.height)]
