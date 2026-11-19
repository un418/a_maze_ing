import sys

from maze_app import (
    ConfigData,
    ImporterError,
    Maze,
    ValidationError,
    config_importer,
    maze_generation,
)

if __name__ == "__main__":
    # Importing configData Block
    try:
        val_data: ConfigData = config_importer()
    except (ValueError, ValidationError, OSError, ImporterError) as e:
        print(f"Config error: {e}", file=sys.stderr)
        sys.exit(42)
    # Generating a maze Block
    try:
        maze: Maze = maze_generation(val_data)
    except Exception as e:  # PLACEHOLDER
        print(f"Maze Generation Error: {e}", file=sys.stderr)
        sys.exit(42)
    # Solving the maze
