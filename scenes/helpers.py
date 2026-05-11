from utils.save import load_config, update_config_value

def new_game(app, update_save):
    new_night = 1
    update_config_value("save.json", "curr_night", new_night)
    update_save()
    app.set_scene("game", {"night_num": new_night})