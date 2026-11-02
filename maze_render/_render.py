"""Terminal rendering of a maze as ASCII boxes."""

from collections.abc import Callable
from typing import Literal
import os

from core import Dir, CellState
from maze_generator import Maze, Cell

RenderMode = Literal["default", "bits", "hex"]

# Cell body renderers: (wall mask, solver state) -> box content
_BOX_RENDERERS: dict[RenderMode, Callable[[int, CellState | None], str]] = {
    "default": lambda wall, state: (
        "▒▒▒" if state is CellState.DEAD_END
        else "▓▓▓" if state is CellState.SOLVER_VISITED
        else "███" if wall == 0b1111
        else "   "),
    "bits": lambda wall, state: f" {wall:04b} ",
    "hex": lambda wall, state: f" {wall:X} ",
}


class MazeRender:
    """Draws a maze in the terminal and handles the screen around it.

    Attributes:
        maze: Maze currently drawn.
    """

    def __init__(self, maze: Maze) -> None:
        """Bind the renderer to `maze`.

        Args:
            maze: Maze to draw.
        """
        self.maze = maze

    def attach(self, maze: Maze) -> None:
        """Draw another maze from now on, e.g. the solver's working copy.

        Args:
            maze: Maze to draw instead of the current one.
        """
        self.maze = maze

    def print_metadata(self) -> None:
        """Print the grid flags: B (border), L (logo), 0 (plain), E (error)."""
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

    def frame(self,
              mode: RenderMode = "default",
              cursor: Cell | None = None
              ) -> str:
        """Draw the maze as boxes.

        Args:
            mode: How a cell body is rendered (see `_BOX_RENDERERS`).
            cursor: Cell to highlight, e.g. the generator's current cell.

        Returns:
            The whole maze as a multi-line string.
        """
        render_box = _BOX_RENDERERS[mode]
        box_size = len(render_box(0b1111, None))
        lines: list[str] = []
        for row in self.maze.grid:
            top = ""
            mid = ""
            for cell in row:
                wall = cell.wall
                state = cell.state
                box = ("░" * box_size if cell is cursor
                       else render_box(wall, state))
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
        for cell in self.maze.grid[-1]:
            wall = cell.wall
            width = len(render_box(wall, None))
            bottom += "+" + ("-" if wall & Dir.S else " ") * width
        lines.append(bottom + "+")
        return "\n".join(lines)

    def clear(self) -> None:
        """Clear the terminal."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def flush(self, frame: str) -> None:
        """Print `frame` from the top-left corner, over the previous one.

        Args:
            frame: Maze drawing, as returned by `frame()`.
        """
        print("\033[H" + frame)

    def disable_term_cursor(self) -> None:
        """Hide the terminal cursor during the animation."""
        print("\033[?25l")

    def enable_term_cursor(self) -> None:
        """Show the terminal cursor again."""
        print("\033[?25h")
