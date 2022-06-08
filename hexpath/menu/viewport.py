import pygame.display
from functions.functions import *


class Viewport:
    def __init__(self, surface=None):
        if not surface:
            surface = pygame.display.get_surface()
        self.surface = surface

        rect = surface.get_rect()
        self.w, self.h = rect.size
        # half width and half height
        self.hw, self.hh = rect.center

        # view port at the left top of the field
        self.x, self.y = (0, 0)

    def set_location(self, x, y):
        self.x, self.y = (x, y)

    def object_visible(self, obj):
        if obj.x < self.x - obj.w or obj.x > self.x + self.w or obj.y < self.y - obj.h or obj.y > self.y + self.h:
            return False
        return True

    def object_clickable(self, obj):
        if obj.x < self.x - obj.w or obj.x > self.x + self.w or obj.y < self.y - obj.h or obj.y > self.y + self.h:
            return False
        return True

    def center_on_x(self, x):
        self.x = x - self.hw

    def center_on_y(self, y):
        self.y = y - self.hh


class Manager:
    # width and height here of the full stage, not the viewport
    def __init__(self, width, height, layers):
        self.w, self.h = width, height
        self.viewport = Viewport()
        self.layers = layers
        self.objects = list([list([]) for z in range(layers)])
        self.focus = None
        self.acquired = []

    def focus_on(self, obj):
        self.focus = obj

    def focus_off(self):
        self.focus = None

    def add_object(self, layer, obj):
        self.objects[layer].append(obj)

        # test if methods exists?
        obj.movable = callable(getattr(obj, "move", None))
        obj.drawable = callable(getattr(obj, "draw", None))
        obj.extension = callable(getattr(obj, "extension", None))

        return obj

    def get_clicked(self, x, y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """

        for obj in self.objects[1]:

            if self.viewport.object_clickable(obj):
                if obj.click(obj, self.viewport.x, self.viewport.y):
                    return obj
        return None

    def get_hover(self, x, y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """

        for obj in self.objects[1]:

            if self.viewport.object_clickable(obj):
                if obj.click(obj, self.viewport.x, self.viewport.y):
                    return obj
        return None

    def get_acquired(self):
        for layer in range(self.layers):
            for obj in self.objects[layer]:
                if obj.selected:
                    self.acquired.append(obj.code)

    def do(self):
        self.acquired = []
        self.get_acquired()
        for layer in range(self.layers):
            for obj in self.objects[layer]:
                x = obj.x - self.viewport.x
                y = obj.y - self.viewport.y

                if obj.prerequisite in self.acquired or not obj.prerequisite:
                    obj.enabled = True

                if obj.movable:
                    obj.move(x, y, self)

                if self.focus:
                    if self.focus == obj:
                        if obj.x <= self.viewport.hw:
                            self.viewport.x = 0
                        elif obj.x >= self.w - self.viewport.hw:
                            self.viewport.x = self.w - self.viewport.w
                        else:
                            self.viewport.center_on_x(obj.x)

                        if obj.y <= self.viewport.hh:
                            self.viewport.y = 0
                        elif obj.y >= self.h - self.viewport.hh:
                            self.viewport.y = self.h - self.viewport.h
                        else:
                            self.viewport.center_on_y(obj.y)

                if obj.drawable:
                    if self.viewport.object_visible(obj):
                        obj.draw(x, y, self)


class block_obj:
    def __init__(self, x, y, w, h):
        """

        :param x: int of y
        :param y: int y
        :param size: tuple of width, height
        """
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.enabled = False
        self.prerequisite = None
        self.selected = False

    def click(self, me, x_adj=0, y_adj=0):
        return False

    def draw(self, x, y, win):
        # win may be stage? display surface
        pygame.draw.rect(win.viewport.surface, (22,44,66), (x, y, self.w, self.h), 1)

class img_obj:
    # sm_green_hex, "Attack +1", "ATK002", "ATK001", False
    def __init__(self, x, y, w, h, img, desc, code, prerequisite, selected, status=False, cost=0):
        """

        :param x: int of y
        :param y: int y
        :param size: tuple of width, height
        """
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.img = img
        self.desc = desc
        self.code = code
        self.selected = selected
        self.cost = cost
        self.enabled = status
        self.prerequisite = prerequisite


    def click(self, obj, x_adj=0, y_adj=0):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        mx, my = pygame.mouse.get_pos()
        obj_x = obj.x - x_adj
        obj_y = obj.y - y_adj
        if mx <= obj_x + obj.w and mx >= obj_x:
            if my <= obj_y + obj.h and my >= obj_y:
                return True
        return False

    def draw(self, x, y, win):
        # win may be stage? display surface
        # pygame.draw.rect(win.viewport.surface, (22,44,66), (x, y, self.w, self.h), 1)

        if self.selected:
            pygame.draw.circle(
                win.viewport.surface,  # Surface to draw on
                [150, 100, 50],  # Color in RGB Fashion
                (x + self.w//2 - 7, y + 13),  # Center
                8,  # Radius
            )
        elif self.enabled:
            pygame.draw.circle(
                win.viewport.surface,  # Surface to draw on
                [255, 255, 255],  # Color in RGB Fashion
                (x + self.w//2 - 7, y + 13),  # Center
                8,  # Radius
            )
        else:
            pygame.draw.circle(
                win.viewport.surface,  # Surface to draw on
                [66, 66, 66],  # Color in RGB Fashion
                (x + self.w//2 - 7, y + 13),  # Center
                8,  # Radius
            )

        win.viewport.surface.blit(self.img, (x, y))



class moveable_obj:
    def __init__(self, x, y):
        """

        :param x: int of y
        :param y: int y
        :param size: tuple of width, height
        """
        self.x, self.y = x, y
        self.w, self.h = (2, 2)
        self.enabled = False
        self.prerequisite = None
        self.selected = False

    def move(self, x, y, win):
        mx, my = pygame.mouse.get_pos()
        xdist = (mx - x) / 50 # reduce the speed of movement
        ydist = (my - y) / 50

        self.x += xdist
        self.y += ydist

    def click(self, me, x_adj=0, y_adj=0):
        return False

    def draw(self, x, y, win):
        # win may be stage? display surface
        pygame.draw.rect(win.viewport.surface, (255,0,0), (x, y, self.w, self.h), 0)

