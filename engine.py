# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
	import pygame 
	import math
	import random
	from pygame import mixer

except ImportError:
	raise ImportError("The Defender Engine couldn't import all of the necessary packages.")

# Pygame & Mixer Initializations: #

pygame.init()
mixer.init()

# Display: #

screenWidth = 800
screenHeight = 600

window = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Fort Defender: ")

# Engine Functions: #

def loadGameEnemies(enemyTypes : list, animationTypes : list, enemyHealth : list):
	enemyAnimations = []

	for enemy in enemyTypes:

	    animationList = []

	    for animation in animationTypes:

	        tempList = []
	        spriteFrames = 5

	        for i in range(spriteFrames):

	            image = pygame.image.load(f'assets/{enemy}/{animation}/{i}.png').convert_alpha()
	            enemyWidth = image.get_width()
	            enemyHeight = image.get_height()
	            image = pygame.transform.scale(image, (int(enemyWidth * 0.15), int(enemyHeight * 0.15)))
	            tempList.append(image)

	        animationList.append(tempList)

	    enemyAnimations.append(animationList)

	return enemyAnimations, enemyTypes, enemyHealth

def toggleMouseCursorOn():
	pygame.mouse.set_visible(True)

def toggleMouseCursorOff():
	pygame.mouse.set_visible(False)

def playMusic(path : str, volume : int):
	pygame.mixer.music.load(path)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play(-1, 0.0, 5000)

def stopMusic():
	pygame.mixer.music.stop()

def drawText(engineWindow : pygame.Surface, text : str, size : int, color : tuple, x : int, y : int):
    textImage = pygame.font.SysFont('Impact', size).render(text, True, color)
    engineWindow.blit(textImage, (x, y))

def loadGameSound(path : str, volume : float):
	sound = pygame.mixer.Sound(path)
	sound.set_volume(volume)
	return sound

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image, (width, height))
		return image

def destroyGame():
	pygame.quit()
	quit()

# Fort: #

class Fort():
	def __init__(self, game, x : int, y : int, health : int):

    	# Game: 

		self.game = game

    	# Fort Settings: 

		self.health = health
		self.maxHealth = self.health
		self.alreadyFired = False

        # Fort Sprites: 

		self.firstImage = loadGameImage('assets/Fort/Fort.png', 300, 300)
		self.secondImage = loadGameImage('assets/Fort/Fort_Damaged.png', 300, 300)
		self.thirdImage = loadGameImage('assets/Fort/Fort_Heavily_Damaged.png', 300, 300)
		self.image = self.firstImage

        # Fort Rectangle: 

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y

	def fireBall(self, particles, soundStatus : bool, sound : mixer.Sound):
		position = pygame.mouse.get_pos()
		xDistance = (position[0] - self.rect.midleft[0])
		yDistance = -(position[1] - self.rect.midleft[1])
		self.angle = math.degrees(math.atan2(yDistance, xDistance))

		if(pygame.mouse.get_pressed()[0] and self.alreadyFired == False and position[0] <= 500 and position[1] > 100 and self.game.availableBalls > 0):

			ball = Ball(self.rect.midleft[0] + 30, self.rect.midleft[1] - 25, self.angle)

			self.game.cannonBalls.add(ball)

			self.alreadyFired = True
			self.game.availableBalls -= 1

			if(soundStatus):

				sound.play()

			particles.addGameParticle("fort",  self.rect.midleft[0] + 30, self.rect.midleft[1] - 25)

		if(pygame.mouse.get_pressed()[0] == False):

			self.alreadyFired = False


	def drawFort(self):
		if(self.health <= 250):

			self.image = self.thirdImage

		elif(self.health <= 500):

			self.image = self.secondImage

		else:

			self.image = self.firstImage

		self.game.display.blit(self.image, self.rect)

	def repairFort(self, soundStatus, success : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 500 and self.health < self.maxHealth):

			self.health += 250
			self.game.coins -= 500

			if(self.health > self.maxHealth):

				self.health = self.maxHealth

			if(soundStatus):

				sound.play()

		else:

			error.play()

	def upgradeArmour(self, soundStatus : bool, sound : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 1000):

			self.maxHealth += 500
			self.game.coins -= 1000

			if(soundStatus):

				sound.play()

		else:

			error.play()

	def addBullets(self, soundStatus : bool, sound : mixer.Sound, error : mixer.Sound):
		if(self.game.coins >= 250):

				self.game.availableBalls += 5
				self.game.coins -= 250

				if(soundStatus):
					sound.play()

		else:

			error.play()

# Enemy: #

