from enum import Enum


class Tile(Enum):
    """Types of tile on the map."""

    WALL = '|'
    DOT = '0'
    POWER_DOT = '8'
    BLANK = '_'
    NODE = 'O'
    RESTRICTED_NODE = 'o'
    NODE_NO_FOOD = '.'
    NODE_POWER_DOT = '9'

    @property
    def is_node(self) -> bool:
        return self.name == 'NODE' or self.name == 'RESTRICTED_NODE' or \
               self.name == 'NODE_NO_FOOD' or self.name == 'NODE_POWER_DOT'
    
    @property
    def is_dot(self) -> bool:
        return self.name == 'DOT' or self.name == 'NODE' or self.is_power_dot
    
    @property
    def is_power_dot(self) -> bool:
        return self.name == 'POWER_DOT' or self.name == 'NODE_POWER_DOT'