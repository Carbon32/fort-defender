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

# Assets loading: #

gameBackground = pygame.image.load('assets/Background.png').convert_alpha()
fortUndamaged = pygame.image.load('assets/Fort.png').convert_alpha()
cannonBall = pygame.image.load('assets/Ball.png').convert_alpha()
ballWidth = cannonBall.get_width()
ballHeight = cannonBall.get_height()
cannonBall = pygame.transform.scale(cannonBall, (int(ballWidth * 0.4), (int(ballHeight * 0.4))))

enemyAnimations = []
enemyTypes = ['Tank']
enemyHealth = [100]
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
            image = pygame.transform.scale(image, (int(enemyWidth * 0.2), int(enemyHeight * 0.2)))
            tempList.append(image)
        animationList.append(tempList)
        enemyAnimations.append(animationList)

# Game Classes: #

class Fort():
    def __init__(self, image, x, y, scale):
        self.health = 1000
        self.maxHealth = self.health
        self.fired = False
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def fireBall(self):
        position = pygame.mouse.get_pos()
        xDistance = (position[0] - self.rect.midleft[0])
        yDistance = -(position[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(yDistance, xDistance))
        pygame.draw.line(gameWindow, (255, 255, 255), (self.rect.midleft[0], self.rect.midleft[1]), (position))
        if (pygame.mouse.get_pressed()[0] and self.fired == False):
            ball = Ball(cannonBall, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            cannonBalls.add(ball)
            self.fired = True
        if (pygame.mouse.get_pressed()[0] == False):
            self.fired = False


    def drawFort(self):
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, health, animationList, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.speed = speed
        self.health = health
        self.animationList = animationList
        self.frameIndex = 0
        self.action = 0
        self.updateTime = pygame.time.get_ticks()
        self.image = self.animationList[self.action][self.frameIndex]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def update(self):
        self.updateAnimation()
        gameWindow.blit(self.image, self.rect)

    def updateAnimation(self):
        animationTime = 100
        self.image = self.animationList[self.action][self.frameIndex]
        if (pygame.time.get_ticks() - self.updateTime > animationTime):
            self.updateTime = pygame.time.get_ticks()
            self.frameIndex += 1
        if(self.frameIndex >= len(self.animationList[self.action])):
            self.frameIndex = 0



# Game Loop: #

fort = Fort(fortUndamaged, 500, 235, 3) # Fort Creation
cannonBalls = pygame.sprite.Group()
gameEnemies = pygame.sprite.Group()
enemyTank = Enemy(enemyHealth[0], enemyAnimations[0], 200, 300, 1)
gameEnemies.add(enemyTank)

while gameRunning: 

    handleFPS.tick(60)
    gameWindow.blit(gameBackground, (0, 0))
    fort.drawFort()
    fort.fireBall()
    gameEnemies.update()
    cannonBalls.update()
    cannonBalls.draw(gameWindow)

    # Events handler: #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
            
    pygame.display.update()
            
pygame.quit()