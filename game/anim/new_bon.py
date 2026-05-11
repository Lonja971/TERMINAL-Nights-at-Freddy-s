from game.anim.anim import Anim
import time
from utils.log import debug_log

class NewBon(Anim):
    def __init__(self, intelligence, locations):
        self.name = "new_bon"
        super().__init__(intelligence, locations)

    def update(self):
        if not self.is_active:
            return

        if self.next_move_time == None:
            self.schedule_next_move()
            return
        
        if time.time() >= self.next_move_time:
            self.try_move()
            self.schedule_next_move()