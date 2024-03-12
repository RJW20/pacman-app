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

    @property
    def remaining(self) -> int:
        """Return the number of dots and powered dots left."""
        return len(self.dots) + len(self.power_dots)

    def check_if_eaten(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a pacdot.
        
        Also remove that pacdot from self.dots.
        """

        for dot in self.dots:
            if pacman.on_new_tile and pacman.position.tile_pos == dot:
                self.dots.remove(dot)
                return True

        return False 
    
    def check_if_powered(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a powered pacdot.
        
        Also remove that pacdot from self.power_dots.
        """

        for dot in self.power_dots:
            if pacman.on_new_tile and pacman.position.tile_pos == dot:
                self.power_dots.remove(dot)
                return True
            
        return False 