import sys
from time import sleep

from config_parser import ConfigData, ValidationError, config_validator
from maze_generator import Logo, Maze, MazeGenDFS
from maze_render import AsciiMazeRender
from maze_solver import DeadEndSolver
from output_file import OutputFileContructor

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
        maze = Maze(val_data.WIDTH, val_data.HEIGHT)
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
        # Solving
        solver = DeadEndSolver(maze)
        render.attach(solver.maze)
        render.disable_term_cursor()
        try:
            solver_iter = solver.fill_dead_end()
            while solver_iter:
                cursor = next(solver_iter)
                frame = render.frame(mode="default")
                render.flush(frame)
                sleep(1 / 60)

        except StopIteration as e:
            print(f"Maze solved in {e.value} ops")
        except Exception as e:
            print(f"Caught {type(e).__name__}: {e}")
        finally:
            render.enable_term_cursor()
            for x in solver.solve():
                pass

            # TESTING OUTPUT
            test = OutputFileContructor(mazegen, val_data, solver)
            test.constructor()
            sys.exit(1111)

    except (KeyboardInterrupt, EOFError):
        print("\n Program interrupted by user")
