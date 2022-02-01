# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
from pygame import mixer
import math
import random

# Pygame & Mixer Initializations: #

pygame.init()
mixer.init()

# Global Variables: #

# Window:

windowWidth = 0
windowHeight = 0

# Main Menu:

mainMenu = True

# Level: #

gameLevel = 1
nextLevel = False
levelDifficulty = 0
levelResetTime = 0

# Difficulty:

gameDifficulty = 1000
difficultyMultiplier = 2

# Enemy:

enemyTimer = 2000
lastEnemy = pygame.time.get_ticks()
enemiesAlive = 0
randomEnemy = 0

# Game State:

gameOver = False

# Balls:

availableBalls = 10

# Day & Night Cycle:
currentTime = pygame.time.get_ticks()
cycleTimer = 1000
cycle = 0
day = None

# Default Background Color:

red = 135
green = 206
blue = 255

# Tower Spawn Positions: #

towerPositions = [
[600, 440],
[400, 445],
]

# Particles:

fortParticles = []
enemyParticles = []
grassParticles = []
smokeParticles = []
moveParticles = []

# Sprite Groups: #

cannonBalls = pygame.sprite.Group()
gameEnemies = pygame.sprite.Group()
gameTowers = pygame.sprite.Group()

# Engine Functions: #

def updateTime():
	global currentTime
	global cycleTimer
	global cycle
	if(pygame.time.get_ticks() - currentTime >= cycleTimer):
		cycle += 1
		currentTime = pygame.time.get_ticks()

def circleSurface(radius : int, color : tuple):
	surface = pygame.Surface((radius * 2, radius * 2))
	pygame.draw.circle(surface, color, (radius, radius), radius)
	surface.set_colorkey((0, 0, 0))
	return surface

def addFortParticle(x : int, y : int):
	global fortParticles
	fortParticles.append([[x - 150, y + 150], [random.randint(0, 3) / 2 - 1, -0.5], random.randint(16, 24)])

def addGrassParticle(x : int, y : int):
	global grassParticles
	grassParticles.append([[x, y], [random.randint(0, 10) / 10 - 1, -2], random.randint(4, 6)])

def addSmokeParticle(x : int, y : int):
	global smokeParticles
	smokeParticles.append([[x + 10, y + 40], [random.randint(0, 5) / 3 - 1, -1], random.randint(1, 3)])

def addMoveParticle(x : int, y : int):
	global moveParticles
	moveParticles.append([[x + 10, y + 60], [-1, -1], random.randint(1, 2)])

def addEnemyParticle(x : int, y : int):
	global enemyParticles
	enemyParticles.append([[x + 30, y + 30], [random.randint(0, 20) / 10 - 1, -2], random.randint(8, 10)])

def drawFortParticles(engineWindow : pygame.Surface, color : tuple):
	global fortParticles
	for particle in fortParticles:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		particle[2] -= 0.1
		pygame.draw.circle(engineWindow, color, [int(particle[0][1]), int(particle[0][0])], int(particle[2]))

		if(particle[2] <= 0):
			fortParticles.remove(particle)

