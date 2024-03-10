import pygame


class SpriteSheet:
    """Converter from spritesheet to individual sprites."""

    def __init__(self) -> None:
        self.sheet = pygame.image.load('resources/spritesheet.png').convert()
        self.padding = 1
        self.length = 14

    def image_at(self, i: int, j: int) -> pygame.Surface:
        """Load image in (i, j) position on spritesheet."""

        x = (self.padding * 2 + self.length) * i + self.padding
        y = (self.padding * 2 + self.length) * j + self.padding
        rect = pygame.Rect((i, j), (self.length, self.length))
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        return image