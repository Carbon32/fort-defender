# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Clouds: #

class Clouds():
    def __init__(self, game):

        # Game: 

        self.game = game

        # Movement:

        self.move = 1

        # Clouds: 

        self.clouds = [ [0, 0, 0], 
                        [1, game.screen_width // 2, game.screen_height // 2],
                        [2, game.screen_width // 6, game.screen_height // 3],
                        [3, game.screen_width // 3, game.screen_height // 6],
                        [4, 0, game.screen_height // 2],
                        [5, game.screen_width, game.screen_height // 6],
                        [6, game.screen_width, game.screen_height // 3],
                        [7, game.screen_width // 18, game.screen_height // 4],
                        [8, game.screen_width // 6, game.screen_height // 6],
                        [9, game.screen_width // 16, game.screen_height // 8],
                        [10, game.screen_width // 4, game.screen_height // 10]
        ]

        self.cloud_sprites = [self.game.load_game_image(f'assets/clouds/{cloud[0]}.png', self.game.screen_width // 6, self.game.screen_height // 12) for cloud in self.clouds]

    def handle_clouds(self):
        if(self.game.clouds and self.game.started):
            for cloud in self.clouds:
                if(cloud[1] < self.game.screen_width):
                    self.move = (self.game.screen_width // 100) // 8
                else:
                    cloud[1] = 0 - (self.game.screen_width // 2)

                cloud[1] += self.move
                self.game.display.blit(self.cloud_sprites[cloud[0]], (cloud[1], cloud[2]))
