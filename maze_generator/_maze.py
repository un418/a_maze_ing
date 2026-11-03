"""Maze grid container."""

from ._cell import Cell


class Maze:
    """Grid of cells indexed as `grid[y][x]`.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        x_max: Index of the last column.
        y_max: Index of the last row.
        grid: Rows of fully closed cells.
    """

    def __init__(self, width: int, height: int) -> None:
        """Build a `width` x `height` grid of fully closed cells.

        Args:
            width: Number of columns.
            height: Number of rows.
        """
        self.width = width
        self.height = height
        self.x_max = width - 1
        self.y_max = height - 1
        self.grid: list[list[Cell]] = [
            [Cell(x, y) for x in range(self.width)]
            for y in range(self.height)]

    def pregen(self) -> None:
        """Define constraints before generating the maze.

        Rebuilds the grid with the outer cells flagged as `border`.
        """
        # TODO (#9) Probably useless now, check later
        self.grid = [
            [Cell(x, y,
                  border=(y == 0 or x == 0 or
                          y == self.y_max or x == self.x_max))
             for x in range(self.width)]
            for y in range(self.height)]
