import pygame


class SpriteSheet:
    """Converter from spritesheet to individual sprites."""

    def __init__(self, tile_size: int) -> None:
        self.sheet: pygame.image = pygame.image.load('resources/spritesheet.png').convert()
        self.padding: int = 1
        self.length: int = 14
        self.sprite_size: float = tile_size * 1.8

    def image_at(self, i: int, j: int, length: int) -> pygame.Surface:
        """Load image in (i, j) position on spritesheet with given square side length."""

        x = (self.padding * 2 + self.length) * i + self.padding
        y = (self.padding * 2 + self.length) * j + self.padding
        rect = pygame.Rect((x, y), (length, length))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image.set_colorkey('black', pygame.RLEACCEL)
        image = pygame.transform.scale(image, (self.sprite_size, self.sprite_size))
        return image