from pacman_app.map.position import Position


class Fruit:
    """The fruit that appears after certain amount of pacdots are eaten."""

    first_threshold = 174
    second_threshold = 74
    position = Position((14, 20), (4, 0))

    def __init__(self) -> None:
        self.available: bool = False