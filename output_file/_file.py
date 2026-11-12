from typing import IO

from config_parser import ConfigData
from core import Step
from maze_generator import MazeGenDFS
from maze_solver import DeadEndSolver


class OutputFileContructor:
    def __init__(
        self, mazegen: MazeGenDFS, val_data: ConfigData, solver: DeadEndSolver
    ):

        self.mazegen = mazegen
        self.val_data = val_data
        self.solver = solver

    def constructor(self) -> None:  # handle excpetions outside

        with open(f"{self.val_data.OUTPUT_FILE}", "x") as file:
            self._maze_layout_writer(file, self.mazegen.maze.grid)
            self._entry_exit_writer(file)
            self._path_dir_writer(file)

    def _maze_layout_writer(self, file: IO, grid: list[list]) -> None:
        """
        Writes the maze's cell's walls, represented by a hex digit, into the output file
        """
        for row in grid:
            file.writelines(self._clean_hex(curr_cell.wall) for curr_cell in row)
            file.write("\n")
        file.write("\n")

    def _entry_exit_writer(self, file: IO) -> None:
        """
        Writes the entry and exit coordinates into the output file
        """
        file.write(f"{self.val_data.ENTRY}     #ENTRY (x, y)\n")
        file.write(f"{self.val_data.EXIT}     #EXIT (x, y)\n")

    def _path_dir_writer(self, file: IO) -> None:
        """
        checks solver.solution coordinate tuples to know the direction for the solution
        """
        sol_list: list[tuple[int, int]] = self.solver.solution
        for i in range(len(sol_list) - 1):
            curr: tuple[int, int] = sol_list[i]
            foll: tuple[int, int] = sol_list[i + 1]

            delta: tuple[int, int] = (foll[0] - curr[0], foll[1] - curr[1])
            file.write(f"{str(Step(delta))[5:]}")
        file.write("\n")

    @staticmethod
    def _clean_hex(wall: int) -> str:
        """
        Removes '0x' from hex() function's output
        """
        clean = hex(wall)[2:]

        return clean
