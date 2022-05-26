import pygame
import math
import os
from functions.functions import *
from projectiles.projectiles import Projectile

projectile_image = pygame.transform.scale(load_image("resources", "cannonball.png"),(50, 50))


class Bullet(Projectile):
    """
    Abstract class for projectiles
    """
    def __init__(self, x, y, target_x, target_y, target, speed, size):
        super().__init__(x, y, target_x, target_y, target, speed, size)
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
        self.force_delete = False
        self.base_size = 3
        self.modifier = size
        # self.change_size(size)

    def set_target(self, x, y):
        self.target_x = x
        self.target_y = y

    def draw(self, win):
        """
        draws the tower
        :param win: surface
        :return: None
        """
        # if not self.delete and not self.force_delete:
        range = self.base_size + self.modifier
        surface = pygame.Surface((range, range), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (50, 50, 50, 255), (range//2, range//2), range//2, 0)
        win.blit(surface, (self.x - range//2, self.y - range//2))

    def set_direction(self):
        delta_x =  self.x - self.target_x
        delta_y = self.y - self.target_y
        distance = math.sqrt(delta_x ** 2 + delta_y ** 2)
        y_mod = -1
        spin = 0
        if 0 < delta_y > 0:
            y_mod = delta_y / abs(delta_y)
            spin = 180
        slope_angle = point_direction(self.target_x, self.target_y, self.x, self.y, False) * y_mod * 0.0174532925
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
        if get_distance(self.x, self.y, self.source_x, self.source_y) >= self.projectile_max_distance:
            self.force_delete = True

        for enemy in enemies:
            check_distance = self.get_distance(enemy.x, enemy.y)
            if check_distance < self.boundary:
                self.delete = True

        if not self.delete and not self.force_delete:
            self.x = self.x + self.move_x
            self.y = self.y + self.move_y
            return True
        else:
            return False

    def force_move(self):
        self.x = self.x + self.move_x
        self.y = self.y + self.move_y

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
