"""Depth-first search maze generation.

Classes:
    MazeGenDFS: Randomized depth-first search (recursive backtracker).
"""

from collections import deque
from random import choice
from typing import Generator

from ._maze import Maze
from ._cell import Cell

from core import Dir, OppDir, Step


class MazeGenDFS:
    """Carves a maze with an iterative randomized DFS (backtracker).

    Attributes:
        maze: Maze whose walls get carved in place.
        start: (x, y) the carving starts from.
        visited: Coordinates already carved or reserved (e.g. the logo).
    """

    def __init__(self, maze: Maze) -> None:
        """Prepare a generator that carves `maze` from the top-left cell.

        Args:
            maze: Maze whose walls get carved in place.
        """
        self.maze = maze
        self.start = (0, 0)
        self.visited: set[tuple[int, int]] = set()

    def import_logoset(self, logoset: set[tuple[int, int]]) -> None:
        """Add logo cells to the visited set so the DFS never carves them.

        Args:
            logoset: (x, y) coordinates of the logo cells.
        """
        self.visited.update(logoset)

    def gen(self) -> Generator[Cell, None, int]:
        """Carve the maze lazily, one step per iteration.

        Yields:
            The cell the DFS is currently on, after each move or backtrack.

        Returns:
            Number of operations (moves + backtracks), as
            `StopIteration.value`.
        """
        stack: deque[tuple[int, int]] = deque()
        op_count = 0
        stack.append(self.start)
        next_step = ""
        x, y = self.start
        yield self.maze.grid[y][x]
        while stack:
            x, y = stack[0]
            self.visited.add((x, y))
            possible_step = self.gen_possible_step(x, y)
            if not possible_step:
                stack.popleft()
                op_count += 1
                if stack:
                    x, y = stack[0]
                yield self.maze.grid[y][x]
                continue
            next_step = choice(possible_step)
            dx, dy = Step[next_step].value
            nx, ny = x + dx, y + dy
            stack.appendleft((nx, ny))
            self.maze.grid[y][x].wall -= Dir[next_step].value
            self.maze.grid[ny][nx].wall -= Dir[OppDir[next_step].value].value
            op_count += 1
            yield self.maze.grid[ny][nx]
        return op_count

    def gen_possible_step(self, x: int, y: int) -> list[str]:
        """Look for unvisited neighbours while taking care of the borders.

        Args:
            x: Column of the current cell.
            y: Row of the current cell.

        Returns:
            Direction names ("N", "S", "W", "E") the DFS can move to.
        """
        ret: list[str] = []
        if (y != 0 and
                (x, y - 1) not in self.visited):
            ret.append("N")
        if (y != self.maze.y_max and
                (x, y + 1) not in self.visited):
            ret.append("S")
        if (x != 0 and
                (x - 1, y) not in self.visited):
            ret.append("W")
        if (x != self.maze.x_max and
                (x + 1, y) not in self.visited):
            ret.append("E")
        return ret
