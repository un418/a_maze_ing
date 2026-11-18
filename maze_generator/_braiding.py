"""Open walls in a generated maze to reduce dead ends."""

from core import Dir, Step
from core.maze_enum import OppDir

from ._cell import Cell
from ._maze import Maze


class Braider:
    """Braid a generated maze by opening extra passages in place.

    Attributes:
        maze: Generated maze whose walls can be opened.
    """

    def __init__(self, maze: Maze):
        """Store the maze to braid.

        Args:
            maze: Maze to modify after generation.
        """
        self.maze = maze

    def gen_braiding(self):
        """Make one pass through the maze and try to open its dead ends.

        For each dead end outside the logo, try its closed sides until one
        opening is accepted or all candidates have been tried.
        """
        dead_ends: list[int] = [
            14,
            13,
            11,
            7,
        ]  # all 3 closed wall combos: 1110/1101/1011/0111
        grid: list[list[Cell]] = self.maze.grid

        for row in grid:
            for cell in row:
                if cell.wall in dead_ends and not cell.logo:
                    closed_sides: list[str] = self._closed_detection(cell)
                    for side in closed_sides:
                        if self._valid_open(cell, Dir[side], grid):
                            break

    @staticmethod
    def _closed_detection(cell: Cell) -> list[str]:
        """List the directions whose wall bits are set on a cell.

        Args:
            cell: Cell whose wall mask is inspected.

        Returns:
            Names of the cell's closed sides, such as ``N`` and ``E``.
        """
        closed_sides: list = []

        for direction in Dir:
            if cell.wall & direction:
                closed_sides.append(direction.name)

        return closed_sides

    def _valid_open(self, curr_cell: Cell, side: Dir, grid: list[list[Cell]]) -> bool:
        """Try to open a shared wall and keep it if the opening is valid.

        Restore both wall masks if the resulting grid has an open 3x3 square.

        Args:
            curr_cell: Cell on the starting side of the wall.
            side: Direction of the closed wall to try.
            grid: Maze grid indexed by row and column.

        Returns:
            True if the opening was kept, or False if it was rejected.

        Raises:
            IndexError: If the neighbour lookup goes beyond the grid.
        """
        offset_x, offset_y = Step[side.name].value
        neighbor_y = curr_cell.y + offset_y
        neighbor_x = curr_cell.x + offset_x
        if not (
            0 <= neighbor_y < self.maze.height and 0 <= neighbor_x < self.maze.width
        ):  # In case the neighbour is outside the maze!
            return False
        neighbor_cell: Cell = grid[neighbor_y][neighbor_x]
        if neighbor_cell.logo:
            return False
        neighbor_wall_bkp: int = neighbor_cell.wall
        curr_wall_bkp: int = curr_cell.wall
        curr_cell.wall = curr_cell.wall - side
        neighbor_cell.wall = neighbor_cell.wall - Dir[OppDir[side.name].value]
        if self._3x3_scan(grid):
            curr_cell.wall = curr_wall_bkp
            neighbor_cell.wall = neighbor_wall_bkp
            return False
        return True

    def _3x3_scan(self, grid: list[list[Cell]]):
        """Detect any 3x3 square with all 12 internal walls open.

        Args:
            grid: Maze grid indexed by row and column.

        Returns:
            True if a fully open square exists, or False otherwise.
        """
        for top in range(self.maze.height - 2):
            for left in range(self.maze.width - 2):
                open_walls = 0

                for y in range(top, top + 3):
                    for x in range(left, left + 3):
                        cell = grid[y][x]

                        if x < left + 2 and not (cell.wall & Dir.E):
                            open_walls += 1
                        if y < top + 2 and not (cell.wall & Dir.S):
                            open_walls += 1

                if open_walls == 12:
                    return True

        return False
