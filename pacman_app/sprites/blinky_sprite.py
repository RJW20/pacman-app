import pygame

from pacman_app import Blinky, PacMan
from pacman_app.sprites.spritesheet import SpriteSheet
from pacman_app.map import Direction
from pacman_app.characters.ghosts.mode import Mode
from pacman_app.pixels import to_pixels


class BlinkySprite(Blinky):
    """Blinky with his sprite."""

    def __init__(self, pacman: PacMan, spritesheet: SpriteSheet) -> None:
        super().__init__(pacman)

        self.up = [spritesheet.image_at(4, 4, 14), spritesheet.image_at(5, 4, 14)]
        self.right = [spritesheet.image_at(0, 4, 14), spritesheet.image_at(1, 4, 14)]
        self.down = [spritesheet.image_at(6, 4, 14), spritesheet.image_at(7, 4, 14)]
        self.left = [spritesheet.image_at(2, 4, 14), spritesheet.image_at(3, 4, 14)]
        self.frightened_blue = [spritesheet.image_at(8, 4, 14), spritesheet.image_at(9, 4, 14)]
        self.frightened_white = [spritesheet.image_at(10, 4, 14), spritesheet.image_at(11, 4, 14)]
        self.eyes = [spritesheet.image_at(10, 5, 14), spritesheet.image_at(8, 5, 14), 
                     spritesheet.image_at(11, 5, 14), spritesheet.image_at(9, 5, 14)]
        self.sprite_count = -1
        self.repeat_count = 10
        self.frightened_color_switches = [self.repeat_count * i for i in range(1,10)]

    @property
    def sprite(self) -> pygame.Surface:
        """Return the sprite corresponding to PacMan's current position and state."""

        if not self.mode == Mode.RETURN_TO_HOME:

            self.sprite_count = (self.sprite_count + 1) % (2 * self.repeat_count)

            if not self.frightened:
                match(self.direction):
                    case Direction.UP:
                        sprite_list = self.up
                    case Direction.RIGHT:
                        sprite_list = self.right
                    case Direction.DOWN:
                        sprite_list = self.down
                    case Direction.LEFT:
                        sprite_list = self.left
                return sprite_list[self.sprite_count // self.repeat_count]
            else:
                if self.frightened_count > self.frightened_color_switches[8] or \
                   (self.frightened_count <= self.frightened_color_switches[7] and
                    self.frightened_count > self.frightened_color_switches[6]) or \
                   (self.frightened_count <= self.frightened_color_switches[5] and
                    self.frightened_count > self.frightened_color_switches[4]) or \
                   (self.frightened_count <= self.frightened_color_switches[3] and
                    self.frightened_count > self.frightened_color_switches[2]) or \
                   (self.frightened_count <= self.frightened_color_switches[1] and
                    self.frightened_count > self.frightened_color_switches[0]):
                    return self.frightened_blue[self.sprite_count // self.repeat_count]
                else:
                    return self.frightened_white[self.sprite_count // self.repeat_count]
        
        else:
            match(self.direction):
                case Direction.UP:
                    return self.eyes[0]
                case Direction.RIGHT:
                    return self.eyes[1]
                case Direction.DOWN:
                    return self.eyes[2]
                case Direction.LEFT:
                    return self.eyes[3]
                
    def draw(self, surface: pygame.Surface, tile_size: int) -> None:
        """Draw self's current sprite onto the surface at the correct position."""

        rect = self.sprite.get_rect()
        rect.center = to_pixels(self.position, tile_size)
        surface.blit(self.sprite, rect)