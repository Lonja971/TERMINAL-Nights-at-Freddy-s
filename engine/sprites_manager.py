from config.generators import GENERATORS
from utils.sprite_loader import load_sprite
from utils.log import debug_log
from config.rooms import ROOMS
from config.sprite_registry import SPRITES
import copy

class SpritesManager:
    def __init__(self, win_size, curr_state):
        self.win_size = win_size
        self.prev_state = curr_state

    def get_update(self, frame_data):
        frame_data.setdefault("sprites", {})
        room_name = frame_data["room"]
        room_def = ROOMS[room_name]
        room_def.setdefault("sprites", {})

        update_package = {
            "bg_changed": False,
            "sprites": {}
        }

        # -----------------------------
        # 1. Перевірка зміни фону
        # -----------------------------
        bg_cfg = room_def.get("bg")
        bg_name = bg_cfg["name"] if bg_cfg else "None"

        if room_name != (self.prev_state.get("room") if self.prev_state else None):
            update_package["bg_changed"] = True
            update_package["sprites"][bg_name] = self._make_full_sprite(
                bg_name, frame_data["sprites"].get(bg_name, {}))
        else:
            update_package["sprites"][bg_name] = {"changed": False}

        # -----------------------------
        # 2. Опрацювати інші спрайти
        # -----------------------------
        for name, runtime in frame_data["sprites"].items():
            cfg = room_def["sprites"].get(name, {})
            if cfg == {}:
                continue

            changed = self._sprite_changed(name, runtime)

            if changed or update_package["bg_changed"]:
                update_package["sprites"][name] = self._make_full_sprite(cfg["name"], runtime, cfg)
            else:
                update_package["sprites"][name] = {"changed": False}

        # -----------------------------
        # 3. Оновити prev_state (deepcopy!)
        # -----------------------------
        self.prev_state = copy.deepcopy(frame_data)

        return update_package

    # -----------------------------
    # CHECK IF SPRITE CHANGED
    # -----------------------------
    def _sprite_changed(self, name, runtime):
        prev = self.prev_state["sprites"].get(name) if self.prev_state else None

        # 1. Новий спрайт
        if prev is None:
            return True

        # 2. Порівнюємо "data", якщо є
        prev_data = prev.get("data")
        curr_data = runtime.get("data")
        if prev_data != curr_data:
            return True

        # 3. Перевіряємо інші атрибути (type, z, x, y, padding тощо)
        prev_copy = {k: v for k, v in prev.items() if k != "data"}
        curr_copy = {k: v for k, v in runtime.items() if k != "data"}
        if prev_copy != curr_copy:
            return True

        # 4. Немає змін
        return False

    # -----------------------------
    # CREATE FULL SPRITE CONTENT
    # -----------------------------
    def _make_full_sprite(self, name, runtime, room_cfg=None):
        reg = SPRITES[name]
        tp = reg["type"]

        # Базовий обʼєкт
        out = {
            "changed": True,
            "z": room_cfg.get("z", 0) if room_cfg else 0,
            "x": room_cfg.get("x", "left") if room_cfg else "left",
            "y": room_cfg.get("y", "top") if room_cfg else "top",
            "padding": room_cfg.get("padding", {"x": 0, "y": 0}) if room_cfg else {"x": 0, "y": 0},
            "sprite": None
        }

        runtime_data = runtime.get("data", {})

        # -----------------------------
        # Отримати sprite
        # -----------------------------
        if tp == "static":
            out["sprite"] = load_sprite(reg["path"])

        elif tp == "animation":
            frame_idx = runtime_data.get("curr_frame", 0)
            out["sprite"] = load_sprite(reg["frames"][frame_idx])

        elif tp == "generated":
            reg_copy = reg.copy()
            reg_copy["win_size"] = self.win_size
            reg_copy["data"] = runtime_data
            gen_func = GENERATORS[name]
            out["sprite"] = gen_func(reg_copy)

        return out
