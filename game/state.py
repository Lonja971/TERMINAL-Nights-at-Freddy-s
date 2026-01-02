class GameState:
    def __init__(self):
        self.hour = 12
        self.buttery = 100
        self.time = [12, 0]
        self.miliseconds = 0

        self.office_pos = "l"
        self.camera = None
        self.is_mask = False
        self.light = False

        self.visible_sprites = {}

    def build_render_data(self):
        return {
            "sprites": self.visible_sprites,
            "full_reset": False
        }
    
    def set_office_pos(self, pos):
        self.office_pos = pos.lower()

    def set_light(self):
        self.light = not self.light