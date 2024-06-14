# Pac-Man
A Python implementation of the game Pac-Man using [pygame](https://www.pygame.org/docs/). This creation is made as close to the intentions of the original developers as possible, so certain glitches (such as Pinky targeting the tile 4 in front and 4 to the left when Pac-Man is pointing up) are not present. There is however no implementation of lives, so good luck ;)

![Pac-Man](https://i.imgur.com/ugP02mD.png "Pac-Man")

## Basic Requirements
1. [Python](https://www.python.org/downloads/).
2. [Poetry](https://python-poetry.org/docs/) for ease of installing the dependencies.

## Getting Started
1. Clone or download the repo `git clone https://github.com/RJW20/pacman-app.git`.
2. Set up the virtual environment with `poetry install`.
3. (Optional) Set your desired screen width in `settings.py` (the height will be then be determined by the aspect ratio 5:6).
4. Run the game with `poetry run main`.
5. Turn Pac-Man with the arrow keys and enjoy!
