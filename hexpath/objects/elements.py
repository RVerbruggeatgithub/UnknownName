import pygame


class Element:
    """
    Abstract class for Elements
    :param bgcolor: surface, (r, g, b, a)
    """
    def __init__(self, x, y, width, height, color, bgcolor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.bgcolor = bgcolor

    def draw(self, win):
        surface = pygame.Surface((self.x, self.y), pygame.SRCALPHA, 32)
        surface.fill(self.bgcolor)
        # med_font= pygame.font.SysFont("segoeuisemilight", 25)
        # small_font = pygame.font.SysFont("segoeuisemilight", 18)
        rectangle = pygame.Rect(self.x,  self.y, self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, color, rectangle, width=2, border_radius=0)


class Frame(Element):
    """
    Abstract class for Frame
    A box to be put inside an element
    """
    def __init__(self, x, y, width, height, color, bgcolor):
        super().__init__(x, y, width, height, color, bgcolor)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.bgcolor = bgcolor

class TextArea(Element):
    """
     :param pygame_font: pygame.font object
    """
    def __init__(self, x, y, width, height, color, bgcolor, pygame_font):
        super().__init__(x, y, width, height, color, bgcolor)
        self.font = pygame_font