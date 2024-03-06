import pygame

from pacman_app.map import Map, Tile, Direction
from pacman_app import PacMan, PacDots, to_pixels
from settings import settings


def main() -> None:

    #pygame setup
    width = settings['game_width']
    tile_size = width // 28
    game_size = (tile_size * 28, tile_size * 31)
    game_offset = tile_size
    game = pygame.Surface((game_size))
    screen_size = (tile_size * 30, tile_size * 33)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("PacMan")
    clock = pygame.time.Clock()
    running = True

    #initialise the background
    #bg = pygame.image.load('resources/background.png')
    #bg = pygame.transform.scale(bg, game_size)

    map = Map()
    pacman = PacMan(map)
    pacdots = PacDots(map)
    pacman.initialise()
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

        
        #wipe the last frame
        screen.fill('black')
        game.fill('black')
        #game.blit(bg, (0,0))

        for j, line in enumerate(map.grid):
            for i, tile in enumerate(line):
                if tile == Tile.WALL:
                    pixel_point = to_pixels((i,j), tile_size)
                    pygame.draw.rect(game, 'blue', pygame.Rect(pixel_point, (tile_size, tile_size)), 1)

        pacman.move(move)

        if pacdots.check_if_eaten(pacman):
            pacman.score += 10

        for dot in pacdots:
            pygame.draw.rect(game, 'pink', pygame.Rect(to_pixels(dot, tile_size), (tile_size/2, tile_size/2)))

        pacman_position = to_pixels(pacman.position, tile_size)
        pacman_center = (pacman_position[0] + (tile_size+1)/2, pacman_position[1] + (tile_size+1)/2)
        pygame.draw.circle(game, 'yellow', pacman_center, tile_size*0.7)
        
        #display the changes
        screen.blit(game, (game_offset, game_offset))
        pygame.display.flip()

        clock.tick(45)

    pygame.quit()
