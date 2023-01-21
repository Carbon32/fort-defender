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

        # Buttons:
        
        self.button_start = ButtonText(self.game, 'Start', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 2 - (self.game.screen_height // 6), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.button_quit =  ButtonText(self.game, 'Exit', self.game.screen_width // 2 - (self.game.screen_width // 10), self.game.screen_height // 3 + (self.game.screen_height // 5), self.game.screen_width // 4, self.game.screen_width // 12, self.game.screen_width // 80, 'large')
        self.button_music = ButtonImage(self.game.display, self.game.load_game_image('assets/Buttons/music_on.png', self.game.screen_width // 30, self.game.screen_width // 30), self.game.screen_height // 128, self.game.screen_height // 64, self.game.screen_width // 30, self.game.screen_width // 30, 6, self.game.screen_width // 38)
        self.button_sound = ButtonImage(self.game.display, self.game.load_game_image('assets/Buttons/sound_on.png', self.game.screen_width // 30, self.game.screen_width // 30), self.game.screen_height // 128, self.game.screen_height // 10, self.game.screen_width // 30, self.game.screen_width // 30, 6, self.game.screen_width // 38)

        # Title:

        self.step = 0
        self.title_background_color = (184, 160, 238)

    def handle_menu(self, sounds):
        if(self.menu_status):
            self.game.display.fill((40, 42, 53))
            bounce = -1 * math.sin(self.step) * self.game.screen_width // 64
            pygame.draw.rect(self.game.display, self.title_background_color, pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), border_radius = self.game.screen_width // 38)
            pygame.draw.rect(self.game.display, (0, 0, 0), pygame.Rect(self.game.screen_width // 3.7, self.game.screen_height // 24 + bounce, self.game.screen_width - (self.game.screen_width // 2), self.game.screen_height // 5), self.game.screen_width // 128, border_radius = self.game.screen_width // 38)
            self.game.draw_custom_text(self.game.fonts['huge'], 'Fort Defender', (0, 0, 0), self.game.screen_width // 3.3, (0 + self.game.screen_height // 12) + bounce)
            self.step += 0.05
            if(sounds.music_status):
                self.button_music.change_button(self.game.load_game_image('assets/buttons/music_on.png', self.game.screen_width // 30, self.game.screen_width // 30))
            else:
                self.button_music.change_button(self.game.load_game_image('assets/buttons/music_off.png', self.game.screen_width // 30, self.game.screen_width // 30))

            if(sounds.sound_status):
                self.button_sound.change_button(self.game.load_game_image('assets/buttons/sound_on.png', self.game.screen_width // 30, self.game.screen_width // 30))
            else:
                self.button_sound.change_button(self.game.load_game_image('assets/buttons/sound_off.png', self.game.screen_width // 30, self.game.screen_width // 30))

    def check_menu(self):
        if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.menu_status == False):
            self.button_start.change_text('large', 'Continue')
            self.menu_status = True
            self.game.toggle_mouse_cursor_on()
