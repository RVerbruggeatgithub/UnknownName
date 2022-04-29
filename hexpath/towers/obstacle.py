import pygame
from .tower import Tower
import os
import math
from menu.menu import *
from functions import *
import random

pygame.init()
# bullet_hole = pygame.transform.scale(load_image("resources", "bullet_hole.png").convert_alpha(), (10, 10))
obstacle = pygame.transform.scale(load_image("resources", "obstruction.png").convert_alpha(), (50, 50))
minigun_sound = pygame.mixer.Sound(os.path.join("resources", "minigun.mp3"))


# load tower images
turret_imgs = []
for x in range(1, 4):
    turret_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources", "minigun_" +str(x) + ".png")).convert_alpha(), (50, 50)))


class Obstacle(Tower):
    def __init__(self, x,y):
        super().__init__(x, y)
        self.turret_image = turret_imgs[0]
        self.turret_imgs = turret_imgs
        self.tower_base = obstacle
        self.tower_count = 0
        self.range = 25
        self.original_range = self.range
        self.inRange = False
        self.left = True
        self.damage = 2
        self.accuracy = 0.5
        self.original_damage = self.damage
        self.width = self.height = self.tower_base.get_width()
        self.moving = False
        self.name = "Obstacle"
        self.ico_name = "buy_obstacle"
        self.sell_value = [500,1000,2000]
        self.price = [1000,2000, "MAX"]
        self.upgrade_bonus_dmg = [0, 1, 3]
        self.upgrade_bonus_range = [0, 15, 25]
        self.upgrade_bonus_accuracy = [0, 0.05, 0.05]
        self.upgrade_bonus_atk_speed = [0, 4, 5]
        self.menu.set_tower_details(self)
        # attack speed, higher is faster. Anything above max_delay (tower()) will be set to 0 delay)
        self.attack_speed = 16
        # bullet hole image
        # self.bullet_hole = bullet_hole
        # holes: [timer, x, y] remove when timer = 0
        self.holes = []
        self.action_sound = minigun_sound
        self.kill_locations = []

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the tower base and animated Minigun
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.tower_count += 1
            if self.tower_count >= len(self.turret_imgs):
                self.tower_count = 0
        else:
            self.tower_count = 0

        # draw shadow
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, 40), 16, 0)
        win.blit(surface, (self.x - 32, self.y - 32))


