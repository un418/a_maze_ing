# mazegen

Generate a maze with a "42" logo in the middle, and get a path through it.

## Usage

```bash
pip install mazegen-0.1.0-py3-none-any.whl
```

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,      # in cells, at least 8
    height=15,     # in cells, at least 8
    entry=(0, 0),  # (x, y), (0, 0) is top-left
    exit=(19, 14),
    perfect=True,  # False: adds loops
    seed=42,       # optional, reproducible maze
)

print(maze.grid[0][0].wall)  # grid[y][x]
print(maze.solution)  # shortest path of (x, y)
```

- **Walls**: `cell.wall` is the sum of the closed walls: North 1, East 2, South 4, West 8 (`3` = north and east).
- **Logo**: `cell.logo` is `True` for the fully closed cells of the "42" logo.
