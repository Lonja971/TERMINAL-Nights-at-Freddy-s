import curses
from scenes.main_menu import MainMenu
from scenes.game import GameScene
from scenes.settings import SettingsScene
from utils.log import debug_log

class ScenesManager:
    def __init__(self, win):
        self.win = win
        self.scenes = {
            "menu": MainMenu,
            "game": GameScene,
            "settings": SettingsScene,
        }
        self.current_scene = None

    def set_scene(self, name):
        if self.current_scene:
            self.current_scene.on_exit()

        self.current_scene = self.scenes[name](self)
        self.current_scene.on_enter()

    def run(self):
        self.win.nodelay(True)
        curses.curs_set(0)

        while True:
            self.current_scene.update()
            key = self.win.getch()
            if key != -1:
                self.current_scene.handle_input(key)

            if self.current_scene.has_frame_changed():
                self.current_scene.render(self.win)
                self.win.refresh()

            curses.napms(16)
