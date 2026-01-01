from engine.generator_fx import (
    generate_dot_background,
    generate_main_menu_options,
    none_bg,
    generate_game_buttery,
    game_timeblock,
    game_nightnumber
)

GENERATORS = {
    "None": none_bg,
    "background_dots": generate_dot_background,
    "main_menu_options": generate_main_menu_options,
    "game_buttery": generate_game_buttery,
    "game_timeblock": game_timeblock,
    "game_nightnumber": game_nightnumber
}