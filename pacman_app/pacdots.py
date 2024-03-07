from math import isclose

from pacman_app.map import MAP, Tile
from pacman_app import PacMan


class PacDots:
    """The dots the PacMan eats."""

    def __init__(self) -> None:
        self.dots: list[tuple[int,int]] = []
        for j, line in enumerate(MAP.grid):
            for i, tile in enumerate(line):
                if tile == Tile.PATH or tile == Tile.NODE:
                    self.dots.append((i,j))

    def __getitem__(self, index: int) -> tuple[int,int]:
        return self.dots[index]
    
    def check_if_eaten(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a pacdot.
        
        Also remove that pacdot from self.dots.
        """

        for dot in self.dots:
            if abs(pacman.position.true_x - dot[0]) < 0.15 and \
               abs(pacman.position.true_y - dot[1]) < 0.15:
                self.dots.remove(dot)
                return True

        return False 
