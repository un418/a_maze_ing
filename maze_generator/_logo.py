"""Logo drawn in the middle of the maze as fully closed cells."""

from ._maze import Maze


class MazeLogoError(Exception):
    """Raised if the maze grid is too small to draw the logo."""
    def __init__(self, message: str = "Unknown Maze Logo error") -> None:
        """Create the error.

        Args:
            message: Error description.
        """
        super().__init__(message)


class Logo:
    """Computes which cells form the logo, centred in the maze.

    Attributes:
        maze: Maze the logo is placed in.
        center: (x, y) of the grid's centre cell.
    """

    def __init__(self, maze: Maze) -> None:
        """Bind the logo to `maze` and compute its centre.

        Args:
            maze: Maze the logo is placed in.
        """
        self.maze = maze
        self.center = (maze.width // 2, maze.height // 2)

    def gen_coordset(self) -> set[tuple[int, int]]:
        """Generate the coordinates of the logo's fully closed cells.

        Returns:
            Set of (x, y) coordinates the generator must leave closed.

        Raises:
            MazeLogoError: If the grid is too small for the logo.
        """
        if self.maze.width <= 8 or self.maze.width <= 8:
            raise MazeLogoError(
                'Maze grid is too little to print logo (min=8x8)')
        logo_coords: list[tuple[int, int]] = []
        scale_factor = 0  # TODO (Bonus) Scaling
        # scale factor = ..... (depends on width and height)
        size = 3 + scale_factor
        x_center, y_center = self.center
        # 4 - from top to bottom
        x, y = x_center - size, y_center - size
        logo_coords.append((x, y))
        for _ in range(size - 1):
            y += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            x += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            y += 1
            logo_coords.append((x, y))
        # 2 - from top to bottom
        x, y = x_center + 1, y_center - size
        logo_coords.append((x, y))
        for _ in range(size - 1):
            x += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            y += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            x -= 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            y += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            x += 1
            logo_coords.append((x, y))
        return set(logo_coords)
