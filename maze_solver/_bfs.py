"""Find shortest paths through mazes using breadth-first search."""

from core import Dir, Step
from maze_generator import Cell, Maze

class SolverError(Exception):

    def __str__(self):
        return "Solver couldn't solve the maze"


class BFSsolver:
    """Solve a maze by exploring cells in order of distance from the entry.

    Attributes:
        maze: Generated maze to search.
    """

    def __init__(self, maze: Maze):
        """Store the maze for the search.

        Args:
            maze: Generated maze with closed outer walls.
        """
        self.maze = maze

    def solver(self) -> list[tuple[int, int]]:
        """Find the shortest path from the entry to the exit.

        Follow open passages and record where each cell was first reached
        from, then use those records to reconstruct the path.

        Returns:
            Path as (x, y) coordinates, including the entry and exit
        Raises:
            SolverError if the exit is unreachable.
        """
        queue: list[tuple[int, int]] = [self.maze.entry]
        seen: set[tuple[int, int]] = {self.maze.entry}
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        exit: tuple[int, int] = self.maze.exit
        grid = self.maze.grid
        while queue:
            x, y = queue[0]
            queue.pop(0)
            curr_cell: Cell = grid[y][x]
            if (curr_cell.x, curr_cell.y) == exit:
                break
            for step in Step:
                if curr_cell.wall & Dir[step.name]:  # skip dir with walls
                    continue
                x_offset, y_offset = step.value
                neighbour_x, neighbour_y = x + x_offset, y + y_offset
                
                if not (0 <= neighbour_x < self.maze.width
                        and 0 <= neighbour_y < self.maze.height):
                    continue # skip out of bounds lookup
                neighbour_cell = grid[neighbour_y][neighbour_x]
                if (
                    not self._is_valid_cell(neighbour_cell)
                    or self._was_seen(neighbour_cell, seen)
                ):
                    continue

                queue.append((neighbour_x, neighbour_y))
                came_from[neighbour_x, neighbour_y] = (
                    curr_cell.x,
                    curr_cell.y,
                )

        if exit not in seen:  # Exit wasn't found
            raise SolverError

        current = self.maze.exit
        path: list[tuple[int, int]] = [current]

        while current != self.maze.entry:  # Registering shortest path from exit-entry
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path

    def _was_seen(self, cell: Cell, seen: set[tuple[int, int]]) -> bool:
        """Check whether the cell was seen and record it on the first visit.

        Args:
            cell: Candidate cell to check.
            seen: Set of discovered coordinates, updated in place.

        Returns:
            True if the cell was already in the set, or False if just added.
        """
        if (cell.x, cell.y) in seen:
            return True
        else:
            seen.add((cell.x, cell.y))
            return False

    def _is_valid_cell(self, cell: Cell) -> bool:
        """Check whether an existing cell is usable by the search.

        Args:
            cell: Candidate cell already retrieved from the grid.

        Returns:
            True if the cell is in bounds and outside the logo.
        """
        if cell.logo:
            return False

        x, y = cell.x, cell.y
        if 0 <= x < self.maze.width and 0 <= y < self.maze.height:
            return True

        return False
