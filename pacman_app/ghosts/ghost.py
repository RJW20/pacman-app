from typing import Literal

from pacman_app.map import MAP, Tile, Position, Direction, distance_between
from pacman_app.pacman import PacMan
from pacman_app.ghosts.mode import Mode


class Ghost:
    """Base class for one of the ghosts that chase PacMan."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.position: Position
        self.direction: Direction
        self.reverse_next: bool
        self.scatter: bool
        self.scatter_chase_index: int
        self.scatter_chase_max: int
        self.scatter_chase_count: int
        self.fright_inactive_max: int
        self.fright_inactive_count: int

    @property
    def scatter(self) -> bool:
        """Return True if we are (or would be if not returning to home or inactive) in SCATTER mode."""
        
        return self._scatter
    
    @scatter.setter
    def scatter(self, value: bool) -> bool:

        if not value:
            self.scatter_chase_index += 1
            self.scatter_chase_max = Mode.SCATTER.durations[self.scatter_chase_index]
        else:
            self.scatter_chase_max = Mode.CHASE.durations[self.scatter_chase_index]

        self.scatter_chase_count = 0
        self._scatter = value


    @property
    def mode(self) -> Mode:
        return self._mode
    
    @mode.setter
    def mode(self, value: Mode) -> None:

        self._mode = value

        match(value):

            case Mode.SCATTER:
                self.scatter = True
                self.reverse_next = True

            case Mode.CHASE:
                self.scatter = False
                self.reverse_next = True

            case Mode.FRIGHTENED:
                self.fright_inactive_max = self.mode.durations[0]
                self.fright_inactive_count = 0
                self.reverse_next = True

            case Mode.RETURN_TO_HOME | Mode.INACTIVE:
                self.fright_inactive_max = self.mode.durations[0]
                self.fright_inactive_count = 0

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

        if self.mode == Mode.RETURN_TO_HOME:
            return self.home_target
        if self.scatter:
            return self.scatter_target
        else:
            return self.chase_target

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
    
    def check_mode(self) -> None:
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
                self.fright_inactive_count += 1
                if self.fright_inactive_count == self.fright_inactive_max:
                    if self.scatter:
                        self.mode = Mode.SCATTER
                    else:
                        self.mode = Mode.CHASE

            case Mode.RETURN_TO_HOME:
                self.scatter_chase_count += 1
                if self.scatter_chase_count == self.scatter_chase_max:
                    self.scatter = not self.scatter

            case Mode.INACTIVE:
                self.fright_inactive_count += 1
                self.scatter_chase_count += 1
                if self.scatter_chase_count == self.scatter_chase_max:
                    self.scatter = not self.scatter
                if self.fright_inactive_count == self.fright_inactive_max:
                    if self.scatter:
                        self.mode = Mode.SCATTER
                    else:
                        self.mode = Mode.CHASE

    def move(self) -> None:
        """Set Ghost's direction and move in it.
        
        The Ghost's mode for this frame has already been set on the last frame.
        """

        if not self.mode == Mode.INACTIVE:

            #only ever change direction on new tiles
            if self.on_new_tile:

                #carry out a forced reversal
                if self.reverse_next:
                    self.direction = self.direction.reverse
                    self.reverse_next = False

                else:

                    match(self.mode):

                        case Mode.SCATTER | Mode.CHASE | Mode.RETURN_TO_HOME:

                            if MAP[self.position] == Tile.NODE:
                                self.direction = self.target_direction(self.target)

                        case Mode.FRIGHTENED:
                            #move randomly including up on yellow nodes
                            pass

            #move
            self.position += self.direction.value

        #update counts and change mode if needed
        self.check_mode()

        #check if made it home
        if self.mode == Mode.RETURN_TO_HOME:
            if self.position.tile_pos == self.target and self.on_new_tile:
                self.mode = Mode.INACTIVE
        else:
            #check if hit pacman
            if self.pacman.collided_with(self):
                if self.mode == Mode.FRIGHTENED:
                    self.mode = Mode.RETURN_TO_HOME
                elif self.mode == Mode.SCATTER or self.mode == Mode.CHASE:
                    self.mode = Mode.RETURN_TO_HOME
                    #self.pacman.kill()