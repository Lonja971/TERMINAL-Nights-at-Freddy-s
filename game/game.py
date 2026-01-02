from .state import GameState
from .scene_frames import GameSceneFrames
from .systems.buttery import ButterySystem
from .systems.time import TimeSystem
from utils.log import debug_log

class Game:
    def __init__(self):
        self.night = 1
        self.state = GameState()
        self.scene_frames = GameSceneFrames(self.state, self.night)
        self.buttery = ButterySystem()
        self.time = TimeSystem()


    def update_states(self, dt):      # systems -> ai, cameras, energy
        self.buttery.update(self.state, dt)
        self.time.update(self.state)

    def update_scene_frames(self, curr_scene_frames):
        processed_frames = self.scene_frames.process_scene_frames(curr_scene_frames)

        return processed_frames