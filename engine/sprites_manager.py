from config.sprite_registry import SPRITES
from utils.sprite_loader import load_sprite
from config.generators import GENERATORS
from utils.log import debug_log

class SpritesManager:
    def __init__(self, win_size):
        self.registry = SPRITES
        self.win_size = win_size

    def get_all_sprites(self, active_sprites):
        elements = []

        for spr in active_sprites:
            name = spr["name"]
            data = spr.get("data", {})

            # Перевіряємо чи є такий спрайт у реєстрі
            if name not in self.registry:
                # Можеш додати debug_log якщо треба
                continue

            sprite_data = self.registry[name]

            # Передаємо дані зі списку активних спрайтів у sprite_data
            # Наприклад можна дозволити overriding x,y,z
            merged_data = {**sprite_data, **spr}

            element = self.resolve_element(name, data, merged_data)
            elements.append(element)

        # Сортировка за z (якщо не передано, default = 0)
        elements.sort(key=lambda e: e.get("z", 0))

        return elements

    def resolve_element(self, key, element_data, registry_data):
        if registry_data["type"] == "static":
            frame = load_sprite(registry_data["path"])

        elif registry_data["type"] == "animation":
            frame = load_sprite(registry_data["frames"][element_data["curr_frame"]])

        elif registry_data["type"] == "generated":
            debug_log(registry_data["name"])
            gen_func = GENERATORS[registry_data["name"]]
            registry_data["win_size"] = self.win_size
            frame = gen_func(registry_data)

        return {
            "name": key,
            "frame": frame,
            "z": registry_data.get("z", 0),
            "x": registry_data.get("x", 0),
            "y": registry_data.get("y", 0),
            "padding": registry_data.get("padding", {})
        }