from maze_generator import Maze, MazeGenDFS, Logo
from maze_render import MazeRender
from maze_solver import DeadEndSolver
from time import sleep

if __name__ == "__main__":
    try:
        maze = Maze(30, 10)
        # maze.pregen()
        mazegen = MazeGenDFS(maze)
        render = MazeRender(maze)
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
                sleep(1/150)
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
                sleep(1/60)
        except StopIteration as e:
            print(f"Maze solved in {e.value} ops")
        except Exception as e:
            print(f"Caught {type(e).__name__}: {e}")
        finally:
            render.enable_term_cursor()

    except (KeyboardInterrupt, EOFError):
        print("\n Program interrupted by user")
