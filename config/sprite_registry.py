SPRITES = {
    # -------------------------- #
    #        МЕНЮ                #
    # -------------------------- #
    "menu_bg": {
        "type": "static",
        "path": "menu/bg/bg0.txt",
        "z": 2,
        "x": "right",
        "y": "bottom",
        #"padding": {"x": 10, "y": 5}
    },
    "game_office_l": {
        "type": "static",
        "path": "game/office/l.txt",
    },
    "game_office_r": {
        "type": "static",
        "path": "game/office/r.txt",
    },

    # -------------------- #
    #      АНІМАЦІЇ        #
    # -------------------- #
    "menu_anim_bg": {
        "type": "animation",
        "frames": [
            "menu/bg/bg0.txt",
            "menu/bg/bg1.txt",
            "menu/bg/bg2.txt",
            "menu/bg/bg3.txt"
        ],
        "update_in": 1,
        "loop": True,
        "z": 2,
        "x": "right",
        "y": "bottom",
        "padding": {"x": 10, "y": 5}
    },

    # -------------------------- #
    #      ПРОЦЕДУРНІ ФОНИ       #
    # -------------------------- #
    "background_dots": {
        "type": "generated",
        "bg": True,
        "z": 0
    },
    "main_menu_options": {
        "type": "generated",
        "bg": True,
        "z": 3,
        "x": "left",
        "y": "bottom",
        "padding": {"x":5, "y":2}
    },
}
