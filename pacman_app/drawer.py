from pacman_app.map import CharacterPosition


def to_pixels(coordinate: CharacterPosition | tuple[int, int],
              screen_size: tuple[int,int],
              ) -> tuple[int,int]:
    """Convert a character position or tile in the map to pixel position on the screen."""

    if isinstance(coordinate, tuple):
        coordinate = CharacterPosition(coordinate)

    pixel_x = (coordinate.x.absolute + coordinate.x.relative * 0.25) * screen_size[0]/28
    pixel_y = (coordinate.y.absolute + coordinate.y.relative * 0.25) * screen_size[1]/31
    return pixel_x, pixel_y