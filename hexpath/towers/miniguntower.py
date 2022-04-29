import pygame
from .tower import Tower
import os
import math
from menu.menu import *
from functions import *
from projectiles.bullet import *
from objects.labels import *
import random

pygame.init()
# bullet_hole = pygame.transform.scale(load_image("resources", "bullet_hole.png").convert_alpha(), (10, 10))
minigun_sound = pygame.mixer.Sound(os.path.join("resources", "minigun.mp3"))


# load tower images
turret_imgs = []
for x in range(1, 4):
    turret_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources", "minigun_" +str(x) + ".png")).convert_alpha(), (50, 50)))



class MinigunTower(Tower):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.turret_image = turret_imgs[0]
        self.turret_imgs = turret_imgs
        self.tower_count = 0
        self.range = 300
        self.original_range = self.range
        self.delay = self.attack_speed = 5  # lower is slower
        self.crit_chance = 0.05
        self.crit_damage = 1.2
        self.inRange = False
        self.left = True
        self.damage = 5
        self.accuracy = 0.5
        self.original_damage = self.damage
        self.width = self.height = self.tower_base.get_width()
        self.moving = False
        self.name = "Minigun Tower"
        self.ico_name = "buy_minigun"
        self.sell_value = [700, 1400, 2800]
        self.price = [1400, "MAX", "MAX"]
        self.menu.set_tower_details(self)
        self.max_splash_range = 10
        # attack speed, higher is faster. Anything above max_delay (tower()) will be set to 0 delay)
        self.action_sound = minigun_sound
        self.projectiles = []
        self.enable_double_fire = False

    def get_upgrade_cost(self):
        """
        gets the upgrade cost
        :return: int
        """
        return self.menu.get_item_cost()

    def draw(self, win):
        """
        draw the tower base and animated Minigun
        :param win: surface
        :return: int
        """
        super().draw_radius(win)
        super().draw(win)

        if self.inRange and not self.moving:
            self.tower_count += 1
            if self.tower_count >= len(self.turret_imgs):
                self.tower_count = 0
        else:
            self.tower_count = 0

        if len(self.projectiles) > 0:
            for projectile in self.projectiles:
                # win.blit(self.bullet_hole, (hole[1], hole[2]))
                projectile.draw(win)

        # draw shadow
        surface = pygame.Surface((200, 200), pygame.SRCALPHA, 32)
        pygame.draw.circle(surface, (0, 0, 0, 94), (32, 40), 16, 0)
        win.blit(surface, (self.x - 32, self.y - 32))

        pivot_point = [self.x, self.y]
        offset = pygame.math.Vector2(-8, 0)
        turret_image, rect = self.rotate(self.turret_angle, offset, pivot_point)

        win.blit(turret_image, rect)
        if self.selected:
            self.menu.draw(win)

    def change_range(self, r):
        """
        change range of archer tower
        :param r: int
        :return: None
        """
        self.range = r

    def upgrade(self):
        """
        upgrades the tower for a given cost
        :return: None
        """
        if self.level < len(self.turret_imgs):
            self.level += 1
            self.damage += self.upgrade_bonus_dmg[self.level - 1]
            self.accuracy += self.upgrade_bonus_accuracy[self.level - 1]
            self.range += self.upgrade_bonus_range[self.level - 1]
            self.attack_speed += self.upgrade_bonus_atk_speed[self.level - 1]
            self.turret_image = self.turret_imgs[self.level][0]
            self.max_splash_range += self.upgrade_bonus_splash_range[self.level - 1]

        if self.level > 1:
            self.enable_double_fire = True

    def find_target(self, enemies):
        """
        attacks an enemy in the enemy list, modifies the list
        :param enemies: list of enemies
        :return: None
        """
        labels = []
        if len(self.projectiles) > 0:
            for projectile in self.projectiles:
                if not projectile.move(enemies):
                    x_money = 0
                    # projectile has hit target!
                    # get all enemies in range of explosion projectile.explosion_range
                    for enemy in enemies:
                        check_distance = projectile.get_distance(enemy.x, enemy.y)
                        if check_distance <= self.max_splash_range:
                            # The closer the unit to the source 'explosion' the more damage.
                            projectile.delete = True
                            resulting_damage = self.damage
                            color = (255, 0, 0)
                            label_font_size = 14
                            if random.random() < self.crit_chance:
                                resulting_damage = resulting_damage * self.crit_damage
                                color = (255,215,0)
                                label_font_size = 18
                            resulting_damage = int(resulting_damage)
                            # cur_opponent.hp -= resulting_damage
                            labels.append(Label(enemy.x, enemy.y, resulting_damage, color, label_font_size))

                            enemy.hit(resulting_damage)
                                # death_ = pygame.mixer.Sound(projectile.target.death_sound)
                                # death_.set_volume(0.1)
                                # death_.play()

                                # dropping_items.append(enemy.items)
                                # enemies.remove(enemy)

                        # add
                    self.projectiles.remove(projectile)
                    return labels

        self.inRange = False
        enemy_closest = []
        for enemy in enemies:
            twr_center_x = self.x + self.turret_image.get_width() / 2 + 20
            twr_center_y = self.y + self.turret_image.get_height() / 2 + 20
            nme_center_x = enemy.x + enemy.img.get_width() / 2
            nme_center_y = enemy.y + enemy.img.get_height() / 2

            dis = math.sqrt((twr_center_x - nme_center_x) ** 2 + (twr_center_y - nme_center_y) ** 2)
            if dis < self.range:
                self.inRange = True
                enemy_closest.append(enemy)

        enemy_closest.sort(key=lambda x: x.path_pos)
        enemy_closest = enemy_closest[::-1]
        if len(enemy_closest) > 0:
            first_enemy = enemy_closest[0]
            y_mod = -1
            delta_y = first_enemy.y - self.y
            if 0 < delta_y > 0:
                y_mod = delta_y / abs(delta_y)
            self.turret_angle = point_direction(first_enemy.x, first_enemy.y, self.x, self.y)

            self.attack(enemies, first_enemy)
            """
            if self.tower_count == 50:
                if first_enemy.hit(self.damage) == True:
                    money = first_enemy.money * 2
                    enemies.remove(first_enemy)
            """
        else:
            self.turret_image = self.turret_imgs[2]

    def attack(self, enemies, enemy):
        """
        rotate images here too?
        """
        # self.turret_image = turret_imgs[0]
        # self.turret_imgs = turret_imgs
        money = 0
        self.turret_image = turret_imgs[self.tower_count]
        # do bullets cycle here?

        self.delay -= self.attack_speed
        if (self.delay <= 0):
            """
            action_sound = pygame.mixer.Sound(self.action_sound)
            action_sound.set_volume(0.1)
            channel = pygame.mixer.find_channel(False)
            if not channel is None:
                channel.play(action_sound)

            """
            death_ = pygame.mixer.Sound(self.action_sound)
            death_.set_volume(0.1)
            death_.play()
            if not self.enable_double_fire:
                self.projectiles.append(Bullet(self.x, self.y, enemy.x, enemy.y, enemy))
            else:
                spawn_x_mod_a = random.randint(1, 30) - 15
                spawn_y_mod_a = random.randint(1, 30) - 15
                spawn_x_mod_b = random.randint(1, 30) - 15
                spawn_y_mod_b = random.randint(1, 30) - 15
                self.projectiles.append(Bullet(self.x + spawn_x_mod_a, self.y + spawn_y_mod_a, enemy.x + spawn_x_mod_b,
                                               enemy.y + spawn_y_mod_b, enemy))
                self.projectiles.append(Bullet(self.x + spawn_x_mod_b, self.y + spawn_y_mod_b, enemy.x + spawn_x_mod_a,
                                               enemy.y + spawn_y_mod_a, enemy))

            self.delay = self.max_delay

        return money
