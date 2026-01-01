from .state import GameState
from .systems.buttery import ButterySystem
from .systems.time import TimeSystem
from utils.log import debug_log

class Game:
    def __init__(self):
        self.state = GameState()
        self.buttery = ButterySystem()
        self.time = TimeSystem()

        self.night = 1

    def update(self, dt):      # systems -> ai, cameras, energy
        self.buttery.update(self.state, dt)
        self.time.update(self.state)
