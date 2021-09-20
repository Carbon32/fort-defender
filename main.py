# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Fort Kruz, defender video game                              #
#                                   based in World War II                     #
#                                             Developer: Carbon               #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame
import math
import random

# Pygame Initialization: #

pygame.init()

# Game Window: #

screenWidth = 800
screenHeight = 600
gameRunning = True
gameWindow = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Fort Kruz:")

# Frames per second handler: #

handleFPS = pygame.time.Clock()

# Game Variables: #

gameLevel = 1
levelDifficulty = 0
gameDifficulty = 1000
enemyTimer = 2000
lastEnemy = pygame.time.get_ticks()
enemiesAlive = 0

# Assets loading: #

gameBackground = pygame.image.load('assets/Background.png').convert_alpha()
fortUndamaged = pygame.image.load('assets/Fort.png').convert_alpha()
fortDamaged = pygame.image.load('assets/Fort_Damaged.png').convert_alpha()
fortHeavilyDamaged = pygame.image.load('assets/Fort_Heavily_Damaged.png').convert_alpha()
cannonBall = pygame.image.load('assets/Ball.png').convert_alpha()
ballWidth = cannonBall.get_width()
ballHeight = cannonBall.get_height()
cannonBall = pygame.transform.scale(cannonBall, (int(ballWidth * 0.4), (int(ballHeight * 0.4))))
enemyAnimations = []
enemyTypes = ['Tank', 'Heavy',]
enemyHealth = [50, 100]
animationTypes = ['Move', 'Attack', 'Explosion']

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


# Game Classes: #

class Fort():
    def __init__(self, image, secondImage, thirdImage, x, y, scale):
        self.health = 1000
        self.maxHealth = self.health
        self.fired = False
        self.money = 0
        self.kills = 0
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.secondImage = pygame.transform.scale(secondImage, (int(width * scale), int(height * scale)))
        self.thirdImage = pygame.transform.scale(thirdImage, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def fireBall(self):
        position = pygame.mouse.get_pos()
        xDistance = (position[0] - self.rect.midleft[0])
        yDistance = -(position[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(yDistance, xDistance))
        if (pygame.mouse.get_pressed()[0] and self.fired == False):
            ball = Ball(cannonBall, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            cannonBalls.add(ball)
            self.fired = True
        if (pygame.mouse.get_pressed()[0] == False):
            self.fired = False


    def drawFort(self):
        if(self.health <= 250):
            self.image = self.thirdImage
        elif(self.health <= 500):
            self.image = self.secondImage
        else:
            self.image = self.image
        gameWindow.blit(self.image, self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)
        self.speed = 10
        self.deltaX = math.cos(self.angle) * self.speed
        self.deltaY = -(math.sin(self.angle) * self.speed)


    def update(self):
        if(self.rect.right < 0 or self.rect.left > screenWidth or self.rect.bottom < 0 or self.rect.top > screenHeight):
            self.kill()
        self.rect.x += self.deltaX
        self.rect.y += self.deltaY

class Crosshair():
    def __init__(self, scale):
        crosshair = pygame.image.load('assets/Crosshair.png')
        cWidth = crosshair.get_width()
        cHeight = crosshair.get_height()
        self.crosshair = pygame.transform.scale(crosshair, (int(cWidth * scale), (int(cHeight * scale))))
        self.rect = self.crosshair.get_rect()
        pygame.mouse.set_visible(False)
        
    def drawCrosshair(self):
        position = pygame.mouse.get_pos()
        self.rect.center = (position[0], position[1])
        gameWindow.blit(self.crosshair, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animationList, x, y, speed):
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


    def update(self):
        if(self.alive):
            if(pygame.sprite.spritecollide(self, cannonBalls, True)):
                self.health -= 25

            if(self.rect.right > fort.rect.left):
                self.updateAction(1)

            if(self.action == 0):
                self.rect.x += self.speed

            if(self.action == 1):
                if(pygame.time.get_ticks() - self.lastAttack > self.attackCooldown):
                    fort.health -= 25
                    if(fort.health < 0):
                        fort.health = 0
                    self.lastAttack = pygame.time.get_ticks()   

            if(self.health <= 0):
                fort.money += 50
                fort.kills += 1
                self.updateAction(2)
                self.alive = False

        self.updateAnimation()
        gameWindow.blit(self.image, (self.rect.x, self.rect.y - 16))

    def updateAnimation(self):
        animationTime = 100
        self.image = self.animationList[self.action][self.frameIndex]
        if (pygame.time.get_ticks() - self.updateTime > animationTime):
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
        if(self.frameIndex >= len(self.animationList[self.action])):
            if(self.action == 2):
                self.frameIndex = len(self.animationList[self.action]) - 1
                pass
            else:
                self.frameIndex = 0

    def updateAction(self, newAction):
        if(newAction != self.action):
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()


# Game Loop: #

fort = Fort(fortUndamaged, fortDamaged, fortHeavilyDamaged, 500, 235, 3) # Fort Creation
crosshair = Crosshair(1.5)
cannonBalls = pygame.sprite.Group()
gameEnemies = pygame.sprite.Group()

while gameRunning: 

    handleFPS.tick(60)
    gameWindow.blit(gameBackground, (0, 0))
    fort.drawFort()
    fort.fireBall()
    crosshair.drawCrosshair()
    cannonBalls.update()
    cannonBalls.draw(gameWindow)

    gameEnemies.update()
    if(levelDifficulty < gameDifficulty):
        if(pygame.time.get_ticks() - lastEnemy > enemyTimer):
            randomEnemy = random.randint(0, len(enemyTypes) - 1)
            gameEnemy = Enemy(enemyHealth[randomEnemy], enemyAnimations[randomEnemy], -100, 499, 1)
            print(randomEnemy)
            gameEnemies.add(gameEnemy)
            lastEnemy = pygame.time.get_ticks()
            levelDifficulty += enemyHealth[randomEnemy]

    # Events handler: #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
            
    pygame.display.update()
            
pygame.quit()