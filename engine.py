# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon              				  #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

import pygame
import math
import random

# Pygame Initialization: #

pygame.init()

# Global Variables: #

windowWidth = 0
windowHeight = 0
gameLevel = 1

# Sprite Groups: #

cannonBalls = pygame.sprite.Group()
gameEnemies = pygame.sprite.Group()
gameTowers = pygame.sprite.Group()

# Engine Functions: #

def loadGameImage(path : str, width : int, height : int):
		image = pygame.image.load(path)
		image = pygame.transform.scale(image, (width, height))
		return image

def updateGameMechanics(engineWindow : pygame.Surface, fort : pygame.Surface):
        cannonBalls.update(windowWidth, windowHeight)
        cannonBalls.draw(engineWindow)
        gameEnemies.update(engineWindow, fort)
        gameEnemies.draw(engineWindow)
        showStats(engineWindow, fort, gameLevel)

def loadGameEnemies(enemyTypes : list, enemyHP : list, anims : list):
	enemyAnimations = []
	enemyTypes = enemyTypes
	enemyHealth = enemyHP
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
	return enemyAnimations

def drawText(engineWindow : pygame.Surface, text : str, size : int, color : tuple, x : int, y : int):
    textImage = pygame.font.SysFont('Impact', size).render(text, True, color)
    engineWindow.blit(textImage, (x, y))

def showStats(engineWindow : pygame.Surface, fort : pygame.Surface, level : int):
    drawText(engineWindow, 'Coins: ' + str(fort.coins), 20, (0, 153, 0), 10, 10)
    drawText(engineWindow, 'Score: ' + str(fort.kills), 20, (0, 153, 0), 180, 10)
    drawText(engineWindow, 'Level: ' + str(level), 20, (0, 153, 0), 400, 10)
    drawText(engineWindow, 'Health: ' + str(fort.health) + "/" + str(fort.maxHealth), 18, (0, 153, 0), 585, 225)
   # drawText(engineWindow, '500', 20, (0, 153, 0), 715, 130)
   # drawText(engineWindow, '1000', 20, (0, 153, 0), 715, 210)
   # drawText(engineWindow, '2000', 20, (0, 153, 0), 715, 290)

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
		self.engineWindow = pygame.display.set_mode((self.screenWidth, self.screenHeight))
		pygame.display.set_caption(self.windowTitle)
		self.engineRunning = True

	def updateDisplay(self):
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				self.engineRunning = False
		pygame.display.update()

	def limitFPS(self, fps : int):
		self.fpsLimit.tick(fps)
	
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

    def fireBall(self, ballSprite : pygame.Surface):
        position = pygame.mouse.get_pos()
        xDistance = (position[0] - self.rect.midleft[0])
        yDistance = -(position[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(yDistance, xDistance))
        if (pygame.mouse.get_pressed()[0] and self.alreadyFired == False and position[0] <= 500 and position[1] > 100):
            ball = Ball(ballSprite, self.rect.midleft[0] + 30, self.rect.midleft[1] - 25, self.angle)
            cannonBalls.add(ball)
            self.alreadyFired = True
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

    def repairFort(self):
        if(self.coins >= 500 and self.health < self.maxHealth):
            self.health += 250
            self.coins -= 500
            if (self.health > self.maxHealth):
                self.health = self.maxHealth

    def upgradeArmour(self):
        if(self.coins >= 1000):
            self.maxHealth += 500
            self.coins -= 1000


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
        self.rect = pygame.Rect(0, 0, 65, 48)
        self.rect.x = x
        self.rect.y = y


    def update(self, engineWindow : pygame.Surface, fort : pygame.Surface):
        if(self.alive):
            if(pygame.sprite.spritecollide(self, cannonBalls, True)):
                self.health -= 25

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
                fort.coins += 50
                fort.kills += 1
                self.updateAction(2)
                self.alive = False

        self.updateAnimation()
        engineWindow.blit(self.image, (self.rect.x, self.rect.y - 16))

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

    def updateAction(self, newAction):
        if(newAction != self.action):
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()