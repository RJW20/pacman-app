from enum import Enum


class Tile(Enum):
    """Types of tile on the map."""

    WALL = '|'
    PATH = '.'
    BLANK = '_'