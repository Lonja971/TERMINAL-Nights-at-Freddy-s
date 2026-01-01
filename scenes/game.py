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

            self.game.update(dt)

            if int(self.game.state.buttery) != self.curr_frame_data["sprites"]["game_buttery"]["data"]["value"]:
                self.curr_frame_data["sprites"]["game_buttery"]["data"]["value"] = self.game.state.buttery

            game_time = self.game.state.time
            sprite_time = self.curr_frame_data["sprites"]["game_timeblock"]["data"]["time"]
            
            if game_time != sprite_time:
                self.curr_frame_data["sprites"]["game_timeblock"]["data"]["time"] = game_time.copy()



    def handle_input(self, key):
        if key == 27:  # ESC
            self.app.set_scene("menu")
        elif key in [ord('a'), ord('A')]:

            self.curr_frame_data["room"] = "game_office_l"

        elif key in [ord('d'), ord('D')]:

            self.curr_frame_data["room"] = "game_office_r"
    