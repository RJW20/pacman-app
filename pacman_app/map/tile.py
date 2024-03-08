from enum import Enum


class Tile(Enum):
    """Types of tile on the map."""

    WALL = '|'
    PATH = '.'
    BLANK = '_'
    NODE = 'O'
    RESTRICTED_NODE = 'o'

    @property
    def is_node(self) -> bool:
        return self.name == 'NODE' or self.name == 'RESTRICTED_NODE'