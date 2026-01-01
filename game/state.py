class GameState:
    def __init__(self):
        self.hour = 12
        self.room = "office"
        self.camera = None
        self.buttery = 100
        self.time = [12, 0]
        self.miliseconds = 0

        self.visible_sprites = {}

    def build_render_data(self):
        return {
            "sprites": self.visible_sprites,
            "full_reset": False
        }