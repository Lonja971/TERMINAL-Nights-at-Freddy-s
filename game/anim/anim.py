from config.anim import ANIMATRONICS
import time, random
from utils.log import debug_log

class Anim:
    def __init__(self, intelligence, locations):
        self.locations = locations
        anim_data = ANIMATRONICS[self.name]
        self.def_pos = anim_data["default_position"]
        self.path_graph = anim_data["path_graph"]
        self.is_active = False

        self.intelligence = intelligence
        self.pos = self.def_pos
        self.move_time = anim_data["move_time"]
        self.time_for_screamer = max(3, anim_data["time_for_screamer"] - self.intelligence)
        self.office_time = anim_data["office_time"]
        self.min_activation_time = anim_data["min_activation_time"]
        self.next_move_time = None

        if self.pos not in self.locations:
            self.locations[self.pos] = []
        self.locations[self.pos].append(self.name)

    def schedule_next_move(self):
        speed = self.intelligence * 0.4
        delay = max(2.0, self.move_time - speed)
        delay += random.uniform(-1.5, 1.5)

        self.next_move_time = time.time() + delay

    def try_move(self):
        roll = random.randint(0, 1)

        if roll < self.intelligence:
            self.move()

    def move(self):
        posible_positions = self.path_graph.get(self.pos, [])
        if len(posible_positions) == 0:
            self.change_pos(self.def_pos)
            return
        
        index = random.randint(1, len(posible_positions))
        self.change_pos(posible_positions[index - 1])

    def change_pos(self, new_pos):
        if self.name in self.locations[self.pos]:
            self.locations[self.pos].remove(self.name)

        self.pos = new_pos

        if self.pos not in self.locations:
            self.locations[self.pos] = []
        self.locations[self.pos].append(self.name)

        debug_log(f"{self.name} moved to {self.pos}")

    def update(self):
        if not self.is_active:
            return

        pass