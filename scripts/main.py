import pygame

from pacman_app.map import MAP, Tile, Direction
from pacman_app import PacDots, Ghosts, Blinky, Pinky, Inky, Clyde
from pacman_app.sprites import PacManSprite, BlinkySprite
from pacman_app.drawer import to_pixels
from pacman_app.sprites import SpriteSheet
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

    spritesheet = SpriteSheet(tile_size)

    pacman = PacManSprite(spritesheet)
    pacdots = PacDots()
    ghosts = Ghosts(pacman)
    ghosts.blinky = BlinkySprite(pacman, spritesheet)
    ghosts.pinky = Pinky(pacman)
    ghosts.inky = Inky(pacman)
    ghosts.clyde = Clyde(pacman)

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
                    ghosts.frightened = True
        
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

        ghosts.move()
        pacman.move(move)
        
        ghosts.check_collision()

        if pacdots.check_if_eaten(pacman):
            pacman.score += 10
            if pacdots.remaining == 214:
                ghosts.inky.inactive = False
            elif pacdots.remaining == 164:
                ghosts.clyde.inactive = False
        elif pacdots.check_if_powered(pacman):
            pacman.score += 50
            ghosts.frightened = True
            if pacdots.remaining == 214:
                ghosts.inky.inactive = False
            elif pacdots.remaining == 164:
                ghosts.clyde.inactive = False

        for dot in pacdots.dots:
            dot_position = to_pixels(dot, tile_size)
            pygame.draw.circle(game, 'yellow', dot_position, tile_size*0.15)

        for dot in pacdots.power_dots:
            dot_position = to_pixels(dot, tile_size)
            pygame.draw.circle(game, 'yellow', dot_position, tile_size*0.3)

        '''
        for i, ghost in enumerate(ghosts):

            pixel_point = to_pixels(ghost.target, tile_size)
            tile_rect = pygame.Rect((0,0), (tile_size, tile_size))
            tile_rect.center = pixel_point
            pygame.draw.rect(game, ghost_colours[i], tile_rect, 1)

            if not ghost.inactive:

                ghost_position = to_pixels(ghost.position, tile_size)
                ghost_rect = ghost_sprites[i].get_rect()
                ghost_rect.center = ghost_position 
                game.blit(ghost_sprites[i], ghost_rect)
                #pygame.draw.circle(game, ghost_colours[i], ghost_position, tile_size*0.7)
        '''

        if not ghosts.blinky.inactive:
            ghost_position = to_pixels(ghosts.blinky.position, tile_size)
            ghost_rect = ghosts.blinky.sprite.get_rect()
            ghost_rect.center = ghost_position 
            game.blit(ghosts.blinky.sprite, ghost_rect)

        pacman_position = to_pixels(pacman.position, tile_size)
        pacman_rect = pacman.sprite.get_rect()
        pacman_rect.center = pacman_position 
        game.blit(pacman.sprite, pacman_rect)
        #pygame.draw.circle(game, 'yellow', pacman_position, tile_size*0.7)
        
        #display the changes
        screen.blit(game, (game_offset, 0))
        pygame.display.flip()

        clock.tick(45)

    pygame.quit()
