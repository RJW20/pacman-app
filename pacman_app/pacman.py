from pacman_app.map import Map, Tile, CharacterPosition, Direction


class PacMan:
    """The playable character."""

    def __init__(self, map: Map) -> None:
        self.map: Map = map
        self.position: CharacterPosition
        self.direction: Direction
        self.score: int

    def initialise(self) -> None:
        """Get self in a state to start the game."""

        self.score = 0
        self.position = CharacterPosition((13, 23), (4,0), 8)
        self.direction = Direction.LEFT

    def can_move_in_direction(self, direction: Direction) -> bool:
        """Return True if moving in the given direction is a valid move."""

        #if transitioning between two tiles
        if direction == Direction.RIGHT or direction == Direction.LEFT:
            if self.position.x.relative != 0:
                return True
            elif self.position.y.relative != 0:
                return False
        else:
            if self.position.y.relative != 0:
                return True
            elif self.position.x.relative != 0:
                return False
            
        #check if the tile in given direction is wall
        if self.map[self.position + direction.value * self.position.norm] != Tile.WALL:
            return True
        
        return False

    def move(self, move: Direction) -> None:
        """Move PacMan in the given direction if possible, otherwise continue."""

        if self.can_move_in_direction(move):
            self.direction = move
            self.position += self.direction.value
        else:
            if move != self.direction:
                self.position += self.direction.value