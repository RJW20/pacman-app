import pygame


class Background:
    """Class the contains the maze background."""

    def __init__(self, tile_size: int) -> None:
        bg_top_right = pygame.image.load('resources/background_top_right.png')
        bg_bottom_right = pygame.image.load('resources/background_bottom_right.png')
        panel_size = (tile_size * 15, tile_size * 18)

        self.bg_top_right = pygame.transform.scale(bg_top_right, panel_size)
        self.bg_top_right_rect = self.bg_top_right.get_rect()
        self.bg_top_right_rect.topright = (tile_size * 30, 0)

        self.bg_top_left = pygame.transform.flip(self.bg_top_right, True, False)
        self.bg_top_left_rect = self.bg_top_left.get_rect()
        self.bg_top_left_rect.topleft = (0, 0)

        self.bg_bottom_right = pygame.transform.scale(bg_bottom_right, panel_size)
        self.bg_bottom_right_rect = self.bg_bottom_right.get_rect()
        self.bg_bottom_right_rect.bottomright = (tile_size * 30, tile_size * 36)

        self.bg_bottom_left = pygame.transform.flip(self.bg_bottom_right, True, False)
        self.bg_bottom_left_rect = self.bg_bottom_left.get_rect()
        self.bg_bottom_left_rect.bottomleft = (0, tile_size * 36)

    def draw(self, surface: pygame.Surface) -> None:
        """Draw self's current sprite onto the surface at the correct position."""

        surface.blit(self.bg_top_right, self.bg_top_right_rect)
        surface.blit(self.bg_top_left, self.bg_top_left_rect)
        surface.blit(self.bg_bottom_right, self.bg_bottom_right_rect)
        surface.blit(self.bg_bottom_left, self.bg_bottom_left_rect)