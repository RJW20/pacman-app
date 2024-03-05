from typing import Literal

from pacman_app.map import CharacterPosition, Direction


class PacMan:
    """The playable character."""

    def __init__(self) -> None:
        self.position: CharacterPosition
        self.direction: Direction
        self.score: int

    def initialise(self) -> None:
        """Get self in a state to start the game."""

        self.score = 0
        self.position = CharacterPosition((13, 23), (2,0))
        self.direction = Direction.LEFT

    def move(self, move: Literal['up', 'right', 'down', 'left']) -> None:

        match(move):
            case 'up':
                self.direction = Direction.UP
            case 'right':
                self.direction = Direction.RIGHT
            case 'down':
                self.direction = Direction.DOWN
            case 'left':
                self.direction = Direction.LEFT


        self.position += self.direction