import pygame
from functions.functions import *
pygame.font.init()
pygame.display.init()
pygame.display.set_mode((1500, 800))

ico_background_image = pygame.transform.scale(load_image("resources", "button_empty.png").convert_alpha(), (64,64))
# upgrade_btn = pygame.transform.scale(load_image("resources", "button_upgrade.png").convert_alpha(), (32, 32))
sell_btn = pygame.transform.scale(load_image("resources", "button_sell.png").convert_alpha(), (32, 32))
pictogram_attack_speed = pygame.transform.scale(load_image("resources", "icon_atk_speed.png").convert_alpha(), (50, 50))
pictogram_attack_damage = pygame.transform.scale(load_image("resources", "icon_atk_damage.png").convert_alpha(), (50, 50))
pictogram_accuracy = pygame.transform.scale(load_image("resources", "icon_accuracy.png").convert_alpha(), (50, 50))
pictogram_attack_range = pygame.transform.scale(load_image("resources", "icon_atk_range.png").convert_alpha(), (50, 50))
pictogram_crit_chance = pygame.transform.scale(load_image("resources", "icon_crit_chance.png").convert_alpha(), (50, 50))
pictogram_crit_damage = pygame.transform.scale(load_image("resources", "icon_crit_damage.png").convert_alpha(), (50, 50))
pictogram_projectile_size = pygame.transform.scale(load_image("resources", "icon_projectile_size.png").convert_alpha(), (50, 50))
pictogram_projectile_speed = pygame.transform.scale(load_image("resources", "icon_projectile_speed.png").convert_alpha(), (50, 50))
pictogram_splash_range = pygame.transform.scale(load_image("resources", "icon_splash_range.png").convert_alpha(), (50, 50))
pictogram_not_implemented = pygame.transform.scale(load_image("resources", "icon_not_implemented.png").convert_alpha(), (50, 50))
pictogram_shield = pygame.transform.scale(load_image("resources", "icon_shield.png").convert_alpha(), (50, 50))

class Button:
    """
    Button class for menu objects
    """
    def __init__(self, menu, img, name, x, y, title=None):
        self.name = name
        self.title = title
        self.img = img
        self.menu = menu
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x
        self.y = y
        self.x_adj = 0
        self.y_adj = 0
        self.quantity = 0

    def click(self, X, Y):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.x_adj + self.width and X >= self.x + self.x_adj:
            if Y <= self.y + self.y_adj + self.height and Y >= self.y + self.y_adj:
                return True
        return False

    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """
        win.blit(self.img, (self.x + self.x_adj, self.y + self.y_adj))
        if self.title is not None:
            small_font = pygame.font.SysFont("segoeuisemilight", 10)
            title = small_font.render(str(self.name) +":"+ str(self.title), 1, (255, 255, 255))
            win.blit(title, (self.x + self.img.get_width() / 2 - title.get_width() / 2 + 2, self.y + self.img.get_height() / 2 + 10))

    def update(self):
        """
        updates button position
        :return: None
        """
        self.x = self.menu.x - 50
        self.y = self.menu.y - 110

class BuildMenuIcon(Button):
    def __init__(self, img, name, fullname, x, y, quantity):
        self.img = img
        self.name = name
        self.fullname = fullname
        self.x = x
        self.y = y
        self.quantity = quantity
        self.buildmenu_icon_background_image = ico_background_image

    def update_quantity(self, qty):
        self.quantity += qty


    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """
        win.blit(self.buildmenu_icon_background_image, (self.x-5, self.y-8))
        small_font = pygame.font.SysFont("segoeuisemilight", 10)
        title = small_font.render(self.fullname, 1, (255, 255, 255))
        qty = small_font.render("QTY:" + str(self.quantity), 1, (255, 255, 255))
        win.blit(self.img, (self.x, self.y))
        win.blit(title, (self.x + self.img.get_width()/2 - title.get_width()/2 + 2, self.y + self.img.get_height()/2 + 10))
        win.blit(qty, (self.x + self.img.get_width() / 2 - title.get_width() / 2 + 2, self.y + self.img.get_height() / 2 + 30))

    def click(self, X, Y):
        """
        returns if the positon has collided with the menu
        :param X: int
        :param Y: int
        :return: bool
        """
        if X <= self.x + self.img.get_width() and X >= self.x:
            if Y <= self.y + self.img.get_height() and Y >= self.y:
                return True
        return False

