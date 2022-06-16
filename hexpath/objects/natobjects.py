import random
import pygame
from .objects import Object
from functions.functions import *

imgs = []
imgs.append(pygame.transform.scale(load_image("resources", "trees_1.png"), (80, 80)))
imgs.append(pygame.transform.scale(load_image("resources", "trees_2.png"), (80, 80)))
imgs.append(pygame.transform.scale(load_image("resources", "trees_3.png"), (80, 80)))
imgs.append(pygame.transform.scale(load_image("resources", "stones_1.png"), (80, 80)))
imgs.append(pygame.transform.scale(load_image("resources", "stones_2.png"), (80, 80)))
imgs.append(pygame.transform.scale(load_image("resources", "stones_3.png"), (80, 80)))

class NatObject(Object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.img = random.choice(imgs)

    def draw(self, win):
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))