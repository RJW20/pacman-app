from pacman_app.ghosts.ghost import Ghost
from pacman_app.map import MAP, Tile, Position, Direction


class Blinky(Ghost):

    def initialise(self) -> None:

        """Get self in a state to start the game."""
        self.position = Position((13, 11), (5, 0), 9)
        self.direction = Direction.LEFT