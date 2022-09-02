# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Background: #

class Background():
	def __init__(self, game : pygame.Surface):

		# Display:

		self.game = game

		# Settings:

		self.currentTime = pygame.time.get_ticks()
		self.cycleTimer = 1000
		self.cycle = 0 
		self.night = False
		self.skyColor = [135, 206, 255]

		# Background Design:

		self.gameBackground = pygame.Surface((self.game.screenWidth, self.game.screenHeight))
		self.backgroundDesign = self.game.loadGameImage('assets/background.png', self.game.screenWidth, self.game.screenHeight)

	def updateGameBackground(self):
		if(self.night == False):

			self.skyColor[0] = 135 - self.cycle

			if(self.skyColor[0] < 0):

				self.skyColor[0] = 0

			self.skyColor[1] = 206 - self.cycle

			if(self.skyColor[1] < 0):

				self.skyColor[1] = 0

			self.skyColor[2] = 255 - self.cycle

			if(self.skyColor[2] <= 0):

				self.skyColor[2] = 0
				self.cycle = 0
				self.night = True

		if(self.night == True):

			self.skyColor[0] = 35 + self.cycle
			self.skyColor[1] = 26 + self.cycle
			self.skyColor[2] = 30 + self.cycle

			if(self.skyColor[0] >= 135):

				self.skyColor[0] = 135

			if(self.skyColor[1] >= 206):

				self.skyColor[1] = 206

			if(self.skyColor[2] >= 255):

				self.skyColor[2] = 255

			if(self.skyColor[0] == 135 and self.skyColor[1] == 206 and self.skyColor[2] == 255):

				self.cycle = 0
				self.night = False

		self.gameBackground.fill((self.skyColor[0], self.skyColor[1], self.skyColor[2]))
		self.gameBackground.blit(self.backgroundDesign, (0, 0))

	def drawLevelDesign(self, x : int, y : int):
		self.game.display.blit(self.gameBackground, (x, y))

	def updateTime(self):
		if(pygame.time.get_ticks() - self.currentTime >= self.cycleTimer):

			self.cycle += 1
			self.currentTime = pygame.time.get_ticks()