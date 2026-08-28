#!/usr/bin/env python3
from enum import IntFlag
import random

from ._cell import Cell


class Wallset:
    BASESET = frozenset((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))
    PERFECTSET = frozenset((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14))


class Dir(IntFlag):
    N = 1  # 0b0001
    E = 2  # 0b0010
    S = 4  # 0b0100
    W = 8  # 0b1000
    # max (all close) = 15


class Maze:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.x_max = width - 1
        self.y_max = height - 1
        self.grid: list[list[Cell]] = [
            [Cell(x ,y) for x in range(self.width)]
            for y in range(self.height)]

    def pregen_maze(self) -> None:
        """"define constraint before generating maze"""
        # TODO: add logo logic
        for y in range(self.height):
            for x in range(self.width):
                border = False
                logo = False
                # border
                if (y == 0 or
                        x == 0 or
                        y == self.y_max or
                        x == self.x_max):
                    border = True
                self.grid[y][x] = Cell(x, y, border=border, logo=logo)
