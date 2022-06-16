import pygame


class Popup:
    def __init__(self, x, y, content, cost):
        self.x = x
        self.y = y
        self.content = content
        self.cost = cost
        self.bg_color = (100, 20, 120, 150)
        self.border_color = (100, 20, 120)

    def draw(self, win):
        popup_font = pygame.font.SysFont("segoeuisemilight", 14)
        popt = popup_font.render(str(self.content) +"     Cost: "+ str(self.cost), 1, (255, 222, 100))

        rectangle = pygame.Rect(int(self.x), int(self.y), popt.get_width() + 10, popt.get_height() + 10)
        surface = pygame.Surface((popt.get_width() + 10, popt.get_height() + 10), pygame.SRCALPHA, 32)
        surface.fill(self.bg_color)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, self.border_color, rectangle, width=1, border_radius=0)

        win.blit(popt, (self.x + 5, self.y + 5))
