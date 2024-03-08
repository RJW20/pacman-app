from math import sqrt

from pacman_app.map.direction import Vector


def distance_between(pos_1: tuple[int,int], pos_2: tuple[int,int]) -> float:
    """Return the straight-line distance between two tile positions.
    
    This is inline with how distance's were calculated in the original game.
    """

    return sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)

def vector_between(pos_1: tuple[int,int], pos_2: tuple[int,int]) -> Vector:
    """Return the vector that goes from pos_1 to pos_2."""

    return Vector(pos_2[0] - pos_1[0], pos_2[1] - pos_1[1])