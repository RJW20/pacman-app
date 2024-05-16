from pacman_app.map import Position, Direction
from pacman_app.characters.speed import Speed


class Character:
    """Base class for PacMan or Ghost."""

    def __init__(self) -> None:
        self.position: Position
        self.direction: Direction
        self.step_size: int

    @property
    def speed(self) -> Speed:
        return self._speed
    
    @speed.setter
    def speed(self, value: Speed) -> None:
        self._speed = value
        self._speed_count = 0

    @property
    def on_new_tile(self) -> bool:
        """Return True if on centre of a tile.
        
        This indicates the character has finished transitioning from one tile to another.
        Note we ignore times when the previous step size was zero, as we will have already 
        accounted for this instance of being here.
        """

        return self.position.offset_x == 0 and self.position.offset_y == 0 and \
            self.step_size != 0

    def move(self) -> None:
        """Update position using direction and speed."""

        self.step_size = int(self.speed.step_sizes[self._speed_count])
        offset_x = self.position.offset_x
        offset_y = self.position.offset_y
        x_change = self.direction.value.d_x
        y_change = self.direction.value.d_y

        #ensure land on node centers
        if self.step_size == 2:
            if x_change == 1 and offset_x == -1 or \
               x_change == -1 and offset_x == 1 or \
               y_change == 1 and offset_y == -1 or \
               y_change == -1 and offset_y == 1:
                self.step_size = 1

        self.position += self.direction.value * self.step_size
        self._speed_count = (self._speed_count + 1) % 16