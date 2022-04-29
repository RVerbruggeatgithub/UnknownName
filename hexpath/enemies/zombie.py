import os

import pygame

from .enemy import Enemy
from functions.functions import *
# from items.gold import Gold
# from items.metal import Metal
imgs = []
imgs_elite = []

for x in range(3):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "zombie_0_" + add_str + ".png"),
        (64, 64))
    imgs.append(pygame.transform.rotozoom(img, 90 * -1, 1))

death_sequence = []
for x in range(1, 6):
    death_sequence.append(pygame.transform.scale(load_image("resources", "dead_explode_" + str(x) + ".png"),
        (64, 64)))
pygame.init()
death_sound = pygame.mixer.Sound(os.path.join("resources", "zombie_death.mp3"))

class Zombie(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Zombie"
        self.max_health = 23
        self.health = self.max_health
        self.gate_damage = 100
        self.imgs = imgs[:]
        self.speed_increase = 1.8
        self.size = 0.6
        self.boundary = (0.85 * self.speed_increase)
        self.death_sequence = death_sequence
        self.death_sound = death_sound
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]
        #imgs[:]
