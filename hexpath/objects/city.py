import pygame
from functions import *
from .objects import Object
from functions.functions import *
import random
pygame.font.init()
popup_font = pygame.font.SysFont("segoeuisemilight", 14)
item_images = []

city_imgs = []
"""
for x in range(1, 5):
    city_imgs.append(pygame.transform.scale(
        pygame.image.load(os.path.join("resources", "city_" +str(x) + ".png")).convert_alpha(), (60, 60)))
        
        https://www.bing.com/images/search?view=detailV2&ccid=VumPh0ez&id=78498B7A653EFA9B5D846659D8116A299C7F7FBF&thid=OIP.VumPh0ezPhnhroL8lRjShQAAAA&mediaurl=https%3A%2F%2Fi.pinimg.com%2Foriginals%2Fab%2F5e%2F8c%2Fab5e8ce8ac7fec7c2b1b1e39523e97b4.png&cdnurl=https%3A%2F%2Fth.bing.com%2Fth%2Fid%2FR.56e98f8747b33e19e1ae82fc9518d285%3Frik%3Dv39%252fnClqEdhZZg%26pid%3DImgRaw%26r%3D0&exph=312&expw=339&q=rpg+castle+icon&simid=608025068608750682&form=IRPRST&ck=4D3912478400599CD07BDEAC2F08FB6C&selectedindex=2&ajaxhist=0&ajaxserp=0&pivotparams=insightsToken%3Dccid_5z1IDWT5*cp_0AA1355A10BB635BEB77F043A33376CA*mid_5765BE6C03191C550F3F71D6521BDB0D9F7609B5*simid_608014606062588454*thid_OIP.5z1IDWT5!_SqC1XZ1LnsVowHaFP&vt=0&sim=11&iss=VSI&ajaxhist=0&ajaxserp=0
"""
item_image = pygame.transform.scale(load_image("resources", "castle.png"), (80, 80))

class City(Object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_y = y
        self.img = item_image # city_imgs[random.randint(1, len(city_imgs)-1)]
        self.despawn_timer = 50
        self.angle = 0

    def draw(self, win):
        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2))