import pygame

from pacman_app.map import MAP, Tile, Direction
from pacman_app import PacMan, PacDots, Ghosts
from pacman_app.ghosts.mode import Mode
from pacman_app.drawer import to_pixels
from settings import settings


def main() -> None:

    #pygame setup
    width = settings['game_width']
    tile_size = width // 28
    game_size = (tile_size * 28, tile_size * 36)
    game_offset = tile_size
    game = pygame.Surface((game_size))
    screen_size = (tile_size * 30, tile_size * 36)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("PacMan")
    clock = pygame.time.Clock()
    running = True

    #initialise the background
    #bg = pygame.image.load('resources/background.png')
    #bg = pygame.transform.scale(bg, game_size)

    pacman = PacMan()
    pacdots = PacDots()
    ghosts = Ghosts(pacman)
    ghost_colours = ['red', 'pink']

    pacman.initialise()
    ghosts.initialise()

    move = pacman.direction

    while running:

        for event in pygame.event.get():
            #so can quit
            if event.type == pygame.QUIT: 
                running = False
                break

            #set move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move = Direction.UP
                elif event.key == pygame.K_RIGHT:
                    move = Direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    move = Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    move = Direction.LEFT
                elif event.key == pygame.K_SPACE:
                    pass
        
        #wipe the last frame
        screen.fill('black')
        game.fill('black')
        #game.blit(bg, (0,0))

        for j, line in enumerate(MAP.grid):
            for i, tile in enumerate(line):
                if tile == Tile.WALL:
                    pixel_point = to_pixels((i,j), tile_size)
                    tile_rect = pygame.Rect((0,0), (tile_size, tile_size))
                    tile_rect.center = pixel_point
                    pygame.draw.rect(game, 'blue', tile_rect, 1)


        ######################
        # Move the ghosts
        # Move pacman
        # Check for collisions between pacman and ghosts/dots         
        ######################


        ghosts.move()
        pacman.move(move)
        
        ghosts.check_collision()

        if pacdots.check_if_eaten(pacman):
            pacman.score += 10

        for dot in pacdots:
            dot_position = to_pixels(dot, tile_size)
            pygame.draw.circle(game, 'yellow', dot_position, tile_size*0.15)

        for i, ghost in enumerate(ghosts):

            pixel_point = to_pixels(ghost.target, tile_size)
            tile_rect = pygame.Rect((0,0), (tile_size, tile_size))
            tile_rect.center = pixel_point
            pygame.draw.rect(game, ghost_colours[i], tile_rect, 1)

            if not ghost.inactive:

                ghost_position = to_pixels(ghost.position, tile_size)
                pygame.draw.circle(game, ghost_colours[i], ghost_position, tile_size*0.7)

        pacman_position = to_pixels(pacman.position, tile_size)
        pygame.draw.circle(game, 'yellow', pacman_position, tile_size*0.7)
        
        #display the changes
        screen.blit(game, (game_offset, 0))
        pygame.display.flip()

        clock.tick(45)

    pygame.quit()
