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

    SCATTER = [400, 100, 500, 500]
    CHASE = [400, 100, 2000, math.inf]
    RETURN_TO_HOME = [math.inf]


FRIGTHENED_DURATION = 300
INACTIVE_DURATION = 10