from engine.generator_fx import (
    generate_dot_background,
    generate_main_menu_options,
    none_bg
)

GENERATORS = {
    "None": none_bg,
    "background_dots": generate_dot_background,
    "main_menu_options": generate_main_menu_options
}