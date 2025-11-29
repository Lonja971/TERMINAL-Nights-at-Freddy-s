from utils.log import debug_log

TRANSPARENT_CHAR = "№"

class Renderer:
    def __init__(self, win):
        self.win = win

    def compute_position(self, element, frame):
        # Window size
        win_h, win_w = self.win.getmaxyx()

        # Padding
        pad_x = element.get("padding", {}).get("x", 0)
        pad_y = element.get("padding", {}).get("y", 0)

        # Sprite size
        sprite_h = len(frame)
        sprite_w = max(len(line) for line in frame) if frame else 0

        # ----- Y -----
        y = element.get("y", 0)
        if isinstance(y, str):
            if y == "top":
                y = pad_y
            elif y == "bottom":
                y = win_h - sprite_h - pad_y
            else:
                raise ValueError(f"Unknown y alignment '{y}'")
        else:
            y = y + pad_y

        # ----- X -----
        x = element.get("x", 0)
        if isinstance(x, str):
            if x == "left":
                x = pad_x
            elif x == "right":
                x = win_w - sprite_w - pad_x
            else:
                raise ValueError(f"Unknown x alignment '{x}'")
        else:
            x = x + pad_x

        return y, x

    # ---------------------------
    #   DRAWING ONE FRAME
    # ---------------------------
    def draw_frame(self, frame, y0, x0):
        win_h, win_w = self.win.getmaxyx()

        for i, line in enumerate(frame):
                sy = y0 + i
                if sy < 0 or sy >= win_h:
                    continue

                # рядок — звичайний string
                if isinstance(line, str):
                    for j, ch in enumerate(line):
                        if ch == TRANSPARENT_CHAR:   # пропускаємо спеціальні прозорі символи
                            continue
                        sx = x0 + j
                        if 0 <= sx < win_w:
                            try:
                                self.win.addch(sy, sx, ch)
                            except:
                                pass

                # рядок — styled (список кортежів (ch, attr))
                else:
                    for j, (ch, attr) in enumerate(line):
                        if ch == TRANSPARENT_CHAR:   # прозорість контролюється символом
                            continue
                        sx = x0 + j
                        if 0 <= sx < win_w:
                            try:
                                self.win.addch(sy, sx, ch, attr)
                            except:
                                pass



    # ---------------------------
    #   MAIN RENDER CALL
    # ---------------------------
    def render(self, elements):
        for element in elements:
            frame = element["frame"]

            # Calculate final position
            y, x = self.compute_position(element, frame)

            # Draw sprite
            self.draw_frame(frame, y, x)
