import os

import pygame

from .enemy import Enemy
from functions.functions import *
# from items.gold import Gold
# from items.metal import Metal
imgs = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "squaremon_" + add_str + ".png"),
        (50, 50))
    imgs.append(pygame.transform.rotozoom(img, 90 * -1, 1))



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
        self.boundary = (1 * self.speed_increase)
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        imgs = []
        for t in range(4):
            t_str = str(t)
            img = pygame.transform.scale(
                load_image("resources", "squaremon_" + t_str + ".png"),
                (50, 50))
            imgs.append(pygame.transform.rotozoom(img, 90 * -1, 1))
        return imgs


class SquaremonGreen(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonGreen"
        self.max_health = 30
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 0.7
        self.size = 0.5
        self.boundary = (2 * self.speed_increase)
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]
        #imgs[:]

    def load_image(self):
        imgs = []
        for t in range(4):
            t_str = str(t)
            img = pygame.transform.scale(
                load_image("resources", "squaremon_green_" + t_str + ".png"),
                (50, 50))
            imgs.append(pygame.transform.rotozoom(img, 90 * -1, 1))
        return imgs
