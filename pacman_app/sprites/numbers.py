import pygame

from pacman_app.sprites.spritesheet import SpriteSheet
from pacman_app.pixels import to_pixels


class Numbers:
    """Numbers as sprites."""
    
    def __init__(self, spritesheet: SpriteSheet) -> None:
        self.zero = spritesheet.image_at(8, 6, 7, 0.9)
        self.one = spritesheet.image_at(9, 6, 7, 0.9)
        self.two = spritesheet.image_at(10, 6, 7, 0.9)
        self.three = spritesheet.image_at(11, 6, 7, 0.9)
        self.four = spritesheet.image_at(8, 7, 7, 0.9)
        self.five = spritesheet.image_at(9, 7, 7, 0.9)
        self.six = spritesheet.image_at(10, 7, 7, 0.9)
        self.seven = spritesheet.image_at(11, 7, 7, 0.9)
        self.eight = spritesheet.image_at(8, 8, 7, 0.9)
        self.nine = spritesheet.image_at(9, 8, 7, 0.9)
        
    def draw_score(self, surface: pygame.Surface, tile_size: int) -> None:
        """Draw the score onto the surface."""