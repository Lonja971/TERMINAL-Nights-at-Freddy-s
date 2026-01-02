from engine.scene import Scene
from utils.log import debug_log
from game.game import Game
import time

class GameScene(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.game = Game()
        self.tick_rate = 0.10
        self._last_tick = time.time()
        self.paused = False
        self.curr_frame_data = {
            "room": "game_office_l",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.game.state.buttery
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.game.state.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.game.night
                    }
                },
                "office_vent_anima": {
                    "type": "animation",
                    "update_in": 0.07,
                    "frames_num": 4,
                    "loop": True
                },
                "center_light": {
                    "type": "static",
                }
            }
        }

    def extra_update(self):
        now = time.time()

        if self.paused:
            return

        if now - self._last_tick >= self.tick_rate:
            dt = now - self._last_tick
            self._last_tick = now

            self.game.update_states(dt)
            self.process_scene_frames()

            debug_log(self.curr_frame_data)

    def process_scene_frames(self):
        processed_frames = self.game.update_scene_frames(self.curr_frame_data)

        if processed_frames["rewrite"] == True:
            self.curr_frame_data = processed_frames["update"]
            return
        
        if processed_frames["delete"]:
            for key in processed_frames["delete"]:
                self.curr_frame_data["sprites"].pop(key)

        if processed_frames["update"]:
            for key, sprite in processed_frames["update"].items():
                self.curr_frame_data["sprites"][key] = sprite

    def handle_input(self, key):
        if key == 27:  # ESC
            self.app.set_scene("menu")
        elif key in [ord('a'), ord('A')]:
            self.game.state.set_office_pos("l")

        elif key in [ord('d'), ord('D')]:
            self.game.state.set_office_pos("r")

        elif key in [ord(' ')]:
            self.game.state.set_light()
    