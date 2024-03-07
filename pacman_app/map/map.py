from functools import cached_property

from pacman_app.map.tile import Tile
from pacman_app.map.position import Position


class Map:
    """Array with entries from map.txt.
    
    We convert the entries to instances of the Tile enumeration.
    """

    @cached_property
    def grid(self) -> list[list[str]]:
        """Table containing the tiles."""

        grid = []
        with open('resources/map.txt', 'r') as map_as_txt:
            for line in map_as_txt:
                grid.append([Tile(char) for char in line if char != '\n'])
        return grid
    
    def __getitem__(self, index: Position | tuple[int, int]):
        """Return the tile at the given index.
        
        If index is a CharacterPosition then will return the tile at the absolute x, y values.
        """

        if isinstance(index, Position):
            index = index.tile_pos

        return self.grid[index[1]][index[0]]