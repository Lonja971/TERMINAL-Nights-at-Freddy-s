from utils.log import debug_log
from assets.ui.alphabet import ASCII_ALPHABET, ASCII_ALPHABET_HEIGHT
import curses

def none_bg(data):
    return []

def generate_dot_background(element_data):
    win_size = element_data["win_size"]
    content = []

    for i in range(win_size[0]):
        content.append("."*(win_size[1]))

    return content

def generate_main_menu_options(element_data):
    selected = element_data["data"].get("selected", 0)
    options = element_data["data"].get("options", [])
    frame = []

    for idx, item in enumerate(options):
            char_blocks = []
            for ch in item.lower():
                if ch in ASCII_ALPHABET:
                    char_blocks.append(ASCII_ALPHABET[ch])
                else:
                    char_blocks.append([ch, " ", " ", " "])

            ascii_lines = ["", "", "", ""]

            for block in char_blocks:
                for i in range(ASCII_ALPHABET_HEIGHT):
                    ascii_lines[i] += block[i]

            for line in ascii_lines:
                line_data = []
                for ch in line:
                    if idx == selected:
                        if ch == "№":
                            ch = "."

                        line_data.append((ch, curses.A_REVERSE))
                    else:
                        line_data.append((ch, 0))
                frame.append(line_data)

    return frame

def generate_game_buttery(data):
    SPRITE_HEIGHT = 4
    BUTTERY_DEELS = 4
    MAX_BATTERY_VALUE = 100

    full = ["━━━", "██ ", "██ ", "━━━"]
    empty = ["━━━", "   ", "   ", "━━━"]
    start = ["┏━", "┃ ", "┃ ", "┗━"]
    end = ["┓", "┗┓", "┏┛", "┛"]

    value = data["data"]["value"]
    deel_size = MAX_BATTERY_VALUE / BUTTERY_DEELS

    (value)

    rows = ["", "", "", ""]

    for i in range(SPRITE_HEIGHT):
        rows[i] += start[i]

    for i in range(BUTTERY_DEELS):
        threshold = i * deel_size
        block = full if value > threshold else empty

        for row in range(SPRITE_HEIGHT):
            rows[row] += block[row]

    for i in range(SPRITE_HEIGHT):
        rows[i] += end[i]

    frame = []
    for line in rows:
        line_data = []
        for ch in line:
            line_data.append((ch, 0))
        frame.append(line_data)

    return frame

def game_timeblock(data):
    SPRITE_HEIGHT = 4

    time = data["data"]["time"]
    hour = str(time[0])
    minutes = str(time[1]) if len(str(time[1])) == 2 else ("0" + str(time[1]))

    frame = ["", "", "", ""]

    for ch in hour.lower():
        if ch in ASCII_ALPHABET:
            block = ASCII_ALPHABET[ch]
        else:
            block = [ch, " ", " ", " "]

        for i in range(SPRITE_HEIGHT):
            frame[i] += block[i]


    middle = ASCII_ALPHABET[":"]
    for i in range(SPRITE_HEIGHT):
        frame[i] += middle[i]


    for ch in minutes.lower():
        if ch in ASCII_ALPHABET:
            block = ASCII_ALPHABET[ch]
        else:
            block = [ch, " ", " ", " "]

        for i in range(SPRITE_HEIGHT):
            frame[i] += block[i]

    return frame

def game_nightnumber(data):
    SPRITE_HEIGHT = 4
    number = data["data"]["number"]
    text = f"night {number}"

    frame = ["", "", "", ""]

    for ch in text.lower():
        if ch in ASCII_ALPHABET:
            block = ASCII_ALPHABET[ch]
        else:
            block = [ch, " ", " ", " "]

        for i in range(SPRITE_HEIGHT):
            frame[i] += block[i]

    return frame