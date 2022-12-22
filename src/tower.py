# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.ball import *

# Towers: #

class Tower(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        pygame.sprite.Sprite.__init__(self)

        # Game:

        self.game = game

        # Tower Settings:

        self.ready = False
        self.angle = 0
        self.last_shot = pygame.time.get_ticks()

        # Tower Sprites: 

        self.tower_images = [self.game.load_game_image(f'assets/towers/{i}.png', self.game.screen_width // 12, self.game.screen_height // 8) for i in range(len(os.listdir('assets/towers')))]
        self.tower_upgrades = [self.game.load_game_image(f'assets/tower_upgrades/{i}.png', self.game.screen_width // 12, self.game.screen_height // 8) for i in range(len(os.listdir('assets/tower_upgrades')))]
        self.image = self.tower_images[0]

        # Tower Rectangle: 

        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self, fort, sounds):
        self.ready = False
        for enemy in self.game.game_enemies:
            if(enemy.alive and enemy.rect.x > self.game.screen_width // 2):
                target_x, target_y = enemy.rect.top, enemy.rect.bottom
                self.ready = True
                break

        if(self.ready):
            x_distance = (target_x - self.rect.midleft[0])
            y_distance = -(target_y - self.rect.midleft[1])
            self.angle = math.degrees(math.atan2(y_distance, x_distance))
            shot_cooldown = 1000

            if(pygame.time.get_ticks() - self.last_shot > shot_cooldown):
                self.last_shot = pygame.time.get_ticks()
                ball = Ball(self.game, self.rect.midleft[0], self.rect.midleft[1] - 50, self.angle, self.game.ball_type)
                self.game.cannon_balls.add(ball)
                if(sounds.sound_status):
                    sounds.shoot.play()

        if(fort.health <= 250):
            self.image = self.tower_images[2]

        elif(fort.health <= 500):
            self.image = self.tower_images[1]
        else:
            self.image = self.tower_images[0]

        self.game.display.blit(self.image, self.rect)
        self.game.display.blit(self.tower_upgrades[fort.upgrades], self.rect)
