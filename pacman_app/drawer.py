from pacman_app.map import CharacterPosition


def to_pixels(coordinate: CharacterPosition | tuple[int, int],
              tile_size: float,
              ) -> tuple[int,int]:
    """Convert a character position or tile in the map to pixel position on the screen."""

    if isinstance(coordinate, CharacterPosition):
        pixel_x = coordinate.true_x * tile_size
        pixel_y = coordinate.true_y * tile_size

    elif isinstance(coordinate, tuple):
        pixel_x = coordinate[0] * tile_size
        pixel_y = coordinate[1] * tile_size

    return pixel_x, pixel_y