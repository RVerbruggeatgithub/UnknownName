import itertools
from hex.hexmap import Hexmap
from enemies.squaremon import *
from hexpath.objects.natobjects import NatObject
from menu import viewport
from towers.miniguntower import MinigunTower
from towers.obstacle import Obstacle
from objects.portal import Portal
from objects.city import City
from objects.popup import *
from objects.items import *
from effects.bonuses import *
from functions.functions import *
from savegame.save import *

pygame.display.init()
SCRN_SIZE = (1200, 750)
pygame.display.set_mode(SCRN_SIZE, pygame.RESIZABLE)
pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN])

tech_tree_map = load_image("resources", "techtree.png")
background_image = load_image("resources", "porro_village.png")
sm_green_hex = pygame.transform.scale(load_image("resources", "menu_small_green_hex.png").convert_alpha(), (25, 25))
sm_lblue_hex = pygame.transform.scale(load_image("resources", "menu_small_lblue_hex.png").convert_alpha(), (25, 25))
sm_pink_hex = pygame.transform.scale(load_image("resources", "menu_small_pink_hex.png").convert_alpha(), (25, 25))
sm_purple_hex = pygame.transform.scale(load_image("resources", "menu_small_purple_hex.png").convert_alpha(), (25, 25))
sm_red_hex = pygame.transform.scale(load_image("resources", "menu_small_red_hex.png").convert_alpha(), (25, 25))
sm_yellow_hex = pygame.transform.scale(load_image("resources", "menu_small_yellow_hex.png").convert_alpha(), (25, 25))

play_btn = pygame.transform.scale(load_image("resources", "button_play.png").convert_alpha(), (32, 32))
pause_btn = pygame.transform.scale(load_image("resources", "button_pause.png").convert_alpha(), (32, 32))
ico_minigun = pygame.transform.scale(load_image("resources", "ico_minigun.png").convert_alpha(), (30, 30))
ico_obstruction = pygame.transform.scale(load_image("resources", "ico_obstruction.png").convert_alpha(), (30, 30))
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

savegame_data = GameData()


