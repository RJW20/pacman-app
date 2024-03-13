from enum import Enum
from typing import Iterator
import math


class Mode(Enum):
    """The mode of a ghost.
    
    Contains the total number of frames that the ghost will be in this 
    mode for.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
    
    def __init__(self, durations: list[int | float]):
        self.DURATIONS = durations

    SCATTER = [420, 420, 300, 300]
    CHASE = [1200, 1200, 1200, math.inf]
    RETURN_TO_HOME = [math.inf]


FRIGHTENED_DURATION = 360
INACTIVE_DURATION = 60