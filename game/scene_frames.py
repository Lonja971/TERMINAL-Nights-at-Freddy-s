from config.rooms import ROOMS
from config.sprite_registry import SPRITES
from utils.log import debug_log

class GameSceneFrames:
    def __init__(self, state, night):
        self.state = state
        self.night = night

    def office_frames(self, curr_scene_frames):
        vent_name = ROOMS[curr_scene_frames["room"]]["sprites"]["office_vent_anima"]["name"]

        frames = {
            "room": "game_office_l" if self.state.office_pos == "l" else "game_office_r",
            "sprites": {
                "game_buttery": {
                    "type": "generated",
                    "data": {
                        "value": self.state.buttery
                    }
                },
                "game_timeblock": {
                    "type": "generated",
                    "data": {
                        "time": self.state.time.copy()
                    }
                },
                "game_nightnumber": {
                    "type": "generated",
                    "data": {
                        "number": self.night
                    }
                },
                "office_vent_anima": {
                    "type": "animation",
                    "update_in": SPRITES[vent_name]["update_in"],
                    "frames_num": len(SPRITES[vent_name]["frames"]),
                    "loop": SPRITES[vent_name]["loop"]
                }
            }
        }

        if self.state.light != "center":
            frames["sprites"]["center_light"] = {
                "type": "static"
            }

        if self.state.office_pos == "l":
            if self.state.light == "left":
                frames["sprites"]["left_light"] = {
                    "type": "static"
                }

        if self.state.office_pos == "r":
            if self.state.light == "right":
                frames["sprites"]["right_light"] = {
                    "type": "static"
                }

        return frames
    
    def update_office_frames(self, curr_scene_frames):
        frames_data = {
            "update": {},
            "delete": []
        }
        curr_sprites_frames = curr_scene_frames["sprites"]

        if self.state.light == "center" and "center_light" in curr_sprites_frames:
            frames_data["delete"].append("center_light")

        if not self.state.light == "center" and "center_light" not in curr_sprites_frames:
            frames_data["update"]["center_light"] = {
                "type": "static"
            }

        if curr_sprites_frames["game_buttery"]["data"]["value"] != int(self.state.buttery):
            frames_data["update"]["game_buttery"] = {
                "type": "generated",
                    "data": {
                        "value": int(self.state.buttery)
                    }
            }

        if curr_sprites_frames["game_timeblock"]["data"]["time"] != self.state.time:
            frames_data["update"]["game_timeblock"] = {
                "type": "generated",
                    "data": {
                        "time": self.state.time.copy()
                    }
            }

        if self.state.office_pos == "l":
            if self.state.light == "left" and "left_light" not in curr_sprites_frames:
                frames_data["update"]["left_light"] = {
                    "type": "static"
                }

            if self.state.light != "left" and "left_light" in curr_sprites_frames:
                frames_data["delete"].append("left_light")
        else:
            if self.state.light == "right" and "right_light" not in curr_sprites_frames:
                frames_data["update"]["right_light"] = {
                    "type": "static"
                }

            if self.state.light != "right" and "right_light" in curr_sprites_frames:
                frames_data["delete"].append("right_light")

        return frames_data

    def process_scene_frames(self, curr_scene_frames):
        frames_data = {
            "rewrite": False,
            "update": {},
            "delete": []
        }

        if self.state.camera == None and self.state.is_mask == False:
            if curr_scene_frames["room"] != f"game_office_{self.state.office_pos}":
                frames_data["rewrite"] = True
                frames_data["update"] = self.office_frames(curr_scene_frames)

            else:
                updated_frames = self.update_office_frames(curr_scene_frames)
                frames_data["update"] = updated_frames["update"]
                frames_data["delete"] = updated_frames["delete"]

        return frames_data