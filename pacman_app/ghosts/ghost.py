from pacman_app.map import MAP, Tile, Position, Direction, distance_between
from pacman_app.pacman import PacMan
from pacman_app.ghosts.modes import Mode


class Ghost:
    """Base class for one of the ghosts that chase PacMan."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.position: Position
        self.direction: Direction
        self.mode: Mode
        self.chase_scatter_count: int

    @property
    def chase_target(self) -> tuple[int,int]:
        """Return the Ghost's chase target as tile coordinate."""

    @property
    def scatter_target(self) -> tuple[int,int]:
        """The Ghost's corner tile it retreats to during scatter mode."""

    @property
    def home_target(self) -> tuple[int,int]:
        """Return the Ghost's home target as tile coordinate."""

        return (13, 11)
    
    @property
    def target(self) -> tuple[int,int]:
        """Return the current target depending on the mode."""

        match(self.mode):
            case Mode.CHASE:
                return self.chase_target
            case Mode.SCATTER:
                return self.scatter_target
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

    def move(self) -> None:
        """Set Ghost's direction and move in it."""

        if not self.on_new_tile or not MAP[self.position] == Tile.NODE:
            self.position += self.direction.value
            return
        
        #add some check to see if hit pacman or if should be frightened
        #probably will set to frightened elsewhere so second part fine
        
        self.direction = self.target_direction(self.target)

        self.position += self.direction.value