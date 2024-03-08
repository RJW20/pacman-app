from pacman_app.ghosts.ghost import Ghost
from pacman_app.ghosts.blinky import Blinky
from pacman_app.ghosts.pinky import Pinky
from pacman_app.ghosts.inky import Inky
from pacman_app.ghosts.mode import Mode, FRIGTHENED_DURATION, INACTIVE_DURATION
from pacman_app.pacman import PacMan


class Ghosts:
    """Contains all 4 Ghosts and controls their modes."""

    def __init__(self, pacman: PacMan) -> None:
        self.pacman: PacMan = pacman
        self.items: list[Ghost]
        self.scatter_chase_index: int
        self.scatter_chase_max: int
        self.scatter_chase_count: int
        self.frightened_count: int

    def __getitem__(self, key: int) -> Ghost:
        return self.items[key]

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

        #set all ghosts that aren't returning to home
        for ghost in self:
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

        else:
            #revert all ghosts that were frightened
            for ghost in self:
                ghost.frightened = False

    def initialise(self) -> None:
        """Get Ghosts in a state to start the game."""

        #initialise list of ghosts
        blinky = Blinky(self.pacman)
        pinky = Pinky(self.pacman)
        inky = Inky(self.pacman)
        self.items = []
        self.items.append(blinky)
        self.items.append(pinky)
        self.items.append(inky)

        #initialise each ghost
        blinky.initialise()
        pinky.initialise()
        inky.initialise(blinky)

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
            if self.frightened_count == FRIGTHENED_DURATION:
                self.frightened = False
        else:
            self.scatter_chase_count += 1
            if self.scatter_chase_count == self.scatter_chase_max:
                self.scatter = not self.scatter

        #advance any regenerating ghosts
        for ghost in self:
            if ghost.mode == Mode.RETURN_TO_HOME and ghost.made_it_home:
                ghost.mode = self.scatter_or_chase
                ghost.inactive = True
                ghost.inactive_max = INACTIVE_DURATION
                ghost.inactive_count = 0
            elif ghost.inactive and ghost.inactive_count == ghost.inactive_max:
                ghost.inactive = False

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
                    ghost.mode = Mode.RETURN_TO_HOME
                else:
                    #self.pacman.kill()
                    ghost.mode = Mode.RETURN_TO_HOME