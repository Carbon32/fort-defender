# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *

# Enemy: #

class Enemy(pygame.sprite.Sprite):
	def __init__(self, health : int, animationList : pygame.Surface, x : int, y : int, speed : int):
		pygame.sprite.Sprite.__init__(self)

		# Enemy Settings:

		self.alive = True
		self.speed = speed
		self.health = health
		self.maxHealth = health

		# Enemy Attack: 

		self.lastAttack = pygame.time.get_ticks()
		self.attackCooldown = 2000

		# Enemy Animations: 

		self.animationList = animationList
		self.frameIndex = 0
		self.action = 0

		# Enemy Timer: 

		self.updateTime = pygame.time.get_ticks()
		self.destroySprite = pygame.time.get_ticks()

		# Enemy Sprite:

		self.image = self.animationList[self.action][self.frameIndex]
		self.transparency = 255

		# Enemy Rectangle:

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def update(self, game, particles, fort, soundStatus : bool, sound : mixer.Sound):
		if(self.alive):

			if(pygame.sprite.spritecollide(self, game.cannonBalls, True)):

				if(game.ballType == 0):

					self.health -= 15

				if(game.ballType == 1):

					self.health -= 20

				else:

					self.health -= (20 * game.ballType)

				if(self.rect.x > 0):

					particles.addGameParticle("hit", self.rect.x, self.rect.y)

			if(self.rect.right > fort.rect.left):

				self.updateAction(1)

			if(self.action == 0):

				self.rect.x += self.speed

			if(self.action == 1):

				if(pygame.time.get_ticks() - self.lastAttack > self.attackCooldown):

					fort.health -= 50

					if(fort.health < 0):

						fort.health = 0

					self.lastAttack = pygame.time.get_ticks()   

			if(self.health <= 0):

				game.coins += 50
				game.kills += 1
				game.availableBalls += 3
				self.updateAction(2)
				self.alive = False

				if(soundStatus):

					sound.play()

		self.updateAnimation()

		if(self.rect.x > 0):

			if(self.alive):

				if(self.health > self.maxHealth // 2):

					particles.addGameParticle("white_smoke", self.rect.midleft[0] + 10, self.rect.midleft[1] - (self.rect.midleft[1] // 128))

				else:

					particles.addGameParticle("black_smoke", self.rect.midleft[0] + 10, self.rect.midleft[1] - (self.rect.midleft[1] // 128))
					particles.addGameParticle("small_hit", self.rect.midleft[0], self.rect.midleft[1] - (self.rect.midleft[1] // 64))


				pygame.draw.rect(game.display, (250, 0, 0), (self.rect.x, self.rect.y - (self.rect.h // 4), self.rect.w, 5))
				pygame.draw.rect(game.display, (0, 250, 0), (self.rect.x, self.rect.y - (self.rect.h // 4), self.rect.w * (self.health / self.maxHealth), 5))

			game.display.blit(self.image, (self.rect.x, self.rect.y))

	def updateAnimation(self):
		animationTime = 40
		self.image = self.animationList[self.action][self.frameIndex]

		if (pygame.time.get_ticks() - self.updateTime > animationTime):

			self.updateTime = pygame.time.get_ticks()
			self.frameIndex += 1

		if(self.frameIndex >= len(self.animationList[self.action])):

			if(self.action == 2):

				self.frameIndex = len(self.animationList[self.action]) - 1

			else:

				self.frameIndex = 0

	def updateAction(self, newAction : int):
		if(newAction != self.action):

			self.action = newAction
			self.frameIndex = 0
			self.updateTime = pygame.time.get_ticks()