from math import isclose

from pacman_app.map import MAP, Tile
from pacman_app import PacMan


class PacDots:
    """The dots the PacMan eats."""

    def __init__(self) -> None:
        self.dots: list[tuple[int,int]] = []
        self.power_dots: list[tuple[int,int]] = []
        for j, line in enumerate(MAP.grid):
            for i, tile in enumerate(line):
                if tile.is_dot:
                    self.dots.append((i,j))
                elif tile.is_power_dot:
                    self.power_dots.append((i,j))

    def check_if_eaten(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a pacdot.
        
        Also remove that pacdot from self.dots.
        """

        for dot in self.dots:
            if abs(pacman.position.true_x - dot[0]) < 0.15 and \
               abs(pacman.position.true_y - dot[1]) < 0.15:
                self.dots.remove(dot)
                return True
            
        for dot in self.power_dots:
            if abs(pacman.position.true_x - dot[0]) < 0.15 and \
               abs(pacman.position.true_y - dot[1]) < 0.15:
                self.power_dots.remove(dot)
                return True

        return False 
