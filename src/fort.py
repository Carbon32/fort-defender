# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.ball import *

# Fort: #

class Fort():
    def __init__(self, game, x, y, health):

        # Game: 

        self.game = game

        # Fort Settings: 

        self.health = health
        self.max_health = self.health
        self.already_fired = False
        self.upgrades = 0
        self.reload_time = 2000
        self.start_reload = False
        self.timer_reload = 0

        # Fort Sprites: 

        self.fort_images = [self.game.load_game_image(f'assets/fort/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/fort')))]
        self.fort_upgrades = [self.game.load_game_image(f'assets/upgrades/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/upgrades')))]
        self.construction = [self.game.load_game_image(f'assets/construction/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/construction')))]
        self.image = self.fort_images[0]

        # Construction Properties:

        self.construction_start = False
        self.construction_animations = 0
        self.construction_current_time = pygame.time.get_ticks()
        self.construction_timer = 500

        # Ball Properties:

        self.current_balls = 8
        self.ball_type = 0
        self.total_balls = len(os.listdir('assets/ball')) - 1

        # Fort Rectangle: 

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def fire_ball(self, particles, sounds):
        position = pygame.mouse.get_pos()
        x_distance = (position[0] - self.rect.midleft[0])
        y_distance = -(position[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_distance, x_distance))
        accuracy = random.randint(-5, 5)
        if(pygame.mouse.get_pressed()[0] and self.already_fired == False and self.current_balls > 0 and position[0] < (self.game.screen_width // 2) + (self.game.screen_width // 3)):
            ball = Ball(self.game, self.rect.midleft[0] + 30, self.rect.midleft[1] - 25, self.angle + accuracy, self.ball_type)
            self.game.cannon_balls.add(ball)
            self.already_fired = True
            self.current_balls -= 1

            if(sounds.sound_status):
                sounds.shoot.play()

            if(self.game.screen_width == 1280 or self.game.screen_width == 1920):
                particles.add_game_particle("fort_smoke", (self.rect.midleft[0] // 2) - (self.rect.midleft[1] // 12 - self.rect.midleft[1] // 6), self.rect.midleft[0]  + (self.rect.midleft[1] // 16))
            else:
                particles.add_game_particle("fort_smoke", self.rect.midleft[0] - (self.rect.midleft[1] // 3), self.rect.midleft[0]  + (self.rect.midleft[1] // 16))

        if(pygame.mouse.get_pressed()[0] == False):
            self.already_fired = False

        if(self.start_reload == False and self.current_balls == 0):
            self.timer_reload = pygame.time.get_ticks()
            self.start_reload = True

        if(self.current_balls == 0 and self.game.available_balls >= 8):
            if(pygame.time.get_ticks() - self.timer_reload > self.reload_time):
                self.current_balls = 8
                self.game.available_balls -= 8
                self.start_reload = False

        if(self.current_balls == 0 and self.game.available_balls >= 1):
            if(pygame.time.get_ticks() - self.timer_reload > self.reload_time):
                self.current_balls = self.game.available_balls
                self.game.available_balls -= self.game.available_balls
                self.start_reload = False


    def draw_fort(self):
        if(self.health <= 250):
            self.image = self.fort_images[2]

        elif(self.health <= 500):
            self.image = self.fort_images[1]
        else:
            self.image = self.fort_images[0]

        self.game.display.blit(self.image, self.rect)
        self.game.display.blit(self.fort_upgrades[self.upgrades], self.rect)
        self.game.display.blit(self.construction[self.construction_animations], self.rect)

        pygame.draw.rect(self.game.display, (250, 0, 0), (0 + self.game.screen_width // 12, 0 + self.game.screen_height // 64, self.rect.w, self.rect.h // 6), border_radius = self.game.screen_width // 64)
        pygame.draw.rect(self.game.display, (0, 250, 0), (0 + self.game.screen_width // 12, 0 + self.game.screen_height // 64, self.rect.w * (self.health / self.max_health), self.rect.h // 6), border_radius = self.game.screen_width // 64)
        pygame.draw.rect(self.game.display, (0, 0, 0), (0 + self.game.screen_width // 12, 0 + self.game.screen_height // 64, self.rect.w, self.rect.h // 6), self.game.screen_width // 256, border_radius = self.game.screen_width // 64)
        self.game.draw_text('(' + str(self.health) + "/" + str(self.max_health) + ")", 1 * (self.game.screen_height // 52), (69, 69, 69), self.game.screen_width // 7, 0 + self.game.screen_height // 42)

        if(self.construction_start):
            if(pygame.time.get_ticks() - self.construction_current_time >= self.construction_timer):
                self.construction_current_time = pygame.time.get_ticks()

                if(self.construction_animations < len(self.construction) - 1):
                    self.construction_animations += 1
                else:
                    self.construction_start = False
                    self.construction_animations = 0

    def repair_fort(self, sounds):
        if(self.game.coins >= 500 and self.health < self.max_health):
            self.health += 250
            self.game.coins -= 500

            if(self.health > self.max_health):
                self.health = self.max_health

            if(sounds.sound_status):
                sounds.build.play()
        else:
            sounds.error.play()

    def upgrade_balls(self, sounds):
        if(self.game.coins >= 5000 and self.ball_type != self.total_balls):
                self.ball_type += 1
                self.game.coins -= 5000
                if(sounds.sound_status):
                    sounds.ball_load.play()
        else:
            sounds.error.play()

    def upgrade_armour(self, sounds):
        if(self.game.coins >= 1000 and not self.construction_start):
            self.max_health += 500
            self.game.coins -= 1000
            self.construction_start = True
            if(self.upgrades < 3):
                self.upgrades += 1
            else:
                self.upgrades = 3
            if(sounds.sound_status):
                sounds.build.play()
        else:
            sounds.error.play()

    def add_balls(self, sounds):
        if(self.game.coins >= 250):
                self.game.available_balls += 5
                self.game.coins -= 250
                if(sounds.sound_status):
                    sounds.ball_load.play()
        else:
            sounds.error.play()