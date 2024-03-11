import pygame

from pacman_app import PacDots, Ghosts
from pacman_app.sprites import SpriteSheet, PacManSprite, BlinkySprite, PinkySprite, InkySprite, ClydeSprite
from pacman_app.map import MAP, Tile, Direction
from pacman_app.pixels import to_pixels


class Game:
    """Controller of all game objects."""

    def __init__(self, settings: dict) -> None:

        #pygame set up
        width = settings['game_width']
        self.tile_size = width // 28
        self.game_offset = self.tile_size
        game_size = (self.tile_size * 28, self.tile_size * 36)
        self.game = pygame.Surface((game_size))
        screen_size = (self.tile_size * 30, self.tile_size * 36)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("PacMan")
        self.clock = pygame.time.Clock()

        #character set up
        spritesheet = SpriteSheet(self.tile_size)
        self.pacman = PacManSprite(spritesheet)
        self.pacdots = PacDots()
        self.ghosts = Ghosts(self.pacman)
        self.ghosts.blinky = BlinkySprite(self.pacman, spritesheet)
        self.ghosts.pinky = PinkySprite(self.pacman, spritesheet)
        self.ghosts.inky = InkySprite(self.pacman, spritesheet)
        self.ghosts.clyde = ClydeSprite(self.pacman, spritesheet)

        self.pacman.initialise()
        self.ghosts.initialise()

    def check_move(self, move: Direction) -> Direction:
        """Check for new PacMan move."""

        for event in pygame.event.get():
            #so can quit
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()

            #set move
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move = Direction.UP
                elif event.key == pygame.K_RIGHT:
                    move =  Direction.RIGHT
                elif event.key == pygame.K_DOWN:
                    move =  Direction.DOWN
                elif event.key == pygame.K_LEFT:
                    move =  Direction.LEFT

        return move
    
    def advance(self, move: Direction) -> None:
        """Advance to the next frame."""

        self.ghosts.move()
        self.pacman.move(move)
        
        self.ghosts.check_collision()

        if self.pacdots.check_if_eaten(self.pacman):
            self.pacman.score += 10
            if self.pacdots.remaining == 214:
                self.ghosts.inky.inactive = False
            elif self.pacdots.remaining == 184:
                self.ghosts.clyde.inactive = False
        elif self.pacdots.check_if_powered(self.pacman):
            self.pacman.score += 50
            self.ghosts.frightened = True
            if self.pacdots.remaining == 214:
                self.ghosts.inky.inactive = False
            elif self.pacdots.remaining == 184:
                self.ghosts.clyde.inactive = False

    def update_screen(self) -> None:
        """Draw the current frame to the screen."""

        #wipe the last frame
        self.screen.fill('black')
        self.game.fill('black')

        #draw the map
        for j, line in enumerate(MAP.grid):
            for i, tile in enumerate(line):
                if tile == Tile.WALL:
                    pixel_point = to_pixels((i,j), self.tile_size)
                    tile_rect = pygame.Rect((0,0), (self.tile_size, self.tile_size))
                    tile_rect.center = pixel_point
                    pygame.draw.rect(self.game, 'blue', tile_rect, 1)

        #draw dots first so characters drawn oven them
        for dot in self.pacdots.dots:
            dot_position = to_pixels(dot, self.tile_size)
            pygame.draw.circle(self.game, 'yellow', dot_position, self.tile_size*0.15)

        for dot in self.pacdots.power_dots:
            dot_position = to_pixels(dot, self.tile_size)
            pygame.draw.circle(self.game, 'yellow', dot_position, self.tile_size*0.3)

        #ghosts next
        for ghost in self.ghosts:
            if not ghost.inactive:
                ghost.draw(self.game, self.tile_size)

        #finally pacman
        self.pacman.draw(self.game, self.tile_size)

        #update the screen
        self.screen.blit(self.game, (self.game_offset, 0))
        pygame.display.flip()

    def run(self) -> None:
        """Run the main game loop."""

        pacman_move = self.pacman.direction

        while True:
            pacman_move = self.check_move(pacman_move)
            self.advance(pacman_move)
            self.update_screen()

            self.clock.tick(60)
