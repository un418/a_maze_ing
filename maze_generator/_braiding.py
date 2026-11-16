from ._maze import Maze
from ._cell import Cell

class braiding():

    def __init__(self, maze: Maze):
        self.maze = maze
    

    def braider(self):
        
        dead_ends: list[int] = [14, 13, 11, 7] # all 3 closed wall combos: 1110/1101/1011/0111
        grid: list[list[Cell]] = self.maze.grid

        for row in grid:
            for cell in row:
                if cell.wall in dead_ends:

