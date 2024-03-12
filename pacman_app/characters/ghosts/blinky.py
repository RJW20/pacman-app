from typing import Literal

from pacman_app.characters.ghosts.ghost import Ghost
from pacman_app.characters.speed import Speed


class Blinky(Ghost):
    """Ghost that directly targets PacMan."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

        return self.pacman.position.tile_pos

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

        return (26, 0)

    def initialise(self) -> None:
        """Get in a state to start the game."""

        super().initialise()
        self.inactive = False
        self.elroy = 0

    @property
    def elroy(self) -> None:
        return self._elroy
    
    @elroy.setter
    def elroy(self, value: Literal[0,1,2]) -> None:
        """Set to correct speed if change in elroy stage."""

        self._elroy = value

        match(value):
            #only set this value at the beginning or restart
            case 0:
                self.speed = Speed.GHOST_NORMAL
            case 1:
                self.speed = Speed.ELROY_1
            case 2:
                self.speed = Speed.ELROY_2
            case _:
                raise Exception(f"Invalid elroy mode {value}")