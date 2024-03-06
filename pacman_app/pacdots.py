from math import isclose

from pacman_app.map import Map, Tile
from pacman_app import PacMan


class PacDots:
    """The dots the PacMan eats."""

    def __init__(self, map: Map) -> None:
        self.dots: list[tuple[int,int]] = []
        for j, line in enumerate(map.grid):
            for i, tile in enumerate(line):
                if tile == Tile.PATH:
                    self.dots.append((i,j))

    def __getitem__(self, index: int) -> tuple[int,int]:
        return self.dots[index]
    
    def check_if_eaten(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a pacdot.
        
        Also remove that pacdot from self.dots.
        """

        for dot in self.dots:
            if isclose(pacman.position.true_x, dot[0]) and \
               isclose(pacman.position.true_y, dot[1]):
                self.dots.remove(dot)
                return True

        return False 
