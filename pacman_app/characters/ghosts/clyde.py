import math

from pacman_app.characters.ghosts.ghost import Ghost
from pacman_app.map import vector_between


class Clyde(Ghost):
    """Ghost that's scared of PacMan."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

        vec = vector_between(self.position.tile_pos, self.pacman.position.tile_pos)

        if abs(vec.d_x) + abs(vec.d_y) > 8:
            return self.pacman.position.tile_pos
        else:
            return self.scatter_target

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

        return (0, 35)

    def initialise(self) -> None:
        """Get in a state to start the game."""

        super().initialise()
        self.inactive = True
        self.inactive_max = math.inf
        self.inactive_count = 0