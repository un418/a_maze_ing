_This project has been created as part of the 42 curriculum by adaferna, apinho-a._

# A-Maze-ing

Table of Contents
* [Description](#description)
* [Instructions](#instructions)
* [Config file](#config-file)
* [Maze generation](#maze-generation)
* [Maze solving](#maze-solving)
* [Reusable module](#reusable-module)
* [Team and project management](#team-and-project-management)
* [Bonus](#bonus)
* [Resources](#resources)
  * [AI Usage](#ai-usage)

## Description

The goal of this project is to build a **maze generator** in Python.

The program reads a config file, generates a random maze (reproducible with a seed), writes it to a file in hexadecimal and displays it in the terminal.

Two kinds of maze, picked with the `PERFECT` key:
- **Perfect** (`PERFECT=True`): exactly one path between the entry and the exit, no loop at all.
- **Pac-Man board** (`PERFECT=False`): every corridor is reachable, with loops and almost no dead-end.

Each maze shows a **"42"** in the middle, made of fully closed cells (when the maze is big enough).

The generation part is meant to be reused: it ships as a standalone pip package, `mazegen`.

## Instructions

## Config file

One `KEY=VALUE` pair per line. Lines starting with `#` are comments.

```ini
# Maze size, in cells
WIDTH=20
HEIGHT=15

# Coordinates x,y
ENTRY=0,0
EXIT=19,14

OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

| Key | Description |
| --- | --- |
| `WIDTH`, `HEIGHT` | Maze size, in cells |
| `ENTRY`, `EXIT` | Entry and exit coordinates `x,y`, different and inside the maze |
| `OUTPUT_FILE` | File the maze is written to |
| `PERFECT` | `True` for a perfect maze, `False` for a Pac-Man board |
| `SEED` | Seed of the random generator |

- Every key is mandatory except `SEED`, and a key can only appear once.
- `x` is the column, `y` the row, and `0,0` is the top-left corner.

## Maze generation

### Algorithm

**Randomized depth-first search**, also called the *recursive backtracker*. It's written with an explicit stack instead of recursion.

1. Start from a cell and mark it as visited.
2. Pick a random unvisited neighbour, open the wall between the two cells and move there.
3. If there is no unvisited neighbour left, go back to the previous cell.
4. Stop when the stack is empty: every cell has been visited.

The cells of the "42" are marked as visited before starting, so the DFS never opens them and they stay fully closed.

### Why this algorithm

## Maze solving

### Algorithm

**Dead-end filling**. Instead of looking for the path, the solver removes everything that is *not* the path.

1. Find every dead end: a cell with only one opening left (3 walls closed), except the entry and the exit.
2. Wall it up: close its last opening, on both sides. Its neighbour may now become a dead end too.
3. Do it again, pass after pass, until there is no dead end left.
4. Only the path from the entry to the exit is still open: walk it from the entry, there is only one way to go at each cell.

### Why this algorithm

Mostly because it looks cool. In the animation, every dead-end corridor shrinks back at the same time, one cell per pass, until only the solution is left. A BFS or an A\* would find the path just as well, but watching them is much less fun.

## Reusable module

### Basic usage

### Custom parameters

### Maze structure and solution

## Team and project management

### Roles

- **adaferna**: maze generation, solver and terminal render.
- **apinho-a**: config file parsing and validation.

### Planning

### What worked well and what could be improved

### Tools

- **GitHub Projects**: a kanban board to follow our tasks.
- **Issues and pull requests**: one issue per task, one branch per issue, and every PR is reviewed by the other teammate before it's merged into `master`.

## Bonus

- **Animated generation**: the maze is drawn while it's being carved, with a cursor on the current cell, so you can watch the backtracking.

## Resources

* [Maze generation algorithm](https://en.wikipedia.org/wiki/Maze_generation_algorithm) and [Maze-solving algorithm](https://en.wikipedia.org/wiki/Maze-solving_algorithm) on Wikipedia: the classic algorithms, all in one place.
* [Randomized Depth-First Search Algorithm for Maze Generation](https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742) by Nacer Kroudir, with [his Python code](https://github.com/NacerKROUDIR/MazeGeneration/blob/main/Maze_Generator.py).
* [Maze Generation Algorithms - An Exploration](https://professor-l.github.io/mazes/): each algorithm animated, with a short explanation.
* [42BELGIUM: A-MAZE-ING | Random Maze Generation & Visualisation](https://www.youtube.com/watch?v=TnMn02CwirY) (YouTube).
* [Choose a License](https://choosealicense.com/): to pick the license of the reusable module.
* [Obsidian.md](https://obsidian.md/) to take notes while working on this project. You can find them [here](https://github.com/un418/42.common.core/blob/master/_docs/99_Projects/M2_A-Maze_Ing.md).

### AI Usage

Claude (Anthropic) was used during this project for:
* **Clarifying concepts**: graphs and spanning trees, maze algorithms, bitmasks, packaging.
* **Reviews**: it plays a 42 evaluator on the project. It points out what doesn't match the subject yet and gives hints, never the fix.
* **Planning**: splitting what's left to do into tasks.
* **Docstrings**: drafting the Google-style docstrings of `core`, `maze_generator`, `maze_render` and `maze_solver`, following the convention we set in [#3](https://github.com/un418/a_maze_ing/issues/3).
* **This README**: structure and English.

AI-assisted or not, every change goes through a PR reviewed by the other teammate.
