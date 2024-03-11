from pacman_app.characters.ghosts.ghost import Ghost


class Blinky(Ghost):
    """Ghost that directly targets PacMan."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

        return self.pacman.position.tile_pos

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

        return (25, 0)

    def initialise(self) -> None:
        """Get in a state to start the game."""

        super().initialise()
        self.inactive = False