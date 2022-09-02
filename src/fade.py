# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Fade In: #

class Fade():
	def __init__(self, display : pygame.Surface, direction : int, color : tuple, speed : int):

		# Display: 

		self.display = display

		# Fade Settings: 

		self.direction = direction
		self.color = color
		self.speed = speed
		self.fadeCounter = 0

	def fade(self, screenWidth : int, screenHeight : int):
		fadeCompleted = False
		self.fadeCounter += self.speed

		if(self.direction == 1):

			pygame.draw.rect(self.display, self.color, (0 - self.fadeCounter, 0, screenWidth // 2, screenHeight))
			pygame.draw.rect(self.display, self.color, (screenWidth // 2 + self.fadeCounter, 0, screenWidth, screenHeight))
			pygame.draw.rect(self.display, self.color, (0, 0 - self.fadeCounter, screenWidth, screenHeight // 2))
			pygame.draw.rect(self.display, self.color, (0, screenHeight // 2 + self.fadeCounter, screenWidth, screenHeight))

		if(self.direction == 2):

			pygame.draw.rect(self.display, self.color, (0, 0, screenWidth, 0 + self.fadeCounter))
		
		if(self.fadeCounter >= screenWidth):
			fadeCompleted = True

		return fadeCompleted