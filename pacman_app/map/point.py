from __future__ import annotations

from pacman_app.map.direction import Direction


class Point:
    """(x, y) point."""

    def __init__(self) -> None:
        self.x: int
        self.y: int

    def __add__(self, other: Direction) -> Point:
        diff_x = self.x + other.value.d_x
        diff_y = self.y + other.value.d_y
        return Point(diff_x, diff_y)
    
    def __eq__(self, other: Point) -> bool:
        return self.x == other.x and self.y == other.y