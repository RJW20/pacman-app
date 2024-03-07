from enum import Enum
import math


class Mode(Enum):
    """The mode of a ghost.
    
    Contains the total number of frames that the ghost will be in this 
    mode for and the id of the mode the ghost will transition to if it lasts the 
    full duration.
    """

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
    
    def __init__(self, duration: int | float, next_id: int):
        self.duration = duration
        self.next_id = next_id

    CHASE = 10000, 2
    SCATTER = 2000, 1
    RETURN_TO_HOME = math.inf, 1