# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Crosshair: #

class Crosshair():
	def __init__(self, game : pygame.Surface):

		# Display: 

		self.game = game

		# Crosshair Sprite: 

		self.crosshair = self.game.loadGameImage('assets/crosshair/crosshair.png', 32, 32)

		# Crosshair Rectangle: 

		self.rect = self.crosshair.get_rect()
        
	def drawCrosshair(self):
		position = pygame.mouse.get_pos()
		self.rect.center = (position[0], position[1])
		self.game.display.blit(self.crosshair, self.rect)