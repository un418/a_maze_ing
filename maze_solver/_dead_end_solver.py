"""Maze solving by dead-end filling.

Classes:
    DeadEndSolver: Seals dead ends until only the path is left.
"""

from copy import deepcopy
from typing import Generator

from maze_generator import Maze, Cell
from core import Dir, OppDir, Step, CellState


class DeadEndSolver:
    """Solves a maze by sealing dead ends until only the path is left.

    Works on a deep copy, so several solvers can share one maze.

    Attributes:
        origin: Maze given to the solver.
        maze: Working copy that gets sealed.
        start: (x, y) of the entry.
        end: (x, y) of the exit.
        visited: Coordinates already walked by `solve`.
        solution: Path from `start` to `end`, filled by `solve`.
    """

    def __init__(self, maze: Maze) -> None:
        """Copy `maze` and set the start and end points.

        Args:
            maze: Generated maze to solve.
        """
        self.origin = maze
        self.maze = deepcopy(maze)
        self.start = (0, 0)
        self.end = (self.maze.x_max, self.maze.y_max)  # TODO change later
        self.visited: set[tuple[int, int]] = set()
        self.solution: list[tuple[int, int]] = []

    def find_dead_end(self) -> list[tuple[int, int]]:
        """Dead ends of this pass: one opening left, start and end apart.

        Returns:
            (x, y) coordinates of every current dead end.
        """
        keep_out = {self.start, self.end}
        return [(cell.x, cell.y)
                for row in self.maze.grid
                for cell in row
                if cell.wall.bit_count() == 3
                and (cell.x, cell.y) not in keep_out]

    def opening(self, cell: Cell) -> str:
        """The single direction a dead end is still open on.

        Args:
            cell: Dead end to inspect.

        Returns:
            Name of the open direction ("N", "E", "S" or "W").

        Raises:
            Exception: If the cell has no opening left.
        """
        for step in Step:
            if not cell.wall & Dir[step.name]:
                return step.name
        raise Exception(f"Solver opening error: ({cell.x},{cell.y}) is sealed")

    def fill_cell(self, x: int, y: int) -> Generator[Cell, None, int]:
        """Seal a single dead end and stop, next pass takes its neighbour.

        Args:
            x: Column of the cell.
            y: Row of the cell.

        Yields:
            The cell, once marked DEAD_END, then once sealed.

        Returns:
            1 if the cell was sealed, 0 otherwise.
        """
        if (x, y) in {self.start, self.end}:
            return 0
        cell = self.maze.grid[y][x]
        if cell.wall.bit_count() != 3:
            # not a dead end (any more): a branch, or already sealed
            return 0
        cell.state = CellState.DEAD_END
        yield cell
        step = self.opening(cell)
        dx, dy = Step[step].value
        nx, ny = x + dx, y + dy
        cell.wall |= Dir[step].value
        cell.state = CellState.SOLVER_VISITED
        yield cell
        if (0 <= nx <= self.maze.x_max and
                0 <= ny <= self.maze.y_max):
            self.maze.grid[ny][nx].wall |= Dir[OppDir[step].value].value
        return 1

    def fill_dead_end(self) -> Generator[Cell, None, int]:
        """Wall up every dead end, pass after pass, until none is left.

        Yields:
            Each cell as `fill_cell` updates it.

        Returns:
            Number of cells sealed.
        """
        op_count = 0
        while True:
            dead_end = self.find_dead_end()
            if not dead_end:
                return op_count
            for x, y in dead_end:
                op_count += yield from self.fill_cell(x, y)

    def solve(self) -> Generator[Cell, None, None]:
        """Walk the only path left from `start` to `end`.

        Meant to run after `fill_dead_end`. Records the path in `solution`.

        Yields:
            Each cell reached along the path.
        """
        x, y = self.start
        while True:
            next_step = self.walk(x, y)
            dx, dy = Step[next_step].value
            nx, ny = x + dx, y + dy
            self.visited.add((x, y))
            self.solution.append((x, y))
            x, y = nx, ny
            yield self.maze.grid[y][x]
            if (x, y) == self.end:
                return

    def walk(self, x: int, y: int) -> str:
        """Pick the next step through the maze from (x, y).

        Args:
            x: Column of the current cell.
            y: Row of the current cell.

        Returns:
            Name of the only open, unvisited direction.

        Raises:
            Exception: If more than one direction is open.
        """
        ret = ""
        counter = 0
        wall = self.maze.grid[y][x].wall
        if (y != 0 and
                (x, y - 1) not in self.visited and
                not wall & Dir.N):
            ret = "N"
            counter += 1
        if (y != self.maze.y_max and
                (x, y + 1) not in self.visited and
                not wall & Dir.S):
            ret = "S"
            counter += 1
        if (x != 0 and
                (x - 1, y) not in self.visited and
                not wall & Dir.W):
            ret = "W"
            counter += 1
        if (x != self.maze.x_max and
                (x + 1, y) not in self.visited and
                not wall & Dir.E):
            ret = "E"
            counter += 1
        if counter > 1:
            raise Exception("Solver walk error: should not happen")
        return ret
