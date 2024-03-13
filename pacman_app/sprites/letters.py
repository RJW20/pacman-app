import pygame

from pacman_app.sprites.spritesheet import SpriteSheet
from pacman_app.pixels import to_pixels


class Letters:
    """Letters as sprites."""
    
    def __init__(self, spritesheet: SpriteSheet) -> None:
        self.S = spritesheet.image_at(8, 9, 7, 0.9)
        self.S_rect = self.S.get_rect()
        self.S_rect.topleft = to_pixels((12, 0), spritesheet.tile_size)

        self.C = spritesheet.image_at(9, 9, 7, 0.9)
        self.C_rect = self.C.get_rect()
        self.C_rect.topleft = to_pixels((13, 0), spritesheet.tile_size)

        self.O = spritesheet.image_at(10, 9, 7, 0.9)
        self.O_rect = self.O.get_rect()
        self.O_rect.topleft = to_pixels((14, 0), spritesheet.tile_size)

        self.R = spritesheet.image_at(11, 9, 7, 0.9)
        self.R_rect = self.R.get_rect()
        self.R_rect.topleft = to_pixels((15, 0), spritesheet.tile_size)

        self.E = spritesheet.image_at(8, 10, 7, 0.9)
        self.E_rect = self.E.get_rect()
        self.E_rect.topleft = to_pixels((16, 0), spritesheet.tile_size)
        
    def draw_score(self, surface: pygame.Surface) -> None:
        """Draw 'score' onto the surface."""

        surface.blit(self.S, self.S_rect)
        surface.blit(self.C, self.C_rect)
        surface.blit(self.O, self.O_rect)
        surface.blit(self.R, self.R_rect)
        surface.blit(self.E, self.E_rect)