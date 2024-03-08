from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Vector:
    """(d_x, d_y) vector."""

    d_x: int
    d_y: int

    def __mul__(self, other: int) -> Vector:
        return Vector(self.d_x * other, self.d_y * other)
    
    def __radd__(self, other: tuple[int,int]) -> tuple[int,int]:
        return other[0] + self.d_x, other[1] + self.d_y
    
    def __eq__(self, other: Vector) -> bool:
        return self.d_x == other.d_x and self.d_y == other.d_y


class Direction(Enum):
    """Possible directions for pacman to travel in."""

    UP = Vector(0, -1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)

    @property
    def reverse(self) -> bool:
        """Opposite direction."""

        return Direction(self.value * -1)

    def __eq__(self, other: Direction) -> bool:
        return self.value == other.value
