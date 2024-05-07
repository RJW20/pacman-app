from pacman_app.characters.character import Character
from pacman_app.characters.speed import Speed
from pacman_app.fruit import Fruit
from pacman_app.map import MAP, Tile, Position, Direction


class PacMan(Character):
    """The playable character."""

    def __init__(self) -> None:
        super().__init__()
        self.score: int
        self.move_next: bool
        self.dead: bool

    def initialise(self) -> None:
        """Get in a state to start the game."""

        self.score = 0
        self.move_next = True
        self.dead = False
        self.position = Position((14, 26), (4, 0))
        self.direction = Direction.LEFT
        self.speed = Speed.PACMAN_NORMAL

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
        if MAP[(self.position + direction.value * self.position.norm).tile_pos] != Tile.WALL:
            return True
        
        return False

    def move(self, move: Direction) -> None:
        """Move PacMan in the given direction if possible, otherwise continue."""

        if not self.move_next:
            self.move_next = True
            return
        
        if self.can_move_in_direction(move):
            self.direction = move
            super().move()
        else:
            if move != self.direction and self.can_move_in_direction(self.direction):
                super().move()

    def collided_with(self, other: Character | Fruit) -> bool:
        """Return True if on the same tile as the other entity."""

        return self.position.tile_pos == other.position.tile_pos
    
    def kill(self) -> None:
        """Kill PacMan."""
        self.dead = True