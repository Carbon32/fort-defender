# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Sounds: #

class Sounds():
    def __init__(self, game):

        # Game:

        self.game = game

        # Music:

        self.music_status = True

        # Sounds: 

        self.sound_status = True

        # Available Sounds: 

        self.shoot = self.game.load_game_sound('sounds/shoot.wav', 0.2)
        self.explosion = self.game.load_game_sound('sounds/explosion.mp3', 0.2)
        self.build = self.game.load_game_sound('sounds/build.mp3', 0.2)
        self.ball_load = self.game.load_game_sound('sounds/ball_load.mp3', 0.2)
        self.error = self.game.load_game_sound('sounds/no.wav', 0.2)


    def play_music(self):
        pygame.mixer.music.load('sounds/music.mp3')
        pygame.mixer.music.set_volume(10)
        #pygame.mixer.music.play(-1, 0.0, 5000)

    def stop_music(self):
        pygame.mixer.music.stop()
