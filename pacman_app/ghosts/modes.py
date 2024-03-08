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
        self.durations = durations

    SCATTER = [200, 200, 500, 500]
    CHASE = [1000, 200, 2000, math.inf]
    FRIGHTENED = [2000]
    RETURN_TO_HOME = [math.inf]
    INACTIVE = 4000