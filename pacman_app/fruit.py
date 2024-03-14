from pacman_app.map.position import Position


class Fruit:
    """The fruit that appears after certain amount of pacdots are eaten."""

    first_threshold = 174
    second_threshold = 74
    position = Position((14, 20), (4, 0))
    available_duration = 540

    def __init__(self) -> None:
        self._available: bool = False
        self.available_countdown: int

    @property
    def available(self) -> bool:
        """Return True if fruit can be eaten."""

        return self._available
    
    @available.setter
    def available(self, value: bool) -> None:

        self._available = value
        if value:
            self.available_countdown = self.available_duration