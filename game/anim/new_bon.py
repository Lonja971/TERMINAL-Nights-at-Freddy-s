from game.anim.anim import Anim
import time
from utils.log import debug_log

class NewBon(Anim):
    def __init__(self, intelligence, locations):
        self.name = "new_bon"
        super().__init__(intelligence, locations)

    def update(self):
        super().update()

        if self.next_move_time == None:
            self.schedule_next_move()
            return
        
        if time.time() >= self.next_move_time:
            is_moving = super().try_move()

            if is_moving:
                self.move()