class PlayPauseButton(Button):
    def __init__(self, play_img, pause_img, x, y):
        self.img = play_img
        self.play = play_img
        self.pause = pause_img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.paused = True
        self.cost = None
        self.name = None
        self.x_adj = 0
        self.y_adj = 0
        self.quantity = 0

    def toggle(self):
        self.paused = not self.paused


    def draw(self, win):
        if self.paused:
            win.blit(self.play, (self.x, self.y))
        else:
            win.blit(self.pause, (self.x, self.y))


class VerticalButton(Button):
    """
    Button class for menu objects
    """
    def __init__(self, x, y, img, name, cost=None):
        self.name = name
        self.img = img
        self.x = x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.cost = cost

    def add_toggle_btn(self, imgs, name):
        """
        adds buttons to menu
        :param imgs: list of images to toggle through
        :param name: str
        :return: None
        """
        self.items += 1
        self.buttons.append(Button(self, img, name))


class BonusMenuButton(Button):
    """
    Button class for menu objects
    """
    def __init__(self, action, name, bonus, pictogram, color, bcolor, item_w, item_h, item_p, item_s):
        self.name = name
        self.action = action
        self.img = None
        self.x = item_p * item_w + 50 + item_p * 25
        self.y = item_s * item_h + 20 + (item_s-1) * 25
        self.width = item_w
        self.pictogram = pictogram
        self.height = item_h
        self.color = color
        self.border_color = bcolor
        self.bonus = bonus
        self.x_adj = 0
        self.y_adj = 0

    def draw(self, win):
        """
        draws the button image
        :param win: surface
        :return: None
        """
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(self.color)
        small_font= pygame.font.SysFont("segoeuisemilight", 20)
        rectangle = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, self.border_color, rectangle, width=2, border_radius=6)

        name = small_font.render(self.name, 1, (255, 255, 255))
        bonus = small_font.render(str(self.bonus), 1, (255, 255, 255))

        mid = self.x + self.width / 2 - self.pictogram.get_width()/2
        win.blit(self.pictogram, (mid, self.y))
        win.blit(name, (self.x + self.width/2 - name.get_width()/2 + 2, self.y + self.height/2 + 40))
        win.blit(bonus, (self.x + self.width / 2 - bonus.get_width() / 2 + 2, self.y + self.height / 2 + 60))



class BonusPickerMenu:
    def __init__(self, win, items):
        self.x = 25
        self.y = 100
        max_w, max_h = win.get_size()
        self.width = max_w - (self.x * 2)
        self.line_height = max_h /2 - (self.y * 2)
        self.height = self.line_height
        if items > 5:
            self.height = self.line_height * 2
        else:
            self.y = self.y + self.height/2
        # max items per line
        self.items = items
        self.max_items = 10
        self.font = pygame.font.SysFont("segoeuisemilight", 25)
        self.small_font = pygame.font.SysFont("segoeuisemilight", 10)
        # self.bg = menu_bg
        self.buttons = []

    def add_btn(self, action, name, bonus, pictogram, color, bcolor):
        # item width has padding of 30
        item_p = len(self.buttons)
        item_s = 1
        if item_p + 1 <= 5:
            item_w = self.width / self.items - 30
            item_h = self.line_height - 30
        else:
            self.height = self.line_height * 2
            item_w = self.width / self.items - 30
            item_p = item_p - 5
            item_h = self.height / 2 - 30
            item_s = 2
        self.buttons.append(BonusMenuButton(action, name, bonus, pictogram, color, bcolor, item_w, item_h, item_p, item_s))

    def get_clicked(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.action
        return None

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """

        border_color = (0, 49, 83, 200)
        background_color = (44, 56, 99, 255)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)

        rectangle = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        win.blit(surface, rectangle)
        for item in self.buttons:
            item.draw(win)



class Menu:
    """
    menu

    """
    def __init__(self, x, y, width, height, menu_bg, sell_value=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("segoeuisemilight", 25)
        self.small_font = pygame.font.SysFont("segoeuisemilight", 10)
        self.bg = menu_bg
        self.buttons = []
        self.items = 0
        self.x_adj = 0
        self.y_adj = 0

    def add_btn(self, img, name):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        self.buttons.append(Button(self, img, name, self.x + (self.items * 32) + 50, self.y - self.height + 10))
        self.items += 1

    def add_configured_btn(self, configured_button):
        self.items += 1
        self.buttons.append(configured_button)

    def get_clicked(self, X, Y):
        """
        return the clicked item from the menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X,Y):
                return btn.name

        return None

    def update(self):
        """
        update menu and button location
        :return: None
        """
        for btn in self.buttons:
            btn.update()

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.width/2, self.y-120))
        for item in self.buttons:
            item.draw(win)


