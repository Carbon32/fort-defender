# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Enemy: #

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)

        # Enemy Settings:

        self.alive = True
        self.speed = speed
        self.health = health
        self.max_health = health

        # Enemy Attack: 

        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 2000

        # Enemy Animations: 

        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0

        # Enemy Timer: 

        self.update_time = pygame.time.get_ticks()
        self.destroy_sprite = pygame.time.get_ticks()

        # Enemy Sprite:

        self.image = self.animation_list[self.action][self.frame_index]
        self.transparency = 255

        # Enemy Rectangle:

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, game, particles, fort, sounds):
        if(self.alive):
            if(pygame.sprite.spritecollide(self, game.cannon_balls, True)):
                if(game.ball_type == 0):
                    self.health -= 15
                if(game.ball_type == 1):
                    self.health -= 20
                else:
                    self.health -= (20 * game.ball_type)

                if(self.rect.x > 0):
                    particles.add_game_particle("hit", self.rect.x, self.rect.y)

            if(self.rect.right > fort.rect.left):
                self.update_action(1)

            if(self.action == 0):
                self.rect.x += self.speed

            if(self.action == 1):
                if(pygame.time.get_ticks() - self.last_attack > self.attack_cooldown):
                    fort.health -= 50
                    if(fort.health < 0):
                        fort.health = 0

                    self.last_attack = pygame.time.get_ticks()   

            if(self.health <= 0):
                game.coins += 50
                game.kills += 1
                game.available_balls += 3
                self.update_action(2)
                self.alive = False

                if(sounds.sound_status):
                    sounds.explosion.play()

        self.update_animation()

        if(self.rect.x > 0):
            if(self.alive):
                if(self.health > self.max_health // 2):
                    particles.add_game_particle("white_smoke", self.rect.midleft[0] + 10, self.rect.midleft[1] - (self.rect.midleft[1] // 128))
                else:
                    particles.add_game_particle("black_smoke", self.rect.midleft[0] + 10, self.rect.midleft[1] - (self.rect.midleft[1] // 128))

                pygame.draw.rect(game.display, (250, 0, 0), (self.rect.x, self.rect.y - (self.rect.h // 4), self.rect.w, 5))
                pygame.draw.rect(game.display, (0, 250, 0), (self.rect.x, self.rect.y - (self.rect.h // 4), self.rect.w * (self.health / self.max_health), 5))

            game.display.blit(self.image, (self.rect.x, self.rect.y))

    def update_animation(self):
        animation_time = 40
        self.image = self.animation_list[self.action][self.frame_index]
        if (pygame.time.get_ticks() - self.update_time > animation_time):
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        if(self.frame_index >= len(self.animation_list[self.action])):
            if(self.action == 2):
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        if(new_action != self.action):
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()