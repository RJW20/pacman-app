import math

from pacman_app.ghosts.ghost import Ghost
from pacman_app.map import vector_between


class Inky(Ghost):
    """Ghost that uses Blinky to ambush PacMan."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

        return self.pacman.position.tile_pos + \
            vector_between(self.blinky.position.tile_pos, self.pacman.position.tile_pos)

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

        return (27, 35)

    def initialise(self, blinky: Ghost) -> None:
        """Get in a state to start the game."""

        self.blinky = blinky
        super().initialise()
        self.inactive = True
        self.inactive_max = math.inf
        self.inactive_count = 0