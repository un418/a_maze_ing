"""Terminal screen and cursor control, shared by the terminal renderers.

Functions:
    clear_term: Clear the terminal.
    hide_term_cursor: Hide the terminal cursor.
    show_term_cursor: Show the terminal cursor again.
"""


def clear_term() -> None:
    """Clear the terminal."""
    # Deprecated: os.system('cls' if os.name == 'nt' else 'clear')
    # An external command is overkill here, and less portable
    # \033[H: cursor to the top-left corner, \033[2J: erase the screen
    print("\033[H\033[2J", end="")


def hide_term_cursor() -> None:
    """Hide the terminal cursor during the animation."""
    print("\033[?25l")


def show_term_cursor() -> None:
    """Show the terminal cursor again."""
    print("\033[?25h")