def drawEnemyParticles(engineWindow : pygame.Surface, color : tuple):
	global enemyParticles
	for particle in enemyParticles:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		particle[2] -= 0.1
		pygame.draw.circle(engineWindow, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
		radius = particle[2] * 2
		engineWindow.blit(circleSurface(radius, color), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
		if(particle[2] <= 0):
			enemyParticles.remove(particle)

def drawSmokeParticles(engineWindow : pygame.Surface, color : tuple):
	global smokeParticles
	for particle in smokeParticles:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		particle[2] -= 0.1
		pygame.draw.circle(engineWindow, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
		radius = particle[2] * 2
		engineWindow.blit(circleSurface(radius, color), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
		if(particle[2] <= 0):
			smokeParticles.remove(particle)

def drawMoveParticles(engineWindow : pygame.Surface, color : tuple):
	global moveParticles
	for particle in moveParticles:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		particle[2] -= 0.1
		pygame.draw.circle(engineWindow, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
		radius = particle[2] * 2
		engineWindow.blit(circleSurface(radius, color), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
		if(particle[2] <= 0):
			moveParticles.remove(particle)

def drawGrassParticles(engineWindow : pygame.Surface, color : tuple):
	global grassParticles
	for particle in grassParticles:
		particle[0][0] += particle[1][0]
		particle[0][1] += particle[1][1]
		particle[2] -= 0.1
		pygame.draw.circle(engineWindow, color, [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
		radius = particle[2] * 2
		engineWindow.blit(circleSurface(radius, (51, 25, 0)), (int(particle[0][0] - radius), int(particle[0][1] - radius)), special_flags = pygame.BLEND_RGB_ADD)
		if(particle[2] <= 0):
			grassParticles.remove(particle)

def toggleMouseCursorOn():
	pygame.mouse.set_visible(True)

def toggleMouseCursorOff():
	pygame.mouse.set_visible(False)

def setGameIcon(path : str):
	icon = pygame.image.load(path)
	pygame.display.set_icon(icon)

def playMusic(path : str, volume : int):
	pygame.mixer.music.load(path)
	pygame.mixer.music.set_volume(volume)
	pygame.mixer.music.play(-1, 0.0, 5000)

def loadGameSound(path : str, volume : float):
	sound = pygame.mixer.Sound(path)
	sound.set_volume(volume)
	return sound

def changeSpawnTimer(newSpawnTimer : int):
	global enemyTimer
	enemyTimer = newSpawnTimer

def changeGameDifficulty(newLevelDifficulty : int, newGameDifficulty : int, newDifficultyMultiplier : int):
	global levelDifficulty
	global gameDifficulty
	global difficultyMultiplier
	levelDifficulty = newLevelDifficulty
	gameDifficulty = newGameDifficulty
	newDifficultyMultiplier = newDifficultyMultiplier

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path).convert_alpha()
		image = pygame.transform.scale(image, (width, height))
		return image

def updateGameTowers(engineWindow : pygame.Surface, fort : pygame.Surface, ballSprite : pygame.Surface):
	global gameEnemies
	gameTowers.update(engineWindow, fort, gameEnemies, ballSprite)
	gameTowers.draw(engineWindow)

def updateGameMechanics(engineWindow : pygame.Surface, fort : pygame.Surface, enemyAnimations : list, enemyTypes : list, enemyHealth : list, sound : mixer.Sound):
		global levelDifficulty
		global gameDifficulty
		global lastEnemy
		global randomEnemy
		global nextLevel
		global gameLevel
		global levelResetTime
		global availableBalls
		cannonBalls.update(windowWidth, windowHeight)
		cannonBalls.draw(engineWindow)
		gameEnemies.update(engineWindow, fort, sound)
		gameEnemies.draw(engineWindow)
		if(levelDifficulty < gameDifficulty):
			if(pygame.time.get_ticks() - lastEnemy > enemyTimer):
				if(gameLevel == 1):
					randomEnemy = random.randint(0, len(enemyTypes) - 3)
				elif(gameLevel == 2):
					randomEnemy = random.randint(0, len(enemyTypes) - 2)
				else:
					randomEnemy = random.randint(0, len(enemyTypes) - 1)
				lastEnemy = pygame.time.get_ticks()
				gameEnemy = Enemy(enemyHealth[randomEnemy], enemyAnimations[randomEnemy], -100, 525, 1)
				gameEnemies.add(gameEnemy)
				levelDifficulty += enemyHealth[randomEnemy]
		if(levelDifficulty >= gameDifficulty):
			enemiesAlive = 0
			for enemy in gameEnemies:
				if enemy.alive == True:
					enemiesAlive += 1
			if(enemiesAlive == 0 and nextLevel == False):
				nextLevel = True
				levelResetTime = pygame.time.get_ticks()

		if(nextLevel == True):
			drawText(engineWindow, 'LEVEL COMPLETE', 50, (120, 244, 20), 240, 200)
			if(pygame.time.get_ticks() - levelResetTime > 1500):
				nextLevel = False
				gameLevel += 1
				lastEnemy = pygame.time.get_ticks()
				gameDifficulty *= difficultyMultiplier
				levelDifficulty = 0
				gameEnemies.empty()
				fort.coins += 1000
		if(fort.health <= 0):
			gameOver = True

def loadGameEnemies(enemyTypes : list, anims : list):
	enemyAnimations = []
	enemyTypes = enemyTypes
	animationTypes = anims

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
	return enemyAnimations, enemyTypes

def assignEnemyHealth(enemyHealth : list):
	return enemyHealth

def drawText(engineWindow : pygame.Surface, text : str, size : int, color : tuple, x : int, y : int):
    textImage = pygame.font.SysFont('Impact', size).render(text, True, color)
    engineWindow.blit(textImage, (x, y))

def showStats(engineWindow : pygame.Surface, fort : pygame.Surface):
	drawText(engineWindow, 'Coins: ' + str(fort.coins), 20, (255, 255, 255), 10, 10)
	drawText(engineWindow, 'Cannon Balls: ' + str(availableBalls), 20, (255, 255, 255), 10, 60)
	drawText(engineWindow, 'Score: ' + str(fort.kills), 20, (255, 255, 255), 180, 10)
	drawText(engineWindow, 'Level: ' + str(gameLevel), 20, (255, 255, 255), 400, 10)
	drawText(engineWindow, 'Health: ' + str(fort.health) + "/" + str(fort.maxHealth), 18, (255, 255, 255), 585, 225)
	drawText(engineWindow, '500c', 16, (255, 255, 255), 660, 42)
	drawText(engineWindow, '250c (3b)', 16, (255, 255, 255), 482, 42)
	drawText(engineWindow, '1,000c', 16, (255, 255, 255), 650, 112)
	drawText(engineWindow, '2,000c (Max: 2)', 16, (255, 255, 255), 600, 183)

def resetGame(engineWindow : pygame.Surface, fort : pygame.Surface):
	global gameOver
	global level
	global gameDifficulty
	global levelDifficulty
	global lastEnemy
	global gameEnemies
	global gameTowers
	global availableBalls
	drawText(engineWindow, 'GAME OVER', 50, (204, 0, 0), 280, 200)
	drawText(engineWindow, 'PRESS "SPACE" TO RESTART', 30, (204, 0, 0), 235, 250)
	pygame.mouse.set_visible(True)
	key = pygame.key.get_pressed()
	if(key[pygame.K_SPACE]):
		gameOver = False
		level = 1
		gameDifficulty = 1000
		levelDifficulty = 0
		lastEnemy = pygame.time.get_ticks()
		gameEnemies.empty()
		gameTowers.empty()
		fort.score = 0
		fort.health = 1000
		fort.coins = 0
		availableBalls = 10
		pygame.mouse.set_visible(False)
		return gameOver

# Engine Window: #

class Window():
	def __init__(self, screenWidth : int, screenHeight : int, windowTitle : str):
		global windowWidth, windowHeight
		windowWidth = screenWidth
		windowHeight = screenHeight
		self.screenWidth = screenWidth
		self.screenHeight = screenHeight
		self.engineRunning = False
		self.windowTitle = windowTitle
		self.fpsLimit = pygame.time.Clock()
	
	def init(self):
		global day
		self.engineWindow = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption(self.windowTitle)
		self.engineRunning = True
		day = False

	def quit(self):
		pygame.quit()

	def updateDisplay(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.engineRunning = False
		pygame.display.update()

	def limitFPS(self, fps : int):
		self.fpsLimit.tick(fps)

	def setGameBackground(self):
		global cycle
		global day
		global red, green, blue
		if(day == False):
			red = 135 - cycle
			if(red < 0):
				red = 0
			green = 206 - cycle
			if(green < 0):
				green = 0
			blue = 255 - cycle
			if(blue <= 0):
				blue = 0
				cycle = 0
				day = True

		if(day == True):
			red = 35 + cycle
			green = 26 + cycle
			blue = 30 + cycle
			if(red >= 135):
				red = 135
			if(green >= 206):
				green = 206
			if(blue >= 255):
				blue = 255
			if(red == 135 and green == 206 and blue == 255):
				cycle = 0
				day = False

		color = (red, green, blue)
		self.engineWindow.fill((color))

	def setBackground(self, background : pygame.Surface, x : int, y : int):
		self.engineWindow.blit(background, (x, y))

# Game Fort: #

class Fort():
    def __init__(self, firstImage : pygame.Surface, secondImage : pygame.Surface, thirdImage : pygame.Surface, x : int, y : int, health : int, coins : int):
        self.health = health
        self.maxHealth = self.health
        self.alreadyFired = False
        self.coins = coins
        self.kills = 0
        self.firstImage = firstImage
        self.secondImage = secondImage
        self.thirdImage = thirdImage
        self.image = firstImage
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def fireBall(self, ballSprite : pygame.Surface, sound : mixer.Sound):
        global availableBalls
        position = pygame.mouse.get_pos()
        xDistance = (position[0] - self.rect.midleft[0])
        yDistance = -(position[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(yDistance, xDistance))
        if (pygame.mouse.get_pressed()[0] and self.alreadyFired == False and position[0] <= 500 and position[1] > 100 and availableBalls > 0):
            ball = Ball(ballSprite, self.rect.midleft[0] + 30, self.rect.midleft[1] - 25, self.angle)
            cannonBalls.add(ball)
            self.alreadyFired = True
            availableBalls -= 1
            sound.play()
            addFortParticle(self.rect.midleft[0] + 30, self.rect.midleft[1] - 25)
        if (pygame.mouse.get_pressed()[0] == False):
            self.alreadyFired = False


    def drawFort(self, engineWindow : pygame.Surface):
        if(self.health <= 250):
            self.image = self.thirdImage
        elif(self.health <= 500):
            self.image = self.secondImage
        else:
            self.image = self.firstImage
        engineWindow.blit(self.image, self.rect)

    def repairFort(self, sound : mixer.Sound):
        if(self.coins >= 500 and self.health < self.maxHealth):
            self.health += 250
            self.coins -= 500
            if (self.health > self.maxHealth):
                self.health = self.maxHealth
            sound.play()

    def upgradeArmour(self, sound : mixer.Sound):
        if(self.coins >= 1000):
            self.maxHealth += 500
            self.coins -= 1000
            sound.play()

    def addBullets(self, sound : mixer.Sound):
    	global availableBalls
    	availableBalls += 5
    	sound.play()


# Cannon Ball: #

class Ball(pygame.sprite.Sprite):
    def __init__(self, image : pygame.Surface, x : int, y : int, angle : int):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 5
        self.deltaX = math.cos(self.angle) * self.speed
        self.deltaY = -(math.sin(self.angle)) * self.speed


    def update(self, screenWidth : int, screenHeight : int):
        if(self.rect.right < 0 or self.rect.left > screenWidth or self.rect.bottom < 0 or self.rect.top > screenHeight):
            self.kill()

        if(self.rect.bottom > screenHeight - 20):
        	addGrassParticle(self.rect.x, self.rect.y)
        	self.kill()

        self.rect.x += self.deltaX
        self.rect.y += self.deltaY

# Crosshair: #

class Crosshair():
    def __init__(self, image : pygame.Surface):
        self.crosshair = image
        self.rect = self.crosshair.get_rect()
        pygame.mouse.set_visible(False)
        
    def drawCrosshair(self, engineWindow : pygame.Surface):
        position = pygame.mouse.get_pos()
        self.rect.center = (position[0], position[1])
        engineWindow.blit(self.crosshair, self.rect)

# Enemy: #

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health : int, animationList : pygame.Surface, x : int, y : int, speed : int):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.lastAttack = pygame.time.get_ticks()
        self.attackCooldown = 2000
        self.animationList = animationList
        self.frameIndex = 0
        self.action = 0
        self.updateTime = pygame.time.get_ticks()
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self, engineWindow : pygame.Surface, fort : pygame.Surface, sound : mixer.Sound):
        global availableBalls
        if(self.alive):
            if(pygame.sprite.spritecollide(self, cannonBalls, True)):
                self.health -= 25
                addEnemyParticle(self.rect.x, self.rect.y)

            if(self.rect.right > fort.rect.left):
                self.updateAction(1)

            if(self.action == 0):
                self.rect.x += self.speed
                addMoveParticle(self.rect.x, self.rect.y)

            if(self.action == 1):
                if(pygame.time.get_ticks() - self.lastAttack > self.attackCooldown):
                    fort.health -= 50
                    if(fort.health < 0):
                        fort.health = 0
                    self.lastAttack = pygame.time.get_ticks()   

            if(self.health <= 0):
                fort.coins += 50
                fort.kills += 1
                availableBalls += 3
                self.updateAction(2)
                self.alive = False
                sound.play()

        self.updateAnimation()
        addSmokeParticle(self.rect.x, self.rect.y)
        engineWindow.blit(self.image, (self.rect.x, self.rect.y))

    def updateAnimation(self):
        animationTime = 100
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

# Buttons: #

class Button():
    def __init__(self, x : int, y : int, image : pygame.Surface):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def drawButton(self, engineWindow : pygame.Surface):
        action = False
        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if(pygame.mouse.get_pressed()[0] == 1 and self.clicked == False):
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        engineWindow.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Towers: #

class Tower(pygame.sprite.Sprite):
    def __init__(self, firstImage : pygame.Surface, secondImage : pygame.Surface, thirdImage : pygame.Surface, x : int, y : int):
        pygame.sprite.Sprite.__init__(self)
        self.ready = False
        self.angle = 0
        self.lastShot = pygame.time.get_ticks()
        self.image = firstImage
        self.firstImage = firstImage
        self.secondImage = secondImage
        self.thirdImage = thirdImage
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self, engineWindow : pygame.Surface, fort : pygame.Surface, gameEnemies : pygame.sprite.Group, ballSprite : pygame.Surface):
        self.ready = False
        for enemy in gameEnemies:
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
                ball = Ball(ballSprite, self.rect.midleft[0], self.rect.midleft[1]-50, self.angle)
                cannonBalls.add(ball)

        if(fort.health <= 250):
            self.image = self.thirdImage
        elif(fort.health <= 500):
            self.image = self.secondImage
        else:
            self.image = self.firstImage
        engineWindow.blit(self.image, self.rect)

# Fade In: 

class Fade():
	def __init__(self, direction : int, color : tuple, speed : int):
		self.direction = direction
		self.color = color
		self.speed = speed
		self.fadeCounter = 0

	def fade(self, engineWindow : pygame.Surface, screenWidth : int, screenHeight : int):
		fadeCompleted = False
		self.fadeCounter += self.speed
		if(self.direction == 1):
			pygame.draw.rect(engineWindow, self.color, (0 - self.fadeCounter, 0, screenWidth // 2, screenHeight))
			pygame.draw.rect(engineWindow, self.color, (screenWidth // 2 + self.fadeCounter, 0, screenWidth, screenHeight))
			pygame.draw.rect(engineWindow, self.color, (0, 0 - self.fadeCounter, screenWidth, screenHeight // 2))
			pygame.draw.rect(engineWindow, self.color, (0, screenHeight // 2 + self.fadeCounter, screenWidth, screenHeight))
		if(self.direction == 2):
			pygame.draw.rect(engineWindow, self.color, (0, 0, screenWidth, 0 + self.fadeCounter))
		
		if(self.fadeCounter >= screenWidth):
			fadeCompleted = True
		return fadeCompleted