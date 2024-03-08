import random

from pacman_app.map import MAP, Tile, Position, Direction, distance_between
from pacman_app.pacman import PacMan
from pacman_app.ghosts.mode import Mode


class Ghost:
    """Base class for one of the ghosts that chase PacMan."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.mode: Mode
        self.position: Position
        self.direction: Direction
        self.reverse_next: bool
        self.frightened: bool
        self.inactive: bool
        self.inactive_max: int
        self.inactive_count: int

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

        match(self.mode):
            case Mode.SCATTER:
                return self.scatter_target
            case Mode.CHASE:
                return self.chase_target
            case Mode.RETURN_TO_HOME:
                return self.home_target
        
    @property
    def made_it_home(self) -> bool:
        """Return True if on the home entrace tile."""

        return self.position.tile_pos == self.home_target and self.position.offset_x == self.position.norm//2

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

    def move(self) -> None:
        """Set Ghost's direction and move in it.
        
        The Ghost's mode for this frame has already been set on the last frame.
        """

        if not self.inactive:

            #only ever change direction on new tiles
            if self.on_new_tile:

                #carry out a forced reversal
                if self.reverse_next:
                    self.direction = self.direction.reverse
                    self.reverse_next = False

                #pick new direction if on a node
                elif (current_tile := MAP[self.position.tile_pos]).is_node:

                    available_moves = MAP.available_moves(self.position.tile_pos)
                    available_moves.remove(self.direction.reverse)

                    if not self.frightened:
                        self.direction = self.target_direction(self.target, available_moves, current_tile)
                    else:
                        self.direction = random.choice(available_moves)
                            
            #move
            self.position += self.direction.value