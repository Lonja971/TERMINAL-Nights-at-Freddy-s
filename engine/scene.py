from utils.log import debug_log
from engine.renderer import Renderer
from engine.sprites_manager import SpritesManager
import copy, time

class Scene:
    def __init__(self, app):
        self.app = app
        self.force_redraw = True
        self.prev_frame_data = None
        self.curr_frame_data = None

        win_size = app.win.getmaxyx()
        self.sprites_manager = SpritesManager(win_size, self.curr_frame_data)
        self.renderer = Renderer(app.win)

    def on_enter(self):
        self.force_redraw = True
        if self.curr_frame_data is not None:
            self.prev_frame_data = self.curr_frame_data.copy()

    def on_exit(self):
        pass

    def handle_input(self, key):
        pass

    def update(self):
        now = time.time()
        
        for name, element in self.curr_frame_data["sprites"].items():
            if element["type"] == "animation":
                last_update = element.get("last_update", 0)
                update_in = element.get("update_in", 1)
                frames_num = element.get("frames_num", 1)
                loop = element.get("loop", True)
                curr_frame = element["data"].get("curr_frame", 0)

                if now - last_update >= update_in:
                    if curr_frame + 1 >= frames_num:
                        if loop:
                            element["data"]["curr_frame"] = 0
                        else:
                            element["data"]["curr_frame"] = frames_num - 1
                    else:
                        element["data"]["curr_frame"] = curr_frame + 1

                    element["last_update"] = now

    def update_background(self):
        pass

    def update_frame(self):
        self.prev_frame_data = self.curr_frame_data

    def has_frame_changed(self):
        if self.force_redraw:
            self.force_redraw = False
            self.prev_frame_data = None
            return True

        if self.prev_frame_data is None:
            self.prev_frame_data = copy.deepcopy(self.curr_frame_data)
            return True

        # порівнюємо тільки рендер-дані
        def extract_render_data(frame_data):
            return {
                "room": frame_data.get("room"),
                "sprites": {
                    name: {
                        "type": s["type"],
                        "data": s.get("data", {})
                    }
                    for name, s in frame_data.get("sprites", {}).items()
                }
            }

        prev_render = extract_render_data(self.prev_frame_data)
        curr_render = extract_render_data(self.curr_frame_data)

        if prev_render != curr_render:
            self.prev_frame_data = copy.deepcopy(self.curr_frame_data)
            return True

        return False

    def render(self, win):
        updated_symbols = self.sprites_manager.get_update(self.curr_frame_data)
        self.renderer.render(updated_symbols)