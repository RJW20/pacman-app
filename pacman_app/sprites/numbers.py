import pygame

from pacman_app.sprites.spritesheet import SpriteSheet
from pacman_app.pixels import to_pixels


class Numbers:
    """Numbers as sprites."""
    
    def __init__(self, spritesheet: SpriteSheet) -> None:
        self.tile_size = spritesheet.tile_size
        self.zero = spritesheet.image_at(8, 6, 7, 0.9)
        self.zero_rect = self.zero.get_rect()
        self.zero_rect.topleft = to_pixels((16, 1), self.tile_size)
        self.one = spritesheet.image_at(9, 6, 7, 0.9)
        self.two = spritesheet.image_at(10, 6, 7, 0.9)
        self.three = spritesheet.image_at(11, 6, 7, 0.9)
        self.four = spritesheet.image_at(8, 7, 7, 0.9)
        self.five = spritesheet.image_at(9, 7, 7, 0.9)
        self.six = spritesheet.image_at(10, 7, 7, 0.9)
        self.seven = spritesheet.image_at(11, 7, 7, 0.9)
        self.eight = spritesheet.image_at(8, 8, 7, 0.9)
        self.nine = spritesheet.image_at(9, 8, 7, 0.9)

    def sprite_from_num(self, num: int) -> pygame.Surface:
        """Return the sprite corresponding to the number input."""

        match(num):
            case 0: return self.zero
            case 1: return self.one
            case 2: return self.two
            case 3: return self.three
            case 4: return self.four
            case 5: return self.five
            case 6: return self.six
            case 7: return self.seven
            case 8: return self.eight
            case 9: return self.nine
        
    def draw_score(self, surface: pygame.Surface, score: int) -> None:
        """Draw the score onto the surface."""

        #score always ends in zero
        surface.blit(self.zero, self.zero_rect)

        score = str(score)
        for i, digit in enumerate(score[-2::-1]):
            num_sprite = self.sprite_from_num(int(digit))
            num_rect = num_sprite.get_rect()
            num_rect.topleft = to_pixels((15 - i, 1), self.tile_size)
            surface.blit(num_sprite, num_rect)