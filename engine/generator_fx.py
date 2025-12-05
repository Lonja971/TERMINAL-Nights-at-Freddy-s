from utils.log import debug_log
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
        line = []
        for ch in item:
            if idx == selected:
                line.append((ch, curses.A_REVERSE))
            else:
                line.append((ch, 0))
        frame.append(line)
    
    return frame