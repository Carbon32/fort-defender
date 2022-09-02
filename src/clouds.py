# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Clouds: #

class Clouds():
	def __init__(self, game):

 		# Game: 

 		self.game = game

 		# Movement:

 		self.move = 1

 		# Clouds: 

 		self.clouds = [[0, 0, 0], 
 					   [1, game.screenWidth // 2, game.screenHeight // 2],
 					   [2, game.screenWidth // 6, game.screenHeight // 3],
 					   [3, game.screenWidth // 3, game.screenHeight // 6],
					   [4, 0, game.screenHeight // 2],
					   [5, game.screenWidth, game.screenHeight // 6],
					   [6, game.screenWidth, game.screenHeight // 3],
					   [7, game.screenWidth // 18, game.screenHeight // 4],
					   [8, game.screenWidth // 6, game.screenHeight // 6],
					   [9, game.screenWidth // 16, game.screenHeight // 8],
					   [10, game.screenWidth // 4, game.screenHeight // 10]
 		]

 		self.cloudSprites = [self.game.loadGameImage(f'assets/clouds/{cloud[0]}.png', self.game.screenWidth // 6, self.game.screenHeight // 12) for cloud in self.clouds]

	def handleClouds(self):

		if(self.game.clouds and self.game.started):

			for cloud in self.clouds:

				if(cloud[1] < self.game.screenWidth):

					self.move = (self.game.screenWidth // 100) // 8

				else:

					cloud[1] = 0 - (self.game.screenWidth // 2)
		 		
				cloud[1] += self.move
				self.game.display.blit(self.cloudSprites[cloud[0]], (cloud[1], cloud[2]))
