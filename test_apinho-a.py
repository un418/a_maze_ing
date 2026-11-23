import sys
from time import sleep

from config_parser import ConfigData, ValidationError, config_validator
from core import CellState
from maze_generator import Braider, Logo, Maze, MazeGenDFS
from maze_render import AsciiMazeRender
from maze_solver import BFSsolver, DeadEndSolver
from output_file import OutputFile

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Missing configuration file. \
Usage: poetry run python3 <PROGRAM.py> <config.txt>"
        )
        sys.exit(42)

    try:
        val_data: ConfigData = config_validator(sys.argv[1])
    except (ValueError, ValidationError, OSError):
        print("Error")  # Placeholder
        sys.exit(42)

    try:
        maze = Maze(val_data.WIDTH, val_data.HEIGHT, val_data.ENTRY, val_data.EXIT)
        # maze.pregen()
        mazegen = MazeGenDFS(maze)
        render = AsciiMazeRender(maze)
        # render.print_metadata()
        logo_coordset = Logo(maze).gen_coordset()
        mazegen.import_logoset(logo_coordset)
        gen = mazegen.gen()
        render.clear()
        render.disable_term_cursor()
        try:
            while gen:
                cursor = next(gen)
                frame = render.frame(mode="default", cursor=cursor)
                render.flush(frame)
                sleep(1 / 150)
        except StopIteration as e:
            print(f"Maze generated in {e.value} ops")
        except Exception as e:
            print(f"Caught {type(e).__name__}: {e}")
        finally:
            render.enable_term_cursor()
        # Non perfect step
        if not val_data.PERFECT:
            maze_braider = Braider(maze)
            maze_braider.gen_braiding()

            # Solving non-Perfect
            solver = BFSsolver(maze)
            render.attach(solver.maze)
            render.disable_term_cursor()
            try:
                solved_path = solver.solver()
                for x, y in solved_path:
                    solver.maze.grid[y][x].state = CellState.SOLVER_VISITED
                    render.flush(render.frame(mode="default"))
                    sleep(1 / 60)

            except StopIteration as e:
                print(f"Maze solved in {e.value} ops")
            except Exception as e:
                print(f"Caught {type(e).__name__}: {e}")
            finally:
                render.enable_term_cursor()
                for x in solver.solver():
                    pass
        else:
            # Solving Perfect
            solver = DeadEndSolver(maze)
            render.attach(solver.maze)
            render.disable_term_cursor()
            try:
                solver_iter = solver.fill_dead_end()
                while solver_iter:
                    frame = render.frame(mode="default")
                    render.flush(frame)
                    sleep(1 / 60)

            except StopIteration as e:
                print(f"Maze solved in {e.value} ops")
            except Exception as e:
                print(f"Caught {type(e).__name__}: {e}")

            # TESTING OUTPUT
            test = OutputFile(mazegen, val_data, solver)
            test.constructor()

    except (KeyboardInterrupt, EOFError):
        print("\n Program interrupted by user")
