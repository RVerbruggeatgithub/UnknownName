import itertools

import pygame
import os
import time
import math
from functions.functions import *
from hex.hex import Hex
from hex.hexmap import Hexmap
from menu.menu import *
import random
from enemies.squaremon import *
from towers.miniguntower import MinigunTower
from towers.obstacle import Obstacle
from objects.portal import Portal

pygame.display.init()
pygame.display.set_mode((500, 500), pygame.RESIZABLE)
background_image = load_image("resources", "heusden.png")
play_btn = pygame.transform.scale(load_image("resources", "button_play.png").convert_alpha(), (32, 32))
pause_btn = pygame.transform.scale(load_image("resources", "button_pause.png").convert_alpha(), (32, 32))
ico_minigun = pygame.transform.scale(load_image("resources", "ico_minigun.png").convert_alpha(), (50, 50))
ico_obstruction = pygame.transform.scale(load_image("resources", "ico_obstruction.png").convert_alpha(), (50, 50))
attack_tower_names = ["Minigun Tower"]
obstacles = ["Obstacle"]
pictogram_attack_speed = pictogram_attack_damage = pygame.transform.scale(load_image("resources", "base_square.png").convert_alpha(), (150, 150))


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 900
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.pause = True
        self.timer = 0
        self.bg = pygame.transform.scale(background_image, (self.width, self.height))
        self.base_map = Hexmap(self.width, self.height - 100)
        self.start = self.end = [0, 0]
        self.set_start = False
        self.target_hex_num = 208
        self.map_update_required = True
        self.selected_hex = None
        # self.update_path([350, 136.60254037844385], [375, 612.9165124598851])
        self.enemies = []
        self.attack_towers = []
        self.obstacles = []
        self.label_collector = []
        self.menu = buildingMenu(100, self.height - 25, 500, 200)
        self.play_pause_button = PlayPauseButton(play_btn, pause_btn, 129, self.height - 142)
        self.menu.add_configured_btn(self.play_pause_button)
        self.menu.add_btn(ico_minigun, "buy_minigun", "Minigun", 3)
        self.menu.add_btn(ico_obstruction, "buy_obstacle", "Obstacle", 5)
        self.gate_health = 10000
        # This mode allow to create a path from point A to B returns start and end location as lists in console.
        self.build_mode = False
        self.wave_complete = True
        self.enemy_counter = 0
        self.wave = 0
        self.moving_object = None
        self.selected_tower = None
        # Set to True to allow tower outside of hexes
        self.tower_no_clip = False
        self.wave_enemy_total = 0
        self.spawn_list = []
        # Should we go through the list of bonuses and apply them to the tower?
        self.update_bonuses = False
        self.bonus_menu = BonusPickerMenu(self.win, 5)
        self.action_list = {
            "ATK_1" : {"Description": "Attack Damage + 1", "modifier" : 1, "pictogram" : pictogram_attack_damage, "color" : (255, 255, 255, 200), "background_color" : (255, 255, 255 ,255) },
            "SPEED_1" : {"Description": "Attack Speed + 10%", "modifier" : 0.1, "pictogram" : pictogram_attack_speed, "color" : (255, 255, 255, 200), "background_color" : (255, 255, 255 ,255) },
            "RANGE_1": {"Description": "Attack Range + 5%", "modifier": 0.05, "pictogram": pictogram_attack_speed,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "BRANGE_1": {"Description": "Blast Range + 5%", "modifier": 0.05, "pictogram": pictogram_attack_speed,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "CRITC_1": {"Description": "Crit Chance + 5%", "modifier": 0.05, "pictogram": pictogram_attack_speed,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "ACC_1": {"Description": "Accuracy + 5%", "modifier": 0.05, "pictogram": pictogram_attack_speed,
                        "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "BULSP_1": {"Description": "Projectile speed + 8%", "modifier": 0.08, "pictogram": pictogram_attack_speed,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
        }

        self.action_list2 = {
            "ATK_2" : {"Description": "Attack Damage + 2", "modifier" : 2, "pictogram" : pictogram_attack_damage, "color" : (0, 32, 255, 200), "background_color" : (0, 32, 255,255) },
            "SPEED_2" : {"Description": "Attack Speed + 20 %", "modifier" : 0.2, "pictogram" : pictogram_attack_speed, "color" : (0, 32, 255, 200), "background_color" : (0, 32, 255,255) },
            "RANGE_2": {"Description": "Attack Range + 10%", "modifier": 0.1, "pictogram": pictogram_attack_speed,
                      "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "BRANGE_2": {"Description": "Blast Range + 10%", "modifier": 0.1, "pictogram": pictogram_attack_speed,
                      "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "OBSTACLE_1": {"Description": "Obstacle +1", "modifier": 1, "pictogram": pictogram_attack_speed,
                         "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "CRITD_1": {"Description": "Crit Damage + 50%", "modifier": 0.50, "pictogram": pictogram_attack_speed,
                        "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
        }

        self.action_list3 = {
            "TOWER_1": {"Description": "Tower! +1", "modifier": 1, "pictogram": pictogram_attack_speed,
                        "color": (221,160,221, 200), "background_color": (221,160,221, 255)},
            "SPEED_3": {"Description": "Attack Speed + 30%", "modifier": 0.3, "pictogram": pictogram_attack_speed,
                        "color": (221,160,221, 200), "background_color": (221,160,221, 255)},
            "OBSTACLE_2": {"Description": "Obstacle +2", "modifier": 2, "pictogram": pictogram_attack_speed,
                         "color": (221,160,221, 200), "background_color": (0, 32, 255, 255)},
        }

        self.bonus_options = []
        self.applied_bonuses = []
        self.build_bonus_menu()



        self.show_bonus_menu = True
        self.show_build_menu = False
        self.enemy_spawn_points = [
            {"source": [250, 396.41016151377545], "destination": [900, 396.41016151377545]},
            {"source": [750, 223.20508075688772], "destination": [450, 656.217782649107]}
        ]
        self.portals = []
        for enemy_spawn_point in self.enemy_spawn_points:
            self.portals.append(Portal(enemy_spawn_point["source"][0], enemy_spawn_point["source"][1]))
        self.waves = [
                [{"type": "Squaremon", "count": 1, "interval": 0.8}],
                [{"type": "Squaremon", "count": 2, "interval": 0.8}],
                [{"type": "Squaremon", "count": 3, "interval": 0.8}],
                [{"type": "Squaremon", "count" : 5, "interval": 0.6}],
                [{"type": "Squaremon", "count": 7, "interval": 0.6}],
                [{"type": "Squaremon", "count": 8, "interval": 0.6}],
                [{"type": "Squaremon", "count": 10, "interval": 0.6}],
                [{"type": "Squaremon", "count" : 4, "interval": 0.5},{"type": "SquaremonGreen", "count" : 1, "interval": 0.5}],
                [{"type": "Squaremon", "count" : 6, "interval": 4},{"type": "SquaremonGreen", "count" : 2, "interval": 0.5}],
                [{"type": "Squaremon", "count": 8, "interval": 4},{"type": "SquaremonGreen", "count": 2, "interval": 0.5}],
                [{"type": "Squaremon", "count": 11, "interval": 0.5},{"type": "SquaremonGreen", "count": 3, "interval": 0.5}],
                [{"type": "Squaremon", "count": 14, "interval": 4},{"type": "SquaremonGreen", "count": 4, "interval": 0.5}],
                [{"type": "Squaremon", "count": 16, "interval": 0.5},{"type": "SquaremonGreen", "count": 5, "interval": 0.5}],
                [{"type": "Squaremon", "count": 16, "interval": 0.5},{"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
                [{"type": "Squaremon", "count": 18, "interval": 0.5},{"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "Squaremon", "count": 18, "interval": 0.5},
             {"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}],
            ]

        self.enemies_removed = 0
        self.paths = []
        self.move_tower = False
        # mark hexes of spawn points as not passable

        # only use this when building a path
        # self.hex_map.remove(self.hex_map[10])
        # build_mode requires pause, pause does NOT require build_mode

    def run(self):
        run = True
        clock = pygame.time.Clock()
        for enemy_spawn_point in self.enemy_spawn_points:
            path = self.base_map.find_path(enemy_spawn_point["source"], enemy_spawn_point["destination"])
            self.paths.append(self.base_map.get_path_from_path_data(path))

        while run:

            mouse_pos = pygame.mouse.get_pos()
            to_del = []
            index = 0

            if self.build_mode:
                self.map_update_required = False
                self.show_bonus_menu = False

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                    clicked_location = None
                    self.selected_hex = None

                    if event.type == pygame.MOUSEBUTTONUP:
                        for map_location in self.base_map.get_map_data():
                            # if map_location.collide(mouse_pos[0], mouse_pos[1]):
                            if map_location.click(mouse_pos[0], mouse_pos[1]):
                                clicked_location = map_location
                        if event.button == 1:
                            if clicked_location is not None:
                                if not self.set_start:
                                    self.start = [clicked_location.x, clicked_location.y]
                                    self.set_start = True
                                else:
                                    self.end = [clicked_location.x, clicked_location.y]
                                    self.set_start = False
                                    self.map_update_required = True
                                    print(self.start, self.end)

                        if event.button == 3:
                            if clicked_location is not None:
                                self.selected_hex = clicked_location
                                self.selected_hex.toggle_passable()
                                self.map_update_required = True

                if self.start[0] == 0 and self.start[1] == 0 and self.end[0] == 0 and self.end[
                    1] == 0:
                    self.map_update_required = False
            else:
                if self.moving_object and self.wave_complete:
                    valid_area = True
                    if not self.tower_no_clip:
                        valid_area, spot = self.base_map.find_closest_hex_coords(mouse_pos[0], mouse_pos[1])
                        self.moving_object.move(spot[0], spot[1])
                    else:
                        self.moving_object.move(mouse_pos[0], mouse_pos[1])
                    # tower_list = self.attack_towers[:] + self.support_towers[:]
                    tower_list = self.attack_towers[:]
                    collide = False
                    if valid_area:
                        self.moving_object.place_color = (0, 0, 255, 100)
                    else:
                        self.moving_object.place_color = (255, 0, 0, 100)

                    for tower in tower_list:
                        if tower.collide(self.moving_object) and valid_area:
                            collide = True
                            tower.place_color = (255, 0, 0, 100)
                            self.moving_object.place_color = (255, 0, 0, 100)
                        else:
                            tower.place_color = (0, 0, 255, 100)
                            if not collide and valid_area:
                                self.moving_object.place_color = (255, 0, 0, 100)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.move_tower = False
                        if self.play_pause_button.click(mouse_pos[0], mouse_pos[1]):
                            self.pause = not (self.pause)
                            self.play_pause_button.toggle()
                            if self.pause:
                                print("paused")
                            else:
                                print("unpaused")
                            self.play_pause_button.paused = self.pause
                        if self.wave_complete:
                            for map_location in self.base_map.get_map_data():
                                # if map_location.collide(mouse_pos[0], mouse_pos[1]):
                                if map_location.click(mouse_pos[0], mouse_pos[1]):
                                    clicked_location = map_location
                            # moving tower, left click tower to move it.
                            for tw in (self.attack_towers + self.obstacles):
                                if tw.click(mouse_pos[0], mouse_pos[1]):
                                    """
                                    Moving tower on left click
                                    1. move tower into self.moving_object
                                    2. add 1 tower count to tower[type]
                                    3. remove tower from tower list (is this needed?)
                                    4. Toggle hex, update paths 
                                    """
                                    sel_tower = tw.ico_name
                                    self.add_tower(tw.ico_name)
                                    self.move_tower = True
                                    for button in self.menu.buttons:
                                        if button.name == sel_tower:
                                            button.update_quantity(1)
                                    if tw in self.attack_towers:
                                        self.attack_towers.remove(tw)
                                    else:
                                        self.obstacles.remove(tw)
                                    self.selected_hex = clicked_location
                                    self.selected_hex.toggle_passable()


                        if self.show_bonus_menu:
                            self.show_build_menu = False
                            bonus_menu_button = self.bonus_menu.get_clicked(mouse_pos[0], mouse_pos[1])
                            # change below to only happen if button is clicked..
                            if bonus_menu_button is not None:
                                # apply structure related directly, don't add to bonuses
                                structures = ["OBSTACLE_1", "OBSTACLE_2", "TOWER_1"]
                                if bonus_menu_button in structures:
                                    if bonus_menu_button == "TOWER_1":
                                        for button in self.menu.buttons:
                                            if button.name == "buy_minigun":
                                                button.update_quantity(1)
                                    if bonus_menu_button == "OBSTACLE_1":
                                        for button in self.menu.buttons:
                                            if button.name == "buy_obstacle":
                                                button.update_quantity(1)
                                    if bonus_menu_button == "OBSTACLE_2":
                                        for button in self.menu.buttons:
                                            if button.name == "buy_obstacle":
                                                button.update_quantity(2)
                                else:
                                    self.applied_bonuses.append(bonus_menu_button)
                                self.update_bonuses = True
                                self.show_bonus_menu = False
                                self.show_build_menu = True
                                self.build_bonus_menu()
                        """
                        if event.button == 3 and self.wave_complete:
                           if clicked_location is not None:
                               self.selected_hex = clicked_location
                               # self.map_update_required = True
                               # if self.selected_hex
                               self.selected_hex.toggle_passable()
                               for num, path in enumerate(self.paths):
                                   if self.selected_hex.get_coords() in path:
                                       # find path
                                       enemy_spawn_point = self.enemy_spawn_points[num]
                                       new_path = self.base_map.find_path(enemy_spawn_point["source"],
                                                                      enemy_spawn_point["destination"])
                                       if not new_path:
                                           print("Cannot place anything here, it will block path")
                                           self.selected_hex.toggle_passable()
                                       else:
                                           self.paths[num] = self.base_map.get_path_from_path_data(new_path)
                           """
                                        # if found, update self.paths[num] with new path
                                        # self.enemy_spawn_points
                        if self.moving_object and not self.move_tower:

                            if event.button == 1:
                                allowed = True
                                hit = False
                                tower_list = self.attack_towers[:] + self.obstacles[:]

                                for tower in tower_list:
                                    if tower.collide(self.moving_object):
                                        allowed = False

                                if allowed:
                                    # clicked_location = None
                                    if (self.moving_object.name in attack_tower_names or self.moving_object.name in obstacles) and self.wave_complete:

                                        allow_build = True
                                        # self.menu.update_tower_quantity(len(self.attack_towers))
                                        for map_location in self.base_map.get_map_data():
                                            if map_location.click(mouse_pos[0], mouse_pos[1]):
                                                clicked_location = map_location
                                                if clicked_location is not None:
                                                    self.selected_hex = clicked_location
                                                    self.selected_hex.toggle_passable()
                                                    # Check if and see if clicked coordinates are in any paths
                                                    for num, path in enumerate(self.paths):
                                                        # coordinates are found in path, check if we can create a new path
                                                        if self.selected_hex.get_coords() in path:
                                                            # find path
                                                            enemy_spawn_point = self.enemy_spawn_points[num]
                                                            new_path = self.base_map.find_path(enemy_spawn_point["source"],
                                                                                               enemy_spawn_point["destination"])
                                                            # couldn't create a new path, the path will get broken if we allow building at coordinates
                                                            if not new_path:
                                                                print("Cannot place anything here, it will block path")
                                                                self.selected_hex.toggle_passable()
                                                                allow_build = False
                                                            # found new path, next: ensure that the coordinates aren't a spawn point
                                                            else:
                                                                update_path = self.base_map.get_path_from_path_data(
                                                                    new_path)
                                                                # ensure that the coordinates aren't a spawn point
                                                                if clicked_location.get_coords() in update_path:
                                                                    print("Cannot place anything here, it will block path")
                                                                    self.selected_hex.toggle_passable()
                                                                    allow_build = False
                                                                else:
                                                                    allow_build = True
                                                                    self.paths[num] = update_path

                                        # self.money -= self.moving_object.price[0]
                                        if allow_build:
                                            self.moving_object.place_structure()
                                            # how do we update the button quantity?
                                            # self.menu.buttons.name
                                            for button in self.menu.buttons:
                                                if button.name == self.moving_object.ico_name:
                                                    button.update_quantity(-1)
                                            if (self.moving_object.name in attack_tower_names):
                                                self.attack_towers.append(self.moving_object)

                                            else:
                                                self.obstacles.append(self.moving_object)
                                            self.moving_object.moving = False
                                            self.moving_object = None
                            elif event.button == 3:
                                self.moving_object = False
                            else:
                                continue
                        else:
                            side_menu_button = self.menu.get_clicked(mouse_pos[0], mouse_pos[1])
                            item_quantity = self.menu.get_item_quantity(side_menu_button)
                            if side_menu_button and item_quantity > 0 and self.show_build_menu:
                                # availability = self.menu.get_item_quantity(buy_minigun)
                                # if self.money >= cost:
                                self.add_tower(side_menu_button)
                                # look if you clicked on attack tower
                                btn_clicked = None
                                if self.selected_tower:
                                    btn_clicked = self.selected_tower.menu.get_clicked(mouse_pos[0], mouse_pos[1])
                                    if btn_clicked:
                                        if btn_clicked == "Sell":
                                            sales_value = self.selected_tower.get_sales_value()
                                            self.money += sales_value # need to change this
                                            self.attack_towers.remove(self.selected_tower)

                                if not btn_clicked:
                                    for tw in self.attack_towers:
                                        if tw.click(mouse_pos[0], mouse_pos[1]):
                                            tw.selected = True
                                            self.selected_tower = tw
                                        else:
                                            tw.selected = False

                if not self.pause:

                    if self.update_bonuses:
                        self.apply_bonuses_to_towers()
                        self.update_bonuses = False

                    if len(self.paths) > 0 and self.wave < len(self.waves):
                        self.moving_object = False
                        self.wave_complete = False
                        enemy_wave_data = self.waves[self.wave]
                        wave_enemy_total = 0

                        temp_counter = 0
                        loop_timer = 0

                        if len(self.spawn_list) == 0:
                            for enemy_wave in enemy_wave_data:
                                wave_enemy_total += enemy_wave["count"]
                                for _ in itertools.repeat(None, enemy_wave["count"]):
                                    enemies = {
                                        "Squaremon": Squaremon(random.choice(self.paths)),
                                        "SquaremonGreen": SquaremonGreen(random.choice(self.paths))
                                    }
                                    wave_enemy = enemies.get(enemy_wave["type"])
                                    self.spawn_list.append(wave_enemy)

                            self.wave_enemy_total = wave_enemy_total
                            random.shuffle(self.spawn_list)
                        timestamp = pygame.time.get_ticks()

                        if timestamp - self.timer >= 500 and self.enemy_counter < self.wave_enemy_total:  # lastTimeStamp is the variable storing time and replace 500 with another integer that works well
                            # get the enemy with the number value from the index variable
                            self.timer = timestamp  # resets the time stamp
                            self.enemies.append(self.spawn_list[self.enemy_counter])
                            self.enemy_counter += 1  # The index variable



                        """
                        if time.time() - self.timer > spawn_interval and self.enemy_counter < self.wave_enemy_total:
                            loop_timer = time.time()
                            self.enemies.append(wave_enemy)
                            self.enemy_counter += 1
                        """
                        # if rtimer - self.timer % spawn_interval == 0:
                        #    print("spawn")


                    for enemy in self.enemies:
                        enemy.move()
                        if enemy.path_pos >= len(enemy.path) - 1 or enemy.health <= 0:
                            to_del.append(enemy)

                    for enemy in to_del:
                        # self.gate_health -= enemy.gate_damage
                        # print(d.travelled_path)
                        self.enemies_removed += 1
                        self.enemies.remove(enemy)

                    for tower in self.attack_towers:
                        # item dropping here..
                        list_of_labels = tower.find_target(self.enemies)
                        if list_of_labels is not None:
                            for label in list_of_labels:
                                self.label_collector.append(label)

                    if self.enemies_removed == self.wave_enemy_total:
                        self.wave_complete = True
                        self.wave_enemy_total = 0
                        self.enemy_counter = 0
                        self.pause = not self.pause
                        self.play_pause_button.toggle()
                        self.enemies_removed = 0
                        self.wave += 1
                        self.spawn_list = []
                        self.show_bonus_menu = True
                        self.show_build_menu = False
            self.draw()
                # End of if not pause block
        pygame.quit()


    def sort_by_y(self, spr):
        """
        sort sprite by Y position
        :param spr: key comparison
        :returns: key value
        """
        return spr.y

    def build_bonus_menu(self):
        u = 0

        self.bonus_options = []
        self.bonus_menu.buttons = []
        while u < 5:
            # 75% chance to get basic item
            roll = random.random()
            if roll > 0.90:
                key, action_item = random.choice(list(self.action_list3.items()))
            elif roll > 0.75:
                key, action_item = random.choice(list(self.action_list2.items()))
            else:
                key, action_item = random.choice(list(self.action_list.items()))

            if key not in self.bonus_options:
                self.bonus_options.append(key)
                self.bonus_menu.add_btn(key, action_item["Description"], action_item["modifier"], action_item["pictogram"], action_item["color"], action_item["background_color"])
                u += 1

    def apply_bonuses_to_towers(self):
        for tower in self.attack_towers:
            tower.clear_modifiers()
            for bonus in self.applied_bonuses:

                if bonus == "ATK_1":
                    tower.mod_damage += self.action_list[bonus]["modifier"]
                if bonus == "ATK_2":
                    tower.mod_damage += self.action_list2[bonus]["modifier"]
                if bonus == "CRITC_1":
                    tower.mod_crit_chance += self.action_list[bonus]["modifier"]

                if bonus == "CRITD_1":
                    tower.mod_crit_damage += tower.crit_damage * \
                                             self.action_list2[bonus]["modifier"]
                if bonus == "SPEED_1":
                    tower.mod_attack_speed += tower.attack_speed * self.action_list[bonus]["modifier"]
                if bonus == "SPEED_2":
                    tower.mod_attack_speed += tower.attack_speed * self.action_list2[bonus]["modifier"]
                if bonus == "SPEED_3":
                    tower.mod_attack_speed += tower.attack_speed * self.action_list3[bonus]["modifier"]
                if bonus == "ACC_1":
                    tower.mod_accuracy += self.action_list[bonus]["modifier"]
                if bonus == "BULSP_1":
                    tower.mod_projectile_speed += tower.projectile_speed * \
                                             self.action_list[bonus]["modifier"]
                if bonus == "RANGE_1":
                    tower.mod_attack_range += tower.range * \
                                             self.action_list[bonus]["modifier"]

            tower.print_modifiers()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        tower_opt_list = {"buy_minigun": MinigunTower(x, y), "buy_obstacle": Obstacle(x, y)}

        # if name == "buy_minigun":
        try:
            self.moving_object = tower_opt_list[name]
        except Exception as e:
            print(str(e) + "Invalid name")

    def draw(self):
        # self.win.blit(self.bg, (0, 0))
        self.win.fill([255,255,255])

        if self.moving_object:
            # , pygame.SRCALPHA, 32
            green_color = pygame.Color(75, 139, 59, 80)
            # for buildable_area in self.buildable_areas:
            #    self.draw_polygon_alpha(self.win, green_color, buildable_area)
            # pygame.draw.polygon(self.win, green_color, self.buildable_areas, width=0)

            for tower in self.attack_towers:
                tower.draw_placement(self.win)
            self.moving_object.draw_placement(self.win)

        for portal in self.portals:
            portal.draw(self.win)

        if self.build_mode:
            self.base_map.draw(self.win)
        else:
            for path in self.paths:
                self.base_map.draw_path(self.win, path)

        if self.show_build_menu:
            self.menu.draw(self.win)



        for tower in self.attack_towers:
            tower.draw(self.win)

        for obstacle in self.obstacles:
            obstacle.draw(self.win)
        # for inode in self.tmp_nodes:
        #    pygame.draw.circle(self.win, (225, 255, 0), (inode["x"], inode["y"]), 5, 0)
        enemies = self.enemies
        for enemy in sorted(enemies, key=self.sort_by_y):
            enemy.draw(self.win)

        if len(self.label_collector) > 0:
            for label in self.label_collector:
                label.draw(self.win)
                label.despawn_timer -= 1
                if label.despawn_timer <= 0:
                    self.label_collector.remove(label)

        if self.show_bonus_menu:
            self.bonus_menu.draw(self.win)

        pygame.display.update()

g = Game()
g.run()