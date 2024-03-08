import random

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

        if value:
            self.scatter_chase_max = Mode.SCATTER.durations[self.scatter_chase_index]
        else:
            self.scatter_chase_max = Mode.CHASE.durations[self.scatter_chase_index]
            self.scatter_chase_index += 1

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
                if not self.scatter:
                    self.scatter = True
                self.reverse_next = True

            case Mode.CHASE:
                if self.scatter:
                    self.scatter = False
                self.reverse_next = True

            case Mode.FRIGHTENED:
                self.fright_inactive_max = self._mode.durations[0]
                self.fright_inactive_count = 0
                self.reverse_next = True

            case Mode.RETURN_TO_HOME:
                pass

            case Mode.INACTIVE:
                self.fright_inactive_max = self._mode.durations[0]
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

        return (13, 14)
    
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
    
    def target_direction(self,
                         target: tuple[int,int],
                         available_moves: list[Direction],
                         current_tile: Tile
                         ) -> Direction:
        """Choose the direction that takes us closest to the current target.
        
        Cannot choose to reverse direction here.
        """

        choices = []
        for direction in available_moves:

            #ignore up direction if on one of the 4 restricted nodes
            if current_tile == Tile.RESTRICTED_NODE and direction == direction.UP:
                continue

            #check distance from tile in the direction to target
            tile_in_direction = self.position.tile_pos + direction.value
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
                if self.position.tile_pos == self.target and self.on_new_tile:
                    self.mode = Mode.INACTIVE

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

                elif (current_tile := MAP[self.position.tile_pos]).is_node:

                    available_moves = MAP.available_moves(self.position.tile_pos)
                    available_moves.remove(self.direction.reverse)

                    match(self.mode):

                        case Mode.SCATTER | Mode.CHASE | Mode.RETURN_TO_HOME:
                            self.direction = self.target_direction(self.target, available_moves, current_tile)

                        case Mode.FRIGHTENED:
                            self.direction = random.choice(available_moves)
                            
            #move
            self.position += self.direction.value

        #update counts and change mode if needed
        self.check_mode()

        #check if hit pacman
        if self.pacman.collided_with(self):
            if self.mode == Mode.FRIGHTENED:
                self.mode = Mode.RETURN_TO_HOME
            elif self.mode == Mode.SCATTER or self.mode == Mode.CHASE:
                self.mode = Mode.RETURN_TO_HOME
                #self.pacman.kill()