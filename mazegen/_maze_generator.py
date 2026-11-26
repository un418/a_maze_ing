"""Maze generator facade to simplify usage of component"""  # TODO to improve

from mazegen.generator import Maze, Logo, MazeGenDFS, Braider
from mazegen.solver import BFSsolver


class MazeGenerator:
    """Maze generated with solution

    Attributes:
            ...
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
