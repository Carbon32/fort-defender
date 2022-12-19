# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Fade In: #

class Fade():
    def __init__(self, display, direction, color, speed):

        # Display: 

        self.display = display

        # Fade Settings: 

        self.direction = direction
        self.color = color
        self.speed = speed
        self.fade_counter = 0

    def fade(self, screen_width, screen_height):
        fade_completed = False
        self.fade_counter += self.speed
        if(self.direction == 1):
            pygame.draw.rect(self.display, self.color, (0 - self.fade_counter, 0, screen_width // 2, screen_height))
            pygame.draw.rect(self.display, self.color, (screen_width // 2 + self.fade_counter, 0, screen_width, screen_height))
            pygame.draw.rect(self.display, self.color, (0, 0 - self.fade_counter, screen_width, screen_height // 2))
            pygame.draw.rect(self.display, self.color, (0, screen_height // 2 + self.fade_counter, screen_width, screen_height))

        if(self.direction == 2):
            pygame.draw.rect(self.display, self.color, (0, 0, screen_width, 0 + self.fade_counter))
        
        if(self.fade_counter >= screen_width):
            fade_completed = True

        return fade_completed