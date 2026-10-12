
from config_parser import config_importer, ConfigData, ValidationError
from maze_generator import Maze, MazeGenDFS, Logo, Generator
import sys


if __name__ == "__main__":

    # Argument validation
    if len(sys.argv) != 2:
        print("Missing configuration file. \
Usage: poetry run python3 <PROGRAM.py> <config.txt>")

    # Input config data validation
    try:
        val_data: ConfigData = config_importer(sys.argv[1])
    except (ValidationError, ValueError) as e:
        print(e)

    # Maze stuff
    try:
        # 'Maze' object creation -> Creating 'Cell' for the grid
        # 0b1111 (full wall) by default
        maze: Maze = Maze(val_data.WIDTH, val_data.HEIGHT)
        # 'MageGenDFS' object uses the  '.gen()' method on the maze.grid
        # (all cells are 0b1111 at the start)
        mazegen: MazeGenDFS = MazeGenDFS(maze)
        # printing the '42' in the correct place
        logo_coordset: set[tuple[int, int]] = Logo(maze).gen_coordset()
        mazegen.import_logoset(logo_coordset)
        # to generate the actual mase (using Depth First Search)
        maze_generator: Generator = mazegen.gen() # type: ignore



    except:

