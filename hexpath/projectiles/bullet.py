import pygame
import math
import os
from functions.functions import *
from projectiles.projectiles import Projectile

projectile_image = pygame.transform.scale(load_image("resources", "cannonball.png"),(5, 5))


class Bullet(Projectile):
    """
    Abstract class for projectiles
    """
    def __init__(self, x, y, target_x, target_y, target, speed):
        super().__init__(x, y, target_x, target_y, target, speed)
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.width = 0
        self.height = 0
        self.speed_increase = speed
        self.boundary = 12
        self.img = projectile_image
        self.angle = 0
        self.move_x = 0
        self.move_y = 0
        self.set_direction()
        self.delete = False

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """

        max_w, max_h = win.get_size()

        if self.x < 0 or self.x >= max_w:
            self.delete = True

        if self.y < 0 or self.y >= max_h:
            self.delete = True

        if not self.delete:
            pivot_point = [self.x, self.y]
            offset = pygame.math.Vector2(0, 70)
            projectile_img, rect = self.rotate(self.angle, offset, pivot_point)
            win.blit(projectile_img, (self.x-self.img.get_width()//2, self.y-self.img.get_height()//2))

    def set_direction(self):
        delta_x =  self.x - self.target.x
        delta_y = self.y - self.target.y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        y_mod = -1
        spin = 0
        if 0 < delta_y > 0:
            y_mod = delta_y / abs(delta_y)
            spin = 180
        slope_angle = point_direction(self.target.x, self.target.y, self.x, self.y, False) * y_mod * 0.0174532925
        self.move_x = self.speed_increase * -math.cos(slope_angle)
        self.move_y = self.speed_increase * math.sin(slope_angle) * -1 * y_mod

    def move(self, enemies):
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
        for enemy in enemies:
            check_distance = self.get_distance(enemy.x, enemy.y)
            if check_distance < self.boundary:
                self.delete = True

        if not self.delete:
            self.x = self.x + self.move_x
            self.y = self.y + self.move_y
            return True
        else:
            return False


    def rotate(self, angle, offset, pivot_point):
        """
        Rotate the surface around the pivot point.
        Args:
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pygame.transform.rotozoom(self.img, (angle - 180)*-1, 1)  # Rotate the image.
        rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
        # Add the offset vector to the center/pivot point to shift the rect.
        rect = rotated_image.get_rect(center=pivot_point + rotated_offset)
        return rotated_image, rect  # Return the rotated image
