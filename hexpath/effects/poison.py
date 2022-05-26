import math


class Poison:
    def __init__(self, duration, damage, frequency):
        self.duration = duration
        self.frequency = self.timer = frequency
        self.damage = damage

    def action(self):
        damage = 0
        hit = False
        if self.duration > 0:
            self.timer -= 1
            self.duration -= 1
            if self.timer == 0:

                self.timer = self.frequency
                hit = True
                damage = math.ceil(self.damage)
        return hit, damage
