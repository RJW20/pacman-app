from math import sqrt


def distance_between(pos_1: tuple[int,int], pos_2: tuple[int,int]) -> float:
    """Return the straight-line distance between two tile positions.
    
    This is inline with how distance's were calculated in the original game.
    """

    return sqrt((pos_1[0] - pos_2[0]) ** 2 + (pos_1[1] - pos_2[1]) ** 2)