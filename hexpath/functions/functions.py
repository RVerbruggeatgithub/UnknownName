import math
import pygame
import os
import random

def load_image(dir, path):
    return pygame.image.load(os.path.join(dir, path))


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def point_direction(x1, y1, x2, y2, radians = False):
    if radians:
        return math.atan2((y2 - y1), (x2 - x1))
    else:
        return math.atan2((y2 - y1), (x2 - x1)) * 180 / math.pi


def generate_alternative_path(path, max_deviation):
    x_deviation = random.randint(0, max_deviation * 2) - max_deviation
    y_deviation = random.randint(0, max_deviation * 2) - max_deviation
    new_path = []
    for segment in path:
        new_path.append((segment[0]+x_deviation, segment[1]+y_deviation))
    return new_path, [x_deviation, y_deviation]
