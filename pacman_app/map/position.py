from __future__ import annotations

from pacman_app.map.direction import Vector


class Position:
    """A point on the grid of tiles.
    
    tile_x, tile_y are the coordinates of the tile (0, 0 is the top left tile).
    offset_x, offset_y are the offset from the centre of the tile.
    All values will automatically update when the offset's are large enough to put 
    self in a different tile.
    Note that only one of offset_x, offset_y will ever be non_zero.
    """

    def __init__(self, tile_pos: tuple[int, int], offset: tuple[int,int], norm: int = 8):
        self._norm: int = norm
        self.tile_x: int = tile_pos[0]
        self.tile_y: int = tile_pos[1]
        self.offset_x: int = offset[0]
        self.offset_y: int = offset[1]

    @property
    def norm(self) -> int:
        """Number of offsets in a tile."""

        return self._norm
    
    @norm.setter
    def norm(self, value: int) -> None:
        """When norm changes adjust offset to still match the true position."""

        if self.offset_x != 0:
            self.offset_x = round(value * self.offset_x/self._norm)
        elif self.offset_y != 0:
            self.offset_y = round(value * self.offset_y/self._norm)

        self._norm = value

    @property
    def translator(self) -> int:
        """Used for keeping the offsets in their correct range."""

        return self.norm - self.norm//2 - 1

    @property
    def tile_x(self) -> int:
        return self._tile_x
    
    @tile_x.setter
    def tile_x(self, value: int) -> None:
        self._tile_x = value

    @property
    def tile_y(self) -> int:
        return self._tile_y
    
    @tile_y.setter
    def tile_y(self, value: int) -> None:
        self._tile_y = value

    @property
    def offset_x(self) -> int:
        """Horizontal offset from the centre of a tile (values in [norm//2 - norm + 1,norm//2])."""

        return self._offset_x

    @offset_x.setter
    def offset_x(self, value: int) -> None:
        """Ensure stays in range and automatically update tile_x."""

        self._offset_x = (value + self.translator) % self.norm - self.translator
        self._tile_x = (((self._tile_x + (value + self.translator) // self.norm) - 1) % 28) + 1

    @property
    def offset_y(self) -> int:
        """Vertical offset from the centre of a tile (values in [norm//2 - norm + 1,norm//2])."""

        return self._offset_y

    @offset_y.setter
    def offset_y(self, value: int) -> None:
        """Ensure stays in range and automatically update tile_y."""

        self._offset_y = (value + self.translator) % self.norm - self.translator
        self._tile_y = self._tile_y + (value + self.translator) // self.norm

    def __add__(self, other: Vector) -> Position:
        """Add to the offset values."""

        offset_x = self.offset_x + other.d_x
        tile_x = (self.tile_x + (offset_x + self.translator) // self.norm) % 28
        offset_x = (offset_x + self.translator) % self.norm - self.translator

        offset_y = self.offset_y + other.d_y
        tile_y = self.tile_y + (offset_y + self.translator) // self.norm
        offset_y = (offset_y + self.translator) % self.norm - self.translator

        return Position((tile_x, tile_y), (offset_x, offset_y), self.norm)
    
    @property
    def tile_pos(self) -> tuple[int,int]:
        """Tuple of tile_x, tile_y."""

        return self.tile_x, self.tile_y

    @property
    def true_x(self) -> float:
        """Float value representing x position.
        
        Note that true_x = 0 corresponds to the centre of tiles in the first column.
        """

        return self.tile_x + self.offset_x/self.norm
    
    @property
    def true_y(self) -> float:
        """Float value representing y position.
        
        Note that true_y = 0 corresponds to the centre of tiles in the first row.
        """
        
        return self.tile_y + self.offset_y/self.norm

    def __str__(self) -> str:
        return f'({self.tile_x}: {self.offset_x}, {self.tile_y}: {self.offset_y})'