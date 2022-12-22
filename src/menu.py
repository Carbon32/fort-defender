# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Menu: #

class Menu():
    def __init__(self, game):

        # Display:

        self.game = game

        # Menu: 

        self.menu_status = True
        self.menu_background = pygame.Surface((self.game.screen_width, self.game.screen_height))
        self.background_design = self.game.load_game_image('assets/menu.png', self.game.screen_width, self.game.screen_height)
        self.menu_background.blit(self.background_design, (0, 0))

        # Buttons:

        
        self.button_start = ButtonText(self.game, 'Start', self.game.screen_width // 3, self.game.screen_height // 4, self.game.screen_width // 3 , self.game.screen_height // 5, 22)
        self.button_quit = ButtonText(self.game, 'Exit', self.game.screen_width // 3, self.game.screen_height // 2, self.game.screen_width // 3, self.game.screen_height // 5, 22)
        self.button_music = ButtonTest(self.game.display, self.game.load_game_image('assets/Buttons/music_on.png', 64, 64), 10, 20, 64, 64, 6, 50)
        self.button_sound = ButtonTest(self.game.display, self.game.load_game_image('assets/Buttons/sound_on.png', 64, 64), 10, 120, 64, 64, 6, 50)

    def handle_menu(self, sounds):
        if(self.menu_status):
            self.game.display.blit(self.menu_background, (0, 0))
            if(sounds.music_status):
                self.button_music.change_button(self.game.load_game_image('assets/buttons/music_on.png', 64, 64))
            else:
                self.button_music.change_button(self.game.load_game_image('assets/buttons/music_off.png', 64, 64))

            if(sounds.sound_status):
                self.button_sound.change_button(self.game.load_game_image('assets/buttons/sound_on.png', 64, 64))
            else:
                self.button_sound.change_button(self.game.load_game_image('assets/buttons/sound_off.png', 64, 64))

    def check_menu(self):
        if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.menu_status == False):
            self.button_start.change_text('Continue')
            self.menu_status = True
            self.game.toggle_mouse_cursor_on()