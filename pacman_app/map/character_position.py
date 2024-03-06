from __future__ import annotations

from pacman_app.map.position_coordinate import PositionCoordinate
from pacman_app.map.direction import Vector


class CharacterPosition:
    """A pair of x, y values representing the position of a character."""

    def __init__(self, position: tuple[int,int], offset: tuple[int,int], norm: int) -> None:
        self.x: PositionCoordinate = PositionCoordinate(position[0], offset[0], norm, loop=True)
        self.y: PositionCoordinate = PositionCoordinate(position[1], offset[1], norm)
        self.norm: int = norm

    def __add__(self, vector: Vector) -> CharacterPosition:
        diff_x = self.x + vector.d_x
        diff_y = self.y + vector.d_y
        return CharacterPosition((diff_x.absolute, diff_y.absolute), (diff_x.relative, diff_y.relative), self.norm)
    
    def __str__(self) -> str:
        return f"({self.x!s}, {self.y!s})"
    
    @property
    def true_x(self) -> float:
        return self.x.absolute + self.x.relative/self.norm
    
    @property
    def true_y(self) -> float:
        return self.y.absolute + self.y.relative/self.norm