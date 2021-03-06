import pygame

from effects.bonuses import *
from menu.menu import *
import os
import math
from functions.functions import *
import random

# menu_bg = pygame.transform.scale(load_image("resources", "tower_menu.png").convert_alpha(), (120, 70))
turret_image = pygame.transform.scale(load_image("resources", "cannonball.png"),(50, 50))
tower_base = pygame.transform.scale(load_image("resources", "tower_base.png").convert_alpha(), (50, 50))
pygame.mixer.pre_init(44100, 16, 2, 4096)
structure_placement_sound = pygame.mixer.Sound(os.path.join("resources", "structure_placement.mp3"))


class Tower:
    """
    Abstract class for towers
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.crit_chance = 0
        self.crit_damage = 1.2
        self.range = 100
        self.sell_value = [0,0,0, None]
        self.price = [0,0,0, None]
        self.upgrade_bonus_dmg = [0, 2, 3, None]
        self.level = 1
        self.selected = False
        self.name = "default tower"
        self.ico_name = "buy_default_tower"
        self.accuracy = 0.5
        # define menu and buttons
        # self.menu_bg = menu_bg
        #self.menu = TowerMenu(self, self.x, self.y, 120, 70, self.menu_bg)
        # self.menu = TowerMenu(self.x, self.y - 50, 250, 122, self.menu_bg, self.sell_value)
        self.turret_angle = 0
        self.turret_image = turret_image
        self.tower_base = tower_base
        self.damage = 1
        self.delay = self.attack_speed = 10 #lower is faster
        self.place_color = (0,0,255, 100)
        self.attack_speed = 1
        self.max_delay = 50
        self.delay = 50
        self.structure_placement_sound = structure_placement_sound
        self.projectiles = None
        self.projectile_speed = 10
        # modifiers:
        self.mod_crit_chance = 0
        self.mod_crit_damage = 0
        self.mod_damage = 0
        self.mod_accuracy = 0
        self.mod_max_splash_range = 0
        self.mod_projectile_speed = 0
        self.mod_attack_speed = 0
        self.mod_attack_range = 0
        self.mod_projectile_size = 0
        self.stun = Stun(0)
        self.poison = Poison(0)
        self.piercing = Piercing(0)
        self.headshot = Headshot(0)
        self.fragmentation = Fragmentation(0)

        #specials:
        # Stun stuff -----
        self.stun_chance = 0
        self.stun_duration = 0

        # Piercing stuff -----
        self.pierce_chance = 0

        # Poison stuff -----
        self.poison_chance = 0
        # percentage of regular damage done in poison (ignored crit/headshots)
        self.poison_damage = 0.25
        self.poison_duration = 100
        self.poison_frequency = 25
        self.max_poison_stacks = 5

        # Headshot stuff -----
        # chance to convert crit to headshot causing X* damage
        self.headshot_chance = 0
        self.headshot_multiplier = 25

        # Fragmentation stuff -----
        self.fragment_chance = 0
        self.fragment_count = 0

        self.bonus_xp = 0

    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        img = self.tower_base
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

        # draw menu
        if self.selected:
            self.menu.draw(win)

    def clear_modifiers(self):
        self.mod_crit_chance = 0
        self.mod_crit_damage = 0
        self.mod_damage = 0
        self.mod_accuracy = 0
        self.mod_max_splash_range = 0
        self.mod_projectile_speed = 0
        self.mod_attack_speed = 0
        self.mod_attack_range = 0
        self.mod_projectile_size = 0

    def print_modifiers(self):
        print ("mod_crit_chance:", self.mod_crit_chance, "mod_crit_damage", self.mod_crit_damage, "mod_damage", self.mod_damage, "mod_accuracy", self.mod_accuracy, "mod_max_splash_range", self.mod_max_splash_range, "mod_projectile_speed", self.mod_projectile_speed, "mod_attack_speed", self.mod_attack_speed, "mod_attack_range", self.mod_attack_range, "mod_projectile_size", self.mod_projectile_size)

    def draw_tower_menu(self, win):
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self, win):
        if self.selected:
            # draw range circle
            surface = pygame.Surface((self.range * 3, self.range * 3), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128, 128, 128, 100), (self.range, self.range), self.range, 0)

            win.blit(surface, (self.x - self.range, self.y - self.range))

    def draw_placement(self, win):
        # draw range circle
        surface = pygame.Surface((self.range * 4, self.range * 4), pygame.SRCALPHA, 32)
        placement_circle = self.turret_image.get_width() / 2
        pygame.draw.circle(surface, self.place_color, (placement_circle, placement_circle), placement_circle, 0)

        win.blit(surface, (self.x - placement_circle, self.y - placement_circle))

    def click(self, X, Y):
        """
        returns if tower has been clicked on
        and selects tower if it was clicked
        :param X: int
        :param Y: int
        :return: bool
        """
        #img = self.tower_imgs[self.level - 1]
        img = self.turret_image
        """
        if X <= self.x - img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
            if Y <= self.y + self.height - img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False
        """
        if X <= self.x - 25 + self.width and X >= self.x - 25:
            if Y <= self.y + self.height - 25 and Y >= self.y - 25:
                return True
        return False

    def sell(self):
        """
        call to sell the tower, returns sell price
        :return: int
        """
        return self.sell_value[self.level-1]

    def get_next_level_info(self, bonus):
        """
        Get the next level value of the requested bonus
        :param bonus: list of int
        :returns: the value of list index of the requested bonus
        """
        if (self.level+1) > len(bonus):
            return "MAX"
        return bonus[self.level]

    def place_structure(self):
        """
        Play sound
        :returns: None
        """
        action_sound = pygame.mixer.Sound(self.structure_placement_sound)
        action_sound.set_volume(0.6)
        action_sound.play()
        # THIS ISN'T QUITE RIGHT!
        # self.menu.add_btn(upgrade_btn, "Upgrade")
        # self.menu.add_btn(sell_btn, "Sell")

    def upgrade(self):
        """
        upgrades the tower for a given cost
        :return: None
        """
        if self.level < len(self.turret_imgs):
            self.level += 1
            self.damage += self.upgrade_bonus_dmg[self.level-1]
            self.accuracy += self.upgrade_bonus_accuracy[self.level - 1]
            self.range += self.upgrade_bonus_range[self.level - 1]
            self.attack_speed += self.upgrade_bonus_atk_speed[self.level - 1]
            self.turret_image = self.turret_imgs[self.level][0]


    def get_upgrade_cost(self):
        """
        returns the upgrade cost, if 0 then can't upgrade anymore
        :return: int
        """
        return self.price[self.level-1]

    def get_sales_value(self):
        """
        returns the sales value
        :return: int
        """
        return self.sell_value[self.level-1]

    def move(self, x, y):
        """
        moves tower to given x and y
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
        # self.menu.x = x
        # self.menu.y = y
        # self.menu.update()

    def collide(self, otherTower):
        """
        Detect collision with towers
        :param otherTower: list of polygon shapes
        :return: Bool
        """

        x1 = self.x
        y1 = self.y
        x2 = otherTower.x
        y2 = otherTower.y
        return self.collide_coordinates(x1, y1, x2, y2)

    def collide_coordinates(self, x1, y1, x2, y2):
        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        #if dis >= self.tower_base.get_width():
        if dis >= 45:
            return False
        else:
            return True

    def locations_collide(self, locations):
        """
        Detect collision with areas
        :param locations: list of polygon shapes
        :return: Bool
        """
        hit = False
        for location in locations:
            hit = self.location_collide(location)
            if hit:
                break
        return hit

    def location_collide(self, location):
        """
        http://www.jeffreythompson.org/collision-detection/poly-point.php
        Detect collision with a polygon
        :param location: list of coordinates of polygon
        :return: Bool
        """
        collision = False

        # go through each of the vertices, plus
        # the next vertex in the list
        pnext = 0

        for idx, current in enumerate(location):
            # get next vertex in list
            # if we've hit the end, wrap around to 0
            pnext = idx + 1
            if pnext == len(location):
                pnext = 0

            # get the PVectors at our current position
            # this makes our if statement a little cleaner
            vc_x = current[0]  # c for "current"
            vc_y = current[1]
            vn_x = location[pnext][0]  # n for "next"
            vn_y = location[pnext][1]
            # compare position, flip 'collision' variable
            # back and forth
            if ((vc_y >= self.y and vn_y < self.y) or (vc_y < self.y and vn_y >= self.y)) and (
                    self.x < (vn_x - vc_x) * (self.y - vc_y) / (vn_y - vc_y) + vc_x):
                collision = not collision
        return collision

    def rotate(self, turret_angle, offset, pivot_point):
        """
        Rotate the surface around the pivot point.
        Args:
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pygame.transform.rotozoom(self.turret_image, (turret_angle - 180)*-1, 1)  # Rotate the image.
        rotated_offset = offset.rotate(turret_angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot_point + rotated_offset)
        return rotated_image, rect  # Return the rotated image

    def find_target(self, enemies, auto_target=True):
        """
        Action for when attacking
        :param enemies: enemy
        :param auto_target: boolean
        :return: Item
        """

    def attack(self, enemies):
        """
        Action for when attacking
        :param enemies: enemy
        :return: Item
        """

    def get_location(self):
        return [self.x, self.y]

    def explode_on_impact(self, x, y, fragment_count):
        """
        Action performed on impact
        :param x: int x location
        :param y: int y locaiton
        :param fragment_count: int amount of fragements
        :return: None
        """
