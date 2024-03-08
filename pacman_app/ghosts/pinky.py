from pacman_app.ghosts.ghost import Ghost
from pacman_app.ghosts.mode import Mode
from pacman_app.map import Position, Direction


class Pinky(Ghost):
    """Ghost that targets 4 tiles in front of PacMan."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

        return self.pacman.position.tile_pos + self.pacman.direction.value * 4

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

        return (2, 0)

    def initialise(self) -> None:
        """Get in a state to start the game."""

        super().initialise()
        self.inactive = False