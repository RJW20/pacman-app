from functools import cached_property

from pacman_app.map.tile import Tile
from pacman_app.map.direction import Direction


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
    
    def __getitem__(self, index: tuple[int,int]) -> Tile:
        """Return the tile at the given index.
        
        If index is a CharacterPosition then will return the tile at the absolute x, y values.
        """

        return self.grid[index[1]][index[0]]
    
    def available_moves(self, index: tuple[int,int]) -> list[Direction]:
        """Return the directions from the given index that are path tiles.
        
        If index refers to a restricted node then the restricted move will still be 
        returned here.
        The options will be returned in UP, LEFT, DOWN, RIGHT preference as in the 
        original.
        """

        directions = [Direction.UP, Direction.LEFT, Direction.DOWN, Direction.RIGHT]
        available = [direction for direction in directions if self[index + direction.value] != Tile.WALL]

        return available