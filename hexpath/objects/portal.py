import pygame
from functions import *
from .objects import Object
from functions.functions import *
pygame.font.init()
popup_font = pygame.font.SysFont("segoeuisemilight", 14)
item_image = pygame.transform.scale(load_image("resources", "black_hole.png"), (150, 150))

class Portal(Object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.img = item_image
        self.despawn_timer = 50
        self.angle = 0

    def draw(self, win):
        self.angle += 4
        if self.angle > 360:
            self.angle -= 360
        portal_image = self.rotate(self.angle)
        win.blit(portal_image, (self.x - portal_image.get_width()/2, self.y - portal_image.get_height()/2))

    def rotate(self, angle):
        """
        Rotate the surface around the pivot point.
        Args:
            angle (float): Rotate by this angle.
            pivot (tuple, list, pygame.math.Vector2): The pivot point.
            offset (pygame.math.Vector2): This vector is added to the pivot.
        """
        rotated_image = pygame.transform.rotozoom(self.img, (angle - 180)*-1, 1)  # Rotate the image.
        return rotated_image  # Return the rotated image