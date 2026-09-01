from collections.abc import Callable
from typing import Literal
import subprocess
import os

from maze_generator import Maze, Cell, Dir

RenderMode = Literal["default", "bits", "hex"]

_BOX_RENDERERS: dict[RenderMode, Callable[[int], str]] = {
    "default": lambda wall: "██" if wall == 0b1111 else "  ",
    "bits": lambda wall: f" {wall:04b} ",
    "hex": lambda wall: f" {wall:X} ",
}

# _CURSORS: dict[RenderMode, Callable[str]] = {
#     "default": lambda: "--" if wall == 0b1111 else "  ",
#     "bits": lambda wall: f" {wall:04b} ",
#     "hex": lambda wall: f" {wall:X} ",
# }



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

    def frame(self, mode: RenderMode = "default", cursor: Cell | None = None) -> str:
        """print the maze as a box drawing; `mode` picks how each cell body is rendered"""
        render_box = _BOX_RENDERERS[mode]
        lines: list[str] = []
        for row in self.maze.grid:
            top = ""
            mid = ""
            for cell in row:
                wall = cell.wall
                box = "░░" if cell is cursor else render_box(wall)
                width = len(box)
                top += "+" + ("-" if wall & Dir.N else " ") * width
                mid += ("|" if wall & Dir.W else " ") + box
                if cell.x == self.maze.x_max:
                    top += "+"
                    mid += "|" if wall & Dir.E else " "
            lines.append(top)
            lines.append(mid)
        # Last line
        bottom = ""
        for cell in row:
            wall = cell.wall
            box = render_box(wall)
            width = len(box)
            bottom += "+" + ("-" if wall & Dir.S else " ") * width
        lines.append(bottom + "+")
        return "\n".join(lines)

    def clear(self) -> None:
        # os.system('cls' if os.name == 'nt' else 'clear')
        subprocess.run('cls' if os.name == 'nt' else 'clear')

    def flush(self, frame: str) -> None:
        print("\033[H" + frame)

    def disable_term_cursor(self) -> None:
        print("\033[?25l")

    def enable_term_cursor(self) -> None:
        print("\033[?25h")
