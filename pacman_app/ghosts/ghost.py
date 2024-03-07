from typing import Literal

from pacman_app.map import MAP, Tile, Position, Direction, distance_between
from pacman_app.pacman import PacMan
from pacman_app.ghosts.modes import Mode


class Ghost:
    """Base class for one of the ghosts that chase PacMan."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.position: Position
        self.direction: Direction
        self.scatter: bool
        self.scatter_chase_index: int
        self.scatter_chase_max: int
        self.scatter_chase_count: int
        self.fright_return_inactive_max: int
        self.fright_return_inactive_count: int

    @property
    def mode(self) -> Mode:
        return self._mode
    
    @mode.setter
    def mode(self, value: Mode) -> None:

        self._mode = value

        match(value):

            case Mode.SCATTER:

                #set/update index so get correct duration (only if we're already 'in' this mode)
                if not self.scatter:
                        self.scatter_chase_index += 1

                self.scatter_chase_max = self.mode.durations[self.scatter_chase_index]
                self.scatter_chase_count = 0
                self.scatter = True

            case Mode.CHASE:
                self.scatter_chase_max = self.mode.durations[self.scatter_chase_index]
                self.scatter_chase_count = 0
                self.scatter = False

            case Mode.FRIGHTENED | Mode.RETURN_TO_HOME | Mode.INACTIVE:
                self.fright_return_inactive_max = self.mode.durations[0]
                self.fright_return_inactive_count = 0

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

    @property
    def home_target(self) -> tuple[int,int]:
        """Return the Ghost's home target as tile coordinate."""

        return (13, 11)
    
    @property
    def target(self) -> tuple[int,int]:
        """Return the current target depending on the mode."""

        match(self.mode):
            case Mode.SCATTER:
                return self.scatter_target
            case Mode.CHASE:
                return self.chase_target
            case Mode.RETURN_TO_HOME:
                return self.home_target

    @property
    def on_new_tile(self) -> bool:
        """Return True if on centre of a tile.
        
        This indicates the Ghost has finished transitioning from one tile to another.
        """

        return self.position.offset_x == 0 and self.position.offset_y == 0
    
    def target_direction(self, target: tuple[int,int]) -> Direction:
        """Choose the direction that takes us closest to the current target.
        
        Cannot choose to reverse direction here.
        """

        #look up, right, down, left
        directions = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]
        choices = []
        for direction in directions:

            #ignore checking reverse direction
            if self.direction.reverse == direction:
                continue

            #check distance from tile in the direction to target
            tile_in_direction = (self.position + direction.value * self.position.norm).tile_pos
            if MAP[tile_in_direction] != Tile.WALL:
                distance = distance_between(target, tile_in_direction)
                choices.append((direction, distance))
        
        #choose direction with smallest distance to target
        choices.sort(key=lambda choice: choice[1])
        return choices[0][0]
    
    def update_counts(self) -> None:
        """Update the counters/maxs and change mode where appropriate."""

        match(self.mode):

            case Mode.SCATTER:
                self.scatter_chase_count += 1
                if self.scatter_chase_count == self.scatter_chase_max:
                    self.mode = Mode.CHASE

            case Mode.CHASE:
                self.scatter_chase_count += 1
                if self.scatter_chase_count == self.scatter_chase_max:
                    self.mode = Mode.SCATTER

            case Mode.FRIGHTENED:
                self.fright_return_inactive_count += 1
                if self.fright_return_inactive_count == self.fright_return_inactive_max:
                    if self.scatter:
                        self.mode = Mode.SCATTER
                    else:
                        self.mode = Mode.CHASE

            case Mode.RETURN_TO_HOME | Mode.INACTIVE:
                self.fright_return_inactive_count += 1
                self.scatter_chase_count += 1
                if self.scatter_chase_count == self.scatter_chase_max:
                    self.scatter = not self.scatter
                if self.fright_return_inactive_count == self.fright_return_inactive_max:
                    if self.scatter:
                        self.mode = Mode.SCATTER
                    else:
                        self.mode = Mode.CHASE

    def move(self) -> None:
        """Set Ghost's direction and move in it.
        
        The Ghost's mode for this frame has already been set on the last frame.
        """

        #only ever change direction on new tiles
        if self.on_new_tile:

            match(self.mode):

                case Mode.SCATTER | Mode.CHASE | Mode.RETURN_TO_HOME:

                    if MAP[self.position] == Tile.NODE:
                        self.direction = self.target_direction(self.target)

        #move
        self.position += self.direction.value

        #update counts (and hence self.mode)
        self.update_counts()

        #check if hit by pacman or made it to home etc and set next mode