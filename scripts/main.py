import pygame

from pacman_app.map import Map, Tile, Direction
from pacman_app.pacman import PacMan
from pacman_app.drawer import to_pixels
from settings import settings


def main() -> None:

    #pygame setup
    width = settings['screen_width']
    tile_size = width / 28
    screen_size = (width, round(31 * tile_size))
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("PacMan")
    clock = pygame.time.Clock()
    running = True

    #initialise the background
    bg = pygame.image.load('resources/background.png')
    bg = pygame.transform.scale(bg, screen_size)

    map = Map()
    pacman = PacMan(map)
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
        screen.blit(bg, (0,0))

        pacman.move(move)

        pacman_position = to_pixels(pacman.position, tile_size)
        pacman_center = (pacman_position[0] + tile_size/2, pacman_position[1] + tile_size/2)
        pygame.draw.circle(screen, 'yellow', pacman_center, tile_size*0.6)
        
        #display the changes
        pygame.display.flip()
        clock.tick(40)

    pygame.quit()
