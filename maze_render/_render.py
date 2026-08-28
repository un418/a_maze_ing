class MazeRender:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze

    def print_metadata(self) -> None:
        for row in self.maze.grid:
            for cell in row:
                match cell:
                    case Cell(border=True):
                        print("B", end="")
                    case Cell(logo=True):
                        print("L", end="")
                    case Cell(border=False):
                        print("0", end="")
                    case _:
                        print("E", end="")
            print()

    def print_maze(self, bits: bool = False) -> None:
        """print the wall bitmask of each case as a box drawing"""
        box: str = "  "
        # box = f" {wall:04b} "
        for row in range(self.row_max):
            top = ""
            mid = ""
            for col in range(self.col_max):
                wall = self.matrix[row][col].wall
                if bits:
                    box = f" {wall:04b} "
                width = len(box)
                top += "+" + ("-" if wall & Dir.N else " ") * width
                mid += ("|" if wall & Dir.W else " ") + box
                if col == self.col_max - 1:
                    top += "+"
                    mid += "|" if wall & Dir.E else " "
            print(top)
            print(mid)
        bottom = ""
        for col in range(self.col_max):
            wall = self.matrix[self.row_max - 1][col].wall
            if bits:
                box = f" {wall:04b} "
            width = len(box)
            bottom += "+" + ("-" if wall & Dir.S else " ") * width
        print(bottom + "+")
