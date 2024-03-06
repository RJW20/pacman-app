from pacman_app.map import Position


def to_pixels(coordinate: Position | tuple[int, int],
              tile_size: float,
              ) -> tuple[int,int]:
    """Convert a character position or tile on the map to pixel position on the screen."""

    if isinstance(coordinate, Position):
        pixel_x = coordinate.true_x * tile_size + tile_size // 2
        pixel_y = coordinate.true_y * tile_size + tile_size // 2

    elif isinstance(coordinate, tuple):
        pixel_x = coordinate[0] * tile_size + tile_size // 2
        pixel_y = coordinate[1] * tile_size + tile_size // 2

    return pixel_x, pixel_y