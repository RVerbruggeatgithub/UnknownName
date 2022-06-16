import math


class Bonus:
    def __init__(self, level=0, chance=0):
        self.level = level
        self.chance = chance

    def upgrade(self):
        if self.level + 1 <= 5:
            self.level += 1
            self.update_stats()

    def update_stats(self):
        """
        Update stats base on level
        :return:
        """


class Poison(Bonus):
    def __init__(self, level=0, chance=0, duration=0, damage=0, frequency=0):
        super().__init__(level, chance)
        self.duration = duration
        self.frequency = self.timer = frequency
        self.damage = damage
        self.max_stacks = 5

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

    def update_stats(self):
        _chance = [0, 0.12, 0.17, 0.23, 0.30, 0.40]
        _duration = [0, 60, 90, 80, 100, 105]
        _frequency = [0, 30, 30, 20, 20, 15]
        self.chance = _chance[self.level]
        self.duration = _duration[self.level]
        self.frequency = _frequency[self.level]


class Stun(Bonus):
    def __init__(self, level=0, chance=0, duration=0):
        super().__init__(level, chance)
        self.duration = duration

    def update_stats(self):
        _chance = [0, 0.1, 0.15, 0.22, 0.3, 0.4]
        _duration = [0, 20, 22, 30, 28, 40]
        self.chance = _chance[self.level]
        self.duration = _duration[self.level]


class Piercing(Bonus):
    def __init__(self, level=0, chance=0):
        super().__init__(level, chance)

    def update_stats(self):
        _chance = [0, 0.1, 0.12, 0.22, 0.35, 0.50]
        self.chance = _chance[self.level]


class Headshot(Bonus):
    def __init__(self, level=0, chance=0):
        super().__init__(level, chance)
        self.headshot_multiplier = 1

    def update_stats(self):
        _chance = [0, 0.1, 0.15, 0.22, 0.3, 0.4]
        _headshot_multiplier = [1, 10, 10, 15, 15, 20]
        self.chance = _chance[self.level]
        self.headshot_multiplier = _headshot_multiplier[self.level]


class Fragmentation(Bonus):
    def __init__(self, level=0, chance=0, damage=0, fragments=0):
        super().__init__(level, chance)
        self.fragments = fragments
        self.damage = damage

    def update_stats(self):
        _chance = [0, 0.08, 0.11, 0.18, 0.25, 0.35]
        _fragments = [0, 1, 1, 2, 2, 3]
        _damage = [0, 0.12, 0.18, 0.28, 0.4, 0.5]
        self.chance = _chance[self.level]
        self.fragments = _fragments[self.level]
        self.damage = _damage[self.level]
