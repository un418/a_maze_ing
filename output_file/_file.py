from typing import IO

from config_parser import ConfigData
from maze_generator import MazeGenDFS


class OutputFileContructor:
    def __init__(self, mazegen: MazeGenDFS, val_data: ConfigData):

        self.mazegen = mazegen
        self.val_data = val_data

    def constructor(self) -> None:  # handle excpetions outside

        with open(f"{self.val_data.OUTPUT_FILE}", "x") as file:
            self._maze_layout_writer(file, self.mazegen.maze.grid)
            self._entry_exit_writer(file)

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

    @staticmethod
    def _clean_hex(wall: int) -> str:
        """
        Removes '0x' from hex() function's output
        """
        clean = hex(wall)[2:]

        return clean
