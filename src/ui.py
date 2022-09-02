# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.button import *

# User Interface: #

class UserInterface():
	def __init__(self, game):

		# Game:

		self.game = game

		# Buttons:

		self.buttonRepair = Button(self.game.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 4, self.game.loadGameImage('assets/buttons/repair.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonArmour = Button(self.game.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 6, self.game.loadGameImage('assets/buttons/armour.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonTower = Button(self.game.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 12, self.game.loadGameImage('assets/buttons/tower.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonBalls = Button(self.game.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight - self.game.screenHeight// 2, self.game.loadGameImage('assets/buttons/addBalls.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonBallType = Button(self.game.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 3, self.game.loadGameImage('assets/buttons/ballType.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))

		# User Interface Container: 

		self.container = self.game.loadGameImage("assets/ui.png", self.game.screenWidth // 2, self.game.screenHeight - self.game.screenHeight // 3)

	def showStats(self, fort, level : int):
		textSize = 1 * (self.game.screenHeight // 54)

		self.game.display.blit(self.container, (self.game.screenWidth // 2, 0))

		self.game.drawText('Coins: ' + str(self.game.coins), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 4, 10)
		self.game.drawText('Cannon Balls: ' + str(fort.currentBalls) + "/" + str(self.game.availableBalls), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 3, 10)
		self.game.drawText('Score: ' + str(self.game.kills), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 14, 10)
		self.game.drawText('Level: ' + str(level), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 7, 10)
		self.game.drawText('500c', textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 11, self.game.screenHeight // 2 - self.game.screenHeight // 5)
		self.game.drawText('5,000c (' + str(self.game.ballType) + "/" + str(self.game.totalBalls) + ")", textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 7, self.game.screenHeight // 2 - self.game.screenHeight // 5 - self.game.screenHeight // 11)
		self.game.drawText('250c (5b)', textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 8, 5 * (self.game.screenHeight // 9))
		self.game.drawText('1,000c', textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 10, self.game.screenHeight // 2 - self.game.screenHeight // 8)
		self.game.drawText('2,000c (Max: 2)', textSize - 2, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 7, self.game.screenHeight // 2 - self.game.screenHeight // 24)
