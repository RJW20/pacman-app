import pygame

from pacman_app import PacMan
from pacman_app.sprites import SpriteSheet
from pacman_app.map import Direction


class PacManSprite(PacMan):
    """PacMan with his sprite."""
    
    def __init__(self, spritesheet: SpriteSheet) -> None:
        super().__init__()

        self.neutral = spritesheet.image_at(2, 0, 13)
        self.up = [spritesheet.image_at(1, 2, 13), spritesheet.image_at(0, 2, 13)]
        self.right = [spritesheet.image_at(1, 0, 13), spritesheet.image_at(0, 0, 13)]
        self.down = [spritesheet.image_at(1, 3, 13), spritesheet.image_at(0, 3, 13)]
        self.left = [spritesheet.image_at(1, 1, 13), spritesheet.image_at(0, 1, 13)]
        self.sprite_count = -1
        self.repeat_count = 5
        
    @property
    def sprite(self) -> pygame.Surface:
        """Return the sprite corresponding to PacMan's current position and state."""

        self.sprite_count = (self.sprite_count + 1) % (4 * self.repeat_count)

        if self.sprite_count // self.repeat_count == 0:
            return self.neutral

        match(self.direction):
            case Direction.UP:
                sprite_list = self.up
            case Direction.RIGHT:
                sprite_list = self.right
            case Direction.DOWN:
                sprite_list = self.down
            case Direction.LEFT:
                sprite_list = self.left

        if self.sprite_count // self.repeat_count < 3:
            return sprite_list[self.sprite_count // self.repeat_count - 1]
        else:
            return sprite_list[0]