from pacman_app.map import Position, Direction
from pacman_app.characters.speed import Speed


class Character:
    """Base class for PacMan or Ghost."""

    def __init__(self) -> None:
        self.position: Position
        self.direction: Direction

    @property
    def speed(self) -> Speed:
        return self._speed
    
    @speed.setter
    def speed(self, value: Speed) -> None:
        self._speed = value
        self._speed_count = 0

    def move(self) -> None:
        """Update position using direction and speed."""

        self.position += self.direction.value * int(self.speed.step_sizes[self._speed_count])
        self._speed_count = (self._speed_count + 1) % 16