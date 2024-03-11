from enum import Enum

class Speed(Enum):
    """Character speeds represented by list of 16 values.
    
    Each value is the number of steps to take in a frame.
    When we reach the end we cycle back to the beginning.
    """

    PACMAN_NORMAL = '1111111111111111'
    PACMAN_FRIGHT = '1111211111112111'
    GHOST_NORMAL = '0111111111111111'
    GHOST_FRIGHT = '0110110101101101'
    GHOST_RETURN = '2222222222222222'
    GHOST_TUNNEL = '0101010101010101'
    ELROY_1 = '1111111111111111'
    ELROY_2 = '1111111121111111'

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj
    
    def __init__(self, step_sizes: str):
        self.step_sizes = step_sizes