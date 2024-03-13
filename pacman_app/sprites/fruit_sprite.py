import pygame

from pacman_app.fruit import Fruit
from pacman_app.sprites.spritesheet import SpriteSheet
from pacman_app.pixels import to_pixels


class FruitSprite(Fruit):
    """Fruit with it's sprite."""

    def __init__(self, spritesheet: SpriteSheet) -> None:
        super().__init__()
        self.sprite = spritesheet.image_at(2, 3, 13, 1.8)
        self.rect = self.sprite.get_rect()
        self.rect.center = to_pixels(self.position, spritesheet.tile_size)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw current sprite onto the surface at the correct position."""

        surface.blit(self.sprite, self.rect)