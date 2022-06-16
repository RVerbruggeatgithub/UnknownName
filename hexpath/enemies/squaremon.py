from objects.labels import *
from .enemy import Enemy
from functions.functions import *
import math

Squaremon_imgs = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "squaremon_" + add_str + ".png"),
        (50, 50))
    Squaremon_imgs.append(pygame.transform.rotozoom(img, 90 * -1, 1))

SquaremonGreen_img = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "squaremon_green_" + add_str + ".png"),
        (50, 50))
    SquaremonGreen_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))

trippet_img = []
for x in range(5):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "trippet_" + add_str + ".png"),
        (50, 50))
    trippet_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))

yolkee_img = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "yolkee_" + add_str + ".png"),
        (50, 50))
    yolkee_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))

juju_img = []
for x in range(4):
    add_str = str(x)
    img = pygame.transform.scale(
        load_image("resources", "juju_" + add_str + ".png"),
        (50, 50))
    juju_img.append(pygame.transform.rotozoom(img, 90 * -1, 1))


pygame.init()


class Squaremon(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Squaremon"
        self.max_health = 12
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.8
        self.size = 0.3
        self.boundary = 2
        self.item_drop = [1]
        self.item_drop_rate = 0.02
        self.xp_value = 1
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return Squaremon_imgs

class SquaremonElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonBoss"
        self.max_health = 250
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.6
        self.size = 0.35
        self.boundary = 2
        self.item_drop = [1,1,1]
        self.item_drop_rate = 0.08
        self.xp_value = 10
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return Squaremon_imgs


class SquaremonGreen(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonGreen"
        self.max_health = 35
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 0.85
        self.size = 0.25
        self.boundary = 2
        self.item_drop = [1]
        self.item_drop_rate = 0.03
        self.xp_value = 2
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]
        #imgs[:]

    def load_image(self):
        return SquaremonGreen_img

class SquaremonGreenElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "SquaremonGreenElite"
        self.max_health = 400
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 0.6
        self.size = 0.35
        self.boundary = 2
        self.item_drop = [1,1,1,1,1]
        self.item_drop_rate = 0.09
        self.xp_value = 20
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]
        #imgs[:]

    def load_image(self):
        return SquaremonGreen_img

