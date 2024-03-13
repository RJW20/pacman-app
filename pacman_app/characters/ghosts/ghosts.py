from typing import Generator

from pacman_app.characters.ghosts.ghost import Ghost
from pacman_app.characters.ghosts.blinky import Blinky
from pacman_app.characters.ghosts.pinky import Pinky
from pacman_app.characters.ghosts.inky import Inky
from pacman_app.characters.ghosts.clyde import Clyde
from pacman_app.characters.ghosts.mode import Mode, FRIGHTENED_DURATION, INACTIVE_DURATION
from pacman_app.characters.pacman import PacMan
from pacman_app.characters.speed import Speed
from pacman_app.map import Direction


class Ghosts:
    """Contains all 4 Ghosts and controls their modes."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.blinky: Blinky
        self.pinky: Pinky
        self.inky: Inky
        self.clyde: Clyde
        self.scatter_chase_index: int
        self.scatter_chase_max: int
        self.scatter_chase_count: int
        self.frightened_count: int

    def __iter__(self) -> Generator[Ghost,None,None]:
        yield self.blinky
        yield self.pinky
        yield self.inky
        yield self.clyde

    @property
    def non_elroy(self) -> list[Ghost]:
        """Return a list of pinky, inky and clyde, along with blinky when he 
        isn't in elroy mode."""

        if self.blinky.elroy == 0:
            return [self.blinky, self.pinky, self.inky, self.clyde]
        else:
            return [self.pinky, self.inky, self.clyde]

    @property
    def scatter(self) -> bool:
        """Return True if Ghosts in scatter mode, false if in chase mode.
        
        If self.frightened is True this value represents what the Ghosts will 
        revert to when no longer frightened.    
        """

        return self._scatter
    
    @scatter.setter
    def scatter(self, value: bool) -> None:
        """Automatically set all Ghosts to appropriate mode."""

        #set the value
        self._scatter = value

        #prepare for advancing through mode
        if self._scatter:
            mode = Mode.SCATTER
        else:
            mode = Mode.CHASE
            self.scatter_chase_index += 1
        self.scatter_chase_max = mode.DURATIONS[self.scatter_chase_index]
        self.scatter_chase_count = 0

        #set all ghosts that aren't returning to home or in elroy
        if self.blinky.elroy != 0:
            if not self.blinky.mode == Mode.RETURN_TO_HOME:
                self.blinky.reverse_next = True

        for ghost in self.non_elroy:
            if not ghost.mode == Mode.RETURN_TO_HOME:
                ghost.mode = mode
                ghost.reverse_next = True

    @property
    def scatter_or_chase(self) -> Mode:
        """Return Mode.SCATTER or Mode.CHASE depending on self.scatter."""

        if self.scatter:
            return Mode.SCATTER
        else:
            return Mode.CHASE
    
    @property
    def frightened(self) -> bool:
        """Return True if PacMan is currently powered up."""

        return self._frightened
    
    @frightened.setter
    def frightened(self, value: bool) -> None:
        """Automatically set all Ghosts to appropriate mode."""

        #set the value
        self._frightened = value

        if self._frightened:
            #prepare for advancing through the frightened state
            self.frightened_count = 0

            #set all ghosts that have a body to frightened
            for ghost in self:
                if not ghost.mode == Mode.RETURN_TO_HOME:
                    ghost.frightened = True
                    ghost.frightened_count = FRIGHTENED_DURATION
                    ghost.reverse_next = True
                    if not ghost.in_tunnel:
                        ghost.speed = Speed.GHOST_FRIGHT

            #set pacman's speed
            self.pacman.speed = Speed.PACMAN_FRIGHT

        else:
            #revert all ghosts that were frightened
            for ghost in self:
                if ghost.frightened:
                    ghost.frightened = False
                    if not ghost.in_tunnel:
                        ghost.speed = Speed.GHOST_NORMAL

            #set pacman's speed
            self.pacman.speed = Speed.PACMAN_NORMAL

    @property
    def not_frightened_count(self) -> int:
        """Return the number of Ghosts not in frightend state."""
        return len([ghost for ghost in self if not ghost.frightened])

    def initialise(self) -> None:
        """Get Ghosts in a state to start the game."""

        #initialise each ghost
        self.blinky.initialise()
        self.pinky.initialise()
        self.inky.initialise(self.blinky)
        self.clyde.initialise()

        #initialise self
        self.scatter_chase_index = 0
        self.scatter = True
        self.frightened = False

        #undo the setting of reverse in self.scatter = True
        for ghost in self:
            ghost.reverse_next = False

    def update(self) -> None:
        """Update the counters/maxs.
         
        All Ghost's modes will change automatically.
        """

        #advance through whichever state self is in
        if self.frightened:
            self.frightened_count += 1
            for ghost in self:
                if ghost.frightened:
                    ghost.frightened_count -= 1
            if self.frightened_count == FRIGHTENED_DURATION:
                self.frightened = False
        else:
            self.scatter_chase_count += 1
            if self.scatter_chase_count == self.scatter_chase_max:
                self.scatter = not self.scatter

        #handle changes to elroy mode blinky
        if self.blinky.elroy != 0:
            if self.blinky.mode == Mode.RETURN_TO_HOME and self.blinky.made_it_home:
                self.blinky.mode = Mode.CHASE
                self.blinky.inactive = True
                self.blinky.inactive_max = INACTIVE_DURATION
                self.blinky.inactive_count = 0
                self.blinky.speed = Speed.GHOST_NORMAL
            elif self.blinky.inactive and self.blinky.inactive_count == self.blinky.inactive_max:
                self.blinky.inactive = False
                self.blinky.direction = False

        for ghost in self.non_elroy:

            #advance any regenerating ghosts
            if ghost.mode == Mode.RETURN_TO_HOME and ghost.made_it_home:
                ghost.mode = self.scatter_or_chase
                ghost.inactive = True
                ghost.inactive_max = INACTIVE_DURATION
                ghost.inactive_count = 0
                ghost.speed = Speed.GHOST_NORMAL
            elif ghost.inactive and ghost.inactive_count == ghost.inactive_max:
                ghost.inactive = False
                ghost.direction = Direction.LEFT

    def move(self) -> None:
        """Move all the Ghosts."""

        for ghost in self:
            ghost.move()

        self.update()

    def check_collision(self) -> None:
        """Check collisions with PacMan and change modes accordingly."""

        for ghost in self:
            #ignore any regenerating ghosts
            if ghost.mode == Mode.RETURN_TO_HOME or ghost.inactive:
                continue

            if self.pacman.collided_with(ghost):
                if ghost.frightened:
                    ghost.frightened = False
                    ghost.mode = Mode.RETURN_TO_HOME
                    ghost.speed = Speed.GHOST_RETURN
                    self.pacman.score += 200 * self.not_frightened_count
                else:
                    #self.pacman.kill()
                    pass            