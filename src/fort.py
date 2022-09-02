# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.ball import *

# Fort: #

class Fort():
	def __init__(self, game, x : int, y : int, health : int):

    	# Game: 

		self.game = game

    	# Fort Settings: 

		self.health = health
		self.maxHealth = self.health
		self.alreadyFired = False
		self.upgrades = 0
		self.reloadTime = 2000
		self.startReload = False
		self.timerReload = 0

        # Fort Sprites: 

		self.fortImages = [self.game.loadGameImage(f'assets/fort/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/fort')))]
		self.fortUpgrades = [self.game.loadGameImage(f'assets/upgrades/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/upgrades')))]
		self.construction = [self.game.loadGameImage(f'assets/construction/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/construction')))]
		self.image = self.fortImages[0]

		# Construction Settings:

		self.constructionStart = False
		self.constructionAnimations = 0
		self.constructionCurrentTime = pygame.time.get_ticks()
		self.constructionTimer = 500

		# Ball Settings:

		self.currentBalls = 8
		self.ballType = 0
		self.totalBalls = len(os.listdir('assets/ball')) - 1

        # Fort Rectangle: 

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

	def fireBall(self, particles, soundStatus : bool, sound : mixer.Sound):
		position = pygame.mouse.get_pos()
		xDistance = (position[0] - self.rect.midleft[0])
		yDistance = -(position[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(yDistance, xDistance))

		accuracy = random.randint(-5, 5)

		if(pygame.mouse.get_pressed()[0] and self.alreadyFired == False and self.currentBalls > 0 and position[0] < (self.game.screenWidth // 2) + (self.game.screenWidth // 3)):

			ball = Ball(self.game, self.rect.midleft[0] + 30, self.rect.midleft[1] - 25, self.angle + accuracy, self.ballType)

			self.game.cannonBalls.add(ball)

			self.alreadyFired = True
			self.currentBalls -= 1


			if(soundStatus):

				sound.play()

			if(self.game.screenWidth == 1280 or self.game.screenWidth == 1920):

				particles.addGameParticle("fort_smoke",  (self.rect.midleft[0] // 2) - (self.rect.midleft[1] // 12 - self.rect.midleft[1] // 6), self.rect.midleft[0]  + (self.rect.midleft[1] // 16))

			else:

				particles.addGameParticle("fort_smoke",  self.rect.midleft[0] - (self.rect.midleft[1] // 3), self.rect.midleft[0]  + (self.rect.midleft[1] // 16))

		if(pygame.mouse.get_pressed()[0] == False):

			self.alreadyFired = False

		if(self.startReload == False and self.currentBalls == 0):

			self.timerReload = pygame.time.get_ticks()
			self.startReload = True

		if(self.currentBalls == 0 and self.game.availableBalls >= 8):

			if(pygame.time.get_ticks() - self.timerReload > self.reloadTime):

				self.currentBalls = 8
				self.game.availableBalls -= 8
				self.startReload = False

		if(self.currentBalls == 0 and self.game.availableBalls >= 1):

			if(pygame.time.get_ticks() - self.timerReload > self.reloadTime):

				self.currentBalls = self.game.availableBalls
				self.game.availableBalls -= self.game.availableBalls
				self.startReload = False


	def drawFort(self):
		if(self.health <= 250):

			self.image = self.fortImages[2]

		elif(self.health <= 500):

			self.image = self.fortImages[1]

		else:

			self.image = self.fortImages[0]


		self.game.display.blit(self.image, self.rect)
		self.game.display.blit(self.fortUpgrades[self.upgrades], self.rect)
		self.game.display.blit(self.construction[self.constructionAnimations], self.rect)

		pygame.draw.rect(self.game.display, (250, 0, 0), (10, 10, self.rect.w, 24))
		pygame.draw.rect(self.game.display, (0, 250, 0), (10, 10, self.rect.w * (self.health / self.maxHealth), 24))
		pygame.draw.rect(self.game.display, (0, 0, 0), (10, 10, self.rect.w, 24), 2)
		self.game.drawText('(' + str(self.health) + "/" + str(self.maxHealth) + ")", 1 * (self.game.screenHeight // 52), (69, 69, 69), self.game.screenWidth // 16, 10)

		if(self.constructionStart):

			if(pygame.time.get_ticks() - self.constructionCurrentTime >= self.constructionTimer):

				self.constructionCurrentTime = pygame.time.get_ticks()

				if(self.constructionAnimations < len(self.construction) - 1):

					self.constructionAnimations += 1

				else:

					self.constructionStart = False
					self.constructionAnimations = 0

	def repairFort(self, soundStatus, sound : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 500 and self.health < self.maxHealth):

			self.health += 250
			self.game.coins -= 500

			if(self.health > self.maxHealth):

				self.health = self.maxHealth

			if(soundStatus):

				sound.play()

		else:

			error.play()

	def upgradeBalls(self, soundStatus : bool, sound : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 5000 and self.ballType != self.totalBalls):

				self.ballType += 1
				self.game.coins -= 5000

				if(soundStatus):
					sound.play()

		else:

			error.play()

	def upgradeArmour(self, soundStatus : bool, sound : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 1000 and not self.constructionStart):

			self.maxHealth += 500
			self.game.coins -= 1000
			self.constructionStart = True

			if(self.upgrades < 3):

				self.upgrades += 1

			else:

				self.upgrades = 3

			if(soundStatus):

				sound.play()

		else:

			error.play()

	def addBalls(self, soundStatus : bool, sound : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 250):

				self.game.availableBalls += 5
				self.game.coins -= 250

				if(soundStatus):
					sound.play()

		else:

			error.play()