class Trippet(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Trippet"
        self.max_health = 75
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.5
        self.size = 0.35
        self.boundary = 2
        self.item_drop = [1,1]
        self.item_drop_rate = 0.06
        self.xp_value = 10
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return trippet_img

class TrippetElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Trippet"
        self.max_health = 200
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.3
        self.size = 0.5
        self.boundary = 2
        self.spawn_count = 5
        self.item_drop = [1,1,1,1]
        self.item_drop_rate = 0.16
        self.xp_value = 25
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return trippet_img

    def dead_action(self, enemies):
        path = self.path[self.path_pos:]
        for i in range(self.spawn_count):
            generated_path, deviation = generate_alternative_path(path, 8)
            new_enemy = Trippet(generated_path)
            new_enemy.deviation = deviation
            enemies.append(new_enemy)

class Yolkee(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Yolkee"
        self.max_health = 250
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.4
        self.size = 0.35
        self.boundary = 2
        self.item_drop = [1]
        self.item_drop_rate = 0.15
        self.xp_value = 25
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return yolkee_img

class YolkeeElite(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Yolkee"
        self.max_health = 800
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1.0
        self.size = 0.45
        self.boundary = 2
        self.item_drop = [1]
        self.item_drop_rate = 0.15
        self.xp_value = 25
        # shield absorbs this much damage before depleted
        self.shield = self.max_shield = 500
        # how much shield restores ? --NOT IMPLEMENTED
        self.shield_restore = 0.05
        self.max_restore_timer = self.restore_timer = 20s
        # reduce chances of getting crit hit on this enemy
        self.crit_resist_rate = 0.2
        # reduces crit damage taken
        self.crit_resist = 25
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def hit(self, damage):
        """
        Returns if an enemy has died and removes one health
        each call
        :return: Bool
        """
        if self.shield > 0 and damage > 0:
            self.shield -= damage
            damage = 0
            # make sure to transfer remaining damage to health after shield collapses
            if self.shield < 0:
                damage = -self.shield

        self.health -= damage
        if self.health <= 0:
            # self.generate_item()
            return True
        if self.health > self.max_health:
            self.health = self.max_health
        return False

    def draw(self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        """
        for dot in self.path:
            pygame.draw.circle(win, (255,0,255), dot, 10, 0)
        """

        self.img = self.imgs[self.animation_count]
        # Draw shadow
        shadow_radius = self.img.get_width() / 4 * self.size
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, (32 + shadow_radius / 2)), shadow_radius, 0)
        win.blit(surface, (self.x - 32, self.y - 32))
        self.img = pygame.transform.scale(self.img, (self.width * self.size, self.height * self.size))
        self.img = pygame.transform.rotate(self.img, (self.angle+90))
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_bar(win)

        if self.shield > 0:
            border_width = math.ceil(self.shield / self.max_shield * 10)
            surface = pygame.Surface((64, 64), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (172, 55, 238, 200), (32, 32), 32, border_width)
            win.blit(surface, (self.x - 32, self.y - 32))

    def move_action(self, target, params=[]):
        """
        Action(s) to perform when moving
        :param target: list of one or multiple targets the move_action is performed on
        :param params: list of additional parameters
        :return:
        """
        if self.restore_timer > 1:
            self.restore_timer -= 1

        if self.restore_timer == 1:
            self.restore_timer = self.max_restore_timer
            if self.shield > 0.2 * self.max_shield:
                self.shield += math.floor(self.shield_restore * self.max_shield)
            if self.shield > self.max_shield:
                self.shield = self.max_shield
        return False

    def load_image(self):
        return yolkee_img

class Juju(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "Juju"
        self.max_health = 500
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1
        self.size = 0.3
        self.boundary = 2
        self.item_drop = [1]
        self.item_drop_rate = 0.12
        self.max_heal_timer = self.heal_timer = 46
        self.heal_amount = 25
        self.heal_range = 75
        self.xp_value = 40
        self.poison_resist_rate = 0.25
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return juju_img

    def move_action(self, target, params=[]):
        """
        Action(s) to perform when moving
        :param target: list of one or multiple targets the move_action is performed on
        :param params: list of additional parameters
        :return:
        """
        if self.heal_timer > 1:
            self.heal_timer -= 1

        if self.heal_timer == 1:
            self.heal_timer = self.max_heal_timer
            for enemy in target:
                if enemy.get_distance(self.x, self.y) <= self.heal_range:
                    enemy.hit(-self.heal_amount)
                    params.append(Label(enemy.x, enemy.y, "+"+str(self.heal_amount), (144,238,144), 16))
        return False

    def draw(self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        """
        for dot in self.path:
            pygame.draw.circle(win, (255,0,255), dot, 10, 0)
        """

        self.img = self.imgs[self.animation_count]
        # Draw shadow
        shadow_radius = self.img.get_width() / 4 * self.size
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, (32 + shadow_radius / 2)), shadow_radius, 0)
        win.blit(surface, (self.x - 32, self.y - 32))
        if self.heal_timer <= 4 or (self.max_heal_timer - self.heal_timer) < 9:
            surface = pygame.Surface((self.heal_range * 4, self.heal_range * 4), pygame.SRCALPHA, 32)
            placement_circle = self.heal_range

            if self.heal_timer <= 3:
                mod = self.heal_timer
            else:
                mod = (self.max_heal_timer - self.heal_timer) + 1

            pygame.draw.circle(surface, (144,238,144, (160/mod)), (placement_circle, placement_circle), placement_circle, 0)
            win.blit(surface, (self.x - placement_circle, self.y - placement_circle))

        self.img = pygame.transform.scale(self.img, (self.width * self.size, self.height * self.size))
        self.img = pygame.transform.rotate(self.img, (self.angle+90))
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_bar(win)

class TestUnit(Enemy):
    def __init__(self, path):
        super().__init__(path)
        self.name = "TestUnit"
        self.max_health = 5000
        self.health = self.max_health
        self.imgs = self.load_image()
        self.speed_increase = 1
        self.size = 0.3
        self.boundary = 2
        self.item_drop = [1]
        self.item_drop_rate = 0.12
        self.max_heal_timer = self.heal_timer = 25
        self.heal_amount = 20
        self.heal_range = 120
        self.xp_value = 500
        self.poison_resist_rate = 0.25
        # self.droppable_items = [Gold(self.x, self.y, 1, 8), Gold(self.x, self.y, 5, 15)]

    def load_image(self):
        return juju_img

    def move_action(self, target, params=[]):
        """
        Action(s) to perform when moving
        :param target: list of one or multiple targets the move_action is performed on
        :param params: list of additional parameters
        :return:
        """
        if self.heal_timer > 1:
            self.heal_timer -= 1

        if self.heal_timer == 1:
            self.heal_timer = self.max_heal_timer
            for enemy in target:
                if enemy.get_distance(self.x, self.y) <= self.heal_range:
                    enemy.hit(-self.heal_amount)
                    params.append(Label(enemy.x, enemy.y, "+"+str(self.heal_amount), (144,238,144), 16))
        return False

    def draw(self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        """
        for dot in self.path:
            pygame.draw.circle(win, (255,0,255), dot, 10, 0)
        """

        self.img = self.imgs[self.animation_count]
        # Draw shadow
        shadow_radius = self.img.get_width() / 4 * self.size
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, (32 + shadow_radius / 2)), shadow_radius, 0)
        win.blit(surface, (self.x - 32, self.y - 32))
        if self.heal_timer <= 4 or (self.max_heal_timer - self.heal_timer) < 9:
            surface = pygame.Surface((self.heal_range * 4, self.heal_range * 4), pygame.SRCALPHA, 32)
            placement_circle = self.heal_range

            if self.heal_timer <= 3:
                mod = self.heal_timer
            else:
                mod = (self.max_heal_timer - self.heal_timer) + 1

            pygame.draw.circle(surface, (144,238,144, (160/mod)), (placement_circle, placement_circle), placement_circle, 0)
            win.blit(surface, (self.x - placement_circle, self.y - placement_circle))

        self.img = pygame.transform.scale(self.img, (self.width * self.size, self.height * self.size))
        self.img = pygame.transform.rotate(self.img, (self.angle+90))
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))
        self.draw_health_bar(win)