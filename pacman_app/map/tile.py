from enum import Enum


class Tile(Enum):
    """Types of tile on the map."""

    WALL = '|'
    BLANK = '_'
    DOT_NO_NODE = '0'
    POWER_DOT_NO_NODE = '1'
    NODE_DOT = '2'
    NODE_POWER_DOT = '3'
    RESTRICTED_NODE_DOT = '4'
    NODE_NO_DOT = '5'
    RESTRICTED_NODE_NO_DOT = '6'

    @property
    def is_restricted_node(self) -> bool:
        return self == Tile.RESTRICTED_NODE_DOT or self == Tile.RESTRICTED_NODE_NO_DOT

    @property
    def is_node(self) -> bool:
        return self.is_restricted_node or self == Tile.NODE_DOT or self == Tile.NODE_NO_DOT \
            or self == Tile.NODE_POWER_DOT

    @property
    def is_power_dot(self) -> bool:
        return self == Tile.POWER_DOT_NO_NODE or self == Tile.NODE_POWER_DOT
    
    @property
    def is_dot(self) -> bool:
        return self == Tile.DOT_NO_NODE or self == Tile.NODE_DOT or self == Tile.RESTRICTED_NODE_DOT