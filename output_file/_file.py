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

        An existing output file is overwritten.
 
        Raises:
            OSError: If the output file cannot be created or written.
            ValueError: If a path step does not match a cardinal direction.
        """
        with open(f"{self.val_data.OUTPUT_FILE}", "w") as file:
            self._maze_layout_writer(file, self.mazegen.maze.grid)
            self._entry_exit_writer(file)
            self._path_dir_writer(file)

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
        entry_x, entry_y = self.val_data.ENTRY
        exit_x, exit_y = self.val_data.EXIT
        file.write(f"{entry_x},{entry_y}\n")
        file.write(f"{exit_x},{exit_y}\n")

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
