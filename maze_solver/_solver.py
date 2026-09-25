from copy import deepcopy
from typing import Generator

from maze_generator import Maze, Cell
from core import Dir, OppDir, Step, CellState


class DeadEndSolver:
    def __init__(self, maze: Maze) -> None:
        self.origin = maze
        self.maze = deepcopy(maze)
        self.start = (0, 0)
        self.end = (self.maze.x_max, self.maze.y_max)  # TODO change later
        self.visited: set[tuple[int, int]] = set()
        self.solution: list[tuple[int, int]] = []

    def find_dead_end(self) -> list[tuple[int, int]]:
        """dead ends of this pass: one opening left, start and end apart"""
        keep_out = {self.start, self.end}
        return [(cell.x, cell.y)
                for row in self.maze.grid
                for cell in row
                if cell.wall.bit_count() == 3
                and (cell.x, cell.y) not in keep_out]

    def opening(self, cell: Cell) -> str:
        """the single direction a dead end is still open on"""
        for step in Step:
            if not cell.wall & Dir[step.name]:
                return step.name
        raise Exception(f"Solver opening error: ({cell.x},{cell.y}) is sealed")

    def fill_cell(self, x: int, y: int) -> Generator[Cell, None, int]:
        """seal a single dead end and stop, next pass takes its neighbour"""
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
        """wall up every dead end, pass after pass, until none is left"""
        op_count = 0
        while True:
            dead_end = self.find_dead_end()
            if not dead_end:
                return op_count
            for x, y in dead_end:
                op_count += yield from self.fill_cell(x, y)

    def solve(self) -> Generator[Cell, None, None]:
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
        """walk  throw the maze"""
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
