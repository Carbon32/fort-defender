# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.enemy import *

# Game: #

class Game():
    def __init__(self, level):

        # Display:

        self.screen_width = 1920
        self.screen_height = 1080
        self.engine_running = True
        self.fps_handler = pygame.time.Clock()
        self.display = pygame.Surface

        # Game Settings: 

        self.coins = 5000
        self.kills = 0
        self.available_balls = 10
        self.over = False
        self.started = False

        # Ball Settings: 

        self.ball_type = 0
        self.total_balls = len(os.listdir('assets/ball')) - 1

        # Graphics Settings: 

        self.clouds = True
        self.effects = True

        # Level Settings: 

        self.level = level
        self.next_level = False
        self.level_difficulty = 0
        self.level_reset_timer = 0

        # Difficulty: 

        self.game_difficulty = 1000
        self.difficulty_multiplier = 2

        # Enemy Spawn Settings: 

        self.enemy_timer = 3000
        self.last_enemy = pygame.time.get_ticks()
        self.enemies_alive = 0
        self.random_enemy = 0

        # Sprite Groups: 

        self.cannon_balls = pygame.sprite.Group()
        self.game_enemies = pygame.sprite.Group()
        self.game_towers = pygame.sprite.Group()

        # Tower Positions: 

        self.tower_positionss = []

    def clear_window(self):
        self.display.fill((0, 0, 0))

    def start_window(self):
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.FULLSCREEN)
        pygame.display.set_caption("Fort Defender: ")

        self.tower_positionss = [
            [self.screen_width - (self.screen_width // 7), (self.screen_height // 3) + (self.screen_height // 2)],
            [self.screen_width - (self.screen_width // 5), (self.screen_height // 3) + (self.screen_height // 2)],
        ]

        self.game_font = pygame.font.Font(os.getcwd() + '/game_font.ttf', self.screen_width // 20)

    def draw_balls(self, particles):
        self.cannon_balls.update(particles, self.screen_width, self.screen_height)
        self.cannon_balls.draw(self.display)

    def set_game_icon(self, path):
        icon = pygame.image.load(path).convert_alpha()
        pygame.display.set_icon(icon)

    def load_game_enemies(self, enemy_types, animation_types, enemy_health):
        enemy_animations = []
        for enemy in enemy_types:
            animation_list = []
            for animation in animation_types:
                temp_list = []
                sprite_frames = len(os.listdir(f'assets/tanks/{enemy}/{animation}'))
                for i in range(sprite_frames):
                    image = pygame.image.load(f'assets/tanks/{enemy}/{animation}/{i}.png').convert_alpha()
                    enemy_width = self.display.get_width() // 4
                    enemy_height = self.display.get_height() // 2
                    image = pygame.transform.scale(image, (int(enemy_width * 0.25), int(enemy_height * 0.20)))
                    temp_list.append(image)
                animation_list.append(temp_list)
            enemy_animations.append(animation_list)
        return enemy_animations, enemy_types, enemy_health

    def toggle_mouse_cursor_on(self):
        pygame.mouse.set_visible(True)

    def toggle_mouse_cursor_off(self):
        pygame.mouse.set_visible(False)

    def draw_text(self, text, size, color, x, y):
        text_image = pygame.font.SysFont('Impact', size).render(text, True, color)
        self.display.blit(text_image, (x, y))

    def load_game_image(self, path, width, height):
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (width, height))
        return image

    def load_game_sound(self, path, volume):
        sound = pygame.mixer.Sound(path)
        sound.set_volume(volume)
        return sound

    def destroy_game(self):
        pygame.quit()
        quit()

    def update_display(self, fps):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.engine_running = False

        self.fps_handler.tick(fps)
        pygame.display.update()

    def update_game_balls(self, particles, ball_type):
        self.cannon_balls.update(particles)
        self.cannon_balls.draw(self.display)
        self.ball_type = ball_type

    def update_game_towers(self, fort, sounds):
        self.game_towers.update(fort, sounds)
        
    def update_game_enemies(self, particles, fort, sounds):
        self.game_enemies.update(self, particles, fort, sounds)
        self.game_enemies.draw(self.display)

    def update_game_mechanics(self, fort, enemy_animations, enemy_types, enemy_health):
        if(self.level_difficulty < self.game_difficulty):
            if(pygame.time.get_ticks() - self.last_enemy > self.enemy_timer):
                if(len(enemy_types) == 1):
                    self.random_enemy = 0

                if(self.level.current_level == 1):
                    self.random_enemy = 0
                elif(self.level.current_level == 2):
                    self.random_enemy = random.randint(0, len(enemy_types) - 3)
                else:
                    self.random_enemy = random.randint(0, len(enemy_types) - 1)

                self.last_enemy = pygame.time.get_ticks()

                game_enemy = Enemy(enemy_health[self.random_enemy], enemy_animations[self.random_enemy], 0 - (self.screen_width // 8), self.screen_height - self.screen_height // 8, (self.screen_width // 100) // 8)
                self.game_enemies.add(game_enemy)
                self.level_difficulty += enemy_health[self.random_enemy]

        if(self.level_difficulty >= self.game_difficulty):
            self.enemies_alive = 0
            for enemy in self.game_enemies:
                if enemy.alive == True:
                    self.enemies_alive += 1

            if(self.enemies_alive == 0 and self.next_level == False):
                self.next_level = True
                self.level_reset_timer = pygame.time.get_ticks()

        if(self.next_level == True):
            text_size = 1 * (self.screen_height // 24)
            self.draw_text('LEVEL COMPLETE', text_size, (120, 244, 20), self.screen_width // 3 + self.screen_width // 9, self.screen_height // 2)
            if(pygame.time.get_ticks() - self.level_reset_timer > 1500):
                self.next_level = False
                self.level.current_level += 1
                self.last_enemy = pygame.time.get_ticks()
                self.game_difficulty *= self.difficulty_multiplier
                self.level_difficulty = 0
                self.game_enemies.empty()
                self.coins += 1000

        if(fort.health <= 0):
            self.game_over = True

    def reset_game(self, fort, background):
        text_size = 1 * (self.screen_height // 24)
        self.draw_text('GAME OVER', text_size, (204, 0, 0), self.screen_width // 3 + self.screen_width // 9, self.screen_height // 2)
        self.draw_text('PRESS "SPACE" TO RESTART', text_size, (204, 0, 0), self.screen_width // 3 + self.screen_width // 22, self.screen_height // 4)
        self.toggle_mouse_cursor_on()

        if(pygame.key.get_pressed()[pygame.K_SPACE]):
            self.over = False
            self.kills = 0
            self.coins = 5000
            self.available_balls = 10
            self.level.current_level = 1
            self.game_difficulty = 1000
            self.level_difficulty = 0
            self.last_enemy = pygame.time.get_ticks()
            self.game_enemies.empty()
            self.game_towers.empty()
            fort.health = 1000
            fort.upgrades = 0
            fort.max_health = 1000
            fort.current_balls = 8
            background.current_time = pygame.time.get_ticks()
            background.cycle_timer = 1000
            background.cycle = 0 
            background.night = False
            background.sky_color = [135, 206, 255]
            self.toggle_mouse_cursor_off()
