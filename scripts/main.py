from pacman_app.game import Game
from settings import settings

def main() -> None:

    game = Game(settings)
    game.run()
