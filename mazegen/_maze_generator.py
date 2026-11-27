"""Single entry point to generate and solve a maze."""

from mazegen.generator import Maze, Logo, MazeGenDFS, Braider
from mazegen.solver import BFSsolver


class MazeGenerator:
    """A maze, generated and solved as soon as it is created.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        entry: (x, y) of the entry.
        exit: (x, y) of the exit.
        grid: Rows of cells, indexed as `grid[y][x]`.
        solution: (x, y) coordinates of a shortest path, from the entry
            to the exit, both included.
    """

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        seed: int | None = None
    ) -> None:
        """Generate the maze, then solve it.

        Args:
            width: Number of columns, at least 8.
            height: Number of rows, at least 8.
            entry: (x, y) of the entry, inside the maze.
            exit: (x, y) of the exit, inside the maze.
            perfect: True for a single path between any two cells, False
                to open extra walls (loops, fewer dead ends).
            seed: Same seed and parameters give the same maze. None gives
                a random one.

        Raises:
            MazeLogoError: If the width or the height is below 8.
            SolverError: If no path leads to the exit, for example when
                the entry or the exit is on a cell of the "42" logo.
        """

        _maze = Maze(width=width, height=height, entry=entry, exit=exit)

        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit

        # generation
        maze_gen = MazeGenDFS(_maze, seed)
        maze_gen.import_logoset(Logo(_maze).gen_coordset())
        gen = maze_gen.gen()
        # TODO: The logic here is too heavy need to simplify
        # create MazeGenDFS -> import logoset -> create the generator ...
        for _ in gen:
            pass
        if not perfect:
            Braider(_maze).gen_braiding()

        # solving
        self.solution = BFSsolver(_maze).solver()

        # save grid for client access at the end
        self.grid = _maze.grid
