# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Cannon Ball: #

class Ball(pygame.sprite.Sprite):
    def __init__(self, game, x, y, angle, ball_type):
        pygame.sprite.Sprite.__init__(self)

        # Game: 

        self.game = game

        # Ball Sprite: 

        self.image = self.game.load_game_image(f'assets/ball/{ball_type}.png', self.game.screen_width // 100, self.game.screen_width // 100)

        # Ball Rectangle: 

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Ball Angle: 

        self.angle = math.radians(angle)

        # Ball Speed: 

        self.speed = self.game.screen_width // 100

        # Ball Direction: 

        self.delta_x = math.cos(self.angle) * self.speed
        self.delta_y = -(math.sin(self.angle)) * self.speed

    def update(self, particles):
        if(self.rect.right < 0 or self.rect.left > self.game.screen_width or self.rect.bottom < 0 or self.rect.top > self.game.screen_height):
            self.kill()

        if(self.rect.bottom > self.game.screen_height - 20):
            particles.add_game_particle("ground_hit", self.rect.x, self.rect.y)
            self.kill()

        self.rect.x += self.delta_x
        self.rect.y += self.delta_y