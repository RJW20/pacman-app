import pygame

from pacman_app.map import Map, Tile, Direction
from pacman_app.pacman import PacMan
from pacman_app.drawer import to_pixels
from settings import settings


def main() -> None:

    #pygame setup
    width = settings['screen_width']
    game_height = round(31 * width / 28)
    screen = pygame.display.set_mode((width, game_height))
    pygame.display.set_caption("PacMan")
    clock = pygame.time.Clock()
    running = True

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

        screen.fill('black')

        for i, line in enumerate(map.grid):
            for j, tile in enumerate(line):
                if tile == Tile.WALL:
                    pixel_point = to_pixels((j,i), (width, game_height))
                    pygame.draw.rect(screen, 'blue', pygame.Rect(pixel_point, (width / 28, game_height / 31)))


        pacman.move(move)
        pygame.draw.rect(screen, 'yellow', pygame.Rect(to_pixels(pacman.position, (width, game_height)), (width / 28, game_height / 31)))
        
        #display the changes
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
