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
        self.curr_frame_data = [
            {
                "type": "generated",
                "name": "main_menu_options",
                "data": {
                    "selected": 0,
                    "options": ["Почати гру", "Налаштування", "Вийти"]
                }
            },
            {
                "type": "generated",
                "name": "background_dots" 
            },
            {
                "type": "animation",
                "update_in": 1,
                "last_update": 0,
                "frames_num": 4,
                "loop": True,
                "name": "menu_anim_bg",
                "data": {
                    "curr_frame": 1
                }
            }
        ]

        super().on_enter()

    def handle_input(self, key):
        menu_element = self.curr_frame_data[0]
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

    def draw_background(self, win, h, w):
        if self.curr_frame_data["background"]["frame_nr"] > 3:
            self.curr_frame_data["background"]["frame_nr"] = 0

        sprite = load_sprite(f"test{self.curr_frame_data["background"]["frame_nr"]}")
        sprite_h = len(sprite)
        sprite_w = max(len(line) for line in sprite)

        start_y = h - sprite_h
        start_x = w - sprite_w

        for i, line in enumerate(sprite):
            try:
                win.addstr(start_y + i, start_x, line[:w-start_x])
            except curses.error:
                pass


    def draw_options(self, win, h, w):
        symb_h = 1
        max_h = h - (len(self.options) * symb_h) - self.options_padding["h"] - 1

        for i, opt in enumerate(self.options):
            y = max_h + symb_h + i

            if i == self.curr_frame_data["selected_option"]:
                win.attron(curses.A_REVERSE)

            win.addstr(y, self.options_padding["w"], opt["title"])

            if i == self.curr_frame_data["selected_option"]:
                win.attroff(curses.A_REVERSE)