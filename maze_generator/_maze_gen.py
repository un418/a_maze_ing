#!/usr/bin/env python3

from enum import IntFlag
from typing import Generator
import random


class Matrix:
    def __init__(self, row_max: int, col_max: int) -> None:
        self.row_max = row_max
        self.col_max = col_max
        self.matrix: list[list[Case]] = [
            [Case(-1, -1) for col in range(col_max)] for row in range(row_max)]

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

    def gen_logo(self) -> None:
        r_center = self.row_max // 2
        c_center = self.col_max
        size = 3
        # 4
        #line 1


        for row in range(self.row_max):
            for col in range(self.col_max):
                ...
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

    def debug_print_maze_wall(self) -> None:
        """print the wall bitmask of each case as a box drawing"""
        for row in range(self.row_max):
            top = ""
            mid = ""
            for col in range(self.col_max):
                wall = self.matrix[row][col].wall
                top += "+" + ("------" if wall & Dir.N else "      ")
                mid += ("|" if wall & Dir.W else " ") + f" {wall:04b} "
                if col == self.col_max - 1:
                    top += "+"
                    mid += "|" if wall & Dir.E else " "
            print(top)
            print(mid)
        bottom = ""
        for col in range(self.col_max):
            wall = self.matrix[self.row_max - 1][col].wall
            bottom += "+" + ("------" if wall & Dir.S else "      ")
        print(bottom + "+")



def gen_wall(matrix: Matrix) -> None:
    for row in range(matrix.row_max):
        for col in range(matrix.col_max):
            wallset = gen_wallset(matrix, row, col)
            matrix.matrix[row][col].wall = random.choice(tuple(wallset))


def gen_wallset(matrix: Matrix, row: int, col: int) -> set[int]:
    baseset = Wall.BASESET
    wallset: set[int] = set(Wall.BASESET.copy())
    to_close: set[int] = set()
    to_open: set[int] = set()
    # border
    if row == 0:
        to_close.add(Dir.N)
    if col == 0:
        to_close.add(Dir.W)
    if row == matrix.row_max - 1:
        to_close.add(Dir.S)
    if col == matrix.col_max - 1:
        to_close.add(Dir.E)
    # antecedent constraint
    if col != 0:
        if matrix.matrix[row][col - 1].wall & Dir.E:
            to_close.add(Dir.W)
        else:
            to_open.add(Dir.W)
    if row != 0:
        if matrix.matrix[row - 1][col].wall & Dir.S:
            to_close.add(Dir.N)
        else:
            to_open.add(Dir.N)

    for wall in to_close:
        # intersection
        wallset = wallset & set(n for n in baseset if n & wall)
    for wall in to_open:
        # difference
        wallset = wallset - set(n for n in baseset if n & wall)
    return wallset


class Wall:
    BASESET = frozenset((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))


class Dir(IntFlag):
    N = 1  # 0001
    E = 2  # 0010
    S = 4  # 0100
    W = 8  # 1000
    # max (all close) = 15


class Case:
    """ Case(-1, -1) for uninitialized object"""
    def __init__(self,
                 x: int,
                 y: int,
                 border: bool = False,
                 logo: bool = False) -> None:
        self.x = x
        self.y = y
        self.border = border  # cannot be open the same way
        self.logo = logo
        self.wall: int = 0


if __name__ == "__main__":
    test_grid = Matrix(7, 7)
    test_grid.pregen_maze()
    test_grid.debug_print_maze()
    gen_wall(test_grid)
    test_grid.debug_print_maze_wall()
