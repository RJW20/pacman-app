from __future__ import annotations


class PositionCoordinate:
    """An x or y cooridinate for a character."""

    def __init__(self, absolute: int, relative: int) -> None:
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
        """Offset from the centre of a tile (values in [0,3])"""

        return self._relative

    @relative.setter
    def relative(self, value: int) -> None:
        """Ensure stays in range [0,3] and automatically update absolute."""

        self._relative = value % 4
        self._absolute += value // 4

    def __add__(self, value: int) -> PositionCoordinate:
        """Add value to self.relative (keeping it in it's range). absolute 
        will be automatically updated if neccessary."""

        relative = self.relative + value
        absolute = self.absolute + relative // 4
        relative = relative % 4
        return PositionCoordinate(absolute, relative)

    def __str__(self) -> str:
        return f'({self.absolute}: {self.relative})'