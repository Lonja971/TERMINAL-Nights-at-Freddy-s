from engine.scene import Scene
from utils.log import debug_log
from game.game import Game
import time
from pynput import keyboard
from config.sprite_registry import SPRITES

class GameScene(Scene):
    def __init__(self, app, save_state, params):
        super().__init__(app)
        debug_log(params)
        self.game = Game(params["night_num"])
        self.tick_rate = 0.10
        self._last_tick = time.time()
        self.paused = False
        self.light_pushed = False
        fan_nmae = "office_fan_anima"
        self.curr_frame_data = {
            "room": "game_office_l",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.game.state.get_buttery_level()
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.game.state.time.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.game.night
                    }
                },
                "office_fan_anima": {
                    "type": "animation",
                    "update_in": SPRITES[fan_nmae]["update_in"],
                    "frames_num": 4,
                    "mode": "loop",
                    "data": {
                        "curr_frame": 0,
                        "last_update": time.time()
                    }
                },
            }
        }

    def extra_update(self):
        now = time.time()

        if self.paused: return

        if now - self._last_tick >= self.tick_rate:
            dt = now - self._last_tick
            self._last_tick = now

            self.game.update_states(dt)
            self.process_scene_frames()

    def process_scene_frames(self):
        processed_frames = self.game.update_scene_frames(self.curr_frame_data, self.anim_state)

        if processed_frames["rewrite"] == True:
            self.curr_frame_data = processed_frames["update"]
            return
        
        if processed_frames["delete"]:
            for key in processed_frames["delete"]:
                self.curr_frame_data["sprites"].pop(key, None)

        if processed_frames["update"]:
            for key, sprite in processed_frames["update"].items():
                self.curr_frame_data["sprites"][key] = sprite

    def handle_input(self, input):
        if self.game.state.state == "end":
            if (input.was_pressed(keyboard.Key.enter)
                or input.was_pressed(keyboard.KeyCode.from_char('\n'))
                or input.was_pressed(keyboard.KeyCode.from_char('z'))
                or input.was_pressed(keyboard.KeyCode.from_char('x'))
            ):
                self.app.set_scene("menu")

        if input.is_held(keyboard.Key.esc):
            self.app.set_scene("menu")

        if input.was_pressed(keyboard.Key.left):
            if self.game.state.is_camera_open:
                self.game.state.change_active_camera("prev")
            else:
                self.game.state.set_office_pos("l")

        if input.was_pressed(keyboard.Key.right):
            if self.game.state.is_camera_open:
                self.game.state.change_active_camera()
            else:
                self.game.state.set_office_pos("r")

        # Mask / Camera
        if input.was_pressed(keyboard.Key.down):
            if self.game.state.is_camera_open:
                self.game.state.start_opening_tablet()
            else:
                self.game.state.set_mask()

        if input.was_pressed(keyboard.Key.up):
            if self.game.state.is_mask:
                self.game.state.set_mask()
            else:
                self.game.state.start_opening_tablet()

        # Light
        if input.was_pressed(keyboard.KeyCode.from_char('x')):
            if self.game.state.is_camera_open or self.game.state.is_tablet_opening_anim:
                if self.game.state.active_camera_num == 11:
                    self.game.state.music_box.charge()
                else:
                    self.game.state.set_camera_light()
            else:
                self.game.state.set_light("center")

        if input.was_released(keyboard.KeyCode.from_char('x')):
            if self.game.state.is_camera_open:
                self.game.state.set_camera_light(False)
            else:
                self.game.state.set_light("center", False)

        if input.was_pressed(keyboard.KeyCode.from_char('z')):
            if self.game.state.is_camera_open or self.game.state.is_tablet_opening_anim:
                if self.game.state.active_camera_num == 11:
                    self.game.state.music_box.charge()
            else:
                self.game.state.set_light("left")

        if input.was_released(keyboard.KeyCode.from_char('z')):
            self.game.state.set_light("left", False)

        if input.was_pressed(keyboard.KeyCode.from_char('c')):
            self.game.state.set_light("right")

        if input.was_released(keyboard.KeyCode.from_char('c')):
            self.game.state.set_light("right", False)