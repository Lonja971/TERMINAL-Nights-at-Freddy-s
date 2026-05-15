from game.anim.anim import Anim
import time
from utils.log import debug_log

class NewBon(Anim):
    def __init__(self, intelligence, locations):
        self.name = "new_bon"
        super().__init__(intelligence, locations)
