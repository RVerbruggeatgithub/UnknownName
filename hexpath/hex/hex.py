import pygame
import math

class Hex:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = pygame.Color(75, 139, 59, 80)
        self.passable = True

    def pointy_hex_corner(self, center, size, i):
        angle_deg = 60 * i - 30
        angle_rad = math.pi / 180 * angle_deg
        return (center[0] + size * math.cos(angle_rad),
                    center[1] + size * math.sin(angle_rad))

    def toggle_passable(self):
        self.passable = not self.passable

    def get_coords(self):
        return [self.x, self.y]

    def hex(self, coords):
        hex_poly = []
        for i in range(0, 6):
            hex_poly.append(self.pointy_hex_corner(coords, 25, i))
        return hex_poly

    def draw_polygon_alpha(self, surface, color, points):
        lx, ly = zip(*points)
        min_x, min_y, max_x, max_y = min(lx), min(ly), max(lx), max(ly)
        target_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y)
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.polygon(shape_surf, color, [(x - min_x, y - min_y) for x, y in points])
        surface.blit(shape_surf, target_rect)

    def collide(self, x, y):
        """
        Detect collision with towers
        :param otherTower: list of polygon shapes
        :return: Bool
        """

        x1 = self.x
        y1 = self.y
        x2 = x
        y2 = y
        return self.collide_coordinates(x1, y1, x2, y2)

    def collide_coordinates(self, x1, y1, x2, y2):
        dis = math.sqrt((x2 - self.x)**2 + (y2 - self.y)**2)
        if dis >= 25:
            return False
        else:
            return True

    def click(self, x, y):
        distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
        if distance <= 26:
            return True
        return False

    def draw(self, win):
        if not self.passable:
            self.color = (0, 10, 121, 80)
        self.draw_polygon_alpha(win, self.color, self.hex([self.x, self.y]))