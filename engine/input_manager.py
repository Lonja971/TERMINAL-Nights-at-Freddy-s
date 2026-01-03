from pynput import keyboard
from collections import deque

class InputManager:
    def __init__(self):
        self.held_keys = set()
        self.pressed_keys = set()
        self.released_keys = set()

        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )

    def start(self):
        self.listener.start()

    def _on_press(self, key):
        if key not in self.held_keys:
            self.pressed_keys.add(key)
        self.held_keys.add(key)

    def _on_release(self, key):
        if key in self.held_keys:
            self.released_keys.add(key)
        self.held_keys.discard(key)

    #--- API ---

    def is_held(self, key):
        return key in self.held_keys

    def was_pressed(self, key):
        return key in self.pressed_keys

    def was_released(self, key):
        return key in self.released_keys

    def end_frame(self):
        # очищаємо edge-події
        self.pressed_keys.clear()
        self.released_keys.clear()