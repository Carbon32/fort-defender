# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.ball import *

# Towers: #

class Tower(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)

		# Game:

		self.game = game

		# Tower Settings:

		self.ready = False
		self.angle = 0
		self.lastShot = pygame.time.get_ticks()

		# Tower Sprites: 

		self.towerImages = [self.game.loadGameImage(f'assets/towers/{i}.png', self.game.display.get_width() // 12, self.game.display.get_height() // 8) for i in range(len(os.listdir('assets/towers')))]
		self.towerUpgrades = [self.game.loadGameImage(f'assets/tower_upgrades/{i}.png', self.game.display.get_width() // 12, self.game.display.get_height() // 8) for i in range(len(os.listdir('assets/tower_upgrades')))]
		self.image = self.towerImages[0]

		# Tower Rectangle: 

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y

	def update(self, fort):
		self.ready = False

		for enemy in self.game.gameEnemies:

			if(enemy.alive and enemy.rect.x > self.game.screenWidth // 2):

				targetX, targetY = enemy.rect.top, enemy.rect.bottom
				self.ready = True
				break

		if(self.ready):

			xDistance = (targetX - self.rect.midleft[0])
			yDistance = -(targetY - self.rect.midleft[1])
			self.angle = math.degrees(math.atan2(yDistance, xDistance))
			shotCooldown = 1000

			if(pygame.time.get_ticks() - self.lastShot > shotCooldown):

				self.lastShot = pygame.time.get_ticks()
				ball = Ball(self.game, self.rect.midleft[0], self.rect.midleft[1] - 50, self.angle, self.game.ballType)
				self.game.cannonBalls.add(ball)

		if(fort.health <= 250):

			self.image = self.towerImages[2]

		elif(fort.health <= 500):

			self.image = self.towerImages[1]

		else:

			self.image = self.towerImages[0]

		self.game.display.blit(self.image, self.rect)
		self.game.display.blit(self.towerUpgrades[fort.upgrades], self.rect)
