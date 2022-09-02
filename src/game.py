# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.modules import *
from src.enemy import *

# Game: #

class Game():
	def __init__(self, level):

		# Display:

		self.screenWidth = 1920
		self.screenHeight = 1080
		self.engineRunning = True
		self.fpsHandler = pygame.time.Clock()
		self.display = pygame.Surface

		# Game Settings: 

		self.coins = 5000
		self.kills = 0
		self.availableBalls = 10
		self.over = False
		self.started = False

		# Ball Settings: 

		self.ballType = 0
		self.totalBalls = len(os.listdir('assets/ball')) - 1

		# Graphics Settings: 

		self.clouds = True
		self.effects = True

		# Level Settings: 

		self.level = level
		self.nextLevel = False
		self.levelDifficulty = 0
		self.levelResetTime = 0

		# Difficulty: 

		self.gameDifficulty = 1000
		self.difficultyMultiplier = 2

		# Enemy Spawn Settings: 

		self.enemyTimer = 3000
		self.lastEnemy = pygame.time.get_ticks()
		self.enemiesAlive = 0
		self.randomEnemy = 0


		# Sprite Groups: 

		self.cannonBalls = pygame.sprite.Group()
		self.gameEnemies = pygame.sprite.Group()
		self.gameTowers = pygame.sprite.Group()

		# Tower Positions: 

		self.towerPositions = []


	def clearWindow(self):
		self.display.fill((0, 0, 0))

	def startWindow(self):
		self.display = pygame.display.set_mode((self.screenWidth, self.screenHeight), pygame.FULLSCREEN)
		pygame.display.set_caption("Fort Defender: ")

		self.towerPositions = [
			[self.screenWidth - (self.screenWidth // 7), (self.screenHeight // 3) + (self.screenHeight // 2)],
			[self.screenWidth - (self.screenWidth // 5), (self.screenHeight // 3) + (self.screenHeight // 2)],
		]

	def drawBalls(self, particles):
		self.cannonBalls.update(particles, self.display.get_width(), self.display.get_height())
		self.cannonBalls.draw(self.display)

	def setGameIcon(self, path : str):
		icon = pygame.image.load(path).convert_alpha()
		pygame.display.set_icon(icon)

	def loadGameEnemies(self, enemyTypes : list, animationTypes : list, enemyHealth : list):
		enemyAnimations = []

		for enemy in enemyTypes:

		    animationList = []

		    for animation in animationTypes:

		        tempList = []
		        spriteFrames = len(os.listdir(f'assets/tanks/{enemy}/{animation}'))

		        for i in range(spriteFrames):

		            image = pygame.image.load(f'assets/tanks/{enemy}/{animation}/{i}.png').convert_alpha()
		            enemyWidth = self.display.get_width() // 4
		            enemyHeight = self.display.get_height() // 2
		            image = pygame.transform.scale(image, (int(enemyWidth * 0.25), int(enemyHeight * 0.20)))
		            tempList.append(image)

		        animationList.append(tempList)

		    enemyAnimations.append(animationList)

		return enemyAnimations, enemyTypes, enemyHealth

	def toggleMouseCursorOn(self):
		pygame.mouse.set_visible(True)

	def toggleMouseCursorOff(self):
		pygame.mouse.set_visible(False)

	def drawText(self, text : str, size : int, color : tuple, x : int, y : int):
	    textImage = pygame.font.SysFont('Impact', size).render(text, True, color)
	    self.display.blit(textImage, (x, y))

	def loadGameImage(self, path : str, width : int, height : int):
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image, (width, height))
		return image

	def loadGameSound(self, path : str, volume : float):
		sound = pygame.mixer.Sound(path)
		sound.set_volume(volume)
		return sound

	def destroyGame(self):
		pygame.quit()

	def updateDisplay(self, fps : int):
		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.engineRunning = False

		self.fpsHandler.tick(fps)
		pygame.display.update()

	def updateGameBalls(self, particles, ballType : int):
		self.cannonBalls.update(particles, self.display.get_width(), self.display.get_height())
		self.cannonBalls.draw(self.display)
		self.ballType = ballType

	def updateGameTowers(self, fort):
		self.gameTowers.update(fort)
		
	def updateGameEnemies(self, particles, fort, soundStatus : bool, sound : mixer.Sound):
		self.gameEnemies.update(self, particles, fort, soundStatus, sound)
		self.gameEnemies.draw(self.display)

	def updateGameMechanics(self, fort, enemyAnimations : list, enemyTypes : list, enemyHealth : list):
		if(self.levelDifficulty < self.gameDifficulty):
			
			if(pygame.time.get_ticks() - self.lastEnemy > self.enemyTimer):

				if(len(enemyTypes) == 1):

					self.randomEnemy = 0

				if(self.level.currentLevel == 1):

					self.randomEnemy = 0

				elif(self.level.currentLevel == 2):

					self.randomEnemy = random.randint(0, len(enemyTypes) - 3)

				else:

					self.randomEnemy = random.randint(0, len(enemyTypes) - 1)

				self.lastEnemy = pygame.time.get_ticks()

				gameEnemy = Enemy(enemyHealth[self.randomEnemy], enemyAnimations[self.randomEnemy], 0 - (self.screenWidth // 8), self.screenHeight - self.screenHeight // 8, (self.screenWidth // 100) // 8)
				self.gameEnemies.add(gameEnemy)

				self.levelDifficulty += enemyHealth[self.randomEnemy]

		if(self.levelDifficulty >= self.gameDifficulty):

			self.enemiesAlive = 0

			for enemy in self.gameEnemies:

				if enemy.alive == True:

					self.enemiesAlive += 1

			if(self.enemiesAlive == 0 and self.nextLevel == False):

				self.nextLevel = True
				self.levelResetTime = pygame.time.get_ticks()

		if(self.nextLevel == True):
			textSize = 1 * (self.screenHeight // 24)
			self.drawText('LEVEL COMPLETE', textSize, (120, 244, 20), self.screenWidth // 3 + self.screenWidth // 9, self.screenHeight // 2)

			if(pygame.time.get_ticks() - self.levelResetTime > 1500):

				self.nextLevel = False
				self.level.currentLevel += 1
				self.lastEnemy = pygame.time.get_ticks()
				self.gameDifficulty *= self.difficultyMultiplier
				self.levelDifficulty = 0
				self.gameEnemies.empty()
				self.coins += 1000

		if(fort.health <= 0):

			self.gameOver = True

	def resetGame(self, fort):
		textSize = 1 * (self.screenHeight // 24)
		self.drawText('GAME OVER', textSize, (204, 0, 0), self.screenWidth // 3 + self.screenWidth // 9, self.screenHeight // 2)
		self.drawText('PRESS "SPACE" TO RESTART', textSize, (204, 0, 0), self.screenWidth // 3 + self.screenWidth // 22, self.screenHeight // 4)
		self.toggleMouseCursorOn()

		if(pygame.key.get_pressed()[pygame.K_SPACE]):

			self.over = False
			self.kills = 0
			self.coins = 5000
			self.availableBalls = 10
			self.level.currentLevel = 1
			self.gameDifficulty = 1000
			self.levelDifficulty = 0
			self.lastEnemy = pygame.time.get_ticks()
			self.gameEnemies.empty()
			self.gameTowers.empty()
			fort.health = 1000
			fort.upgrades = 0
			fort.maxHealth = 1000
			fort.currentBalls = 8
			self.toggleMouseCursorOff()
