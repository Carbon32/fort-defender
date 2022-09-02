# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.game import *
from src.background import *
from src.ball import *
from src.button import *
from src.clouds import *
from src.crosshair import *
from src.enemy import *
from src.fade import *
from src.fort import *
from src.level import *
from src.menu import *
from src.particles import *
from src.sounds import *
from src.tower import *
from src.ui import *

# Game Resolution: #

class Resolution():
	def __init__(self, game):
		
		# Game: 

		self.game = game

		# Display:

		self.resolutionWindow = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Fort Defender: ")
		pygame.display.set_icon(self.game.loadGameImage('assets/icon.png', 32, 32))
		self.resolutionStatus = True

		# Background:

		self.background = self.game.loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.resolutionA = Button(self.resolutionWindow, 0, 0, self.game.loadGameImage('assets/resolution/D.png', 150, 150)) # 800 x 600
		self.resolutionB = Button(self.resolutionWindow, 150, 0, self.game.loadGameImage('assets/resolution/C.png', 150, 150)) # 1024 x 768
		self.resolutionC = Button(self.resolutionWindow, 0, 150, self.game.loadGameImage('assets/resolution/B.png', 150, 150)) # 1280 x 720
		self.resolutionD = Button(self.resolutionWindow, 150, 150, self.game.loadGameImage('assets/resolution/A.png', 150, 150)) # 1920 x 1080

	def updateBackground(self):
		self.resolutionWindow.fill((255, 255, 255))
		self.resolutionWindow.blit(self.background, (0, 0))

	def setResolution(self, screenWidth : int, screenHeight : int):
		self.game.screenWidth = screenWidth
		self.game.screenHeight = screenHeight
		self.resolutionStatus = False

	def updateWindow(self):
		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				self.game.destroyGame()
		pygame.display.update()


# Game Graphics: #

class Graphics():
	def __init__(self, game):
		
		# Game: 

		self.game = game

		# Display:

		self.graphicsWindows = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Fort Defender: ")
		pygame.display.set_icon(self.game.loadGameImage('assets/icon.png', 32, 32))
		self.graphicsStatus = True

		# Background:

		self.background = self.game.loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.effects = Button(self.graphicsWindows, 0, 0, self.game.loadGameImage('assets/graphics/AOn.png', 150, 150)) 
		self.clouds = Button(self.graphicsWindows, 150, 0, self.game.loadGameImage('assets/graphics/BOn.png', 150, 150))
		self.start = Button(self.graphicsWindows, 75, 250, self.game.loadGameImage('assets/graphics/start.png', 150, 150)) 

	def updateBackground(self):
		self.graphicsWindows.fill((255, 255, 255))
		self.graphicsWindows.blit(self.background, (0, 0))

	def setClouds(self):
		if(self.game.clouds):

			self.game.clouds = False

		else:

			self.game.clouds = True

	def setEffects(self):
		if(self.game.effects):

			self.game.effects = False

		else:

			self.game.effects = True

	def updateWindow(self):

		if(self.game.effects):

			self.effects.changeButton(self.game.loadGameImage('assets/graphics/AOn.png', 150, 150))

		else:

			self.effects.changeButton(self.game.loadGameImage('assets/graphics/AOff.png', 150, 150)) 

		if(self.game.clouds):

			self.clouds.changeButton(self.game.loadGameImage('assets/graphics/BOn.png', 150, 150)) 

		else:

			self.clouds.changeButton(self.game.loadGameImage('assets/graphics/BOff.png', 150, 150)) 

		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				self.game.destroyGame()
		pygame.display.update()

