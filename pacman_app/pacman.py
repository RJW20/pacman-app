from pacman_app.map import MAP, Tile, Position, Direction


class PacMan:
    """The playable character."""

    def __init__(self) -> None:
        self.position: Position
        self.direction: Direction
        self.score: int

    def initialise(self) -> None:
        """Get in a state to start the game."""

        self.score = 0
        self.position = Position((13, 26), (4, 0), 8)
        self.direction = Direction.LEFT

    def can_move_in_direction(self, direction: Direction) -> bool:
        """Return True if moving in the given direction is a valid move."""

        #if transitioning between two tiles
        if direction == Direction.RIGHT or direction == Direction.LEFT:
            if self.position.offset_x != 0:
                return True
            elif self.position.offset_y != 0:
                return False
        else:
            if self.position.offset_y != 0:
                return True
            elif self.position.offset_x != 0:
                return False
            
        #check if the tile in given direction is wall
        if MAP[self.position + direction.value * self.position.norm] != Tile.WALL:
            return True
        
        return False

    def move(self, move: Direction) -> None:
        """Move PacMan in the given direction if possible, otherwise continue."""

        if self.can_move_in_direction(move):
            self.direction = move
            self.position += self.direction.value
        else:
            if move != self.direction and self.can_move_in_direction(self.direction):
                self.position += self.direction.value

    def collided_with(self, ghost) -> bool:
        """Return True if ghost is sufficiently close to PacMan.
        
        The original definition is to return True when their centre's are on the same tile.
        ghost is of type .ghosts.ghost.Ghost but type hint requires cyclical import.
        """

        return self.position.tile_pos == ghost.position.tile_pos
    
    def kill(self) -> None:
        """Kill PacMan."""

        pass