import pygame
from functions.functions import *

projectile_image = pygame.transform.scale(load_image("resources", "lives.png"),(50, 50))


class Projectile:
    """
    Abstract class for projectiles
    """
    def __init__(self, x, y, target_x, target_y, target, speed, size=0, is_fragment=False):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.width = 0
        self.height = 0
        self.speed_increase = speed
        self.boundary = 10
        self.img = projectile_image
        self.target = target
        self.base_size = 3
        self.change_size(size)
        self.delete = False
        self.force_delete = False
        self.projectile_max_distance = 400
        self.source_x = self.x
        self.source_y = self.y
        self.is_fragment = is_fragment


    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        img = self.projectile_image
        win.blit(img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

    def update(self):
        if self.target is not None:
            self.target_x = self.target.x
            self.target_y = self.target.y

    def change_size(self, modifier):
        self.img = pygame.transform.scale(self.img, (self.base_size + modifier, self.base_size + modifier))

    def get_distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)

    def move(self):
        """
         Move projectile
         :return: None

        self.anim_seq += 1
        if (self.anim_seq > 5):
            self.animation_count += 1
            self.anim_seq = 0

        if self.animation_count >= len(self.imgs):
            self.animation_count = 0
        """

    def force_move(self):
        self.x = self.x + self.move_x
        self.y = self.y + self.move_y
