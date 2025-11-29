import os
from .log import debug_log

ASSETS_DIR = "assets/sprites"

def load_sprite(name):
    """Завантажує txt-спрайт і повертає як список рядків"""
    path = os.path.join(ASSETS_DIR, f"{name}")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Спрайт {name} не знайдено")
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.rstrip("\n") for line in f]
    return lines

def save_sprite(name, lines):
    """Зберігає список рядків як txt-спрайт"""
    os.makedirs(ASSETS_DIR, exist_ok=True)
    path = os.path.join(ASSETS_DIR, f"{name}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
