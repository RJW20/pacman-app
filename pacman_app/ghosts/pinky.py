from pacman_app.ghosts.ghost import Ghost
from pacman_app.ghosts.mode import Mode
from pacman_app.map import MAP, Tile, Position, Direction


class Pinky(Ghost):
    """Ghost targets 4 tiles in front of PacMan."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

        return self.pacman.position.tile_pos + self.pacman.direction.value * 4

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

        return (1, 1)

    def initialise(self) -> None:
        """Get in a state to start the game."""

        self.position = Position((13, 11), (4, 0), 9)
        self.direction = Direction.LEFT
        self.scatter_chase_index = 0
        self.mode = Mode.SCATTER
        self.reverse_next = False