class IconMenu(Menu):
    """
    menu for holding items
    """
    def __init__(self, x, y, width, height, menu_bg=None):
        super().__init__(x, y, width, height, menu_bg)
        self.icons = []
        self.width = width
        self.height = height
        self.x = x
        self.y = y


    def add_or_update_icon(self, bonus_list):
        # nope
        updated = False
        self.icons = []
        self.items = 0
        for bonus in bonus_list:
            sel_bonus = bonus.split("_", 1)[0]
            counter = bonus.split("_", 1)[1]
            for icon in self.icons:
                if icon.name == sel_bonus:
                    updated = True
                    icon.title = int(icon.title) + int(counter)
            if not updated:
                self.add_icon(sel_bonus, counter)
            updated = False

    def add_icon(self, name, title):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :param title: str
        :return: None
        """
        img = pictogram_attack_speed
        icon_map = {
            "SPEED": pictogram_attack_speed,
            "ATK" : pictogram_attack_damage,
            "ACC": pictogram_accuracy,
            "RANGE": pictogram_attack_range,
            "CRITC": pictogram_crit_chance,
            "CRITD": pictogram_crit_damage,
            "BULSP": pictogram_projectile_speed,
            "RADIUS": pictogram_splash_range,
            "SHIELD": pictogram_shield
        }
        button = Button(self, icon_map[name], name, self.x + (self.items * 51) + 20, self.y + 10, title)
        self.icons.append(button)
        self.items += 1

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        border_color = (0, 49, 83, 155)
        background_color = (44, 56, 99, 90)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)
        rectangle = pygame.Rect(int(self.x), int(self.y), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, border_color, rectangle, width=2, border_radius=6)

        for icon in self.icons:
            icon.draw(win)

class buildingMenu(Menu):
    """
    Vertical Menu for side bar of game
    """
    def __init__(self, x, y, width, height, img=None):
        self.buttons = []
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.items = 0
        self.bg = img
        self.font = pygame.font.SysFont("segoeuisemilight", 25)

    def update_tower_quantity(self, new_value):
        return None

    def add_btn(self, img, name, fullname, quantity):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """

        btn_x = self.x + (self.items)*68
        self.items += 1
        btn_y = self.y-110
        self.buttons.append(BuildMenuIcon(img, name, fullname, btn_x, btn_y, quantity))

    def get_item_quantity(self, name):
        """
        gets cost of item
        :param name: str
        :return: int
        """
        for btn in self.buttons:
            if btn.name == name:
                return btn.quantity
        return -1

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """

        #win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))

        border_color = (0, 49, 83, 200)
        background_color = (44, 56, 99, 200)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)

        rectangle = pygame.Rect(int(self.x), int(self.y-120), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, border_color, rectangle, width=2, border_radius=6)

        for item in self.buttons:
            item.draw(win)
            # if item.cost is not None:
            #    win.blit(star2, (item.x+2, item.y + item.height))
            #    text = self.font.render(str(item.cost), 1, (255,255,255))
            #    win.blit(text, (item.x + item.width/2 - text.get_width()/2 + 7, item.y + item.height + 5))
