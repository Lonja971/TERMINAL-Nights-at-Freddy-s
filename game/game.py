from .state import GameState
from .scene_frames import GameSceneFrames
from utils.log import debug_log

class Game:
    def __init__(self, night_num):
        self.night = night_num
        self.state = GameState(night_num)
        self.scene_frames = GameSceneFrames(self.state, self.night)

    def update_states(self, dt):
        if self.state.state == "end": return

        for name, anim_class in self.state.animatronics.items():
            if anim_class.intelligence > 0:
                if not anim_class.is_active:
                    if anim_class.activation_time[0] >= self.state.time.time[0] and anim_class.activation_time[1] <= self.state.time.time[1]:
                        anim_class.is_active = True
                else:
                    if 15 in self.state.locations and len(self.state.locations[15]) > 0:
                        for name in self.state.locations[15]:
                            self.state.animatronics[name].screamer_timer += 1
                    elif 20 in self.state.locations and len(self.state.locations[20]) > 0:
                        self.state.set_screamer_anima(self.state.locations[20][0])

                    anim_class.update()

        self.state.buttery.update(self.state, dt)
        self.state.music_box.update(self.state)
        self.state.time.update(self.state)

    def update_scene_frames(self, curr_scene_frames, anim_state):
        processed_frames = self.scene_frames.process_scene_frames(curr_scene_frames, anim_state)

        return processed_frames