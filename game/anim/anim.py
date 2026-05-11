from config.anim import ANIMATRONICS
import time, random
from utils.log import debug_log
from utils.game_logic import calculate_activation_time, calculate_iter_for_screamer

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
        self.iter_for_screamer = calculate_iter_for_screamer(intelligence)
        self.office_time = anim_data["office_time"]
        self.activation_time = calculate_activation_time(intelligence)
        self.next_move_time = None

        self.screamer_timer = 0

        if self.pos not in self.locations:
            self.locations[self.pos] = []
        self.locations[self.pos].append(self.name)

        debug_log(f"{self.name} - {self.activation_time}")

    def schedule_next_move(self):
        speed = self.intelligence * 0.4
        delay = max(2.0, self.move_time - speed)
        delay += random.uniform(-1.5, 1.5)

        self.next_move_time = time.time() + delay

    def try_move(self):
        roll = random.randint(0, 1)

        return roll < self.intelligence

    def move(self):
        posible_positions = self.path_graph.get(self.pos, [])
        if len(posible_positions) == 0:
            self.change_pos(self.def_pos)
            return
        
        index = random.randint(1, len(posible_positions))
        self.change_pos(posible_positions[index - 1])
        self.schedule_next_move()

    def change_pos(self, new_pos):
        self.screamer_timer = 0

        if self.name in self.locations[self.pos]:
            self.locations[self.pos].remove(self.name)

        self.pos = new_pos

        if self.pos not in self.locations:
            self.locations[self.pos] = []
        self.locations[self.pos].append(self.name)

        debug_log(f"{self.name} moved to {self.pos}")

    def process_office_watching(self):
        if self.screamer_timer >= self.iter_for_screamer:
            self.change_pos(20)

    def update(self):
        if not self.is_active:
            return

        if self.pos == 15:
            self.process_office_watching()
            debug_log(f"{self.name} = {self.pos} - {self.screamer_timer} ({self.iter_for_screamer})")