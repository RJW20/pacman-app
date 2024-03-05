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


class Direction(Enum):
    """Possible directions for pacman to travel in."""

    UP = Vector(0, -1)
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)