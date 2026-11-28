from time import sleep
from typing import Generator

from config_parser import ConfigData
from mazegen.generator import Braider, Logo, Maze, Cell, MazeGenDFS
from maze_render import AsciiMazeRender, clear_term


def maze_generation(
    val_data: ConfigData,
) -> tuple[Maze, AsciiMazeRender, list[str]]:
    """Build and animate a maze using the configured generation mode.

    Reserve the 42 logo cells before carving with DFS. Braid the maze
    after carving if the configuration selects non-perfect mode.

    Args:
        val_data: Validated settings for the maze and its generation mode.

    Returns:
        The generated maze, its renderer, and a list of status messages.

    Raises:
        MazeLogoError: If the maze is too small for the 42 logo.
    """
    # Creates grid with every wall closed
    maze = Maze(val_data.WIDTH, val_data.HEIGHT, val_data.ENTRY, val_data.EXIT)
    # Object that holds perfect maze generation
    mazegen = MazeGenDFS(maze, val_data.SEED)
    # Assigning logo cells
    logo_coordset = Logo(maze).gen_coordset()
    # Importing logo coordinates into the generation object
    mazegen.import_logoset(logo_coordset)
    # renderer object
    render = AsciiMazeRender(maze)
    # Starting on a clean screen, then drawing each generator step
    clear_term()
    op_count: int = animate_generation(render, mazegen.gen())
    # modding perfect maze to generate non-Perfect
    if not val_data.PERFECT:
        braider = Braider(mazegen.maze)
        braider.gen_braiding()
        render.flush(render.frame())
    status_lines: list[str] = [f"Maze generated in {op_count} ops"]
    if not val_data.PERFECT:
        status_lines.append("Added Braiding! non-Perfect maze created :)")
    # Printing status_lines
    return mazegen.maze, render, status_lines


def animate_generation(
    render: AsciiMazeRender,
    maze_generator: Generator[Cell, None, int],
) -> int:
    """Draw each step of DFS maze generation in the terminal.

    Args:
        render: Renderer attached to the maze being carved.
        maze_generator: Iterator that yields the current cell and returns
            the operation count when carving finishes.

    Returns:
        The number of DFS operations, including moves and backtracks.
    """
    while True:
        try:
            cursor = next(maze_generator)
        except StopIteration as finished:
            return finished.value
        render.flush(render.frame(cursor=cursor))
        sleep(1 / 150)
