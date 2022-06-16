from objects.labels import *
from functions.functions import *


class Enemy:
    def __init__(self, path):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = path
        self.travelled_path = []
        self.x = self.path[0][0]
        self.y = self.path[0][1]
        self.img = pygame.image.load(os.path.join("resources", "lives.png")).convert_alpha()
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.max_health = 0
        self.speed_increase = 1
        # upon survival, it will do this much damage to the gate
        self.gate_damage = 1
        self.angle = 0
        self.anim_seq = 0
        self.size = 1
        self.items = []
        # self.droppable_items = [Gold(self.x, self.y, 3, 10)]
        # max allowed deviation from a node
        self.boundary = (0.93 * self.speed_increase)
        self.death_sequence = []
        self.deviation = [0, 0]
        self.resist_splash_range = 0
        self.dodge_rate = 0
        # reduce chances of getting crit hit on this enemy
        self.crit_resist_rate = 0
        # reduces crit damage taken
        self.crit_resist = 0
        self.item_drop = []
        self.item_drop_rate = 0
        self.survival_damage = 1
        self.xp_value = 1
        self.stun_timer = 0
        self.poison_counters = []
        self.poison_resist_rate = 0
    """
    def generate_item(self):
        item_t = random.choice(self.droppable_items)
        item_t.update_location(self.x, self.y)
        self.items.append(item_t)
    """
    
    def move_action(self, target, params=None):
        """
        Action(s) to perform when moving
        :param target: list of one or multiple targets the move_action is performed on
        :param params: list of parameters
        :return:
        """
        return False

    def draw(self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        """
        for dot in self.path:
            pygame.draw.circle(win, (255,0,255), dot, 10, 0)
        """

        self.img = self.imgs[self.animation_count]
        # Draw shadow
        shadow_radius = self.img.get_width() / 4 * self.size
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, (32 + shadow_radius / 2)), shadow_radius, 0)
        win.blit(surface, (self.x - 32, self.y - 32))
        self.img = pygame.transform.scale(self.img, (self.width * self.size, self.height * self.size))
        self.img = pygame.transform.rotate(self.img, (self.angle+90))
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        draw health bar above enemy
        :param win: surface
        :return: None
        """
        length = 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)
        if self.health < self.max_health:
            pygame.draw.rect(win, (255, 255, 255), (self.x - 31, self.y - 41, (length+2), 6), 0)
            pygame.draw.rect(win, (255, 0, 0), (self.x-30, self.y - 40, length, 4), 0)
            pygame.draw.rect(win, (0, 255, 0), (self.x-30, self.y - 40, health_bar, 4), 0)

    def collide(self, x, y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y: int
        :return: Bool
        """
        if x <= self.x + self.width and x >= self.x:
            if y <= self.y + self.height and y >= self.y:
                return True
        return False

    def move(self):
        """
        Move enemy
        :return: None
        """
        if self.stun_timer > 0:
            self.stun_timer -= 1
            if self.stun_timer <= 0:
                self.stun_timer = 0
        else:
            self.anim_seq += 1
            if self.anim_seq > 5:
                self.animation_count += 1
                self.anim_seq = 0

            if self.animation_count >= len(self.imgs):
                self.animation_count = 0
            x1, y1 = [[0, 0], [0, 0]]
            try:
                x1, y1 = self.path[self.path_pos]
            except ValueError:
                print("Too many values to unpack in:", self.path[self.path_pos], "at path_pos:", self.path_pos, "in:", self.path)
            if self.path_pos + 1 >= len(self.path):
                return
            else:
                x2, y2 = self.path[self.path_pos + 1]
            x2, y2 = self.path[self.path_pos+1]

            delta_y = y2 - y1
            y_mod = -1
            if 0 < delta_y > 0:
                y_mod = delta_y / abs(delta_y)
            slope_angle = point_direction(x2, y2, x1, y1, False) * y_mod * 0.0174532925
            new_move_x = self.speed_increase * -math.cos(slope_angle)
            new_move_y = self.speed_increase * math.sin(slope_angle) * -1 * y_mod

            self.angle = point_direction(x1, y1, x2, y2, False) * -1
            self.x = self.x + new_move_x
            self.y = self.y + new_move_y
            #  self.deviation[0]  self.deviation[1]
            mod_boundary = 0
            if self.path_pos == len(self.path):
                mod_boundary = math.sqrt(self.deviation[0] ** 2 + self.deviation[1] ** 2)
            enemy_distance_to_next_hop = math.sqrt((self.x - x2)**2 + (self.y - y2)**2)
            if -self.boundary - mod_boundary <= enemy_distance_to_next_hop <= self.boundary + mod_boundary:
                self.travelled_path.append(enemy_distance_to_next_hop)
                self.path_pos += 1

    def hit(self, damage):
        """
        Returns if an enemy has died and removes one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            # self.generate_item()
            return True
        if self.health > self.max_health:
            self.health = self.max_health
        return False

    def set_deviation(self, deviation):
        """
        Sets the deviation used to generate individual paths
        :param deviation: list [x, y] coordinates
        :return: None
        """
        self.deviation = deviation

    def get_distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def dead_action(self, enemies):
        """
        Action to perform if killed
        :param enemies: list of enemies
        :return:
        """
        return False
