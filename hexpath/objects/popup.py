import pygame


class Popup:
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content

    def draw(self, win):
        popup_font = pygame.font.SysFont("segoeuisemilight", 14)
        popt = popup_font.render(str(self.content), 1, (255,222,100))
        win.blit(popt, (self.x, self.y))
