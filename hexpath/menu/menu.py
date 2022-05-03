import pygame
from functions.functions import *
pygame.font.init()
pygame.display.init()
pygame.display.set_mode((1500, 800))

ico_background_image = pygame.transform.scale(load_image("resources", "button_empty.png").convert_alpha(), (64,64))
# upgrade_btn = pygame.transform.scale(load_image("resources", "button_upgrade.png").convert_alpha(), (32, 32))
sell_btn = pygame.transform.scale(load_image("resources", "button_sell.png").convert_alpha(), (32, 32))

class Button:
    """
    Button class for menu objects
    """
    def __init__(self, menu, img, name, x, y):
        self.name = name
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
    def __init__(self, x, y, width, height, menu_bg, sell_value):
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


class TowerMenu(Menu):
    """
    menu for holding items
    """
    def __init__(self, x, y, width, height, menu_bg, sell_value):
        super().__init__(x, y, width, height, menu_bg, sell_value)
        self.buttons = []
        self.item_cost = 0
        self.tower = None
        self.item_sale_value = 0
        self.item_upgrade_cost = 0
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.items = 0

    def add_btn(self, img, name):
        """
        adds buttons to menu
        :param img: surface
        :param name: str
        :return: None
        """
        button = Button(self, img, name, self.x + (self.items * 32) + 50, self.y - self.height + 10)
        self.buttons.append(button)
        self.items += 1

    def set_tower_details(self, tower):
        self.tower = tower


    def get_items_upgrade(self):
        """
        gets sales value of tower
        :return: int
        """
        return self.tower[self.tower.level]

    def get_item_cost(self):
        """
        gets cost of upgrade to next level
        :return: int
        """
        return self.tower.price[self.tower.level - 1]

    def adjust_menu_location(self, win, x, y):
        """
        if the menu falls outside of the window, adjust self.x and self.y to make the window fully visible.
        :param win: surface
        :return: None
        """
        x_adj = 0
        y_adj = 0
        max_w, max_h = win.get_size()
        if x < 5:
            x_adj = int(0-x) + 5
        if y < 5:
            y_adj = int(0-y) + 5



        if x > (max_w - self.width -5):
            x_adj = ((x + self.width + 5) - max_w) * -1
        return x_adj, y_adj

    def draw(self, win):
        """
        draws btns and menu bg
        :param win: surface
        :return: None
        """
        #self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        #win.blit(self.bg, (self.x - self.width/2, self.y-120))
        star_str = "⭐"

        border_color = (0, 49, 83, 155)
        background_color = (44, 56, 99, 90)
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32)
        surface.fill(background_color)

        # check if the menu is still inside of map
        rect_x = int(self.x - (self.width/2))
        rect_y = int(self.y-120)
        x_adj, y_adj = self.adjust_menu_location(win, rect_x, rect_y)
        self.x_adj, self.y_adj = x_adj, y_adj

        rectangle = pygame.Rect(int(self.x - (self.width/2)) + x_adj, int(self.y-120) + y_adj, self.width, self.height)
        # rectangle = pygame.Rect(int(adj_x), int(adj_y), self.width, self.height)
        win.blit(surface, rectangle)
        pygame.draw.rect(win, border_color, rectangle, width=2, border_radius=6)

        tower_title = self.small_font.render(self.tower.name, 1, (255, 255, 255))
        win.blit(tower_title, (self.x - self.width/2 + 15 + x_adj, self.y - 110 + y_adj))

        # for i in range(self.tower.level):
        #    win.blit(star, ((self.x - self.width/2 + (i * star.get_width() + 15)) + x_adj, (self.y - 93) + y_adj))
        for item in self.buttons:
            item.x_adj = x_adj
            item.y_adj = y_adj
            item.draw(win)
            tower = self.tower
            upgrade_string = "Upgrade: $"+ str(tower.price[tower.level - 1])
            if tower.price[tower.level - 1] == "MAX":
                upgrade_string = "(Upgrade: " + str(tower.price[tower.level - 1])
            #win.blit(star, (item.x + item.width + 5, item.y+12))
            text = self.small_font.render(upgrade_string + ", sell value: $" + str(tower.sell_value[tower.level - 1]) + ")", 1, (255,255,255))
            win.blit(text, (self.x - self.width/2 + 15 + x_adj, item.y + item.width + 4 + y_adj))
        tower_info = []
        tower_info.append(["Damage", tower.damage, tower.get_next_level_info(tower.upgrade_bonus_dmg)])
        tower_info.append(["Attack Speed", tower.attack_speed, tower.get_next_level_info(tower.upgrade_bonus_atk_speed)])
        tower_info.append(["Attack Range", tower.range, tower.get_next_level_info(tower.upgrade_bonus_range)])
        tower_info.append(["Accuracy", int(tower.accuracy*100)/100, tower.get_next_level_info(tower.upgrade_bonus_accuracy)])

        for idx, details in enumerate(tower_info):
            detail = self.small_font.render((str(details[0]) +":"+ str(details[1])+" ("+ str(details[2])+")"), 1, (255, 255, 255))
            win.blit(detail, (self.x - self.width / 2 + 15  + x_adj, item.y + 50 + 14*idx  + y_adj))

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

        btn_x = self.x + (self.items)*68 - 40
        self.items += 1
        btn_y = self.y-60
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
