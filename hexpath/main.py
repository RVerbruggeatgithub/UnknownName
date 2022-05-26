import itertools
from hex.hexmap import Hexmap
from enemies.squaremon import *
from towers.miniguntower import MinigunTower
from towers.obstacle import Obstacle
from objects.portal import Portal
from objects.city import City
from objects.items import *

pygame.display.init()
pygame.display.set_mode((500, 500), pygame.RESIZABLE)
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])

background_image = load_image("resources", "porro_village.png")
play_btn = pygame.transform.scale(load_image("resources", "button_play.png").convert_alpha(), (32, 32))
pause_btn = pygame.transform.scale(load_image("resources", "button_pause.png").convert_alpha(), (32, 32))
reg_speed = pygame.transform.scale(load_image("resources", "button_reg_speed.png").convert_alpha(), (32, 32))
high_speed = pygame.transform.scale(load_image("resources", "button_hi_speed.png").convert_alpha(), (32, 32))
ico_minigun = pygame.transform.scale(load_image("resources", "ico_minigun.png").convert_alpha(), (50, 50))
ico_obstruction = pygame.transform.scale(load_image("resources", "ico_obstruction.png").convert_alpha(), (50, 50))
attack_tower_names = ["Minigun Tower"]
obstacles = ["Obstacle"]
pictogram_attack_speed = pygame.transform.scale(load_image("resources", "icon_atk_speed.png").convert_alpha(), (100, 100))
pictogram_attack_damage = pygame.transform.scale(load_image("resources", "icon_atk_damage.png").convert_alpha(), (100, 100))
pictogram_accuracy = pygame.transform.scale(load_image("resources", "icon_accuracy.png").convert_alpha(), (100, 100))
pictogram_attack_range = pygame.transform.scale(load_image("resources", "icon_atk_range.png").convert_alpha(), (100, 100))
pictogram_crit_chance = pygame.transform.scale(load_image("resources", "icon_crit_chance.png").convert_alpha(), (100, 100))
pictogram_crit_damage = pygame.transform.scale(load_image("resources", "icon_crit_damage.png").convert_alpha(), (100, 100))
pictogram_projectile_size = pygame.transform.scale(load_image("resources", "icon_projectile_size.png").convert_alpha(), (100, 100))
pictogram_projectile_speed = pygame.transform.scale(load_image("resources", "icon_projectile_speed.png").convert_alpha(), (100, 100))
pictogram_splash_range = pygame.transform.scale(load_image("resources", "icon_splash_range.png").convert_alpha(), (100, 100))
pictogram_not_implemented = pygame.transform.scale(load_image("resources", "icon_not_implemented.png").convert_alpha(), (100, 100))
pictogram_shield = pygame.transform.scale(load_image("resources", "icon_shield.png").convert_alpha(), (100, 100))