class Enemy(pygame.sprite.Sprite):
	def __init__(self, health : int, animationList : pygame.Surface, x : int, y : int, speed : int):
		pygame.sprite.Sprite.__init__(self)

		# Enemy Settings:

		self.alive = True
		self.speed = speed
		self.health = health

		# Enemy Attack: 

		self.lastAttack = pygame.time.get_ticks()
		self.attackCooldown = 2000

		# Enemy Animations: 

		self.animationList = animationList
		self.frameIndex = 0
		self.action = 0

		# Enemy Timer: 

		self.updateTime = pygame.time.get_ticks()

		# Enemy Sprite:

		self.image = self.animationList[self.action][self.frameIndex]

		# Enemy Rectangle:

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y


	def update(self, game, particles, fort, soundStatus : bool, sound : mixer.Sound):
		if(self.alive):

			if(pygame.sprite.spritecollide(self, game.cannonBalls, True)):

				self.health -= 25
				particles.addGameParticle("enemy", self.rect.x, self.rect.y)

			if(self.rect.right > fort.rect.left):

				self.updateAction(1)

			if(self.action == 0):

				self.rect.x += self.speed
				particles.addGameParticle("move", self.rect.x, self.rect.y)

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
		particles.addGameParticle("smoke", self.rect.x, self.rect.y)
		game.display.blit(self.image, (self.rect.x, self.rect.y))

	def updateAnimation(self):
		animationTime = 50
		self.image = self.animationList[self.action][self.frameIndex]

		if (pygame.time.get_ticks() - self.updateTime > animationTime):

			self.updateTime = pygame.time.get_ticks()
			self.frameIndex += 1

		if(self.frameIndex >= len(self.animationList[self.action])):

			if(self.action == 2):

				self.frameIndex = len(self.animationList[self.action]) - 1
				self.kill()

			else:

				self.frameIndex = 0

	def updateAction(self, newAction : int):
		if(newAction != self.action):

			self.action = newAction
			self.frameIndex = 0
			self.updateTime = pygame.time.get_ticks()


# Cannon Ball: #

class Ball(pygame.sprite.Sprite):
	def __init__(self, x : int, y : int, angle : int):
		pygame.sprite.Sprite.__init__(self)

		# Ball Sprite: 

		self.image = loadGameImage('assets/Ball/Ball.png', 16, 16)

		# Ball Rectangle: 

		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		# Ball Angle: 

		self.angle = math.radians(angle)

		# Ball Speed: 

		self.speed = 10

		# Ball Direction: 

		self.deltaX = math.cos(self.angle) * self.speed
		self.deltaY = -(math.sin(self.angle)) * self.speed

	def update(self, particles, screenWidth : int, screenHeight : int):
		if(self.rect.right < 0 or self.rect.left > screenWidth or self.rect.bottom < 0 or self.rect.top > screenHeight):
			self.kill()

		if(self.rect.bottom > screenHeight - 20):
			particles.addGameParticle("grass", self.rect.x, self.rect.y)
			self.kill()

		self.rect.x += self.deltaX
		self.rect.y += self.deltaY

# Towers: #

class Tower(pygame.sprite.Sprite):
	def __init__(self, x : int, y : int):
		pygame.sprite.Sprite.__init__(self)

		# Tower Settings:

		self.ready = False
		self.angle = 0
		self.lastShot = pygame.time.get_ticks()

		# Tower Sprites: 

		self.firstImage = loadGameImage('assets/Towers/Tower.png', 128, 128)
		self.secondImage = loadGameImage('assets/Towers/Tower_Damaged.png', 128, 128)
		self.thirdImage = loadGameImage('assets/Towers/Tower_Heavily_Damaged.png', 128, 128)
		self.image = self.firstImage

		# Tower Rectangle: 

		self.rect = self.image.get_rect()
		self.rect.x = x 
		self.rect.y = y

	def update(self, game, fort):
		self.ready = False

		for enemy in game.gameEnemies:

			if(enemy.alive):

				targetX, targetY = enemy.rect.midbottom
				self.ready = True
				break

		if(self.ready):

			xDistance = (targetX - self.rect.midleft[0])
			yDistance = -(targetY - self.rect.midleft[1])
			self.angle = math.degrees(math.atan2(yDistance, xDistance))
			shotCooldown = 1000

			if(pygame.time.get_ticks() - self.lastShot > shotCooldown):

				self.lastShot = pygame.time.get_ticks()
				ball = Ball(self.rect.midleft[0], self.rect.midleft[1] - 50, self.angle)
				game.cannonBalls.add(ball)

		if(fort.health <= 250):

			self.image = self.thirdImage

		elif(fort.health <= 500):

			self.image = self.secondImage

		else:

			self.image = self.firstImage
		game.display.blit(self.image, self.rect)

