from utils.log import debug_log

class ButterySystem:
    BASE_DRAIN = 0.1
    DOOR_DRAIN = 0.2
    LIGHT_DRAIN = 0.15
    CAMERA_DRAIN = 0.25

    def __init__(self):
        self._accum = 0.0

    def update(self, state, dt: float):
        drain = self.BASE_DRAIN

        state.buttery -= drain