import subprocess
import sys

from config_parser import config_validator
from mazegen import MazeGenerator
from mazegen.core import Step


def check_verdict(output_file: str, verdict: str) -> None:
    """Check the verdict of the maze analyzer (provided with the subject)

    Tests: shared walls, connectivity, perfect or playable maze.
    Not tested: border walls, 3x3 areas, "42" drawing, solution path.
    """
    # the analyzer exits 0 even on a bad verdict: read what it prints
    analyzer = subprocess.run(
        [sys.executable, "tests/maze_analyzer.py", output_file],
        capture_output=True,
        text=True,
    )
    # hidden by pytest when the test passes, see it with: pytest -rP
    print(analyzer.stdout)
    assert verdict in analyzer.stdout


def check_app_eq_facade(config_file: str) -> str:
    """Check that the app and MazeGenerator build the same maze

    Return the output file written by the app.
    """
    # run the app with the Makefile
    # its output is captured: the animation would flood the pytest output
    app = subprocess.run(
        ["make", "run", "CONFIG=" + config_file],
        capture_output=True,
        text=True,
    )
    assert app.returncode == 0, app.stderr

    # same maze with MazeGenerator
    config = config_validator(config_file)
    maze = MazeGenerator(
        config.WIDTH,
        config.HEIGHT,
        config.ENTRY,
        config.EXIT,
        config.PERFECT,
        config.SEED,
    )

    # read the output file of the app
    with open(config.OUTPUT_FILE) as f:
        lines = f.read().splitlines()

    # compare the walls, line by line
    for y in range(config.HEIGHT):
        walls = ""
        for cell in maze.grid[y]:
            walls += hex(cell.wall)[2:]
        assert walls == lines[y]

    # compare the solution path (last line of the file)
    path = ""
    for i in range(len(maze.solution) - 1):
        ax, ay = maze.solution[i]
        bx, by = maze.solution[i + 1]
        path += Step((bx - ax, by - ay)).name
    assert path == lines[-1]

    return config.OUTPUT_FILE


def test_perfect() -> None:
    output_file = check_app_eq_facade("tests/perfect-config.txt")
    check_verdict(output_file, "Verdict: PERFECT maze")


def test_imperfect() -> None:
    output_file = check_app_eq_facade("tests/imperfect-config.txt")
    check_verdict(output_file, "Verdict: Pac-Man-USABLE")