# Crosshair: #

class Crosshair():
	def __init__(self, display : pygame.Surface):

		# Display: 

		self.display = display

		# Crosshair Sprite: 

		self.crosshair = loadGameImage('assets/Crosshair/Crosshair.png', 32, 32)

		# Crosshair Rectangle: 

		self.rect = self.crosshair.get_rect()
        
	def drawCrosshair(self):
		position = pygame.mouse.get_pos()
		self.rect.center = (position[0], position[1])
		self.display.blit(self.crosshair, self.rect)

# Background: #

class Background():
	def __init__(self, display : pygame.Surface):
		self.display = display
		self.currentTime = pygame.time.get_ticks()
		self.cycleTimer = 1000
		self.cycle = 0 
		self.night = False
		self.skyColor = [135, 206, 255]

	def setGameBackground(self):
		if(self.night == False):

			self.skyColor[0] = 135 - self.cycle

			if(self.skyColor[0] < 0):

				self.skyColor[0] = 0

			self.skyColor[1] = 206 - self.cycle

			if(self.skyColor[1] < 0):

				self.skyColor[1] = 0

			self.skyColor[2] = 255 - self.cycle

			if(self.skyColor[2] <= 0):

				self.skyColor[2] = 0
				self.cycle = 0
				self.night = True

		if(self.night == True):

			self.skyColor[0] = 35 + self.cycle
			self.skyColor[1] = 26 + self.cycle
			self.skyColor[2] = 30 + self.cycle

			if(self.skyColor[0] >= 135):

				self.skyColor[0] = 135

			if(self.skyColor[1] >= 206):

				self.skyColor[1] = 206

			if(self.skyColor[2] >= 255):

				self.skyColor[2] = 255

			if(self.skyColor[0] == 135 and self.skyColor[1] == 206 and self.skyColor[2] == 255):

				self.cycle = 0
				self.night = False

		color = (self.skyColor[0], self.skyColor[1], self.skyColor[2])
		self.display.fill((color))

	def setLevelDesign(self, design : pygame.Surface, x : int, y : int):
		self.display.blit(design, (x, y))

	def updateTime(self):
		if(pygame.time.get_ticks() - self.currentTime >= self.cycleTimer):

			self.cycle += 1
			self.currentTime = pygame.time.get_ticks()

# Menu: #

