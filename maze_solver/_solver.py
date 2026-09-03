from typing import Generator

from maze_generator import Maze, Cell
from core import Dir, Step, CellState


class DeadEndSolver:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.start = (0, 0)
        self.end = (self.maze.x_max, self.maze.y_max)  # TODO change later
        self.visited: set[tuple[int, int]] = set()
        self.dead_end: list[tuple[int, int]] = []
        self.solution: list[tuple[int, int]] = []

    def find_dead_end(self) -> None:
        to_pop: list[int] = []
        for y, row in enumerate(self.maze.grid):
            for x, cell in enumerate(row):
                if cell.wall.bit_count() == 3:
                    self.dead_end.append((x, y))
        for i, coord in enumerate(self.dead_end):
            if coord in {self.start, self.end}:
                to_pop.append(i)
        for i in to_pop:
            self.dead_end.pop(i)

    def fill_dead_end(self) -> Generator[Cell, None, None]:
        """walk from dead end to first met branch"""
        self.find_dead_end()
        for coord in self.dead_end:
            x, y = coord
            yield self.maze.grid[y][x]
            while True:
                self.visited.add((x, y))
                next_step = self.walk(x, y)
                dx, dy = Step[next_step].value
                nx, ny = x + dx, y + dy
                next_wall = self.maze.grid[ny][nx].wall
                if next_wall.bit_count() == 1:
                    break
                x, y = nx, ny
                yield self.maze.grid[y][x]
        return

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

    def render_export(self) -> dict[tuple[int, int], CellState]:
        export: dict[tuple[int, int], CellState] = {}
        # order is important here
        for cell in self.dead_end:
            export[cell] = CellState.DEAD_END
        for cell in self.visited:
            export[cell] = CellState.SOLVER_VISITED
        return export


"""     def dead_end_gen(self) -> Generator[Cell, None, int]:
        stack: deque = deque()
        op_count = 0
        stack.append(self.start)
        next_step = ""
        x, y = self.start
        first_block = True
        yield self.maze.grid[y][x]
        while stack:
            x, y = stack[0]
            self.visited.add((x, y))
            possible_step = self.gen_possible_step(x, y)
            if not possible_step:
                if first_block:
                    self.dead_end.append((x, y))
                    first_block = False
                stack.popleft()
                op_count += 1
                if stack:
                    x, y = stack[0]
                yield self.maze.grid[y][x]
                continue
            first_block = True
            next_step = choice(possible_step)
            dx, dy = Step[next_step].value
            nx, ny = x + dx, y + dy
            stack.appendleft((nx, ny))
            self.maze.grid[y][x].wall -= Dir[next_step].value
            self.maze.grid[ny][nx].wall -= Dir[OppDir[next_step].value].value
            op_count += 1
            yield self.maze.grid[ny][nx]
        return op_count """


