"""Write a generated maze and its solution to a text file."""

from typing import IO

from core import Step
from maze_generator import Maze


class OutputFile:
    """Serialize a maze, its endpoints, and its solution path.

    Attributes:
        mazegen: Generator holding the completed maze grid.
        val_data: Validated configuration, including the output filename.
        solver: Solver holding the route from entry to exit.
    """

    def __init__(self, maze: Maze, file_name: str, solution: list[tuple[int, int]]):
        """Store the maze, configuration, and solver used for output.

        Args:
            mazegen: Generator whose maze contains the final wall masks.
            val_data: Validated configuration for the output file and endpoints.
            solver: Solver whose solution has already been populated.
        """

        self.maze = maze
        self.file_name = file_name
        self.solution = solution

    def constructor(self) -> None:  # handle excpetions outside
        """Create the output file and write the maze, endpoints, and path.

        Validate the solution before opening the file for writing.

        Raises:
            OSError: If the output file cannot be created or written.
            ValueError: If the solution is invalid or a path step does not
                match a cardinal direction.
        """
        if not self._validate_solution():
            raise ValueError("Invalid solution list")
        with open(self.file_name, "w") as file:
            self._maze_layout_writer(file, self.maze.grid)
            self._entry_exit_writer(file)
            self._path_dir_writer(file)

    def _validate_solution(self) -> bool:
        """Check the basic requirements of the recorded solution.

        The list must be nonempty, run from the entry to the exit, and have
        no consecutive duplicate coordinates.

        Returns:
            True if these checks pass, otherwise False.
        """
        if not len(self.solution):
            return False
        if self.solution[0] != self.maze.entry:
            return False
        if self.solution[-1] != self.maze.exit:
            return False
        for i in range(len(self.solution) - 1):
            curr: tuple[int, int] = self.solution[i]
            foll: tuple[int, int] = self.solution[i + 1]
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
        entry_x, entry_y = self.maze.entry
        exit_x, exit_y = self.maze.exit
        file.write(f"{entry_x},{entry_y}\n")
        file.write(f"{exit_x},{exit_y}\n")

    def _path_dir_writer(self, file: IO) -> None:
        """Write the solution as a sequence of cardinal direction letters.

        Convert each consecutive pair into a direction, including the move
        into the exit.

        Args:
            file: Open output file.

        Raises:
            ValueError: If a coordinate difference is not a cardinal step.
        """
        for i in range(len(self.solution) - 1):
            curr: tuple[int, int] = self.solution[i]
            foll: tuple[int, int] = self.solution[i + 1]

            delta: tuple[int, int] = (foll[0] - curr[0], foll[1] - curr[1])
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
