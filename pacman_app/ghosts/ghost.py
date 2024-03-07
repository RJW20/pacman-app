from pacman_app.map import MAP, Position, Direction
from pacman_app.pacman import PacMan
from pacman_app.ghosts.modes import Mode, CHASE, SCATTER, FRIGHTENED, RETURN_TO_HOME, INACTIVE


class Ghost:
    """Base class for one of the ghosts that chase PacMan."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.position: Position
        self.direction: Direction
        self.mode: Mode
        self.mode_count: int

    @property
    def target(self) -> tuple[int,int]:
        """Return the ghost's target as tile position for use with astar."""

    def initialise(self) -> None:
        """Get self in a state to start the game."""

    def move(self) -> None:
        """Set self's direction and move in it."""

        #set direction depending on if been hit by pacman, pacman has hit a power dot
        #or if on node use astar to reset path