from __future__ import annotations


class PositionCoordinate:
    """An x or y coordinate for a character.
    
    We assign a norm that tells us how many frames it takes to move from one
    grippoint to another. loop tells us whether to loop the absolute values 
    when we reach the max value."""

    def __init__(self, absolute: int, relative: int, norm: int, loop: bool = False, max: int = 28) -> None:
        self.norm: int = norm
        self.loop = loop
        self.max = max
        self.absolute: int = absolute
        self.relative: int = relative

    @property
    def absolute(self) -> int:
        """Integer position that matches with a tile on the map."""

        return self._absolute
    
    @absolute.setter
    def absolute(self, value: int) -> None:
        self._absolute = value

    @property
    def relative(self) -> int:
        """Offset from the centre of a tile (values in [0,self.norm-1])"""

        return self._relative

    @relative.setter
    def relative(self, value: int) -> None:
        """Ensure stays in range [0,self.norm-1] and automatically update absolute."""

        self._relative = value % self.norm
        self._absolute = self._absolute + value // self.norm
        if self.loop:
            self._absolute = self._absolute % self.max

    def __add__(self, value: int) -> PositionCoordinate:
        """Add value to self.relative (keeping it in it's range). absolute 
        will be automatically updated if neccessary."""

        relative = self.relative + value
        absolute = self.absolute + relative // self.norm
        if self.loop:
            absolute = absolute % self.max
        relative = relative % self.norm
        return PositionCoordinate(absolute, relative, self.norm)

    def __str__(self) -> str:
        return f'({self.absolute}: {self.relative})'