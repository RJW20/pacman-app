from pacman_app.map import MAP
from pacman_app import PacMan


class PacDots:
    """The dots the PacMan eats."""

    def __init__(self) -> None:
        self.dots: dict[int, list[int]] = dict()
        self.power_dots: dict[int, list[int]] = dict()
        for j, line in enumerate(MAP.grid):
            for i, tile in enumerate(line):
                if tile.is_dot:
                    try:
                        self.dots[i].append(j)
                    except KeyError:
                        self.dots[i] = [j]
                elif tile.is_power_dot:
                    try:
                        self.power_dots[i].append(j)
                    except KeyError:
                        self.power_dots[i] = [j]

    @property
    def remaining(self) -> int:
        """Return the number of dots and powered dots left."""
        return sum(len(value) for value in self.dots.values()) + sum(len(value) for value in self.power_dots.values())

    def check_if_eaten(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a pacdot.
        
        Also remove that pacdot from self.dots.
        """

        if not pacman.on_new_tile:
            return False

        try:
            possible_dots = self.dots[pacman.position.tile_x]
        except KeyError:
            return False
        
        for dot_y in possible_dots:
            if pacman.position.tile_y == dot_y:
                self.dots[pacman.position.tile_x].remove(dot_y)
                return True

        return False 
    
    def check_if_powered(self, pacman: PacMan) -> bool:
        """Return True if pacman is considered to have eaten a powered pacdot.
        
        Also remove that pacdot from self.power_dots.
        """

        if not pacman.on_new_tile:
            return False

        try:
            possible_dots = self.power_dots[pacman.position.tile_x]
        except KeyError:
            return False
        
        for dot_y in possible_dots:
            if pacman.position.tile_y == dot_y:
                self.power_dots[pacman.position.tile_x].remove(dot_y)
                return True

        return False 