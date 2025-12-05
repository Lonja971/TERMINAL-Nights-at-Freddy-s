import curses, time
from engine.scene import Scene
from utils.sprite_loader import load_sprite
from utils.log import debug_log

class MainMenu(Scene):
    def __init__(self, app):
        super().__init__(app)
        self.options_action = [
            lambda: self.app.set_scene("game"),
            lambda: self.app.set_scene("settings"),
            lambda: exit()
        ]

        self.curr_frame_data = {
            "room": "main_menu",
            "sprites": {
                "main_menu_options": {
                    "type": "generated",
                    "data": {
                        "selected": 0,
                        "options": ["Почати гру", "Налаштування", "Вийти"]
                    }
                },
                "menu_anim_top_freddy": {
                    "type": "static"
                }
                #"menu_anim_bg": {
                #    "type": "animation",
                #    "update_in": 1,
                #    "last_update": 0,
                #    "frames_num": 4,
                #    "loop": True,
                #    "data": {
                #        "curr_frame": 0,
                #    }
                #}
            }
        }

        super().on_enter()

    def handle_input(self, key):
        menu_element = self.curr_frame_data["sprites"]["main_menu_options"]
        data = menu_element["data"]

        selected_option = data["selected"]
        options = data["options"]

        # --- Навігація ----------------------------
        if key == curses.KEY_UP:
            if selected_option > 0:
                selected_option -= 1

        elif key == curses.KEY_DOWN:
            if selected_option < len(options) - 1:
                selected_option += 1

        # --- Вибір пункту ------------------------
        elif key == curses.KEY_ENTER or key in [10, 13]:
            action = self.options_action[selected_option]
            action()   # викликаємо функцію

        # --- ESC вихід ---------------------------
        elif key == 27:
            exit()

        # --- Оновлюємо значення в curr_frame_data --
        data["selected"] = selected_option
