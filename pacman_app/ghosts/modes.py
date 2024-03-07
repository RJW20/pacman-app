from __future__ import annotations
import math


class Mode:
    """The mode of a ghost.
    
    Contains the total number of frames that the ghost will be in this 
    mode for and the mode the ghost will transition to if it lasts the 
    full duration.
    """

    @property
    def duration(self) -> int:
        return self._duration
    
    @duration.setter
    def duration(self, value: int) -> None:
        self._duration = value


    @property
    def next(self) -> Mode:
        return self._next
    
    @next.setter
    def next(self, value: Mode) -> None:
        self._next = value
        

CHASE = Mode()
SCATTER = Mode()
FRIGHTENED = Mode()
RETURN_TO_HOME = Mode()
INACTIVE = Mode()

CHASE.duration = 10000
CHASE.next = SCATTER

SCATTER.duration = 0
SCATTER.next = CHASE

FRIGHTENED.duration = 0
FRIGHTENED.next = CHASE

RETURN_TO_HOME.duration = math.inf
RETURN_TO_HOME.next = INACTIVE

INACTIVE.duration = 0
INACTIVE.next = CHASE
