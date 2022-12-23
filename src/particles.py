# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Game Particles: #

class Particles():
    def __init__(self, game):

        # Display

        self.game = game

        # Particles: 

        self.particles = {
            'fort_smoke' : [],
            'hit' : [],
            'ground_hit' : [],
            'white_smoke' : [],
            'black_smoke' : []
        }


    def circle_surface(self, radius, color):
        surface = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surface, color, (radius, radius), radius)
        surface.set_colorkey((0, 0, 0))
        return surface

    def add_game_particle(self, particle_type, x, y):
        particle_type.lower()
        if(particle_type == "fort_smoke"):
            self.particles['fort_smoke'].append([[x, y], [random.randint(0, 3) / 2 - 1, -0.5], random.randint(self.game.screen_width // 120, self.game.screen_width // 80)])

        elif(particle_type == "hit"):
            self.particles['hit'].append([[x, y], [random.randint(0, 20) / 10 - 1, -2], random.randint(self.game.screen_width // 240, self.game.screen_width // 180)])

        elif(particle_type == "white_smoke"):
            self.particles['white_smoke'].append([[x, y], [random.randint(0, 5) / 3 - 1, -1], random.randint(self.game.screen_width // 576, self.game.screen_width // 512)])

        elif(particle_type == "black_smoke"):
            self.particles['black_smoke'].append([[x, y], [random.randint(0, 5) / 3 - 1, -1], random.randint(self.game.screen_width // 640, self.game.screen_width // 320)])

        elif(particle_type == "ground_hit"):
            self.particles['ground_hit'].append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(self.game.screen_width // 480, self.game.screen_width // 320)])


        else:
            print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

    def draw_game_particles(self, particle_type, oriented, lighting, first_color, second_color = (0, 0, 0)):
        try:
            for particle in self.particles[particle_type]:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.1
                if(oriented):
                    pygame.draw.circle(self.game.display, first_color, [int(particle[0][1]), int(particle[0][0])], int(particle[2]))
                else:
                    pygame.draw.circle(self.game.display, first_color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))

                if(lighting):
                    radius = particle[2] * 2
                    self.game.display.blit(self.circle_surface(radius, second_color), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)

                if(particle[2] <= 0):
                    self.particles[particle_type].remove(particle)
        except KeyError:
            print(f"Cannot find {particle_type} in the game particles list. The particle won't be displayed.")

    def update_particles(self, game):
        if(game.effects):
            self.draw_game_particles("fort_smoke", True, False, (192, 192, 192))
            self.draw_game_particles("hit", False, True, (255, 165, 0), (255, 165, 0))
            self.draw_game_particles("ground_hit", False, True, (25, 51, 0), (51, 25, 0))
            self.draw_game_particles("white_smoke", False, True, (128, 128, 128), (128, 128, 128))
            self.draw_game_particles("black_smoke", False, True, (0, 0, 0), (0, 0, 0)) 