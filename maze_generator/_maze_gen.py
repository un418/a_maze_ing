#!/usr/bin/env python3

from enum import Enum

class Grid:
    def __init__(self, row_max: int, col_max: int) -> None:
        self.row_max = row_max
        self.col_max = col_max
        self.matrix: list[list[Case | None]] = [
            [None for col in range(col_max)] for row in range(row_max)]

    def pregen_maze(self) -> None:
        """"define constraint before generating maze"""
        for row in range(self.row_max):
            for col in range(self.col_max):
                border = False
                if (row == 0 or
                        col == 0 or
                        row == self.row_max - 1 or
                        col == self.col_max - 1):
                    border = True
                self.matrix[row][col] = Case(row, col, border=border)


    def debug_print_maze(self) -> None:
        for row in range(self.row_max):
            for col in range(self.col_max):
                match self.matrix[row][col]:
                    case Case(border=True):
                        print("B", end="")
                    case Case(border=False):
                        print("0", end="")
                    case _:
                        print("E", end="")
                if col == self.col_max - 1:
                    print()


class Case:
    __match_args__ = ("border", "logo")

    def __init__(self,
                 x: int,
                 y: int,
                 border: bool = False,
                 logo: bool = False) -> None:
        self.x = x
        self.y = y
        self.border = border # cannot be open the same way
        # self.border_type : (left, right, top, bottom)
        self.logo = logo

        @staticmethod
        def gen_border(self) -> None:

        e

if __name__ == "__main__":
    test_grid = Grid(3, 3)
    test_grid.pregen_maze()
    test_grid.debug_print_maze()
