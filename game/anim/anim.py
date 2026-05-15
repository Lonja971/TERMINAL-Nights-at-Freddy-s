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
        self.need_time_to_check = anim_data["checking_time"]
        self.is_active = False
        self.is_attacking = False

        self.intelligence = intelligence
        self.pos = self.def_pos
        self.move_time = anim_data["move_time"]
        self.value_for_screamer = calculate_iter_for_screamer(intelligence)
        self.office_time = anim_data["office_time"]
        self.activation_time = calculate_activation_time(intelligence)
        self.next_move_time = None

        self.screamer_value = 0
        self.checking_time = 0
        self.screamer_timer = 20

        if self.pos not in self.locations:
            self.locations[self.pos] = []
        self.locations[self.pos].append(self.name)

        debug_log(f"{self.name} - {self.activation_time}")

    def process_screamer_waiting(self):
        self.screamer_timer -= 1

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
        self.screamer_value = 0
        self.checking_time = 0

        if self.name in self.locations[self.pos]:
            self.locations[self.pos].remove(self.name)

        self.pos = new_pos

        if self.pos not in self.locations:
            self.locations[self.pos] = []
        self.locations[self.pos].append(self.name)

        debug_log(f"{self.name} moved to {self.pos}")

    def process_office_watching(self):
        if self.screamer_value >= self.value_for_screamer:
            self.is_attacking = True

        self.checking_time += 1

        if self.checking_time >= self.need_time_to_check:
            if self.is_attacking:
                self.change_pos(20)
            else:
                self.change_pos(self.def_pos)

    def update(self):
        if not self.is_active:
            return
        
        if self.pos == 15:
            self.next_move_time = None
            self.process_office_watching()
            debug_log(f"{self.name} = {self.pos} - {self.screamer_value} ({self.value_for_screamer})")
            return

        if self.next_move_time == None:
            self.schedule_next_move()
            return
        
        if time.time() >= self.next_move_time:
            is_moving = self.try_move()

            if is_moving:
                self.move()
                
