from utils.log import debug_log
from engine.sprites_manager import SpritesManager
from engine.renderer import Renderer
import copy, time

class Scene:
    def __init__(self, app):
        self.app = app
        self.force_redraw = True
        self.prev_frame_data = None
        self.curr_frame_data = None

        win_size = app.win.getmaxyx()

        self.sprites_manager = SpritesManager(win_size)
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
        for element in self.curr_frame_data:
            if element["type"] == "animation":
                now = time.time()
                if now - element["last_update"] >= element["update_in"]:
                    if element["data"]["curr_frame"] + 1 >= element["frames_num"]:
                        if element["loop"]:
                            element["data"]["curr_frame"] = 0
                            element["last_update"] = now
                        else:
                            element["data"]["curr_frame"] = element["frames_num"] - 1
                    else:
                        element["data"]["curr_frame"] += 1
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

        if self.prev_frame_data != self.curr_frame_data:
            self.prev_frame_data = copy.deepcopy(self.curr_frame_data)
            return True

        return False

    def render(self, win):
        win.clear()
        sprites = self.sprites_manager.get_all_sprites(self.curr_frame_data)
        self.renderer.render(sprites)