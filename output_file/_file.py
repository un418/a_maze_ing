"""Write a generated maze and its solution to a text file."""

from typing import IO

from config_parser import ConfigData
from core import Step
from maze_generator import MazeGenDFS
from maze_solver import DeadEndSolver


class OutputFile:
    """Serialize a maze, its endpoints, and its solution path.

    Attributes:
        mazegen: Generator holding the completed maze grid.
        val_data: Validated configuration, including the output filename.
        solver: Solver holding the route from entry to exit.
    """

    def __init__(
        self, mazegen: MazeGenDFS, val_data: ConfigData, solver: DeadEndSolver
    ):
        """Store the maze, configuration, and solver used for output.

        Args:
            mazegen: Generator whose maze contains the final wall masks.
            val_data: Validated configuration for the output file and endpoints.
            solver: Solver whose solution has already been populated.
        """

        self.mazegen = mazegen
        self.val_data = val_data
        self.solver = solver

    def constructor(self) -> None:  # handle excpetions outside
        """Create the output file and write the maze, endpoints, and path.

        Check the recorded solution before opening the file. An existing output
        file is overwritten.

        Raises:
            OSError: If the output file cannot be created or written.
            ValueError: If the solution fails validation or a path step does
                not match a cardinal direction.
        """
        if not self._validate_solution():
            raise ValueError("Invalid solution list")

        with open(f"{self.val_data.OUTPUT_FILE}", "w") as file:
            self._maze_layout_writer(file, self.mazegen.maze.grid)
            self._entry_exit_writer(file)
            self._path_dir_writer(file)

    def _validate_solution(self) -> bool:
        """Check the basic requirements of the recorded solution.

        The list must be nonempty, begin at the maze entry, and have no
        consecutive duplicate coordinates.

        Returns:
            True if these checks pass, otherwise False.
        """
        sol_list: list[tuple[int, int]] = self.solver.solution
        if not len(sol_list):
            return False
        if sol_list[0] != self.mazegen.maze.entry:
            return False
        for i in range(len(sol_list) - 1):
            curr: tuple[int, int] = sol_list[i]
            foll: tuple[int, int] = sol_list[i + 1]
            if curr == foll:
                return False

        return True

    def _maze_layout_writer(self, file: IO, grid: list[list]) -> None:
        """Write each row of cell wall masks as hexadecimal digits.

        Add a blank line after the grid to separate it from the path metadata.

        Args:
            file: Open output file.
            grid: Rows of cells from the generated maze.
        """
        for row in grid:
            file.writelines(self._clean_hex(curr_cell.wall) for curr_cell in row)
            file.write("\n")
        file.write("\n")

    def _entry_exit_writer(self, file: IO) -> None:
        """Write the configured entry and exit on separate lines.

        Args:
            file: Open output file.
        """
        file.write(f"{self.val_data.ENTRY}     #ENTRY (x, y)\n")
        file.write(f"{self.val_data.EXIT}     #EXIT (x, y)\n")

    def _path_dir_writer(self, file: IO) -> None:
        """Write the solution as a sequence of cardinal direction letters.

        Convert consecutive coordinates to directions, then add the final
        move to the exit, which the solver omits from its solution list.

        Args:
            file: Open output file.

        Raises:
            ValueError: If a coordinate difference is not a cardinal step.
        """
        sol_list: list[tuple[int, int]] = self.solver.solution
        for i in range(len(sol_list) - 1):
            curr: tuple[int, int] = sol_list[i]
            foll: tuple[int, int] = sol_list[i + 1]

            delta: tuple[int, int] = (foll[0] - curr[0], foll[1] - curr[1])
            file.write(Step(delta).name)

        last_step = sol_list[len(sol_list) - 1]
        delta = (
            self.mazegen.maze.exit[0] - last_step[0],
            self.mazegen.maze.exit[1] - last_step[1],
        )
        file.write(Step(delta).name)
        file.write("\n")

    @staticmethod
    def _clean_hex(wall: int) -> str:
        """Return a wall mask in hexadecimal without the ``0x`` prefix.

        Args:
            wall: Bitmask of the cell's closed walls.

        Returns:
            Hexadecimal digits representing the wall mask.
        """
        clean = hex(wall)[2:]

        return clean
