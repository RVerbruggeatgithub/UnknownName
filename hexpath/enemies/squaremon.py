import os

import pygame

from .enemy import Enemy
from functions.functions import *
# from items.gold import Gold
# from items.metal import Metal
Squaremon_imgs = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "squaremon_" + add_str + ".png"),
        (50, 50))
    Squaremon_imgs.append(pygame.transform.rotozoom(img, 90 * -1, 1))

SquaremonGreen_img = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "squaremon_green_" + add_str + ".png"),
        (50, 50))
    SquaremonGreen_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))

trippet_img = []
for x in range(5):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "trippet_" + add_str + ".png"),
        (50, 50))
    trippet_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))

yolkee_img = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "yolkee_" + add_str + ".png"),
        (50, 50))
    yolkee_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))

juju_img = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "juju_" + add_str + ".png"),
        (50, 50))
    juju_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))


pygame.init()


class Squaremon(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Squaremon"
        self.max_health = 12
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.8
        self.size = 0.6
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return Squaremon_imgs

class SquaremonElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonBoss"
        self.max_health = 250
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.6
        self.size = 0.7
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return Squaremon_imgs


class SquaremonGreen(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonGreen"
        self.max_health = 35
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 0.85
        self.size = 0.5
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]
        #imgs[:]

    def load_image(self):
        return SquaremonGreen_img

class SquaremonGreenElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonGreenElite"
        self.max_health = 400
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 0.6
        self.size = 0.7
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]
        #imgs[:]

    def load_image(self):
        return SquaremonGreen_img

class Trippet(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Trippet"
        self.max_health = 75
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.5
        self.size = 0.7
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return trippet_img

class TrippetElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Trippet"
        self.max_health = 200
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.3
        self.size = 1
        self.boundary = 2
        self.spawn_count = 5
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return trippet_img

    def dead_action(self, enemies):
        path = self.path[self.path_pos:]
        for i in range(self.spawn_count):
            generated_path, deviation = generate_alternative_path(path, 14)
            new_enemy = Trippet(generated_path)
            new_enemy.deviation = deviation
            enemies.append(new_enemy)

class Yolkee(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Yolkee"
        self.max_health = 250
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.4
        self.size = 0.7
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return yolkee_img

class Juju(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Juju"
        self.max_health = 400
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.1
        self.size = 0.6
        self.boundary = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return juju_img