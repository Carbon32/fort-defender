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
	import os
	from pygame import mixer

except ImportError:
	raise ImportError("The Defender Engine couldn't import all of the necessary packages.")

# Pygame Initialization: #

pygame.init()

# Mixer Initialization: #

pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()

# Engine Functions: #

def loadGameEnemies(display : pygame.Surface, enemyTypes : list, animationTypes : list, enemyHealth : list):
	enemyAnimations = []

	for enemy in enemyTypes:

	    animationList = []

	    for animation in animationTypes:

	        tempList = []
	        spriteFrames = len(os.listdir(f'assets/tanks/{enemy}/{animation}'))

	        for i in range(spriteFrames):

	            image = pygame.image.load(f'assets/tanks/{enemy}/{animation}/{i}.png').convert_alpha()
	            enemyWidth = display.get_width() // 4
	            enemyHeight = display.get_height() // 2
	            image = pygame.transform.scale(image, (int(enemyWidth * 0.25), int(enemyHeight * 0.20)))
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

		self.fortImages = [loadGameImage(f'assets/fort/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/fort')))]
		self.fortUpgrades = [loadGameImage(f'assets/upgrades/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/upgrades')))]
		self.construction = [loadGameImage(f'assets/construction/{i}.png', self.game.display.get_width() // 6, self.game.display.get_height() // 4) for i in range(len(os.listdir('assets/construction')))]
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
		drawText(self.game.display, '(' + str(self.health) + "/" + str(self.maxHealth) + ")", 1 * (self.game.screenHeight // 52), (69, 69, 69), self.game.screenWidth // 16, 10)

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


# Cannon Ball: #

class Ball(pygame.sprite.Sprite):
	def __init__(self, game, x : int, y : int, angle : int, ballType : int):
		pygame.sprite.Sprite.__init__(self)

		# Game: 

		self.game = game

		# Ball Sprite: 

		self.image = loadGameImage(f'assets/ball/{ballType}.png', self.game.screenWidth // 100, self.game.screenWidth // 100)

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

		self.towerImages = [loadGameImage(f'assets/towers/{i}.png', self.game.display.get_width() // 12, self.game.display.get_height() // 8) for i in range(len(os.listdir('assets/towers')))]
		self.towerUpgrades = [loadGameImage(f'assets/tower_upgrades/{i}.png', self.game.display.get_width() // 12, self.game.display.get_height() // 8) for i in range(len(os.listdir('assets/tower_upgrades')))]
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


# Crosshair: #

class Crosshair():
	def __init__(self, display : pygame.Surface):

		# Display: 

		self.display = display

		# Crosshair Sprite: 

		self.crosshair = loadGameImage('assets/crosshair/crosshair.png', 32, 32)

		# Crosshair Rectangle: 

		self.rect = self.crosshair.get_rect()
        
	def drawCrosshair(self):
		position = pygame.mouse.get_pos()
		self.rect.center = (position[0], position[1])
		self.display.blit(self.crosshair, self.rect)

# Background: #

class Background():
	def __init__(self, game : pygame.Surface):

		# Display:

		self.game = game

		# Settings:

		self.currentTime = pygame.time.get_ticks()
		self.cycleTimer = 1000
		self.cycle = 0 
		self.night = False
		self.skyColor = [135, 206, 255]

		# Background Design:

		self.gameBackground = pygame.Surface((self.game.screenWidth, self.game.screenHeight))
		self.backgroundDesign = loadGameImage('assets/background.png', self.game.screenWidth, self.game.screenHeight)

	def updateGameBackground(self):
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

		self.gameBackground.fill((self.skyColor[0], self.skyColor[1], self.skyColor[2]))
		self.gameBackground.blit(self.backgroundDesign, (0, 0))

	def drawLevelDesign(self, x : int, y : int):
		self.game.display.blit(self.gameBackground, (x, y))

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
		self.menuBackground = pygame.Surface((self.display.get_width(), self.display.get_height()))
		self.backgroundDesign = loadGameImage('assets/menu.png', self.display.get_width(), self.display.get_height())
		self.menuBackground.blit(self.backgroundDesign, (0, 0))

		# Buttons:

		self.buttonStart = Button(self.display, self.display.get_width() // 3, self.display.get_height() // 4, loadGameImage('assets/Buttons/start.png',  self.display.get_width() // 3 , self.display.get_height() // 5))
		self.buttonQuit = Button(self.display, self.display.get_width() // 3, self.display.get_height() // 2, loadGameImage('assets/Buttons/exit.png',  self.display.get_width() // 3, self.display.get_height() // 5))
		self.buttonMusic = Button(self.display, 10, 20, loadGameImage('assets/Buttons/musicOn.png', 32, 32))
		self.buttonSound = Button(self.display, 10, 80, loadGameImage('assets/Buttons/soundOn.png', 32, 32))

	def gameStarted(self):

		self.buttonStart.changeButton(loadGameImage('assets/Buttons/continue.png',  self.display.get_width() // 3 , self.display.get_height() // 5))

	def handleMenu(self, musicStatus : bool, soundStatus : bool):
		if(self.menuStatus):

			self.display.blit(self.menuBackground, (0, 0))

			if(musicStatus):

				self.buttonMusic.changeButton(loadGameImage('assets/buttons/musicOn.png', 32, 32))

			else:

				self.buttonMusic.changeButton(loadGameImage('assets/buttons/musicOff.png', 32, 32))

			if(soundStatus):

				self.buttonSound.changeButton(loadGameImage('assets/buttons/soundOn.png', 32, 32))

			else:

				self.buttonSound.changeButton(loadGameImage('assets/buttons/soundOff.png', 32, 32))

	def checkMenu(self):

		if(pygame.key.get_pressed()[pygame.K_ESCAPE] and self.menuStatus == False):

			self.menuStatus = True
			toggleMouseCursorOn()

# User Interface: #

class UserInterface():
	def __init__(self, game):

		# Display:

		self.display = game.display

		# Game:

		self.game = game

		# Buttons:

		self.buttonRepair = Button(self.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 4, loadGameImage('assets/buttons/repair.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonArmour = Button(self.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 6, loadGameImage('assets/buttons/armour.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonTower = Button(self.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 12, loadGameImage('assets/buttons/tower.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonBalls = Button(self.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight - self.game.screenHeight// 2, loadGameImage('assets/buttons/addBalls.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))
		self.buttonBallType = Button(self.display, self.game.screenWidth - self.game.screenWidth // 16, self.game.screenHeight // 2 - self.game.screenHeight // 3, loadGameImage('assets/buttons/ballType.png', int((self.game.screenWidth // 4) * 0.19), int((self.game.screenHeight // 2) * 0.17)))

		# User Interface Container: 

		self.container = loadGameImage("assets/ui.png", self.game.screenWidth // 2, self.game.screenHeight - self.game.screenHeight // 3)

	def showStats(self, fort, level : int):
		textSize = 1 * (self.game.screenHeight // 54)

		self.display.blit(self.container, (self.game.screenWidth // 2, 0))

		drawText(self.display, 'Coins: ' + str(self.game.coins), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 4, 10)
		drawText(self.display, 'Cannon Balls: ' + str(fort.currentBalls) + "/" + str(self.game.availableBalls), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 3, 10)
		drawText(self.display, 'Score: ' + str(self.game.kills), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 14, 10)
		drawText(self.display, 'Level: ' + str(level), textSize, (69, 69, 69), self.game.screenWidth // 2 + self.game.screenWidth // 7, 10)
		drawText(self.display, '500c', textSize, (69, 69, 69), self.game.screenWidth - self.display.get_width() // 11, self.game.screenHeight // 2 - self.game.screenHeight // 5)
		drawText(self.display, '5,000c (' + str(self.game.ballType) + "/" + str(self.game.totalBalls) + ")", textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 7, self.game.screenHeight // 2 - self.game.screenHeight // 5 - self.game.screenHeight // 11)
		drawText(self.display, '250c (5b)', textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 8, 5 * (self.game.screenHeight // 9))
		drawText(self.display, '1,000c', textSize, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 10, self.game.screenHeight // 2 - self.game.screenHeight // 8)
		drawText(self.display, '2,000c (Max: 2)', textSize - 2, (69, 69, 69), self.game.screenWidth - self.game.screenWidth // 7, self.game.screenHeight // 2 - self.game.screenHeight // 24)

# Buttons: #

class Button():
	def __init__(self, display : pygame.Surface, x : int, y : int, image : pygame.Surface):
		self.display = display
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.buttonCooldown = 100
		self.buttonTimer = pygame.time.get_ticks()

	def render(self):
		action = False
		position = pygame.mouse.get_pos()
		if self.rect.collidepoint(position):

			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:

				if(pygame.time.get_ticks() - self.buttonTimer >= self.buttonCooldown):

					action = True
					self.clicked = True
					self.buttonTimer = pygame.time.get_ticks()
			
		if pygame.mouse.get_pressed()[0] == 0:

			self.clicked = False

		self.display.blit(self.image, (self.rect.x, self.rect.y))
		return action

	def changeButton(self, image : pygame.Surface):

		self.image = image

# Levels: #

class Level():
	def __init__(self):

		# Level Settings:

		self.currentLevel = 1

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
			drawText(self.display, 'LEVEL COMPLETE', textSize, (120, 244, 20), self.screenWidth // 3 + self.screenWidth // 9, self.screenHeight // 2)

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
		drawText(self.display, 'GAME OVER', textSize, (204, 0, 0), self.screenWidth // 3 + self.screenWidth // 9, self.screenHeight // 2)
		drawText(self.display, 'PRESS "SPACE" TO RESTART', textSize, (204, 0, 0), self.screenWidth // 3 + self.screenWidth // 22, self.screenHeight // 4)
		toggleMouseCursorOn()

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
			toggleMouseCursorOff()

# Fade In: #

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

# Sounds: #

class Sounds():
	def __init__(self):

		# Music:

		self.musicStatus = True

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

# Game Particles: #

class Particles():
	def __init__(self, display : pygame.Surface):

		# Display

		self.display = display

		# Particles: 

		self.fortParticles = []
		self.enemyParticles = []
		self.groundParticles = []
		self.whiteSmokeParticles = []
		self.blackSmokeParticles = []
		self.towerParticles = []

	def circleSurface(self, radius : int, color : tuple):
		surface = pygame.Surface((radius * 2, radius * 2))
		pygame.draw.circle(surface, color, (radius, radius), radius)
		surface.set_colorkey((0, 0, 0))
		return surface

	def addGameParticle(self, particleType : str, x : int, y : int):
		particleType.lower()
		if(particleType == "fort_smoke"):

			self.fortParticles.append([[x, y], [random.randint(0, 3) / 2 - 1, -0.5], random.randint(16, 24)])

		elif(particleType == "hit"):

			if(self.display.get_height() == 720 or self.display.get_height() == 1080):

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(8, 10)])

			else:

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 6)])

		elif(particleType == "small_hit"):

			if(self.display.get_height() == 720 or self.display.get_height() == 1080):

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 10) / 10 - 1, -2], random.randint(2, 3)])

			else:

				self.enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(1, 2)])

		elif(particleType == "white_smoke"):

			self.whiteSmokeParticles.append([[x, y], [random.randint(0, 5) / 3 - 1, -1], random.randint(1, 3)])

		elif(particleType == "black_smoke"):

			self.blackSmokeParticles.append([[x, y], [random.randint(0, 5) / 3 - 1, -1], random.randint(3, 6)])

		elif(particleType == "ground_hit"):

			if(self.display.get_height() == 720 or self.display.get_height() == 1080):

				self.groundParticles.append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(4, 6)])

			else:

				self.groundParticles.append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(2, 4)])

		else:

			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def drawGameParticles(self, particleType : str):
		if(particleType == "fort_smoke"):

			for particle in self.fortParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (138, 134, 142), [int(particle[0][1]), int(particle[0][0])], int(particle[2]))
				
				if(particle[2] <= 0):

					self.fortParticles.remove(particle)

		elif(particleType == "hit"):

			for particle in self.enemyParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (255, 165, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (255, 165, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.enemyParticles.remove(particle)

		elif(particleType == "small_hit"):

			for particle in self.enemyParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (255, 165, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (255, 165, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.enemyParticles.remove(particle)

		elif(particleType == "white_smoke"):

			for particle in self.whiteSmokeParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (128, 128, 128), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (128, 128, 128)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.whiteSmokeParticles.remove(particle)

		elif(particleType == "black_smoke"):

			for particle in self.blackSmokeParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (0, 0, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (0, 0, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):
					self.blackSmokeParticles.remove(particle)


		elif(particleType == "ground_hit"):

			for particle in self.groundParticles:

				particle[0][0] += particle[1][0]
				particle[0][1] += particle[1][1]
				particle[2] -= 0.1
				pygame.draw.circle(self.display, (25, 51, 0), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
				radius = particle[2] * 2
				self.display.blit(self.circleSurface(radius, (51, 25, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
				
				if(particle[2] <= 0):

					self.groundParticles.remove(particle)
		else:

			print(f"Cannot find {particleType} in the game particles list. The particle won't be displayed.")

	def updateParticles(self, game):

		if(game.effects):

			self.drawGameParticles("fort_smoke")
			self.drawGameParticles("hit")
			self.drawGameParticles("ground_hit")
			self.drawGameParticles("white_smoke")
			self.drawGameParticles("black_smoke") 

# Game Resolution: #

class Resolution():
	def __init__(self, game):
		
		# Game: 

		self.game = game

		# Display:

		self.resolutionWindow = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Fort Defender: ")
		pygame.display.set_icon(loadGameImage('assets/icon.png', 32, 32))
		self.resolutionStatus = True

		# Background:

		self.background = loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.resolutionA = Button(self.resolutionWindow, 0, 0, loadGameImage('assets/resolution/D.png', 150, 150)) # 800 x 600
		self.resolutionB = Button(self.resolutionWindow, 150, 0, loadGameImage('assets/resolution/C.png', 150, 150)) # 1024 x 768
		self.resolutionC = Button(self.resolutionWindow, 0, 150, loadGameImage('assets/resolution/B.png', 150, 150)) # 1280 x 720
		self.resolutionD = Button(self.resolutionWindow, 150, 150, loadGameImage('assets/resolution/A.png', 150, 150)) # 1920 x 1080

	def updateBackground(self):
		self.resolutionWindow.fill((255, 255, 255))
		self.resolutionWindow.blit(self.background, (0, 0))

	def setResolution(self, screenWidth : int, screenHeight : int):
		self.game.screenWidth = screenWidth
		self.game.screenHeight = screenHeight
		self.resolutionStatus = False

	def updateWindow(self):
		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				destroyGame()
		pygame.display.update()


# Game Graphics: #

class Graphics():
	def __init__(self, game):
		
		# Game: 

		self.game = game

		# Display:

		self.graphicsWindows = pygame.display.set_mode((300, 400))
		pygame.display.set_caption("Fort Defender: ")
		pygame.display.set_icon(loadGameImage('assets/icon.png', 32, 32))
		self.graphicsStatus = True

		# Background:

		self.background = loadGameImage('assets/menu.png', 300, 400)

		# Buttons: 

		self.effects = Button(self.graphicsWindows, 0, 0, loadGameImage('assets/graphics/AOn.png', 150, 150)) 
		self.clouds = Button(self.graphicsWindows, 150, 0, loadGameImage('assets/graphics/BOn.png', 150, 150))
		self.start = Button(self.graphicsWindows, 75, 250, loadGameImage('assets/graphics/start.png', 150, 150)) 

	def updateBackground(self):
		self.graphicsWindows.fill((255, 255, 255))
		self.graphicsWindows.blit(self.background, (0, 0))

	def setClouds(self):
		if(self.game.clouds):

			self.game.clouds = False

		else:

			self.game.clouds = True

	def setEffects(self):
		if(self.game.effects):

			self.game.effects = False

		else:

			self.game.effects = True

	def updateWindow(self):

		if(self.game.effects):

			self.effects.changeButton(loadGameImage('assets/graphics/AOn.png', 150, 150))

		else:

			self.effects.changeButton(loadGameImage('assets/graphics/AOff.png', 150, 150)) 

		if(self.game.clouds):

			self.clouds.changeButton(loadGameImage('assets/graphics/BOn.png', 150, 150)) 

		else:

			self.clouds.changeButton(loadGameImage('assets/graphics/BOff.png', 150, 150)) 

		for event in pygame.event.get():

			if(event.type == pygame.QUIT):

				self.resolutionStatus = False
				destroyGame()
		pygame.display.update()


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

 		self.cloudSprites = [loadGameImage(f'assets/clouds/{cloud[0]}.png', self.game.screenWidth // 6, self.game.screenHeight // 12) for cloud in self.clouds]

	def handleClouds(self):

		if(self.game.clouds and self.game.started):

			for cloud in self.clouds:

				if(cloud[1] < self.game.screenWidth):

					self.move = (self.game.screenWidth // 100) // 8

				else:

					cloud[1] = 0 - (self.game.screenWidth // 2)
		 		
				cloud[1] += self.move
				self.game.display.blit(self.cloudSprites[cloud[0]], (cloud[1], cloud[2]))

