# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# Menu: #

class Menu():
	def __init__(self, game : pygame.Surface):

		# Display:

		self.game = game

		# Menu: 

		self.menuStatus = True
		self.menuBackground = pygame.Surface((self.game.display.get_width(), self.game.display.get_height()))
		self.backgroundDesign = self.game.loadGameImage('assets/menu.png', self.game.display.get_width(), self.game.display.get_height())
		self.menuBackground.blit(self.backgroundDesign, (0, 0))

		# Buttons:

		self.buttonStart = Button(self.game.display, self.game.display.get_width() // 3, self.game.display.get_height() // 4, self.game.loadGameImage('assets/Buttons/start.png',  self.game.display.get_width() // 3 , self.game.display.get_height() // 5))
		self.buttonQuit = Button(self.game.display, self.game.display.get_width() // 3, self.game.display.get_height() // 2, self.game.loadGameImage('assets/Buttons/exit.png',  self.game.display.get_width() // 3, self.game.display.get_height() // 5))
		self.buttonMusic = Button(self.game.display, 10, 20, self.game.loadGameImage('assets/Buttons/musicOn.png', 32, 32))
		self.buttonSound = Button(self.game.display, 10, 80, self.game.loadGameImage('assets/Buttons/soundOn.png', 32, 32))

	def gameStarted(self):

		self.buttonStart.changeButton(self.game.loadGameImage('assets/Buttons/continue.png',  self.game.display.get_width() // 3 , self.game.display.get_height() // 5))

	def handleMenu(self, musicStatus : bool, soundStatus : bool):
		if(self.menuStatus):

			self.game.display.blit(self.menuBackground, (0, 0))

			if(musicStatus):

				self.buttonMusic.changeButton(self.game.loadGameImage('assets/buttons/musicOn.png', 32, 32))

			else:

				self.buttonMusic.changeButton(self.game.loadGameImage('assets/buttons/musicOff.png', 32, 32))

			if(soundStatus):

				self.buttonSound.changeButton(self.game.loadGameImage('assets/buttons/soundOn.png', 32, 32))

			else:

				self.buttonSound.changeButton(self.game.loadGameImage('assets/buttons/soundOff.png', 32, 32))

	def checkMenu(self):

		if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.menuStatus == False):

			self.menuStatus = True
			self.game.toggleMouseCursorOn()
