from utils.log import debug_log

TRANSPARENT_CHAR = "№"

class Renderer:
    def __init__(self, win):
        self.win = win
        self.win_h, self.win_w = self.win.getmaxyx()

        # Backbuffer: зберігаємо (char, attr) для кожної клітинки
        # attr = 0 або None коли немає атрибуту
        self.backbuffer = [[(" ", 0) for _ in range(self.win_w)] for _ in range(self.win_h)]

        # {name: {"frame": [...], "y": int, "x": int, "z": int}}
        self.elements = {}

    # -------------------------------
    # compute_position (як раніше)
    # -------------------------------
    def compute_position(self, element, frame):
        self.win_h, self.win_w = self.win.getmaxyx()

        pad_x = element.get("padding", {}).get("x", 0)
        pad_y = element.get("padding", {}).get("y", 0)

        sprite_h = len(frame)
        sprite_w = max(len(line) if isinstance(line, str) else len(line) for line in frame) if frame else 0

        # Y
        y = element.get("y", 0)
        if isinstance(y, str):
            if y == "top":
                y = pad_y
            elif y == "bottom":
                y = self.win_h - sprite_h - pad_y
            elif y == "center":
                y = (self.win_h - sprite_h) // 2 + pad_y
            else:
                raise ValueError(f"Unknown y alignment '{y}'")
        else:
            y = y + pad_y

        # X
        x = element.get("x", 0)
        if isinstance(x, str):
            if x == "left":
                x = pad_x
            elif x == "right":
                x = self.win_w - sprite_w - pad_x
            elif x == "center":
                x = (self.win_w - sprite_w) // 2 + pad_x
            else:
                raise ValueError(f"Unknown x alignment '{x}'")
        else:
            x = x + pad_x

        return y, x

    # -------------------------------
    # draw_frame: тепер працює з (char, attr)
    # -------------------------------
    def draw_frame(self, frame, y0, x0):
        self.win_h, self.win_w = self.win.getmaxyx()

        for i, line in enumerate(frame):
            sy = y0 + i
            if sy < 0 or sy >= self.win_h:
                continue

            # plain string row
            if isinstance(line, str):
                for j, ch in enumerate(line):
                    if ch == TRANSPARENT_CHAR:
                        continue
                    sx = x0 + j
                    if not (0 <= sx < self.win_w):
                        continue

                    new_char, new_attr = ch, 0
                    old_char, old_attr = self.backbuffer[sy][sx]

                    # якщо символ або атрибут змінилися -> малюємо
                    if (new_char == " ") or (new_char != old_char) or (new_attr != old_attr):
                        try:
                            if new_attr:
                                self.win.addch(sy, sx, new_char, new_attr)
                            else:
                                self.win.addch(sy, sx, new_char)
                        except:
                            pass
                        self.backbuffer[sy][sx] = (new_char, new_attr)

            # styled row: list of (ch, attr)
            else:
                for j, pair in enumerate(line):
                    # pair may be (ch, attr)
                    if not isinstance(pair, tuple) or len(pair) < 1:
                        continue
                    ch = pair[0]
                    attr = pair[1] if len(pair) > 1 and pair[1] is not None else 0

                    if ch == TRANSPARENT_CHAR:
                        continue
                    sx = x0 + j
                    if not (0 <= sx < self.win_w):
                        continue

                    old_char, old_attr = self.backbuffer[sy][sx]
                    if (ch != old_char) or (attr != old_attr):
                        try:
                            if attr:
                                self.win.addch(sy, sx, ch, attr)
                            else:
                                self.win.addch(sy, sx, ch)
                        except:
                            pass
                        self.backbuffer[sy][sx] = (ch, attr)

    # -------------------------------
    # _remove_element: стираємо і backbuffer (з урахуванням атрибутів)
    # -------------------------------
    def _remove_element(self, name):
        if name not in self.elements:
            return

        elem = self.elements.pop(name)
        frame = elem["frame"]
        y0, x0 = elem["y"], elem["x"]

        self.win_h, self.win_w = self.win.getmaxyx()

        for i, line in enumerate(frame):
            sy = y0 + i
            if sy < 0 or sy >= self.win_h:
                continue

            length = len(line) if isinstance(line, str) else len(line)

            for j in range(length):
                sx = x0 + j
                if 0 <= sx < self.win_w:
                    # erase to default (char " ", attr 0)
                    self.backbuffer[sy][sx] = (" ", 0)
                    try:
                        self.win.addch(sy, sx, " ")
                    except:
                        pass

    # -------------------------------
    # clear: очищає backbuffer і curses
    # -------------------------------
    def clear(self):
        self.win_h, self.win_w = self.win.getmaxyx()
        for y in range(self.win_h):
            for x in range(self.win_w):
                self.backbuffer[y][x] = (" ", 0)
                try:
                    self.win.addch(y, x, " ")
                except:
                    pass
        self.win.refresh()
        self.elements.clear()

    # -------------------------------
    # render: очікує sprites_data як раніше (можна full_reset)
    # -------------------------------
    def render(self, sprites_data):
        # full reset when requested (room changed)
        if sprites_data.get("full_reset"):
            self.clear()

        sprites_dict = sprites_data["sprites"]
        current_names = set(sprites_dict.keys())

        # remove missing elements
        removed = set(self.elements.keys()) - current_names
        for name in removed:
            self._remove_element(name)

        # add/update elements
        for name, s in sprites_dict.items():
            if not s.get("changed", True):
                continue

            frame = s.get("sprite", [])
            z = s.get("z", 0)

            y, x = self.compute_position(s, frame)

            self.elements[name] = {
                "frame": frame,
                "y": y,
                "x": x,
                "z": z
            }

        # draw in z order (lower -> higher)
        sorted_elements = sorted(self.elements.values(), key=lambda e: e["z"])
        for elem in sorted_elements:
            self.draw_frame(elem["frame"], elem["y"], elem["x"])

        self.win.refresh()