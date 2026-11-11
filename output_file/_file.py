from config_parser import ConfigData
from maze_generator import MazeGenDFS


class OutputFileContructor:
    def __init__(self, mazegen: MazeGenDFS, val_data: ConfigData):

        self.mazegen = mazegen
        self.val_data = val_data

    def constructor(self):  # handle excpetions outside

        with open(f"{self.val_data.OUTPUT_FILE}", "x") as file:
            for row in self.mazegen.maze.grid:
                file.writelines(self._clean_hex(curr_cell.wall) for curr_cell in row)
                file.write("\n")
            file.write("\n")

            file.write(f"{self.val_data.ENTRY}     #ENTRY (x, y)\n")
            file.write(f"{self.val_data.EXIT}     #EXIT (x, y)\n")

    @staticmethod
    def _clean_hex(wall: int) -> str:
        """
        Removes '0x' from hex() function's output
        """
        clean = hex(wall)[2:]

        return clean
