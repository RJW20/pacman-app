from pacman_app.ghosts.ghost import Ghost
from pacman_app.map import MAP, Tile, Position, Direction


class Blinky(Ghost):
    """Ghost that directly targets pacman."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile position for use with astar."""

        return self.pacman.position.tile_pos

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

    def initialise(self) -> None:
        """Get in a state to start the game."""

        self.position = Position((13, 11), (5, 0), 9)
        self.direction = Direction.LEFT
