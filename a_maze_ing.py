import sys

from maze_app import (
    ConfigData,
    ImporterError,
    NotSolvedError,
    OutputFile,
    ValidationError,
    config_importer,
    maze_generation,
    maze_solver,
)

if __name__ == "__main__":
    try:
        # Importing configData Block
        try:
            val_data: ConfigData = config_importer()
        except (ValueError, ValidationError, OSError, ImporterError) as e:
            print(f"Config error: {e}", file=sys.stderr)
            sys.exit(42)
        # Generating a maze Block
        try:
            maze, render = maze_generation(val_data)
        except Exception as e:  # PLACEHOLDER
            print(f"Maze Generation Error: {e}", file=sys.stderr)
            sys.exit(42)
        # Solving the maze
        try:
            solution = maze_solver(val_data, maze, render)
        except (Exception, NotSolvedError) as e:  # PLACEHOLDER
            print(f"Maze Solving Error: {e}", file=sys.stderr)
            sys.exit(42)
        # Output file Generation
        try:
            OutputFile(maze, val_data.OUTPUT_FILE, solution).constructor()
        except ValueError as e:
            print(f"Output file generation error: {e}", file=sys.stderr)
    except (KeyboardInterrupt, EOFError):
        print("\n Program interrupted by user...")
