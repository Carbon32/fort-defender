# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.game import *
from src.background import *
from src.ball import *
from src.button import *
from src.clouds import *
from src.crosshair import *
from src.enemy import *
from src.fade import *
from src.fort import *
from src.level import *
from src.menu import *
from src.particles import *
from src.sounds import *
from src.tower import *
from src.ui import *

# Game Resolution: #

class Resolution():
    def __init__(self, game):
        
        # Game: 

        self.game = game

        # Display:

        self.resolution_window = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("Fort Defender: ")
        pygame.display.set_icon(self.game.load_game_image('assets/icon.png', 32, 32))
        self.resolution_status = True

        # Background:

        self.background = self.game.load_game_image('assets/menu.png', 400, 500)

        # Buttons: 

        self.resolution_a = ButtonTest(self.resolution_window, self.game.load_game_image('assets/resolution/D.png', 150, 150), 110, 150, 200, 75, 8, 20) # 800 x 600
        self.resolution_b = ButtonTest(self.resolution_window, self.game.load_game_image('assets/resolution/C.png', 150, 150), 110, 250, 200, 75, 8, 20) # 1024 x 768
        self.resolution_c = ButtonTest(self.resolution_window, self.game.load_game_image('assets/resolution/B.png', 150, 150), 110, 350, 200, 75, 8, 20) # 1280 x 720
        self.resolution_d = ButtonTest(self.resolution_window, self.game.load_game_image('assets/resolution/A.png', 150, 150), 110, 50, 200, 75, 8, 20) # 1920 x 1080

    def update_background(self):
        self.resolution_window.fill((255, 255, 255))
        self.resolution_window.blit(self.background, (0, 0))

    def set_resolution(self, screen_width, screen_height):
        self.game.screen_width = screen_width
        self.game.screen_height = screen_height
        self.resolution_status = False

    def update_window(self):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.resolution_status = False
                self.game.destroy_game()
        pygame.display.update()


# Game Graphics: #

class Graphics():
    def __init__(self, game):
        
        # Game: 

        self.game = game

        # Display:

        self.graphics_window = pygame.display.set_mode((400, 500))
        pygame.display.set_caption("Fort Defender: ")
        pygame.display.set_icon(self.game.load_game_image('assets/icon.png', 32, 32))
        self.graphics_status = True

        # Background:

        self.background = self.game.load_game_image('assets/menu.png', 400, 500)

        # Buttons: 

        self.effects = ButtonTest(self.graphics_window, self.game.load_game_image('assets/graphics/A_on.png', 150, 150), 105, 50, 200, 75, 8, 20) 
        self.clouds = ButtonTest(self.graphics_window, self.game.load_game_image('assets/graphics/B_on.png', 150, 150), 105, 150, 200, 75, 8, 20)
        self.start = ButtonTest(self.graphics_window, self.game.load_game_image('assets/graphics/start.png', 150, 150), 125, 300, 150, 75, 8, 20) 

    def update_background(self):
        self.graphics_window.fill((255, 255, 255))
        self.graphics_window.blit(self.background, (0, 0))

    def set_clouds(self):
        if(self.game.clouds):
            self.game.clouds = False
        else:
            self.game.clouds = True

    def set_effects(self):
        if(self.game.effects):
            self.game.effects = False
        else:
            self.game.effects = True

    def update_window(self):

        if(self.game.effects):
            self.effects.change_button(self.game.load_game_image('assets/graphics/A_on.png', 150, 150))
        else:
            self.effects.change_button(self.game.load_game_image('assets/graphics/A_off.png', 150, 150)) 

        if(self.game.clouds):
            self.clouds.change_button(self.game.load_game_image('assets/graphics/B_on.png', 150, 150)) 
        else:
            self.clouds.change_button(self.game.load_game_image('assets/graphics/B_off.png', 150, 150)) 

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.resolution_status = False
                self.game.destroy_game()
        pygame.display.update()

