# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Sounds: #

class Sounds():
	def __init__(self, game):

		# Game:

		self.game = game

		# Music:

		self.musicStatus = True

		# Sounds: 

		self.soundStatus = True

		# Available Sounds: 

		self.shoot = self.game.loadGameSound('sounds/shoot.wav', 0.2)
		self.explosion = self.game.loadGameSound('sounds/explosion.mp3', 0.2)
		self.build = self.game.loadGameSound('sounds/build.mp3', 0.2)
		self.ballLoad = self.game.loadGameSound('sounds/ball_load.mp3', 0.2)
		self.error = self.game.loadGameSound('sounds/no.wav', 0.2)


	def playMusic(self):
		pygame.mixer.music.load('sounds/music.mp3')
		pygame.mixer.music.set_volume(10)
		pygame.mixer.music.play(-1, 0.0, 5000)

	def stopMusic(self):
		pygame.mixer.music.stop()
