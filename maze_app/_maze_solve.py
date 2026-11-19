from time import sleep

from config_parser._validator import ConfigData
from core import CellState
from maze_generator import Maze
from maze_render import AsciiMazeRender
from maze_solver import BFSsolver, DeadEndSolver


class NotSolvedError(Exception):
    def __str__(self) -> str:
        return "Maze could not be solved!"


def maze_solver(
    val_data: ConfigData, maze: Maze, render: AsciiMazeRender
) -> list[tuple[int, int]]:
    # Non perfect step
    try:
        if not val_data.PERFECT:
            solved_path = non_perfect_solver(maze, render)
        else:
            solved_path = perfect_solver(maze, render)
    except StopIteration as e:
        print(f"Maze solved in {e.value} ops")

    if maze.exit in solved_path:
        return solved_path
    return []


def non_perfect_solver(maze: Maze, render: AsciiMazeRender) -> list[tuple[int, int]]:

    # Solving non-Perfect
    solver = BFSsolver(maze)
    render.attach(solver.maze)
    render.disable_term_cursor()

    solved_path = solver.solver()
    for x, y in solved_path:
        solver.maze.grid[y][x].state = CellState.SOLVER_VISITED
        render.flush(render.frame(mode="default"))
        sleep(1 / 60)

    render.enable_term_cursor()

    return solved_path


def perfect_solver(maze: Maze, render: AsciiMazeRender) -> list[tuple[int, int]]:
    # Solving Perfect
    solver = DeadEndSolver(maze)
    render.attach(solver.maze)
    render.disable_term_cursor()

    solver_iter = solver.fill_dead_end()
    while solver_iter:
        frame = render.frame(mode="default")
        render.flush(frame)
        sleep(1 / 60)
    return SOLVER
