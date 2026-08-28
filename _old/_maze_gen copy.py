#!/usr/bin/env python3

from enum import IntFlag
from typing import Generator
import random

# TODO: Remove global after config mgmt
glob_mode = "perfect"

class Wall:
    BASESET = frozenset((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
    PERFECTSET = frozenset((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))


class Dir(IntFlag):
    N = 1  # 0001
    E = 2  # 0010
    S = 4  # 0100
    W = 8  # 1000
    # max (all close) = 15


class Cell:
    """ Case(-1, -1) for uninitialized object"""
    def __init__(self,
                 x: int,
                 y: int,
                 border: bool = False,
                 logo: bool = False,
                 logo_coridor: bool = False,
                 logo_top: bool = False) -> None:
        self.x = x
        self.y = y
        self.border = border  # cannot be open the same way
        self.logo = logo
        self.logo_coridor = False
        self.logo_top = False
        self.wall: int = 0b1111



class Matrix:
    def __init__(self, row_max: int, col_max: int) -> None:
        self.row_max = row_max
        self.col_max = col_max
        self.matrix: list[list[Cell]] = [
            [Cell(-1, -1) for col in range(col_max)] for row in range(row_max)]

    def pregen_maze(self) -> None:
        """"define constraint before generating maze"""
        # TODO: define logo
        logoset = self.gen_logo_coordset()
        for row in range(self.row_max):
            for col in range(self.col_max):
                border = False
                logo = False
                # border
                if (row == 0 or
                        col == 0 or
                        row == self.row_max - 1 or
                        col == self.col_max - 1):
                    border = True
                # logo
                coord = (col, row)
                print(coord)
                if coord in logoset:
                    logo = True
                self.matrix[row][col] = Cell(row, col,
                                             border=border,
                                             logo=logo)

    # TODO: Maybe to moove in a subclass Logo
    def gen_logo_coordset(self) -> set:
        """ generate logo coordinates"""
        if self.row_max <= 8 or self.col_max <= 8:
            raise Exception('Grid too little for logo')
        r_center = self.row_max // 2
        c_center = self.col_max // 2
        logo_coords: list[tuple[int, int]] = []
        size = 3
        # 4 - from top to bottom
        y = r_center - size
        x = c_center - size
        logo_coords.append((x, y))
        for _ in range(size - 1):
            y += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            x += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            y += 1
            logo_coords.append((x, y))
        # 2 - from top to bottom
        y = r_center - size
        x = c_center + 1
        logo_coords.append((x, y))
        for _ in range(size - 1):
            x += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            y += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            x -= 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            y += 1
            logo_coords.append((x, y))
        for _ in range(size-1):
            x += 1
            logo_coords.append((x, y))
        return set(logo_coords)

    # TODO - Later
    def gen_inner_logo_coords(self) -> set:
        """ generate logo coordinates"""
        if self.row_max <= 8 or self.col_max <= 8:
            raise Exception('Grid too little for logo')
        r_center = self.row_max // 2
        c_center = self.col_max // 2
        inner_logo_coords: list[tuple[int, int]] = []
        return set(inner_logo_coords)

    def debug_print_maze_metadata(self) -> None:
        for row in range(self.row_max):
            for col in range(self.col_max):
                match self.matrix[row][col]:
                    case Cell(border=True):
                        print("B", end="")
                    case Cell(logo=True):
                        print("L", end="")
                    case Cell(border=False):
                        print("0", end="")
                    case _:
                        print("E", end="")
                if col == self.col_max - 1:
                    print()

    def debug_print_maze(self, bits: bool = False) -> None:
        """print the wall bitmask of each case as a box drawing"""
        box: str = "  "
        # box = f" {wall:04b} "
        for row in range(self.row_max):
            top = ""
            mid = ""
            for col in range(self.col_max):
                wall = self.matrix[row][col].wall
                if bits:
                    box = f" {wall:04b} "
                width = len(box)
                top += "+" + ("-" if wall & Dir.N else " ") * width
                mid += ("|" if wall & Dir.W else " ") + box
                if col == self.col_max - 1:
                    top += "+"
                    mid += "|" if wall & Dir.E else " "
            print(top)
            print(mid)
        bottom = ""
        for col in range(self.col_max):
            wall = self.matrix[self.row_max - 1][col].wall
            if bits:
                box = f" {wall:04b} "
            width = len(box)
            bottom += "+" + ("-" if wall & Dir.S else " ") * width
        print(bottom + "+")


def gen_wall(matrix: Matrix) -> None:
    # Can be access directly via object
    #    for row in matrix.matrix:
    #       for cell in row:

    for row in range(matrix.row_max):
        for col in range(matrix.col_max):
            # logo
            if matrix.matrix[row][col].logo:
                matrix.matrix[row][col].wall = 15
            else:
                wallset = gen_wallset(matrix, row, col)
                matrix.matrix[row][col].wall = random.choice(tuple(wallset))


def gen_wallset(matrix: Matrix, row: int, col: int) -> set[int]:
    # if glob_mode == "perfect":
    if True:
        baseset = Wall.PERFECTSET
    else:
        baseset = Wall.BASESET
    wallset: set[int] = set(baseset.copy())
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
    # successor constraint (logo)
    if col < matrix.col_max - 1 and matrix.matrix[row][col + 1].logo:
        to_close.add(Dir.E)
    if row < matrix.row_max - 1 and matrix.matrix[row + 1][col].logo:
        to_close.add(Dir.S)
    for wall in to_close:
        # intersection
        wallset = wallset & set(n for n in baseset if n & wall)
    for wall in to_open:
        # difference
        wallset = wallset - set(n for n in baseset if n & wall)
    return wallset


if __name__ == "__main__":
    test_grid = Matrix(13, 30)
    test_grid.pregen_maze()
    test_grid.debug_print_maze_metadata()
    gen_wall(test_grid)
    test_grid.debug_print_maze(bits=False)
