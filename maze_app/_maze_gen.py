from time import sleep

from config_parser import ConfigData
from maze_generator import Braider, Logo, Maze, MazeGenDFS
from maze_render._ascii_render import AsciiMazeRender


def maze_generation(val_data: ConfigData) -> tuple[Maze, AsciiMazeRender]:
    # Creates grid with every wall closed
    maze = Maze(val_data.WIDTH, val_data.HEIGHT, val_data.ENTRY, val_data.EXIT)
    # Object that holds perfect maze generation
    mazegen = MazeGenDFS(maze)
    # Assigning logo cells
    logo_coordset = Logo(maze).gen_coordset()
    # Importing logo coordinates into the generation object
    mazegen.import_logoset(logo_coordset)
    # renderer object
    render = AsciiMazeRender(maze)
    # helper function to yield generator and draw it in terminal
    op_count: int = animate_generation(render, mazegen.gen())
    # modding perfect maze to generate non-Perfect
    print(f"Maze generated in {op_count} ops")
    if not val_data.PERFECT:
        braider = Braider(mazegen.maze)
        braider.gen_braiding()
        render.flush(render.frame())
    print(f"Maze generated in {op_count} ops")
    if not val_data.PERFECT:
        print("Added Braiding! non-Perfect maze created :)")
    return mazegen.maze, render


def animate_generation(render, maze_generator):
    while True:
        try:
            cursor = next(maze_generator)
        except StopIteration as finished:
            return finished.value
        render.flush(render.frame(cursor=cursor))
        sleep(1 / 150)
