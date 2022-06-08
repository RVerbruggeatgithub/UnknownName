import pygame
from functions import *
from .objects import Object
from functions.functions import *
import random
pygame.font.init()
popup_font = pygame.font.SysFont("segoeuisemilight", 14)
item_images = []

city_imgs = []
"""
for x in range(1, 5):
    city_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources", "city_" +str(x) + ".png")).convert_alpha(), (60, 60)))
"""
class City(Object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.img = None # city_imgs[random.randint(1, len(city_imgs)-1)]
        self.despawn_timer = 50
        self.angle = 0

    def draw(self, win):
        # win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        print("optional to draw destination here..")