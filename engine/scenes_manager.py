import curses
from scenes.main_menu import MainMenu
from scenes.game import GameScene
from scenes.settings import SettingsScene
from utils.log import debug_log
from engine.input_manager import InputManager
from pynput import keyboard

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

        self.input = InputManager()
        self.input.start()

        while True:
            self.current_scene.update()
            self.current_scene.handle_input(self.input)
            self.input.end_frame()

            if self.current_scene.has_frame_changed():
                debug_log("Frames not the same")
                self.current_scene.render(self.win)
                self.win.refresh()

            curses.napms(16)
