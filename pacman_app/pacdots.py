from pacman_app.map import MAP
from pacman_app import PacMan


class PacDots:
    """The dots the PacMan eats."""

    def __init__(self) -> None:
        self.dots: set[tuple[int,int]] = set()
        self.power_dots: set[tuple[int,int]] = set()
        for j, line in enumerate(MAP.grid):
            for i, tile in enumerate(line):
                if tile.is_dot:
                    self.dots.add((i,j))
                elif tile.is_power_dot:
                    self.power_dots.add((i,j))

    @property
    def remaining(self) -> int:
        """Return the number of dots and powered dots left."""
        return len(self.dots) + len(self.power_dots)

    def check_if_eaten(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a pacdot.
        
        Also remove that pacdot from self.dots.
        """

        if not pacman.on_new_tile:
            return False

        if pacman.position.tile_pos in self.dots:
            self.dots.remove(pacman.position.tile_pos)
            return True

        return False 
    
    def check_if_powered(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a powered pacdot.
        
        Also remove that pacdot from self.power_dots.
        """

        if not pacman.on_new_tile:
            return False

        if pacman.position.tile_pos in self.power_dots:
            self.power_dots.remove(pacman.position.tile_pos)
            return True

        return False 