class MainGameMenu:
    def __init__(self):
        self.width = 1200
        self.height = 900
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        """
        Main menu stuff:
        """
        self.show_main_menu = True
        self.start_menu = Menu(25, 25, self.width - 50, self.height - 50, None)
        frame_width = 400
        frame_height = 600
        self.start_menu.add_frame((self.width//2 - frame_width//2), 80, frame_width, frame_height, (100,150,225, 100), (0,0,0, 0))
        self.start_menu.add_plain_button("New Game", None, (self.width//2 - frame_width//2 + frame_width*0.1), 250, frame_width*0.8, 50, (0,0,0, 100))
        self.start_menu.add_plain_button("Help", None, (self.width // 2 - frame_width // 2 + frame_width * 0.1),
                                         325, frame_width * 0.8, 50, (0, 0, 0, 100))
        self.show_start_menu = True
        self.help_menu = Menu(25, 25, self.width - 50, self.height - 50, None)
        self.show_help_menu = False
        self.help_menu.add_frame((self.width//2 - 400), 80, 800, frame_height, (100,150,225, 100), (0,0,0, 0))
        self.help_menu.add_plain_button("Back", None, (self.width//2 - 400) + 725, 100, 65, 50, (0,0,0, 100))

    def draw_current_menu(self, current_menu):
        self.win.fill([255, 255, 255])
        current_menu.draw(self.win)
        pygame.display.update()

    def run(self):
        game = Game()
        game.run()

    def main_menu(self):
        # draw the main menu
        while self.show_main_menu:
            if self.show_start_menu:
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show_main_menu = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.start_menu.buttons:
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "New Game":
                                self.run()
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Help":
                                self.show_start_menu = False
                                self.show_help_menu = True
                draw_menu = self.start_menu

            if self.show_help_menu:
                mouse_pos = pygame.mouse.get_pos()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show_main_menu = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.help_menu.buttons:
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Back":
                                self.show_help_menu = False
                                self.show_start_menu = True
                draw_menu = self.help_menu
            self.draw_current_menu(draw_menu)

        pygame.quit()



class Game:
    def __init__(self):
        self.width = 1200
        self.height = 900
        self.win = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.pause = True
        self.timer = 0
        self.bg = pygame.transform.scale(background_image, (self.width, self.height))

        hexmap_data = [[400, 136.60254037844385], [450, 136.60254037844385], [650, 136.60254037844385], [700, 136.60254037844385], [750, 136.60254037844385], [275, 179.9038105676658], [375, 179.9038105676658], [425, 179.9038105676658], [475, 179.9038105676658], [525, 179.9038105676658], [575, 179.9038105676658], [625, 179.9038105676658], [675, 179.9038105676658], [725, 179.9038105676658], [775, 179.9038105676658], [825, 179.9038105676658], [250, 223.20508075688772], [300, 223.20508075688772], [350, 223.20508075688772], [400, 223.20508075688772], [450, 223.20508075688772], [500, 223.20508075688772], [550, 223.20508075688772], [600, 223.20508075688772], [650, 223.20508075688772], [700, 223.20508075688772], [850, 223.20508075688772], [900, 223.20508075688772], [950, 223.20508075688772], [1000, 223.20508075688772], [1050, 223.20508075688772], [175, 266.50635094610965], [225, 266.50635094610965], [275, 266.50635094610965], [325, 266.50635094610965], [375, 266.50635094610965], [425, 266.50635094610965], [725, 266.50635094610965], [825, 266.50635094610965], [875, 266.50635094610965], [925, 266.50635094610965], [975, 266.50635094610965], [1025, 266.50635094610965], [200, 309.8076211353316], [250, 309.8076211353316], [300, 309.8076211353316], [350, 309.8076211353316], [400, 309.8076211353316], [450, 309.8076211353316], [650, 309.8076211353316], [700, 309.8076211353316], [750, 309.8076211353316], [800, 309.8076211353316], [850, 309.8076211353316], [900, 309.8076211353316], [950, 309.8076211353316], [1000, 309.8076211353316], [1050, 309.8076211353316], [175, 353.1088913245535], [225, 353.1088913245535], [275, 353.1088913245535], [325, 353.1088913245535], [475, 353.1088913245535], [525, 353.1088913245535], [575, 353.1088913245535], [625, 353.1088913245535], [675, 353.1088913245535], [875, 353.1088913245535], [925, 353.1088913245535], [975, 353.1088913245535], [1025, 353.1088913245535], [1075, 353.1088913245535], [100, 396.41016151377545], [150, 396.41016151377545], [200, 396.41016151377545], [250, 396.41016151377545], [300, 396.41016151377545], [350, 396.41016151377545], [450, 396.41016151377545], [500, 396.41016151377545], [550, 396.41016151377545], [600, 396.41016151377545], [650, 396.41016151377545], [850, 396.41016151377545], [900, 396.41016151377545], [950, 396.41016151377545], [1000, 396.41016151377545], [1050, 396.41016151377545], [125, 439.7114317029974], [175, 439.7114317029974], [225, 439.7114317029974], [275, 439.7114317029974], [325, 439.7114317029974], [475, 439.7114317029974], [525, 439.7114317029974], [575, 439.7114317029974], [625, 439.7114317029974], [675, 439.7114317029974], [725, 439.7114317029974], [775, 439.7114317029974], [825, 439.7114317029974], [875, 439.7114317029974], [925, 439.7114317029974], [975, 439.7114317029974], [1025, 439.7114317029974], [1075, 439.7114317029974], [100, 483.0127018922193], [150, 483.0127018922193], [200, 483.0127018922193], [250, 483.0127018922193], [300, 483.0127018922193], [350, 483.0127018922193], [450, 483.0127018922193], [750, 483.0127018922193], [800, 483.0127018922193], [850, 483.0127018922193], [900, 483.0127018922193], [950, 483.0127018922193], [1000, 483.0127018922193], [1050, 483.0127018922193], [1100, 483.0127018922193], [125, 526.3139720814413], [175, 526.3139720814413], [225, 526.3139720814413], [275, 526.3139720814413], [325, 526.3139720814413], [375, 526.3139720814413], [425, 526.3139720814413], [475, 526.3139720814413], [725, 526.3139720814413], [775, 526.3139720814413], [825, 526.3139720814413], [875, 526.3139720814413], [925, 526.3139720814413], [975, 526.3139720814413], [1025, 526.3139720814413], [1075, 526.3139720814413], [100, 569.6152422706632], [150, 569.6152422706632], [200, 569.6152422706632], [250, 569.6152422706632], [300, 569.6152422706632], [350, 569.6152422706632], [400, 569.6152422706632], [450, 569.6152422706632], [500, 569.6152422706632], [550, 569.6152422706632], [600, 569.6152422706632], [650, 569.6152422706632], [700, 569.6152422706632], [750, 569.6152422706632], [800, 569.6152422706632], [850, 569.6152422706632], [900, 569.6152422706632], [950, 569.6152422706632], [1000, 569.6152422706632], [1050, 569.6152422706632], [1100, 569.6152422706632], [175, 612.9165124598851], [225, 612.9165124598851], [275, 612.9165124598851], [325, 612.9165124598851], [375, 612.9165124598851], [425, 612.9165124598851], [475, 612.9165124598851], [525, 612.9165124598851], [575, 612.9165124598851], [625, 612.9165124598851], [675, 612.9165124598851], [725, 612.9165124598851], [775, 612.9165124598851], [825, 612.9165124598851], [875, 612.9165124598851], [925, 612.9165124598851], [975, 612.9165124598851], [250, 656.217782649107], [300, 656.217782649107], [350, 656.217782649107], [400, 656.217782649107], [450, 656.217782649107], [500, 656.217782649107], [550, 656.217782649107], [600, 656.217782649107], [650, 656.217782649107], [700, 656.217782649107], [750, 656.217782649107], [800, 656.217782649107], [850, 656.217782649107], [900, 656.217782649107], [950, 656.217782649107], [375, 699.519052838329], [425, 699.519052838329], [475, 699.519052838329], [525, 699.519052838329], [575, 699.519052838329], [625, 699.519052838329], [675, 699.519052838329], [725, 699.519052838329], [775, 699.519052838329], [825, 699.519052838329], [875, 699.519052838329], [925, 699.519052838329], [400, 742.8203230275509], [450, 742.8203230275509], [500, 742.8203230275509], [550, 742.8203230275509], [600, 742.8203230275509], [650, 742.8203230275509], [700, 742.8203230275509], [800, 742.8203230275509], [850, 742.8203230275509]]

        # remove hexmap_data param to use full map
        self.base_map = Hexmap(self.width, self.height - 100, hexmap_data)
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
        self.menu = buildingMenu(25, self.height - 10, 225, 80)
        self.play_pause_button = PlayPauseButton(play_btn, pause_btn, 40, self.height - 110)
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
        self.spawned_from_spawn_list_counter = 0
        # Should we go through the list of bonuses and apply them to the tower?
        self.update_bonuses = False
        self.icon_menu = IconMenu(250, self.height - 130, 925, 80)
        self.bonus_menu = RouletteMenu(self.win, 8) # BonusPickerMenu(self.win, 5)
        self.action_list = {
            "ATK_1" : {"Description": "Attack Damage + 1", "modifier" : 1, "pictogram" : pictogram_attack_damage,
                       "color" : (255, 255, 255, 200), "background_color" : (255, 255, 255 ,255) },
            "SPEED_1" : {"Description": "Attack Speed + 10%", "modifier" : 0.1, "pictogram" : pictogram_attack_speed,
                         "color" : (255, 255, 255, 200), "background_color" : (255, 255, 255 ,255) },
            "RANGE_1": {"Description": "Attack Range + 8%", "modifier": 0.08, "pictogram": pictogram_attack_range,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "RADIUS_1": {"Description": "Splash Radius +5%", "modifier": 0.05, "pictogram": pictogram_splash_range,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "CRITC_1": {"Description": "Crit Chance + 5%", "modifier": 0.05, "pictogram": pictogram_crit_chance,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "ACC_1": {"Description": "Accuracy + 5%", "modifier": 0.05, "pictogram": pictogram_accuracy,
                        "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "BULSP_1": {"Description": "Projectile speed + 10%", "modifier": 0.1, "pictogram": pictogram_projectile_speed,
                      "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
            "HEAL_1": {"Description": "Heal 10%", "modifier": 0.1,
                        "pictogram": pictogram_not_implemented,
                        "color": (255, 255, 255, 200), "background_color": (255, 255, 255, 255)},
        }
        self.action_list2 = {
            "ATK_2" : {"Description": "Attack Damage + 2", "modifier" : 2, "pictogram" : pictogram_attack_damage, "color" : (0, 32, 255, 200), "background_color" : (0, 32, 255,255) },
            "SPEED_2" : {"Description": "Attack Speed + 20 %", "modifier" : 0.2, "pictogram" : pictogram_attack_speed, "color" : (0, 32, 255, 200), "background_color" : (0, 32, 255,255) },
            "RANGE_2": {"Description": "Attack Range + 16%", "modifier": 0.16, "pictogram": pictogram_attack_range,
                      "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "RADIUS_2": {"Description": "Splash Radius + 10%", "modifier": 0.1, "pictogram": pictogram_splash_range,
                      "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "OBSTACLE_1": {"Description": "Obstacle +1", "modifier": 1, "pictogram": pictogram_not_implemented,
                         "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "CRITD_1": {"Description": "Crit Damage + 50%", "modifier": 0.50, "pictogram": pictogram_crit_damage,
                        "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "SHIELD_1": {"Description": "Protect cities +1", "modifier": 1.00, "pictogram": pictogram_shield,
                        "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
            "HEAL_2": {"Description": "Heal 25%", "modifier": 0.25, "pictogram": pictogram_not_implemented,
                         "color": (0, 32, 255, 200), "background_color": (0, 32, 255, 255)},
        }
        self.action_list3 = {
            "ATK_3": {"Description": "Attack Damage + 3", "modifier": 3, "pictogram": pictogram_attack_damage,
                      "color": (221,160,221, 200), "background_color": (221,160,221, 255)},
            "TOWER_1": {"Description": "Tower! +1", "modifier": 1, "pictogram": pictogram_not_implemented,
                        "color": (221,160,221, 200), "background_color": (221,160,221, 255)},
            "SPEED_3": {"Description": "Attack Speed + 30%", "modifier": 0.3, "pictogram": pictogram_attack_speed,
                        "color": (221,160,221, 200), "background_color": (221,160,221, 255)},
            "OBSTACLE_2": {"Description": "Obstacle +2", "modifier": 2, "pictogram": pictogram_not_implemented,
                         "color": (221,160,221, 200), "background_color": (221,160,221, 255)},
            "HEAL_3": {"Description": "Heal 100%", "modifier": 1, "pictogram": pictogram_not_implemented,
                           "color": (221, 160, 221, 200), "background_color": (221, 160, 221, 255)},
        }

        self.bonus_options = []
        self.applied_bonuses = []
        self.build_bonus_menu()
        self.show_bonus_menu = False
        self.show_build_menu = True
        self.enemy_spawn_points = [
            {"source": [575, 699.519052838329], "destination": [600, 396.41016151377545]},
        ]
        # {"source": [750, 223.20508075688772], "destination": [450, 656.217782649107]}
        self.portals = []
        self.cities = []
        self.waves = [
                [{"type": "Squaremon", "count": 1, "interval": 0.8}],
                [{"type": "Squaremon", "count": 2, "interval": 0.8}],
                [{"type": "Squaremon", "count": 3, "interval": 1.0}],
                [{"type": "Squaremon", "count" : 5, "interval": 0.7}],
                [{"type": "Squaremon", "count": 7, "interval": 0.5}],
                [{"type": "Squaremon", "count": 8, "interval": 0.6}],
                [{"type": "Squaremon", "count": 10, "interval": 0.8}],
                [{"type": "Squaremon", "count" : 6, "interval": 0.5},{"type": "SquaremonGreen", "count" : 2, "interval": 0.5}],
                [{"type": "Squaremon", "count" : 6, "interval": 4},{"type": "SquaremonGreen", "count" : 3, "interval": 0.5}],
                [{"type": "Squaremon", "count": 8, "interval": 4},{"type": "SquaremonGreen", "count": 2, "interval": 0.5}],
                [{"type": "SquaremonElite", "count": 1, "interval": 0.5}],
                # wave 11
                [{"type": "Squaremon", "count": 11, "interval": 0.5},{"type": "SquaremonGreen", "count": 3, "interval": 0.5}],
                [{"type": "Squaremon", "count": 14, "interval": 4},{"type": "SquaremonGreen", "count": 4, "interval": 0.5}],
                [{"type": "Squaremon", "count": 16, "interval": 0.5},{"type": "SquaremonGreen", "count": 5, "interval": 0.5}],
                [{"type": "Squaremon", "count": 16, "interval": 0.5},{"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
                [{"type": "Squaremon", "count": 18, "interval": 0.5},{"type": "SquaremonGreen", "count": 6, "interval": 0.5}],
                [{"type": "Squaremon", "count": 18, "interval": 0.5},{"type": "SquaremonGreen", "count": 6, "interval": 0.5}, {"type": "Trippet", "count": 2, "interval": 0.5}],
                [{"type": "Squaremon", "count": 22, "interval": 0.5},{"type": "SquaremonGreen", "count": 8, "interval": 0.5}, {"type": "Trippet", "count": 4, "interval": 0.5}],
                [{"type": "SquaremonGreen", "count": 12, "interval": 0.5}, {"type": "Trippet", "count": 8, "interval": 0.5}],
                [{"type": "SquaremonGreen", "count": 11, "interval": 0.5}, {"type": "Trippet", "count": 11, "interval": 1}],
                [{"type": "SquaremonElite", "count": 4, "interval": 1.8}],
                [{"type": "SquaremonGreen", "count": 16, "interval": 1}, {"type": "Trippet", "count": 19, "interval": 2}],
                # wave 21:
                [{"type": "Trippet", "count": 25, "interval": 1.8}],
                [{"type": "Trippet", "count": 35, "interval": 1}],
                [{"type": "Trippet", "count": 28, "interval": 1}, {"type": "SquaremonElite", "count": 3, "interval": 1.8}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "Trippet", "count": 40, "interval": 3}, {"type": "SquaremonGreenElite", "count": 4, "interval": 1}],
                [{"type": "SquaremonGreen", "count": 16, "interval": 1}, {"type": "TrippetElite", "count": 8,"interval": 2}],
                [{"type": "Yolkee", "count": 10, "interval": 2}, {"type": "Trippet", "count": 30, "interval": 1}],
                [{"type": "Yolkee", "count": 15, "interval": 2}, {"type": "Trippet", "count": 22, "interval": 1}],
                [{"type": "Trippet", "count": 50, "interval": 4}, {"type": "TrippetElite", "count": 50, "interval": 4}],
                [{"type": "Yolkee", "count": 18, "interval": 1.5}, {"type": "Trippet", "count": 30, "interval": 1}],
                [{"type": "Yolkee", "count": 18, "interval": 1.5}, {"type": "Trippet", "count": 30, "interval": 1}],
                #wave 31:
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
                [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            [{"type": "TrippetElite", "count": 5, "interval": 3}, {"type": "Trippet", "count": 10, "interval": 1}],
            ]

        self.enemies_removed = 0
        self.paths = []
        self.move_tower = False
        self.auto_target = True
        self.interval = 500

        self.game_speed = 20
        self.items_list = []
        self.gems = 0
        self.max_health = self.health = 25
        self.guardian = 1
        self.used_guardian = 0

        self.xp = 0
        self.level = 0
        self.xp_req = [5, 10, 20, 50, 100, 175, 300, 500, 800, 1200, 1750, 2500, 3500, 5000, 7500, 12000, 20000, 32000, 50000, 80000, 130000, 99999999]

    def run(self):
        run = True
        clock = pygame.time.Clock()

        for enemy_spawn_point in self.enemy_spawn_points:
            self.cities.append(City(enemy_spawn_point["destination"][0], enemy_spawn_point["destination"][1]))
            self.portals.append(Portal(enemy_spawn_point["source"][0], enemy_spawn_point["source"][1]))
            path = self.base_map.find_path(enemy_spawn_point["source"], enemy_spawn_point["destination"])
            self.paths.append(self.base_map.get_path_from_path_data(path))

        while run:
            clock.tick(self.game_speed)
            mouse_pos = pygame.mouse.get_pos()
            # need to change the mouse_pos to use hex at location
            hex_at_mouse_pos = self.base_map.get_hex_at_location(mouse_pos[0], mouse_pos[1])
            coordinates_of_hex = hex_at_mouse_pos.get_coords()
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
                        # REMOVE THE NEXT 4 LINES? use coordinates_of_hex?
                        for map_location in self.base_map.get_map_data():
                            # if map_location.collide(mouse_pos[0], mouse_pos[1]):
                            if map_location.click(mouse_pos[0], mouse_pos[1]):
                                clicked_location = map_location
                        if event.button == 1:
                            tiles = []
                            if clicked_location is not None:
                                clicked_location.toggle_passable()
                                if not self.set_start:
                                    self.start = [clicked_location.x, clicked_location.y]
                                    self.set_start = True
                                else:
                                    self.end = [clicked_location.x, clicked_location.y]
                                    self.set_start = False
                                    self.map_update_required = True
                                    print(self.start, self.end)
                            for map_location in self.base_map.get_map_data():
                                if map_location.passable:
                                    tiles.append([map_location.x, map_location.y])
                            print(tiles)

                        if event.button == 3:
                            if clicked_location is not None:
                                self.selected_hex = clicked_location
                                self.selected_hex.passable = True
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
                        self.moving_object.move(coordinates_of_hex[0], coordinates_of_hex[1])
                    # tower_list = self.attack_towers[:] + self.support_towers[:]
                    tower_list = self.attack_towers[:]
                    collide = False
                    # if valid_area:


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
                    for item in self.items_list:
                        if item.collide(mouse_pos[0], mouse_pos[1]):
                            quantity = 0
                            if item.name == "Gem":
                                quantity = item.pickup()
                                self.gems += quantity
                            # self.counter_list.append(Counter(quantity, item.x, item.y))
                            self.items_list.remove(item)
                    if event.type == pygame.MOUSEMOTION:
                        if self.show_bonus_menu:
                            self.bonus_menu.on_hover_over(mouse_pos[0], mouse_pos[1])

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.move_tower = False
                        if self.play_pause_button.click(mouse_pos[0], mouse_pos[1]):
                            self.pause = not (self.pause)
                            self.play_pause_button.toggle()
                            if self.pause:
                                print("paused")
                                for twr in self.attack_towers:
                                    for projectile in twr.projectiles:
                                        print(projectile)
                            else:
                                print("unpaused")
                            self.play_pause_button.paused = self.pause
                        if self.wave_complete:

                            # moving tower, left click tower to move it.
                            for tw in (self.attack_towers + self.obstacles):
                                if tw.click(coordinates_of_hex[0], coordinates_of_hex[1]) and not self.show_bonus_menu:
                                    """
                                    Moving tower on left click
                                    1. move tower into self.moving_object
                                    2. add 1 tower count to tower[type]
                                    3. remove tower from tower list (is this needed?)
                                    4. Toggle hex, update paths 
                                    """
                                    print("mouse pos", mouse_pos, tw.get_location(), coordinates_of_hex)
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
                                    hex_at_mouse_pos.passable = True
                                    # update path?
                                    for num, path in enumerate(self.paths):
                                        # coordinates are found in path, check if we can create a new path
                                        enemy_spawn_point = self.enemy_spawn_points[num]
                                        new_path = self.base_map.update_path(enemy_spawn_point["source"],
                                                                           enemy_spawn_point["destination"])
                                        self.paths[num] = new_path
                                    print("reached B need to update path..", new_path, hex_at_mouse_pos.x, hex_at_mouse_pos.y)


                        if self.show_bonus_menu:
                            self.show_build_menu = False
                            bonus_menu_button = self.bonus_menu.get_clicked(mouse_pos[0], mouse_pos[1])
                            # change below to only happen if button is clicked..
                            if bonus_menu_button is not None:
                                # These are instant bonuses, not applied to towers
                                specials = ["OBSTACLE_1", "OBSTACLE_2", "TOWER_1", "SHIELD_1", "HEAL_1", "HEAL_2", "HEAL_3"]
                                if bonus_menu_button in specials:
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
                                    if bonus_menu_button == "SHIELD_1":
                                        self.guardian += 1
                                        self.applied_bonuses.append(bonus_menu_button)
                                    if bonus_menu_button == "HEAL_1" or bonus_menu_button == "HEAL_2" or bonus_menu_button == "HEAL_3":
                                        self.apply_bonus(bonus_menu_button)
                                else:
                                    self.applied_bonuses.append(bonus_menu_button)
                                self.update_bonuses = True
                                self.icon_menu.add_or_update_icon(self.applied_bonuses)
                                self.show_bonus_menu = False
                                self.show_build_menu = True
                                self.build_bonus_menu()

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
                                        hex_at_mouse_pos.passable = False
                                        print("conditions for A are met")
                                        # Check if and see if clicked coordinates are in any paths
                                        for num, path in enumerate(self.paths):
                                            # coordinates are found in path, check if we can create a new path
                                            if hex_at_mouse_pos.get_coords() in path:
                                                # find path
                                                enemy_spawn_point = self.enemy_spawn_points[num]
                                                new_path = self.base_map.find_path(enemy_spawn_point["source"],
                                                                                   enemy_spawn_point["destination"])
                                                # couldn't create a new path, the path will get broken if we allow building at coordinates
                                                if not new_path:
                                                    print("Cannot place anything here, it will block path")
                                                    hex_at_mouse_pos.passable = True
                                                    print("conditions for A are no longer")
                                                    allow_build = False
                                                # found new path, next: ensure that the coordinates aren't a spawn point
                                                else:
                                                    update_path = self.base_map.get_path_from_path_data(
                                                        new_path)
                                                    # ensure that the coordinates aren't a spawn point
                                                    if hex_at_mouse_pos.get_coords() in update_path:
                                                        print("Cannot place anything here, it will block path")
                                                        hex_at_mouse_pos.passable = True
                                                        print("conditions for A are met again")
                                                        allow_build = False
                                                    else:
                                                        allow_build = True
                                                        self.paths[num] = update_path

                                        # self.money -= self.moving_object.price[0]
                                        if allow_build:
                                            self.moving_object.place_structure()
                                            location = self.moving_object.get_location()
                                            hex_at_mouse_pos.passable = False
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
                                            # update my path?

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
                        if len(self.spawn_list) == 0:
                            for enemy_wave in enemy_wave_data:
                                wave_enemy_total += enemy_wave["count"]

                                for _ in itertools.repeat(None, enemy_wave["count"]):
                                    select_path = random.choice(self.paths)
                                    generated_path, deviation = generate_alternative_path(select_path, 8)
                                    enemies = {
                                        "Squaremon": Squaremon(generated_path),
                                        "SquaremonElite": SquaremonElite(generated_path),
                                        "SquaremonGreen": SquaremonGreen(generated_path),
                                        "SquaremonGreenElite": SquaremonGreenElite(generated_path),
                                        "Trippet": Trippet(generated_path),
                                        "TrippetElite": TrippetElite(generated_path),
                                        "Yolkee": Yolkee(generated_path),
                                        "Juju": Juju(generated_path),
                                    }
                                    wave_enemy = enemies.get(enemy_wave["type"])
                                    wave_enemy.set_deviation(deviation)
                                    interval = enemy_wave["interval"] * 1000
                                    self.spawn_list.append([wave_enemy, interval])

                            self.wave_enemy_total = wave_enemy_total
                            random.shuffle(self.spawn_list)
                        timestamp = pygame.time.get_ticks()

                        if timestamp - self.timer >= self.interval and len(self.spawn_list) > self.spawned_from_spawn_list_counter:  # lastTimeStamp is the variable storing time and replace 500 with another integer that works well
                            # get the enemy with the number value from the index variable
                            try:
                                self.timer = timestamp  # resets the time stamp
                                self.enemies.append(self.spawn_list[self.spawned_from_spawn_list_counter][0])
                                self.interval = self.spawn_list[self.spawned_from_spawn_list_counter][1]
                                self.spawned_from_spawn_list_counter += 1
                                self.enemy_counter += 1  # The index variable
                            except IndexError:
                                print("list index out of range. Requested index:", self.enemy_counter, "In:", self.spawn_list[0], "is outside of range!")

                    for enemy in self.enemies:
                        enemy.move()
                        enemy.move_action(self.enemies, self.label_collector)
                        for poison_counter in enemy.poison_counters:
                            hit, dmg = poison_counter.action()
                            if hit:
                                enemy.hit(dmg)
                                self.label_collector.append(Label(enemy.x, enemy.y, dmg, (20, 200, 20), 12))
                            if poison_counter.duration <= 0:
                                enemy.poison_counters.remove(poison_counter)

                        if enemy.path_pos >= len(enemy.path) - 1 or enemy.health <= 0:
                            if enemy.health <= 0:
                                enemies_count_prev = len(self.enemies)
                                enemy.dead_action(self.enemies)
                                enemies_count_next = len(self.enemies)
                                self.xp += enemy.xp_value
                                if self.xp > self.xp_req[self.level]:
                                    self.level += 1
                                print("XP:", self.xp, "Level:", self.level)
                                count_dif = enemies_count_next - enemies_count_prev
                                self.wave_enemy_total += count_dif
                                self.enemy_counter += count_dif
                            else:
                                self.take_damage(enemy.survival_damage)
                            to_del.append(enemy)

                    for enemy in to_del:
                        # self.gate_health -= enemy.gate_damage
                        # print(d.travelled_path)
                        self.enemies_removed += 1
                        # item dropping here..
                        if len(enemy.item_drop) > 0 and enemy.item_drop_rate > 0 and enemy.health <= 0:
                            for item in enemy.item_drop:
                                if random.random() < enemy.item_drop_rate:
                                    new_item = Item(enemy.x, enemy.y, 1, 1)
                                    new_item.play_pickup_sound()
                                    self.items_list = [*self.items_list, new_item]
                        self.enemies.remove(enemy)

                    for tower in self.attack_towers:

                        list_of_labels = tower.find_target(self.enemies, self.auto_target)
                        if list_of_labels is not None:
                            for label in list_of_labels:
                                self.label_collector.append(label)

                    if self.enemies_removed == self.wave_enemy_total:
                        print("Guardian stuff:" ,self.guardian, self.used_guardian)
                        self.wave_complete = True
                        self.wave_enemy_total = 0
                        self.enemy_counter = 0
                        self.pause = not self.pause
                        self.play_pause_button.toggle()
                        self.enemies_removed = 0
                        self.spawn_list = []
                        self.show_bonus_menu = True
                        self.show_build_menu = False
                        self.spawned_from_spawn_list_counter = 0
                        self.used_guardian = 0
                        # add a new path at wave #
                        if self.wave == 25:
                            """
                            [1075, 439.7114317029974][600, 396.41016151377545]
                            [750, 136.60254037844385][600, 396.41016151377545]
                            [200, 396.41016151377545][600, 396.41016151377545]
                            """
                            # {"source": [750, 223.20508075688772], "destination": [450, 656.217782649107]}
                            self.add_enemy_path([750, 136.60254037844385], [600, 396.41016151377545])
                        self.wave += 1
                        print("Next wave:", self.wave)
            self.draw()
                # End of if not pause block
        # pygame.quit()


    def sort_by_y(self, spr):
        """
        sort sprite by Y position
        :param spr: key comparison
        :returns: key value
        """
        return spr.y

    def draw_xp_bar(self):
        """
        draw XP bar above health bar
        :return: None
        """
        length = self.width - 50
        health_bar = 0
        prev_level_xp = 0
        req_xp = self.xp_req[self.level]
        cur_xp = self.xp
        if self.level > 0:
            prev_level_xp = self.xp_req[self.level - 1]

        # hit the max level?
        # if self.level > len(self.xp_req):
            req_xp = self.xp_req[self.level] - prev_level_xp
            cur_xp = self.xp - prev_level_xp

        move_by = length / req_xp
        health_bar = round(move_by * cur_xp)
        if health_bar == length:
            health_bar = 0
            # print(cur_xp, prev_level_xp, req_xp, move_by, health_bar)
        xp_bar_color = (121, 100, 50)
        pygame.draw.rect(self.win, (50,50,50), (25, self.height - 145, length, 6), 0)
        pygame.draw.rect(self.win, xp_bar_color, (25, self.height - 145, health_bar, 6), 0)

        small_font = pygame.font.SysFont("segoeuisemilight", 12)
        phrase = "LvL:" + str(self.level) + " - XP:" + str(cur_xp) + "/" + str(req_xp)
        xp_line = small_font.render(str(phrase), 1, (255, 255, 255))
        x_center = self.width / 2 - xp_line.get_width() / 2
        self.win.blit(xp_line, (x_center, (self.height - 152)))


    def take_damage(self, dmg):
        if dmg > 0:
            if self.guardian > 0 and self.used_guardian < self.guardian:
                self.used_guardian += dmg
                if self.used_guardian > self.guardian:
                    self.health -= self.used_guardian - self.guardian
                    self.used_guardian = self.guardian
            else:
                self.health -= dmg
        else:
            self.health -= dmg
            if self.health > self.max_health:
                self.health = self.max_health

    def draw_health_bar(self):
        """
        draw health bar above HUD
        :return: None
        """
        length = self.width - 50
        move_by = length / self.max_health
        health_bar = round(move_by * self.health)
        health_bar_color = (0, 255, 0)
        if self.guardian > 0 and self.used_guardian < self.guardian:
            health_bar_color = (255, 215, 0)
        pygame.draw.rect(self.win, (255, 255, 255), (25, self.height - 136, length, 6), 0)
        pygame.draw.rect(self.win, (255,0,0), (25, self.height - 136, length, 6), 0)
        pygame.draw.rect(self.win, health_bar_color, (25, self.height - 136, health_bar, 6), 0)

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
                self.bonus_menu.add_btn(key, action_item["Description"], action_item["modifier"], action_item["pictogram"], action_item["color"], action_item["background_color"], 50)
                u += 1

    def apply_bonus(self, bonus_selector, target=None):
        if bonus_selector == "ATK_1":
            target.mod_damage += self.action_list[bonus_selector]["modifier"]
        if bonus_selector == "ATK_2":
            target.mod_damage += self.action_list2[bonus_selector]["modifier"]
        if bonus_selector == "ATK_3":
            target.mod_damage += self.action_list3[bonus_selector]["modifier"]
        if bonus_selector == "CRITC_1":
            target.mod_crit_chance += self.action_list[bonus_selector]["modifier"]

        if bonus_selector == "CRITD_1":
            target.mod_crit_damage += target.crit_damage * \
                                     self.action_list2[bonus_selector]["modifier"]
        if bonus_selector == "SPEED_1":
            target.mod_attack_speed += target.attack_speed * self.action_list[bonus_selector]["modifier"]
        if bonus_selector == "SPEED_2":
            target.mod_attack_speed += target.attack_speed * self.action_list2[bonus_selector]["modifier"]
        if bonus_selector == "SPEED_3":
            target.mod_attack_speed += target.attack_speed * self.action_list3[bonus_selector]["modifier"]
        if bonus_selector == "ACC_1":
            target.mod_accuracy += self.action_list[bonus_selector]["modifier"]
        if bonus_selector == "BULSP_1":
            target.mod_projectile_speed += target.projectile_speed * \
                                          self.action_list[bonus_selector]["modifier"]
        if bonus_selector == "RANGE_1":
            target.mod_attack_range += target.range * \
                                      self.action_list[bonus_selector]["modifier"]
        if bonus_selector == "RANGE_2":
            target.mod_attack_range += target.range * \
                                      self.action_list2[bonus_selector]["modifier"]
        if bonus_selector == "RADIUS_1":
            target.mod_max_splash_range += target.max_splash_range * \
                                          self.action_list[bonus_selector]["modifier"]
            target.mod_projectile_size += self.action_list[bonus_selector]["modifier"] * 20
        if bonus_selector == "RADIUS_2":
            target.mod_max_splash_range += target.max_splash_range * \
                                          self.action_list2[bonus_selector]["modifier"]
            target.mod_projectile_size += self.action_list2[bonus_selector]["modifier"] * 20
        if bonus_selector == "HEAL_1":
            hp_heal = self.max_health * self.action_list[bonus_selector]["modifier"]
            self.take_damage(-hp_heal)
        if bonus_selector == "HEAL_2":
            hp_heal = self.max_health * self.action_list2[bonus_selector]["modifier"]
            self.take_damage(-hp_heal)
        if bonus_selector == "HEAL_3":
            hp_heal = self.max_health * self.action_list3[bonus_selector]["modifier"]
            self.take_damage(-hp_heal)

    def apply_bonuses_to_towers(self):
        for tower in self.attack_towers:
            tower.clear_modifiers()
            for bonus in self.applied_bonuses:
                self.apply_bonus(bonus, tower)
            tower.print_modifiers()

    def add_enemy_path(self, src, destination):
        """
        Add a new path to the field, if the new path is blocked, return all towers to inventory
        and run again.
        :param src: list of coordinates [x, y]
        :param destination: list of coordinates [x, y]
        :return: None
        """
        spawn_points =  {"source": src, "destination": destination}
        path = self.base_map.find_path(spawn_points["source"], spawn_points["destination"])

        if not path:
            print("Unable to create path, clearing map", path)
            # return all towers and objects
            for tw in (self.attack_towers + self.obstacles):

                sel_tower = tw.ico_name
                self.selected_hex = self.base_map.get_hex_at_location(tw.x, tw.y)
                for button in self.menu.buttons:
                    if button.name == sel_tower:
                        button.update_quantity(1)
                if tw in self.attack_towers:
                    self.attack_towers.remove(tw)
                else:
                    self.obstacles.remove(tw)
                self.selected_hex.passable = True
            self.add_enemy_path(src, destination)

        else:
            get_path = self.base_map.get_path_from_path_data(path)
            self.enemy_spawn_points.append(spawn_points)
            self.cities.append(City(spawn_points["destination"][0], spawn_points["destination"][1]))
            self.portals.append(Portal(spawn_points["source"][0], spawn_points["source"][1]))
            self.paths.append(get_path)

    def add_tower(self, name):
        """
        Create new tower object after clicking on the matching icon in list tower_opt_list and assign it to the
        tower in moving_object
        :param name: string, must match one of the options in tower_opt_list
        :return: None
        """
        x, y = pygame.mouse.get_pos()
        tower_opt_list = {"buy_minigun": MinigunTower(x, y), "buy_obstacle": Obstacle(x, y)}
        # if name == "buy_minigun":
        try:
            self.moving_object = tower_opt_list[name]
        except Exception as e:
            print(str(e) + "Invalid name")




    def draw(self):
        self.win.blit(self.bg, (0, 0))

        if len(self.attack_towers) == 0 and self.moving_object:
            self.moving_object.draw_placement(self.win)

        for portal in self.portals:
            portal.draw(self.win)

        if self.pause:
            self.base_map.clear_paths()
            if not self.build_mode:

                for path in self.paths:
                    self.base_map.set_path(path)
            self.base_map.draw(self.win)

        if len(self.items_list) > 0:
            for item in self.items_list:
                item.draw(self.win)
                item.despawn_timer -= 1
                if item.despawn_timer <= 0:
                    self.items_list.remove(item)

        for tower in self.attack_towers:
            tower.draw(self.win)
            if self.moving_object:
                self.moving_object.draw_placement(self.win)

        if self.show_build_menu:
            self.menu.draw(self.win)

        for obstacle in self.obstacles:
            obstacle.draw(self.win)

        enemies = self.enemies
        for enemy in sorted(enemies, key=self.sort_by_y):
            enemy.draw(self.win)

        if len(self.label_collector) > 0:
            for label in self.label_collector:
                label.draw(self.win)
                label.despawn_timer -= 1
                if label.despawn_timer <= 0:
                    self.label_collector.remove(label)

        self.draw_health_bar()
        self.draw_xp_bar()

        if self.show_bonus_menu:
            self.bonus_menu.draw(self.win)

        self.icon_menu.draw(self.win)
        # Wave display:
        surface = pygame.Surface((180, 50), pygame.SRCALPHA, 32)
        surface.fill((192, 192, 192, 175))
        med_font= pygame.font.SysFont("segoeuisemilight", 25)
        small_font = pygame.font.SysFont("segoeuisemilight", 18)
        rectangle = pygame.Rect(-2,  80, 180, 50)
        self.win.blit(surface, rectangle)
        pygame.draw.rect(self.win, (192, 192, 192, 175), rectangle, width=2, border_radius=0)
        wave = med_font.render("Wave: "+ str(self.wave), 1, (47,79,79))

        #Gem display:
        surface = pygame.Surface((180, 50), pygame.SRCALPHA, 32)
        surface.fill((192, 192, 192, 175))
        med_font= pygame.font.SysFont("segoeuisemilight", 25)
        small_font = pygame.font.SysFont("segoeuisemilight", 18)
        rectangle = pygame.Rect(-2,  160, 180, 50)
        self.win.blit(surface, rectangle)
        pygame.draw.rect(self.win, (192, 192, 192, 175), rectangle, width=2, border_radius=0)
        gems = med_font.render("Gems: "+ str(self.gems), 1, (47,79,79))

        if self.show_bonus_menu:
            phase = "Bonus selection phase"
        elif not self.pause:
            phase = "Attack phase"
        else:
            phase = "Preparation phase"

        step = small_font.render(str(phase), 1, (47, 79, 79))
        self.win.blit(wave, (10, 75))
        self.win.blit(step, (10, 105))

        self.win.blit(gems, (10, 165))
        pygame.display.update()

g = MainGameMenu()
g.main_menu()
#g.run()