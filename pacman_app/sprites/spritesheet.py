import pygame


class SpriteSheet:
    """Converter from spritesheet to individual sprites."""

    def __init__(self, tile_size: int) -> None:
        self.sheet: pygame.image = pygame.image.load('resources/spritesheet.png').convert()
        self.padding: int = 1
        self.length: int = 14
        self.tile_size: int = tile_size

    def image_at(self, i: int, j: int, length: int, sprite_scale: float = 1.0) -> pygame.Surface:
        """Load image in (i, j) position on spritesheet with given square side length, 
        and scale by tile_size * sprite_scale."""

        x = (self.padding * 2 + self.length) * i + self.padding
        y = (self.padding * 2 + self.length) * j + self.padding
        rect = pygame.Rect((x, y), (length, length))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey('black', pygame.RLEACCEL)
        sprite_size = self.tile_size * sprite_scale
        image = pygame.transform.scale(image, (sprite_size, sprite_size))
        return image