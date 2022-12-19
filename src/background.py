# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Background: #

class Background():
    def __init__(self, game):

        # Display:

        self.game = game

        # Properties:

        self.current_time = pygame.time.get_ticks()
        self.cycle_timer = 1000
        self.cycle = 0 
        self.night = False
        self.sky_color = [135, 206, 255]

        # Background Design:

        self.game_background = pygame.Surface((self.game.screen_width, self.game.screen_height))
        self.background_design = self.game.load_game_image('assets/background.png', self.game.screen_width, self.game.screen_height)

    def update_game_background(self):
        if(self.night == False):
            self.sky_color[0] = 135 - self.cycle

            if(self.sky_color[0] < 0):
                self.sky_color[0] = 0

            self.sky_color[1] = 206 - self.cycle

            if(self.sky_color[1] < 0):
                self.sky_color[1] = 0

            self.sky_color[2] = 255 - self.cycle

            if(self.sky_color[2] <= 0):
                self.sky_color[2] = 0
                self.cycle = 0
                self.night = True

        if(self.night == True):
            self.sky_color[0] = 35 + self.cycle
            self.sky_color[1] = 26 + self.cycle
            self.sky_color[2] = 30 + self.cycle

            if(self.sky_color[0] >= 135):
                self.sky_color[0] = 135

            if(self.sky_color[1] >= 206):
                self.sky_color[1] = 206

            if(self.sky_color[2] >= 255):
                self.sky_color[2] = 255

            if(self.sky_color[0] == 135 and self.sky_color[1] == 206 and self.sky_color[2] == 255):
                self.cycle = 0
                self.night = False

        self.game_background.fill((self.sky_color[0], self.sky_color[1], self.sky_color[2]))
        self.game_background.blit(self.background_design, (0, 0))

    def draw_level_design(self, x, y):
        self.game.display.blit(self.game_background, (x, y))

    def update_time(self):
        if(pygame.time.get_ticks() - self.current_time >= self.cycle_timer):
            self.cycle += 1
            self.current_time = pygame.time.get_ticks()