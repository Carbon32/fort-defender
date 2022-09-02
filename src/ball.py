# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Cannon Ball: #

class Ball(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, angle : int, ballType : int):
		pygame.sprite.Sprite.__init__(self)

		# Game: 

		self.game = game

		# Ball Sprite: 

		self.image = self.game.loadGameImage(f'assets/ball/{ballType}.png', self.game.screenWidth // 100, self.game.screenWidth // 100)

		# Ball Rectangle: 

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Ball Angle: 

		self.angle = math.radians(angle)

		# Ball Speed: 

		self.speed = self.game.screenWidth // 100

		# Ball Direction: 

		self.deltaX = math.cos(self.angle) * self.speed
		self.deltaY = -(math.sin(self.angle)) * self.speed

	def update(self, particles, screenWidth : int, screenHeight : int):
		if(self.rect.right < 0 or self.rect.left > screenWidth or self.rect.bottom < 0 or self.rect.top > screenHeight):
			self.kill()

		if(self.rect.bottom > screenHeight - 20):
			particles.addGameParticle("ground_hit", self.rect.x, self.rect.y)
			self.kill()

		self.rect.x += self.deltaX
		self.rect.y += self.deltaY