from ._maze import Maze


class MazeLogoError(Exception):
    """Raise if maze grid size is too litle to print the logo"""
    def __init__(self, message: str = "Unknown Maze Logo error") -> None:
        super().__init__(message)


class Logo:
    def __init__(self, maze: Maze) -> None:
        self.maze = maze
        self.center = (maze.width // 2, maze.height // 2)

    def gen_coordset(self) -> set[tuple[int, int]]:
        """ generate logo fully closed cells coordinates"""
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
