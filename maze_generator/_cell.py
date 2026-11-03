"""Single cell of the maze grid."""

from core import CellState


class Cell:
    """One square of the maze, with its walls and metadata.

    Attributes:
        x: Column index in the grid.
        y: Row index in the grid.
        border: True if the cell lies on the outer edge of the grid.
        logo: True if the cell belongs to the logo.
        wall: 4-bit mask of closed walls (see `core.Dir`), all closed
            by default.
        state: Mark left by the solver, None until it visits the cell.
    """

    def __init__(self,
                 x: int,
                 y: int,
                 border: bool = False,
                 logo: bool = False,
                 wall: int = 0b1111
                 ) -> None:
        """Create a cell at (x, y), with all walls closed by default.

        Args:
            x: Column index in the grid.
            y: Row index in the grid.
            border: Whether the cell lies on the outer edge of the grid.
            logo: Whether the cell belongs to the logo.
            wall: 4-bit mask of closed walls (see `core.Dir`).
        """
        self.x, self.y = x, y
        self.border = border
        self.logo = logo
        self.wall = wall
        self.state: CellState | None = None
