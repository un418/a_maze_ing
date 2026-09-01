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

    def pregen_maze(self) -> None:
        """"define constraint before generating maze"""
        # TODO: add logo logic
        for y in range(self.height):
            for x in range(self.width):
                border = False
                logo = False
                # border
                if (y == 0 or
                        x == 0 or
                        y == self.y_max or
                        x == self.x_max):
                    border = True
                self.grid[y][x] = Cell(x, y, border=border, logo=logo)