class Menu():
	def __init__(self, display : pygame.Surface):

		# Display:

		self.display = display

		# Menu: 

		self.menuStatus = True

		# Buttons:

		self.buttonStart = Button(self.display, 200, 100, loadGameImage('assets/Buttons/start.png', 439, 158))
		self.buttonQuit = Button(self.display, 200, 300, loadGameImage('assets/Buttons/exit.png', 439, 158))
		self.buttonMusic = Button(self.display, self.display.get_width() // 2 + 50, self.display.get_height() // 2 + 300, loadGameImage('assets/Buttons/musicOn.png', 32, 32))
		self.buttonSound = Button(self.display, self.display.get_width() // 2 - 50, self.display.get_height() // 2 + 300, loadGameImage('assets/Buttons/soundOn.png', 32, 32))

	def handleMenu(self, musicStatus : bool, soundStatus : bool):
		if(self.menuStatus):

			self.display.blit(loadGameImage('assets/Background_2.png', 800, 600), (0, 0))

			if(musicStatus):

				self.buttonMusic = Button(self.display, 10, 20, loadGameImage('assets/Buttons/musicOn.png', 32, 32))

			else:

				self.buttonMusic = Button(self.display, 10, 20, loadGameImage('assets/Buttons/musicOff.png', 32, 32))

			if(soundStatus):

				self.buttonSound = Button(self.display, 10, 60, loadGameImage('assets/Buttons/soundOn.png', 32, 32))

			else:

				self.buttonSound = Button(self.display, 10, 60, loadGameImage('assets/Buttons/soundOff.png', 32, 32))

	def checkMenu(self):

		if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.menuStatus == False):

			self.menuStatus = True
			toggleMouseCursorOn()


# User Interface: #

class UserInterface():
	def __init__(self, display : pygame.Surface, game):
		self.display = display
		self.game = game
		self.buttonRepair = Button(self.display, 700, 10, loadGameImage('assets/Buttons/Repair.png', 64, 64))
		self.buttonArmour = Button(self.display, 700, 80, loadGameImage('assets/Buttons/Armour.png', 64, 64))
		self.buttonTower = Button(self.display, 700, 150,  loadGameImage('assets/Buttons/Tower_Button.png', 64, 64))
		self.buttonBullets = Button(self.display, 550, 10,  loadGameImage('assets/Buttons/Bullets.png', 64, 64))

	def showStats(self, fort, level : int):
		drawText(self.display, 'Coins: ' + str(self.game.coins), 20, (69, 69, 69), 10, 10)
		drawText(self.display, 'Cannon Balls: ' + str(self.game.availableBalls), 20, (69, 69, 69), 10, 60)
		drawText(self.display, 'Score: ' + str(self.game.kills), 20, (69, 69, 69), 180, 10)
		drawText(self.display, 'Level: ' + str(level), 20, (69, 69, 69), 400, 10)
		drawText(self.display, 'Health: ' + str(fort.health) + "/" + str(fort.maxHealth), 18, (69, 69, 69), 585, 225)
		drawText(self.display, '500c', 16, (69, 69, 69), 660, 42)
		drawText(self.display, '250c (5b)', 16, (69, 69, 69), 482, 42)
		drawText(self.display, '1,000c', 16, (69, 69, 69), 650, 112)
		drawText(self.display, '2,000c (Max: 2)', 16, (69, 69, 69), 600, 183)

# Buttons: #

class Button():
	def __init__(self, display : pygame.Surface, x : int, y : int, image : pygame.Surface):
		self.display = display
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def render(self):
		action = False
		position = pygame.mouse.get_pos()
		if self.rect.collidepoint(position):

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:

			self.clicked = False

		self.display.blit(self.image, (self.rect.x, self.rect.y))
		return action

# Levels: #

class Level():
	def __init__(self):

		# Level Settings:

		self.currentLevel = 1

# Game: #

class Game():
	def __init__(self, display : pygame.Surface, level):

		# Display: 

		self.display = display
		self.engineRunning = True
		self.fpsHandler = pygame.time.Clock()

		# Game Settings: 

		self.coins = 1000
		self.kills = 0
		self.availableBalls = 10
		self.over = False

		# Level Settings: 

		self.level = level
		self.nextLevel = False
		self.levelDifficulty = 0
		self.levelResetTime = 0

		# Difficulty: 

		self.gameDifficulty = 1000
		self.difficultyMultiplier = 2

		# Enemy Spawn Settings: 

		self.enemyTimer = 2000
		self.lastEnemy = pygame.time.get_ticks()
		self.enemiesAlive = 0
		self.randomEnemy = 0


		# Sprite Groups: 

		self.cannonBalls = pygame.sprite.Group()
		self.gameEnemies = pygame.sprite.Group()
		self.gameTowers = pygame.sprite.Group()

		# Tower Positions: 

		self.towerPositions = [
			[600, 440],
			[400, 445],
		]

	def clearWindow(self):
		self.display.fill((0, 0, 0))

	def drawBalls(self, particles):
		self.cannonBalls.update(particles, self.display.get_width(), self.display.get_height())
		self.cannonBalls.draw(self.display)

	def setGameIcon(self, path : str):
		icon = pygame.image.load(path).convert_alpha()
		pygame.display.set_icon(icon)

	def updateDisplay(self, fps : int):
		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.engineRunning = False

		self.fpsHandler.tick(fps)
		pygame.display.update()

	def updateGameBalls(self, particles):
		self.cannonBalls.update(particles, self.display.get_width(), self.display.get_height())
		self.cannonBalls.draw(self.display)

	def updateGameTowers(self, fort):
		self.gameTowers.update(self, fort)
		self.gameTowers.draw(self.display)
		
	def updateGameEnemies(self, particles, fort, soundStatus : bool, sound : mixer.Sound):
		self.gameEnemies.update(self, particles, fort, soundStatus, sound)
		self.gameEnemies.draw(self.display)

	def updateGameMechanics(self, fort, enemyAnimations : list, enemyTypes : list, enemyHealth : list):
		if(self.levelDifficulty < self.gameDifficulty):

			if(pygame.time.get_ticks() - self.lastEnemy > self.enemyTimer):

				if(self.level.currentLevel == 1):

					self.randomEnemy = random.randint(0, len(enemyTypes) - 3)

				elif(self.level.currentLevel == 2):

					self.randomEnemy = random.randint(0, len(enemyTypes) - 2)

				else:

					self.randomEnemy = random.randint(0, len(enemyTypes) - 1)

				self.lastEnemy = pygame.time.get_ticks()

				gameEnemy = Enemy(enemyHealth[self.randomEnemy], enemyAnimations[self.randomEnemy], -100, 525, 1)
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

			drawText(self.display, 'LEVEL COMPLETE', 50, (120, 244, 20), 240, 200)

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

# Fade In: 

class Fade():
	def __init__(self, display : pygame.Surface, direction : int, color : tuple, speed : int):

		# Display: 

		self.display = display

		# Fade Settings: 

		self.direction = direction
		self.color = color
		self.speed = speed
		self.fadeCounter = 0

	def fade(self, screenWidth : int, screenHeight : int):
		fadeCompleted = False
		self.fadeCounter += self.speed

		if(self.direction == 1):

			pygame.draw.rect(self.display, self.color, (0 - self.fadeCounter, 0, screenWidth // 2, screenHeight))
			pygame.draw.rect(self.display, self.color, (screenWidth // 2 + self.fadeCounter, 0, screenWidth, screenHeight))
			pygame.draw.rect(self.display, self.color, (0, 0 - self.fadeCounter, screenWidth, screenHeight // 2))
			pygame.draw.rect(self.display, self.color, (0, screenHeight // 2 + self.fadeCounter, screenWidth, screenHeight))

		if(self.direction == 2):

			pygame.draw.rect(self.display, self.color, (0, 0, screenWidth, 0 + self.fadeCounter))
		
		if(self.fadeCounter >= screenWidth):
			fadeCompleted = True

		return fadeCompleted

class Sounds():
	def __init__(self):

		# Music:

		self.musicStatus = False

		# Sounds: 

		self.soundStatus = True

		# Available Sounds: 

		self.shoot = loadGameSound('sounds/shoot.wav', 0.2)
		self.explosion = loadGameSound('sounds/explosion.mp3', 0.2)
		self.build = loadGameSound('sounds/build.mp3', 0.2)
		self.ballLoad = loadGameSound('sounds/ball_load.mp3', 0.2)
		self.error = loadGameSound('sounds/no.wav', 0.2)

	def playMusic(self):
		playMusic('sounds/music.mp3', 10)

class Particles():
	def __init__(self, display : pygame.Surface):

		# Display

		self.display = display

		# Particles: 

		self.fortParticles = []
		self.enemyParticles = []
		self.grassParticles = []
		self.smokeParticles = []
		self.moveParticles = []
		self.towerParticles = []

	def circleSurface(self, radius : int, color : tuple):
		surface = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surface, color, (radius, radius), radius)
		surface.set_colorkey((0, 0, 0))
		return surface

	def addGameParticle(self, particleType : str, x : int, y : int):
		particleType.lower()
		if(particleType == "fort"):

			self.fortParticles.append([[x - 150, y + 150], [random.randint(0, 3) / 2 - 1, -0.5], random.randint(16, 24)])

		elif(particleType == "enemy"):

			self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(8, 10)])

		elif(particleType == "smoke"):

			self.smokeParticles.append([[x + 10, y + 40], [random.randint(0, 5) / 3 - 1, -1], random.randint(1, 3)])

		elif(particleType == "move"):

			self.moveParticles.append([[x + 10, y + 60], [-1, -1], random.randint(1, 2)])

		elif(particleType == "grass"):

			self.grassParticles.append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(4, 6)])

		elif(particleType == "tower"):

			self.towerParticles.append([[x - 150, y + 150], [random.randint(0, 3) / 2 - 1, -0.5], random.randint(16, 24)])

		else:

			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawGameParticles(self, particleType : str):
		if(particleType == "fort"):

			for particle in self.fortParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (138, 134, 142), [int(particle[0][1]), int(particle[0][0])], int(particle[2]))
				
				if(particle[2] <= 0):

					self.fortParticles.remove(particle)

		elif(particleType == "enemy"):

			for particle in self.enemyParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (255, 165, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (255, 165, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.enemyParticles.remove(particle)

		elif(particleType == "smoke"):

			for particle in self.smokeParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (128, 128, 128), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (128, 128, 128)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.smokeParticles.remove(particle)

		elif(particleType == "move"):
			
			for particle in self.moveParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (25, 51, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (25, 51, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):

					self.moveParticles.remove(particle)

		elif(particleType == "grass"):

			for particle in self.grassParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (25, 51, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (51, 25, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):

					self.grassParticles.remove(particle)

		elif(particleType == "tower"):

			for particle in self.towerParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (138, 134, 142), [int(particle[0][1]), int(particle[0][0])], int(particle[2]))
				
				if(particle[2] <= 0):

					self.towerParticles.remove(particle)
		else:

			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def updateParticles(self):
		self.drawGameParticles("fort")
		self.drawGameParticles("enemy")
		self.drawGameParticles("grass")
		self.drawGameParticles("smoke") 
		self.drawGameParticles("move")
		self.drawGameParticles("tower")