class MainGameMenu:
    def __init__(self):
        savegame_data.load_game()
        self.gems = savegame_data.gems
        self.width = 1200
        self.height = 750
        self.win = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        """
        Main menu stuff:
        """
        self.show_main_menu = True
        self.start_menu = Menu(25, 25, self.width - 50, self.height - 50, None)
        frame_width = 400
        frame_height = 600
        self.start_menu.add_frame((self.width//2 - frame_width//2), 80, frame_width, frame_height, (100,150,225, 100), (0,0,0, 0))
        self.start_menu.add_plain_button("New Game", None, (self.width//2 - frame_width//2 + frame_width*0.1), 250, frame_width*0.8, 50, (0,0,0, 100))
        self.start_menu.add_plain_button("Upgrades", None, (self.width // 2 - frame_width // 2 + frame_width * 0.1),
                                         325, frame_width * 0.8, 50, (0, 0, 0, 100))
        self.start_menu.add_plain_button("Help", None, (self.width // 2 - frame_width // 2 + frame_width * 0.1),
                                         400, frame_width * 0.8, 50, (0, 0, 0, 100))
        self.start_menu.add_plain_button("Quit", None, (self.width // 2 - frame_width // 2 + frame_width * 0.1),
                                         475, frame_width * 0.8, 50, (0, 0, 0, 100))
        self.show_start_menu = True
        self.help_menu = Menu(25, 25, self.width - 50, self.height - 50, None)
        self.show_help_menu = False
        self.show_upgrade_menu = False
        self.help_menu.add_frame((self.width//2 - 400), 80, 800, frame_height, (100,150,225, 100), (0,0,0, 0))
        self.help_menu.add_plain_button("Back", None, (self.width//2 - 400) + 725, 100, 65, 50, (0,0,0, 100))

        self.upgrade_menu = Menu(25, 25, self.width/4 - 50, self.height - 50, None)
        self.upgrade_menu.add_plain_button("Back", None, (self.width//2 - 400) + 725, 100, 65, 50, (0,0,0, 100))
        self.popup_content = None




    def draw_current_menu(self, current_menu, fill=True):
        if fill:
            self.win.fill([255, 255, 255])
        current_menu.draw(self.win)



    def run(self):
        game = Game()
        game.run()

    def main_menu(self):
        rectangle = pygame.Rect(300, 80, 500, 500)
        VP_surface = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
        mousebeingpressed = False
        stage = viewport.Manager(2000, 2000, 2)
        focus = stage.add_object(0, viewport.moveable_obj(stage.w / 2, stage.h / 2))
        # savegame_data.upgrades
        stage.add_object(0, viewport.img_obj(0, 0, 2000, 2000, tech_tree_map, "Background Image", "", None, False))

        stage.add_object(1, viewport.img_obj(1002, 882, 40, 40, sm_green_hex, "Attack +1", "ATKA01", None, "ATKA01" in savegame_data.upgrades, cost=50))
        # x, y, w, h, img, desc, code, prerequisite, selected, status=False, cost=0
        stage.add_object(1, viewport.img_obj(926, 844, 40, 40, sm_green_hex, "Attack +1", "ATKA02", ["ATKA01"], "ATKA02" in savegame_data.upgrades, cost=80))
        stage.add_object(1, viewport.img_obj(1078, 844, 40, 40, sm_green_hex, "Attack +1", "ATKA03", ["ATKA01"], "ATKA03" in savegame_data.upgrades, cost=125))
        stage.add_object(1, viewport.img_obj(926, 760, 40, 40, sm_green_hex, "Attack +1", "ATKA04", ["ATKA02"], "ATKA04" in savegame_data.upgrades, cost=200))
        stage.add_object(1, viewport.img_obj(1078, 760, 40, 40, sm_green_hex, "Attack +1", "ATKA05", ["ATKA03"], "ATKA05" in savegame_data.upgrades, cost=300))
        stage.add_object(1, viewport.img_obj(1002, 718, 40, 40, sm_green_hex, "Poison 5% chance", "SPECB01", ["ATKA05", "ATKA04"], "SPECB01" in savegame_data.upgrades, cost=500))

        stage.add_object(1, viewport.img_obj(1002, 1100, 40, 40, sm_yellow_hex, "Accuracy +1", "ACCA01", None, "ACCA01" in savegame_data.upgrades, cost=50))
        stage.add_object(1, viewport.img_obj(926, 1142, 40, 40, sm_yellow_hex, "Accuracy +1", "ACCA02", ["ACCA01"], "ACCA02" in savegame_data.upgrades, cost=80))
        stage.add_object(1, viewport.img_obj(1078, 1142, 40, 40, sm_yellow_hex, "Accuracy +1", "ACCA03", ["ACCA01"], "ACCA03" in savegame_data.upgrades, cost=125))
        stage.add_object(1, viewport.img_obj(926, 1226, 40, 40, sm_yellow_hex, "Accuracy +1", "ACCA04", ["ACCA02"], "ACCA04" in savegame_data.upgrades, cost=200))
        stage.add_object(1, viewport.img_obj(1078, 1226, 40, 40, sm_yellow_hex, "Accuracy +1", "ACCA05", ["ACCA03"], "ACCA05" in savegame_data.upgrades, cost=300))
        stage.add_object(1, viewport.img_obj(1002, 1264, 40, 40, sm_yellow_hex, "Penetrate 5% chance", "SPECA01", ["ACCA05", "ACCA04"], "SPECA01" in savegame_data.upgrades, cost=500))

        # top
        stage.add_object(1, viewport.img_obj(1171, 809, 40, 40, sm_red_hex, "Crit +1", "CRITA05", ["CRITA03"], "CRITA05" in savegame_data.upgrades, cost=300))
        # left_top
        stage.add_object(1, viewport.img_obj(1095, 851, 40, 40, sm_red_hex, "Crit +1", "CRITA03", ["CRITA01"], "CRITA03" in savegame_data.upgrades, cost=125))
        # right_top
        stage.add_object(1, viewport.img_obj(1247, 851, 40, 40, sm_red_hex, "Headshot 10% chance", "SPECC01", ["CRITA05", "CRITA04"], "SPECC01" in savegame_data.upgrades, cost=500))
        # left_bottom
        stage.add_object(1, viewport.img_obj(1095, 937, 40, 40, sm_red_hex, "Crit +1", "CRITA01", None, "CRITA01" in savegame_data.upgrades, cost=50))
        # right_bottom
        stage.add_object(1, viewport.img_obj(1247, 937, 40, 40, sm_red_hex, "Crit +1", "CRITA04", ["CRITA02"], "CRITA04" in savegame_data.upgrades, cost=200))
        # bottom
        stage.add_object(1, viewport.img_obj(1171, 979, 40, 40, sm_red_hex, "Crit +1", "CRITA02", ["CRITA01"], "CRITA02" in savegame_data.upgrades, cost=80))

        # top
        stage.add_object(1, viewport.img_obj(837, 809, 40, 40, sm_pink_hex, "Bullet speed +1", "BUSPA05", ["BUSPA03"], "BUSPA05" in savegame_data.upgrades, cost=300))
        # left_top
        stage.add_object(1, viewport.img_obj(761, 851, 40, 40, sm_pink_hex, "Bullet Fragmentation 10% chance", "SPECD01", ["BUSPA04", "BUSPA05"], "SPECD01" in savegame_data.upgrades, cost=500))
        # right_top
        stage.add_object(1, viewport.img_obj(911, 851, 40, 40, sm_pink_hex, "Bullet speed  +1", "BUSPA03", ["BUSPA01"], "BUSPA03" in savegame_data.upgrades, cost=125))
        # left_bottom
        stage.add_object(1, viewport.img_obj(761, 937, 40, 40, sm_pink_hex, "Bullet speed  +1", "BUSPA04", ["BUSPA02"], "BUSPA04" in savegame_data.upgrades, cost=200))
        # right_bottom
        stage.add_object(1, viewport.img_obj(911, 937, 40, 40, sm_pink_hex, "Bullet speed  +1", "BUSPA01", None, "BUSPA01" in savegame_data.upgrades, cost=50))
        # bottom
        stage.add_object(1, viewport.img_obj(837, 979, 40, 40, sm_pink_hex, "Bullet speed  +1", "BUSPA02", ["BUSPA01"], "BUSPA02" in savegame_data.upgrades, cost=80))

        # stage.add_object(0, viewport.block_obj(1050, 1200, 80, 250))
        stage.viewport.center_on_x(1000)
        stage.viewport.center_on_y(1000)
        # draw the main menu
        while self.show_main_menu:
            if self.show_start_menu:
                mouse_pos = pygame.mouse.get_pos()
                draw_menu = self.start_menu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show_main_menu = False
                    if event.type == pygame.MOUSEMOTION:
                        self.start_menu.on_hover(mouse_pos[0], mouse_pos[1])
                    if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.start_menu.buttons:
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "New Game":
                                self.run()
                                savegame_data.load_game()
                                self.gems = savegame_data.gems
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Upgrades":
                                self.show_start_menu = False
                                self.show_help_menu = False
                                self.show_upgrade_menu = True
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Help":
                                self.show_start_menu = False
                                self.show_help_menu = True
                                self.show_upgrade_menu = False
                                self.show_upgrade_menu = True
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Quit":
                                self.show_start_menu = False
                                self.show_help_menu = False
                                self.show_upgrade_menu = False
                                self.show_main_menu = False
                self.draw_current_menu(draw_menu)
                pygame.display.update()

            if self.show_help_menu:
                mouse_pos = pygame.mouse.get_pos()
                draw_menu = self.help_menu
                self.show_start_menu = False
                self.show_help_menu = True
                self.show_upgrade_menu = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show_main_menu = False
                    if event.type == pygame.MOUSEBUTTONUP:
                        for button in self.help_menu.buttons:
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Back":
                                self.show_help_menu = False
                                self.show_start_menu = True
                                self.show_upgrade_menu = False
                self.draw_current_menu(draw_menu)
                pygame.display.update()

            if self.show_upgrade_menu:
                mouse_pos = pygame.mouse.get_pos()
                draw_menu = self.upgrade_menu
                self.show_start_menu = False
                self.show_help_menu = False
                self.show_upgrade_menu = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.show_main_menu = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mousebeingpressed = True
                    if event.type == pygame.MOUSEBUTTONUP:
                        mousebeingpressed = False
                        stage.focus_off()
                        opt_clicked = stage.get_clicked(mouse_pos[0], mouse_pos[1])
                        if opt_clicked:
                            # action to take on click
                            if opt_clicked.cost <= self.gems and opt_clicked.enabled and not opt_clicked.selected:
                                self.gems -= opt_clicked.cost
                                savegame_data.gems = self.gems
                                savegame_data.save_gamedata()
                                opt_clicked.selected = True
                        for button in self.help_menu.buttons:
                            if button.click(mouse_pos[0], mouse_pos[1]) and button.button_text == "Back":
                                print("Following bonusses will be applied:", stage.acquired)
                                savegame_data.upgrades = stage.acquired
                                savegame_data.save_gamedata()
                                self.show_upgrade_menu = False
                                self.show_start_menu = True
                    if event.type == pygame.MOUSEMOTION and mousebeingpressed:
                        stage.focus_on(focus)
                    if event.type == pygame.MOUSEMOTION:
                        hover_obj = stage.get_hover(mouse_pos[0], mouse_pos[1])
                        if hover_obj:
                            self.popup_content = Popup(hover_obj.x - stage.viewport.x + 50, hover_obj.y - stage.viewport.y + 5, hover_obj.desc, hover_obj.cost)
                        else:
                            self.popup_content = None


                # self.win.fill([255, 255, 255])
                stage.do()
                self.draw_current_menu(draw_menu, False)
                # self.win.blit(VP_surface, rectangle)
                if self.popup_content is not None:
                    self.popup_content.draw(self.win)
                ###
                surface = pygame.Surface((180, 50), pygame.SRCALPHA, 32)
                surface.fill((192, 192, 192, 175))
                med_font = pygame.font.SysFont("segoeuisemilight", 25)
                small_font = pygame.font.SysFont("segoeuisemilight", 18)
                rectangle = pygame.Rect(-2, 160, 180, 50)
                self.win.blit(surface, rectangle)
                pygame.draw.rect(self.win, (192, 192, 192, 175), rectangle, width=2, border_radius=0)
                gems = med_font.render("Gems: " + str(self.gems), 1, (47, 79, 79))
                self.win.blit(gems, (10, 165))
                pygame.display.update()


        pygame.quit()



class Game:
    def __init__(self):
        self.width = 1200
        self.height = 750
        self.win = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.pause = True
        self.timer = 0
        self.bg = pygame.transform.scale(background_image, (self.width, self.height))
        # natural objects
        self.natobjects = []
        # usable hex locations:
        hexmap_data = [[400, 130.0], [450, 130.0], [500, 130.0], [550, 130.0], [600, 130.0], [650, 130.0], [700, 130.0], [750, 130.0], [225, 173.30127018922192], [275, 173.30127018922192], [325, 173.30127018922192], [375, 173.30127018922192], [425, 173.30127018922192], [475, 173.30127018922192], [525, 173.30127018922192], [575, 173.30127018922192], [625, 173.30127018922192], [675, 173.30127018922192], [725, 173.30127018922192], [775, 173.30127018922192], [825, 173.30127018922192], [875, 173.30127018922192], [925, 173.30127018922192], [150, 216.60254037844385], [200, 216.60254037844385], [250, 216.60254037844385], [300, 216.60254037844385], [350, 216.60254037844385], [400, 216.60254037844385], [450, 216.60254037844385], [500, 216.60254037844385], [550, 216.60254037844385], [600, 216.60254037844385], [650, 216.60254037844385], [700, 216.60254037844385], [750, 216.60254037844385], [800, 216.60254037844385], [850, 216.60254037844385], [900, 216.60254037844385], [950, 216.60254037844385], [1000, 216.60254037844385], [1050, 216.60254037844385], [175, 259.9038105676658], [225, 259.9038105676658], [275, 259.9038105676658], [325, 259.9038105676658], [375, 259.9038105676658], [425, 259.9038105676658], [475, 259.9038105676658], [525, 259.9038105676658], [575, 259.9038105676658], [625, 259.9038105676658], [675, 259.9038105676658], [725, 259.9038105676658], [775, 259.9038105676658], [825, 259.9038105676658], [875, 259.9038105676658], [925, 259.9038105676658], [975, 259.9038105676658], [1025, 259.9038105676658], [1075, 259.9038105676658], [200, 303.2050807568877], [250, 303.2050807568877], [300, 303.2050807568877], [350, 303.2050807568877], [400, 303.2050807568877], [450, 303.2050807568877], [500, 303.2050807568877], [550, 303.2050807568877], [600, 303.2050807568877], [650, 303.2050807568877], [700, 303.2050807568877], [750, 303.2050807568877], [800, 303.2050807568877], [850, 303.2050807568877], [900, 303.2050807568877], [950, 303.2050807568877], [1000, 303.2050807568877], [1050, 303.2050807568877], [75, 346.50635094610965], [125, 346.50635094610965], [175, 346.50635094610965], [225, 346.50635094610965], [275, 346.50635094610965], [325, 346.50635094610965], [375, 346.50635094610965], [425, 346.50635094610965], [475, 346.50635094610965], [525, 346.50635094610965], [575, 346.50635094610965], [625, 346.50635094610965], [675, 346.50635094610965], [725, 346.50635094610965], [775, 346.50635094610965], [825, 346.50635094610965], [875, 346.50635094610965], [925, 346.50635094610965], [975, 346.50635094610965], [1025, 346.50635094610965], [1075, 346.50635094610965], [100, 389.8076211353316], [150, 389.8076211353316], [200, 389.8076211353316], [250, 389.8076211353316], [300, 389.8076211353316], [350, 389.8076211353316], [400, 389.8076211353316], [450, 389.8076211353316], [500, 389.8076211353316], [550, 389.8076211353316], [600, 389.8076211353316], [650, 389.8076211353316], [700, 389.8076211353316], [750, 389.8076211353316], [800, 389.8076211353316], [850, 389.8076211353316], [900, 389.8076211353316], [950, 389.8076211353316], [1000, 389.8076211353316], [1050, 389.8076211353316], [1100, 389.8076211353316], [1150, 389.8076211353316], [75, 433.1088913245535], [125, 433.1088913245535], [175, 433.1088913245535], [225, 433.1088913245535], [275, 433.1088913245535], [325, 433.1088913245535], [375, 433.1088913245535], [425, 433.1088913245535], [475, 433.1088913245535], [525, 433.1088913245535], [575, 433.1088913245535], [625, 433.1088913245535], [675, 433.1088913245535], [725, 433.1088913245535], [775, 433.1088913245535], [825, 433.1088913245535], [875, 433.1088913245535], [925, 433.1088913245535], [975, 433.1088913245535], [1025, 433.1088913245535], [1075, 433.1088913245535], [1125, 433.1088913245535], [100, 476.41016151377545], [150, 476.41016151377545], [200, 476.41016151377545], [250, 476.41016151377545], [300, 476.41016151377545], [350, 476.41016151377545], [400, 476.41016151377545], [450, 476.41016151377545], [500, 476.41016151377545], [550, 476.41016151377545], [600, 476.41016151377545], [650, 476.41016151377545], [700, 476.41016151377545], [750, 476.41016151377545], [800, 476.41016151377545], [850, 476.41016151377545], [900, 476.41016151377545], [950, 476.41016151377545], [1000, 476.41016151377545], [1050, 476.41016151377545], [1100, 476.41016151377545], [175, 519.7114317029974], [225, 519.7114317029974], [275, 519.7114317029974], [325, 519.7114317029974], [375, 519.7114317029974], [425, 519.7114317029974], [475, 519.7114317029974], [525, 519.7114317029974], [575, 519.7114317029974], [625, 519.7114317029974], [675, 519.7114317029974], [725, 519.7114317029974], [775, 519.7114317029974], [825, 519.7114317029974], [875, 519.7114317029974], [925, 519.7114317029974], [975, 519.7114317029974], [250, 563.0127018922193], [300, 563.0127018922193], [350, 563.0127018922193], [400, 563.0127018922193], [450, 563.0127018922193], [500, 563.0127018922193], [550, 563.0127018922193], [600, 563.0127018922193], [650, 563.0127018922193], [700, 563.0127018922193], [750, 563.0127018922193], [800, 563.0127018922193], [850, 563.0127018922193], [900, 563.0127018922193], [950, 563.0127018922193], [375, 606.3139720814413], [425, 606.3139720814413], [475, 606.3139720814413], [525, 606.3139720814413], [575, 606.3139720814413], [625, 606.3139720814413], [675, 606.3139720814413], [725, 606.3139720814413], [775, 606.3139720814413], [825, 606.3139720814413], [875, 606.3139720814413], [300, 649.6152422706632], [350, 649.6152422706632], [400, 649.6152422706632], [450, 649.6152422706632], [500, 649.6152422706632], [550, 649.6152422706632], [600, 649.6152422706632], [650, 649.6152422706632], [700, 649.6152422706632], [750, 649.6152422706632], [800, 649.6152422706632], [850, 649.6152422706632]]

        # these locations hold object
        self.non_buildable_objects = [[625, 606.3139720814413], [650, 563.0127018922193], [700, 563.0127018922193],
                                 [600, 649.6152422706632], [850, 476.41016151377545], [825, 433.1088913245535],
                                 [850, 389.8076211353316], [900, 389.8076211353316], [875, 433.1088913245535],
                                 [700, 303.2050807568877], [675, 259.9038105676658], [625, 259.9038105676658],
                                 [450, 389.8076211353316], [425, 433.1088913245535], [450, 476.41016151377545],
                                 [400, 476.41016151377545], [375, 433.1088913245535], [325, 433.1088913245535],
                                 [400, 216.60254037844385], [350, 216.60254037844385], [375, 259.9038105676658],
                                 [400, 303.2050807568877], [650, 216.60254037844385], [925, 259.9038105676658],
                                 [975, 259.9038105676658], [600, 476.41016151377545], [425, 606.3139720814413],
                                 [400, 563.0127018922193], [200, 303.2050807568877], [175, 259.9038105676658],
                                 [225, 259.9038105676658], [200, 216.60254037844385], [200, 476.41016151377545],
                                 [150, 476.41016151377545], [100, 476.41016151377545], [600, 130.0],
                                 [400, 130.0], [825, 606.3139720814413], [850, 563.0127018922193],
                                 ]

        # map = hexmap_data - non_buildable_objects\
        for nbo in self.non_buildable_objects:
            hexmap_data.remove(nbo)
            self.natobjects.append(NatObject(nbo[0], nbo[1]))

        # remove hexmap_data param to use full map
        self.build_mode = False

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
        self.menu = buildingMenu(25, 140, 225, 50)
        self.play_pause_button = PlayPauseButton(play_btn, pause_btn, 50, 30)
        self.menu.add_configured_btn(self.play_pause_button)

        self.menu.add_btn(ico_minigun, "buy_minigun", "Minigun", 3)
        self.menu.add_btn(ico_obstruction, "buy_obstacle", "Obstacle", 5)
        self.close_game_button = PlainButton("❌", "Quit", self.width - 50, 20, 50, 50)

        self.gate_health = 10000
        # This mode allow to create a path from point A to B returns start and end location as lists in console.

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
        self.icon_menu = IconMenu(250, 20, 900, 50)
        self.icon_menu.add_configured_btn(self.close_game_button)
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

        savegame_data.load_game()
        self.applied_bonuses = self.applied_bonuses + savegame_data.get_mapped_bonus_ids()

        self.build_bonus_menu()
        self.show_bonus_menu = False
        self.show_build_menu = True
        self.enemy_spawn_points = [
            {"source": [650, 649.6152422706632], "destination": [625, 346.50635094610965]},
        ]
        # {"source": [750, 223.20508075688772], "destination": [450, 656.217782649107]}
        # 1050, 476.41016151377545 ; 1000, 216.60254037844385; 750, 130.0; 250, 216.60254037844385; 225 519.7114317029974
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
                # wave 31:
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
                # wave 41:
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
                # wave 51
                [{"type": "Juju", "count": 25, "interval": 3}],
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

        self.stun = Stun()
        self.poison = Poison()
        self.piercing = Piercing()
        self.headshot = Headshot()
        self.fragmentation = Fragmentation()



        self.icon_menu.add_or_update_icon(self.applied_bonuses)
        self.update_bonuses = True
        self.apply_specials()


    def run(self):
        run = True
        clock = pygame.time.Clock()
        try:
            for enemy_spawn_point in self.enemy_spawn_points:
                self.cities.append(City(enemy_spawn_point["destination"][0], enemy_spawn_point["destination"][1]))
                self.portals.append(Portal(enemy_spawn_point["source"][0], enemy_spawn_point["source"][1]))
                path = self.base_map.find_path(enemy_spawn_point["source"], enemy_spawn_point["destination"])
                self.paths.append(self.base_map.get_path_from_path_data(path))
        except TypeError as e:
            print(e)

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
                                print(map_location.x, map_location.y)
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
                        savegame_data.gems = self.gems
                        savegame_data.save_gamedata()
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
                        self.icon_menu.on_hover(mouse_pos[0], mouse_pos[1])
                        # self.close_game_button.hover_over(mouse_pos[0], mouse_pos[1])

                    if event.type == pygame.MOUSEBUTTONUP:
                        self.move_tower = False
                        if self.close_game_button.click(mouse_pos[0], mouse_pos[1]):
                            savegame_data.gems += self.gems
                            savegame_data.save_gamedata()
                            run = False
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
                        self.apply_specials()
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
                                        "YolkeeElite":YolkeeElite(generated_path),
                                        "Juju": Juju(generated_path),
                                        "TestUnit": TestUnit(generated_path),
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
                        if self.wave == 10 or self.wave == 25 or self.wave == 45 or self.wave == 70 or self.wave == 100:
                            """
                            [1075, 439.7114317029974][600, 396.41016151377545]
                            [750, 136.60254037844385][600, 396.41016151377545]
                            [200, 396.41016151377545][600, 396.41016151377545]
                            """
                            # {"source": [750, 223.20508075688772], "destination": [450, 656.217782649107]}
                            sources = [[1050, 476.41016151377545],
                            [1000, 216.60254037844385],
                            [750, 130.0],
                            [250, 216.60254037844385],
                            [225, 519.7114317029974]]

                            end = [625, 346.50635094610965]
                            # check self.portals or allow overlap.
                            source = random.choice(sources)

                            self.add_enemy_path(source, end)
                        self.wave += 1
                        print("Next wave:", self.wave)
            self.draw()
                # End of if not pause block
        # pygame.quit()

    def apply_specials(self):
        # self.specials
        print("Applying bonuseses")
        self.stun.update_stats()
        self.poison.update_stats()
        self.piercing.update_stats()
        self.headshot.update_stats()
        self.fragmentation.update_stats()
        for twr in self.attack_towers:
            twr.stun = self.stun
            twr.poison = self.poison
            twr.piercing = self.piercing
            twr.headshot = self.headshot
            twr.fragmentation = self.fragmentation

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
        pygame.draw.rect(self.win, (50,50,50), (25, self.height - 45, length, 6), 0)
        pygame.draw.rect(self.win, xp_bar_color, (25, self.height - 45, health_bar, 6), 0)

        small_font = pygame.font.SysFont("segoeuisemilight", 12)
        phrase = "LvL:" + str(self.level) + " - XP:" + str(cur_xp) + "/" + str(req_xp)
        xp_line = small_font.render(str(phrase), 1, (255, 255, 255))
        x_center = self.width / 2 - xp_line.get_width() / 2
        self.win.blit(xp_line, (x_center, (self.height - 52)))


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
        pygame.draw.rect(self.win, (255, 255, 255), (25, self.height - 36, length, 6), 0)
        pygame.draw.rect(self.win, (255,0,0), (25, self.height - 36, length, 6), 0)
        pygame.draw.rect(self.win, health_bar_color, (25, self.height - 36, health_bar, 6), 0)
        small_font = pygame.font.SysFont("segoeuisemilight", 12)
        phrase = "Health:" + str(self.health)
        hp_line = small_font.render(str(phrase), 1, (66, 66, 66))
        x_center = self.width / 2 - hp_line.get_width() / 2
        self.win.blit(hp_line, (x_center, (self.height - 40)))

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
        if bonus_selector == "PEN_1":
            if self.piercing.level < 1:
                self.piercing.level = 1
        if bonus_selector == "PEN_2":
            if self.piercing.level < 2:
                self.piercing.level = 2
        if bonus_selector == "PEN_3":
            if self.piercing.level < 3:
                self.piercing.level = 3
        if bonus_selector == "PEN_4":
            if self.piercing.level < 4:
                self.piercing.level = 4
        if bonus_selector == "PEN_5":
            if self.piercing.level < 5:
                self.piercing.level = 5
        if bonus_selector == "PSN_1":
            self.poison.level = 1
        if bonus_selector == "PSN_2":
            self.poison.level = 2
        if bonus_selector == "PSN_3":
            self.poison.level = 3
        if bonus_selector == "PSN_4":
            self.poison.level = 4
        if bonus_selector == "PSN_5":
            self.poison.level = 5
        if bonus_selector == "HST_1":
            self.headshot.level = 1
        if bonus_selector == "HST_2":
            self.headshot.level = 2
        if bonus_selector == "HST_3":
            self.headshot.level = 3
        if bonus_selector == "HST_4":
            self.headshot.level = 4
        if bonus_selector == "HST_5":
            self.headshot.level = 5
        if bonus_selector == "FRG_1":
            self.fragmentation.level = 1
        if bonus_selector == "FRG_2":
            self.fragmentation.level = 2
        if bonus_selector == "FRG_3":
            self.fragmentation.level = 3
        if bonus_selector == "FRG_4":
            self.fragmentation.level = 4
        if bonus_selector == "FRG_5":
            self.fragmentation.level = 5

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

        for natobj in self.natobjects:
            natobj.draw(self.win)

        for portal in self.portals:
            portal.draw(self.win)


        city_counter = 0
        for city in self.cities:
            if city_counter == 0:
                city.draw(self.win)


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