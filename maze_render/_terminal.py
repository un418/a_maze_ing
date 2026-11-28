"""Terminal screen and cursor control, shared by the terminal renderers.

Functions:
    clear_term: Clear the terminal.
    hide_term_cursor: Hide the terminal cursor.
    show_term_cursor: Show the terminal cursor again.
"""

import os


def clear_term() -> None:
    """Clear the terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def hide_term_cursor() -> None:
    """Hide the terminal cursor during the animation."""
    print("\033[?25l")


def show_term_cursor() -> None:
    """Show the terminal cursor again."""
    print("\033[?25h")
