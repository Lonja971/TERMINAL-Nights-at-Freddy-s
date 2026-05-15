from .systems.buttery import ButterySystem
from .systems.music_box import MusicBox
from .systems.time import TimeSystem
from utils.log import debug_log
from config.nights import NIGHTS
from game.anim.new_bon import NewBon
from game.anim.new_fred import NewFred
from game.anim.new_bird import NewBird
from game.anim.old_bon import OldBon
from game.anim.old_fred import OldFred
from game.anim.old_bird import OldBird
from game.anim.mangle import Mangle
from game.anim.old_foxy import OldFoxy
from game.anim.bb import BB
from game.anim.puppet import Puppet

class GameState:
    def __init__(self, night_num):
        self.state = "processing" # screamer_anima / end
        self.screamer_anima_name = None
        self.buttery = ButterySystem()
        self.music_box = MusicBox(1)
        self.time = TimeSystem()

        self.anim_data = NIGHTS.get(night_num, NIGHTS[1])["anim"]
        self.locations = {}
        self.animatronics = {
            "new_bon": NewBon(self.anim_data.get("new_bon", {}).get("intelligence", 0), self.locations),
            "new_fred": NewFred(self.anim_data.get("new_fred", {}).get("intelligence", 0), self.locations),
            "new_bird": NewBird(self.anim_data.get("new_bird", {}).get("intelligence", 0), self.locations),
            "old_bon": OldBon(self.anim_data.get("old_bon", {}).get("intelligence", 0), self.locations),
            "old_fred": OldFred(self.anim_data.get("old_fred", {}).get("intelligence", 0), self.locations),
            "old_bird": OldBird(self.anim_data.get("old_bird", {}).get("intelligence", 0), self.locations),
            "old_foxy": OldFoxy(self.anim_data.get("old_foxy", {}).get("intelligence", 0), self.locations),
            "mangle": Mangle(self.anim_data.get("mangle", {}).get("intelligence", 0), self.locations),
            "bb": BB(self.anim_data.get("bb", {}).get("intelligence", 0), self.locations),
            "puppet": Puppet(self.anim_data.get("puppet", {}).get("intelligence", 0), self.locations),
        }
        self.office_pos = "l"
        self.is_camera_open = False
        self.is_camera_light = False
        self.is_tablet_opening_anim = False
        self.tablet_anim_dir = "open"
        self.active_camera_num = 9
        self.is_mask = False
        self.is_removing_mask = False
        self.light = None

        self.is_mask_disabled = False
        self.is_tablet_disabled = False

    def get_buttery_level(self):
        return self.buttery.power

    def build_render_data(self):
        return {
            "sprites": {},
            "full_reset": False
        }
    
    def set_screamer_anima(self, name):
        self.state = "screamer_anima"
        self.screamer_anima_name = name
    
    def set_office_pos(self, pos):
        if self.is_camera_open: return
        
        self.office_pos = pos.lower()

    def set_light(self, side, is_on=True):
        if self.buttery.power <= 0: return
        if self.is_mask: return

        if self.light != side and is_on:
            self.light = side
            return
        
        if self.light == side and not is_on:
            self.light = None

    def set_mask(self):
        if self.is_mask_disabled: return
        if self.is_removing_mask: return
        if self.is_camera_open or self.is_tablet_opening_anim: return
        if self.state == "screamer_anima": return

        self.is_mask = not self.is_mask
        if self.is_mask and self.light:
            self.light = None

    def set_camera(self):
        if self.is_mask or self.is_removing_mask: return
        if self.state == "screamer_anima": return

        self.is_camera_open = not self.is_camera_open

        if not self.is_camera_open and self.is_camera_light:
            self.is_camera_light = False

        if self.is_camera_open and self.light:
            self.light = None

    def start_opening_tablet(self):
        if self.is_tablet_disabled: return
        if self.is_mask or self.is_removing_mask: return

        self.is_tablet_opening_anim = not self.is_tablet_opening_anim
        if self.is_camera_open:
            self.tablet_anim_dir = "close"
        else:
            self.tablet_anim_dir = "open"

        if self.is_tablet_opening_anim and self.light:
            self.light = None

        if self.is_camera_open:
            self.is_camera_open = False
            if self.is_camera_light: self.is_camera_light = False 

    def set_camera_light(self, is_on=True):
        if self.buttery.power <= 0: return
        if self.state == "screamer_anima": return

        if self.is_camera_open or self.is_tablet_opening_anim:
            self.is_camera_light = is_on

    def change_active_camera(self, cam="next"):
        if not self.is_camera_open: return

        if cam == "prev":
            if self.active_camera_num - 1 >= 1:
                self.active_camera_num -= 1
            else:
                self.active_camera_num = 12
        elif cam == "next":
            if self.active_camera_num + 1 <= 12:
                self.active_camera_num += 1
            else:
                self.active_camera_num = 1
            
        elif isinstance(cam, int):
            pass

    def screamer_disabeling(self):
        self.is_mask_disabled = True
        self.is_tablet_disabled = True
        self.is_mask = False
        if self.is_camera_open:
            self.is_camera_open = False
            self.tablet_anim_dir = "close"
            self.is_tablet_opening_anim = True