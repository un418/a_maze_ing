from time import sleep

from config_parser import ConfigData
from mazegen.core import CellState
from mazegen.generator import Maze
from maze_render import AsciiMazeRender
from mazegen.solver import BFSsolver, DeadEndSolver


def maze_solver(
    val_data: ConfigData,
    maze: Maze,
    render: AsciiMazeRender,
    status_lines: list[str],
) -> list[tuple[int, int]]:
    """
    Select a solver and display the status messages when it succeeds.

    Args:
        val_data: Validated settings that select the solver.
        maze: Generated maze to solve.
        render: Terminal renderer used during solving.
        status_lines: Existing messages to extend with the solving result.

    Returns:
        A list of (x, y) coordinates from entry to exit, inclusive,

    Raises:
        SolverError: If BFS cannot reach the exit.
    """
    # Non perfect step
    if not val_data.PERFECT:
        solved_path = non_perfect_solver(maze, render, status_lines)
    else:
        solved_path = perfect_solver(maze, render, status_lines)

    for status in status_lines:
        print(status)
    return solved_path


def non_perfect_solver(
    maze: Maze, render: AsciiMazeRender, status_lines: list[str]
) -> list[tuple[int, int]]:
    """
    Find the shortest path with BFS and animate the resulting route.

    Args:
        maze: Generated maze, which may contain loops.
        render: Terminal renderer used to draw the path.
        status_lines: Messages to extend with the number of path moves.

    Returns:
        The shortest path as (x, y) coordinates, including both endpoints.

    Raises:
        SolverError: If BFS cannot reach the exit.
    """

    # Solving non-Perfect
    solver = BFSsolver(maze)
    render.attach(solver.maze)

    solved_path = solver.solver()
    for x, y in solved_path:
        solver.maze.grid[y][x].state = CellState.SOLVER_VISITED
        render.flush(render.frame(mode="default"))
        sleep(1 / 60)

    status_lines.append(f"Maze solved in {len(solved_path) - 1} ops")
    return solved_path


def perfect_solver(
    maze: Maze, render: AsciiMazeRender, status_lines: list[str]
) -> list[tuple[int, int]]:
    """
    Animate dead-end filling and record the remaining route.

    Dead-end filling runs on the solver's copy of the maze. Once filling
    finishes, walk the remaining corridor to record the solution.

    Args:
        maze: Generated perfect maze to solve.
        render: Terminal renderer to attach to the solver's working copy.
        status_lines: Messages to extend with the number of dead ends sealed.

    Returns:
        The path as (x, y) coordinates, including both endpoints.
    """
    # Solving Perfect
    solver = DeadEndSolver(maze)
    render.attach(solver.maze)

    solver_iter = solver.fill_dead_end()
    try:
        while solver_iter:
            next(solver_iter)
            frame = render.frame(mode="default")
            render.flush(frame)
            sleep(1 / 60)
    except StopIteration as e:
        status_lines.append(f"Maze solved in {e.value} ops")

    pop_solution = solver.solve()  # Populate solver.solution
    for x in pop_solution:
        pass
    return solver.solution
