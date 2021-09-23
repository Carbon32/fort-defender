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
difficultyMultiplier = 2
gameOver = False
nextLevel = False
enemyTimer = 2000
lastEnemy = pygame.time.get_ticks()
enemiesAlive = 0
towerPositions = [
[492, 315],
[600, 280],
[492, 460],
[715, 460]
]

# Assets loading: #


# Background: # 
gameBackground = pygame.image.load('assets/Background.png').convert_alpha()

# Fort: # 
fortCannon = pygame.image.load('assets/Cannon.png').convert_alpha()
fortUndamaged = pygame.image.load('assets/Fort.png').convert_alpha()
fortDamaged = pygame.image.load('assets/Fort_Damaged.png').convert_alpha()
fortHeavilyDamaged = pygame.image.load('assets/Fort_Heavily_Damaged.png').convert_alpha()

# Tower: #
towerUndamaged = pygame.image.load('assets/Tower.png').convert_alpha()
towerDamaged = pygame.image.load('assets/Tower_Damaged.png').convert_alpha()
towerHeavilyDamaged = pygame.image.load('assets/Tower_Heavily_Damaged.png').convert_alpha()

# Cannon Ball: #
cannonBall = pygame.image.load('assets/Ball.png').convert_alpha()
ballWidth = cannonBall.get_width()
ballHeight = cannonBall.get_height()
cannonBall = pygame.transform.scale(cannonBall, (int(ballWidth * 0.2), (int(ballHeight * 0.2))))

# Buttons: #
repairButton = pygame.image.load('assets/Repair.png')
armourButton = pygame.image.load('assets/Armour.png')
towerButton = pygame.image.load('assets/Tower_Button.png')

# Enemy: #
enemyAnimations = []
enemyTypes = ['Tank', 'Heavy',]
enemyHealth = [50, 150]
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

# Game Text: #
gameFont = pygame.font.SysFont('Impact', 20)
secondGameFont = pygame.font.SysFont('Impact', 50)

# Functions (Related to Game Text): #
def drawText(text, font, color, x, y):
    textImage = font.render(text, True, color)
    gameWindow.blit(textImage, (x, y))

def showStats():
    drawText('Money: ' + str(fort.money), gameFont, (0, 153, 0), 10, 10)
    drawText('Score: ' + str(fort.kills), gameFont, (0, 153, 0), 180, 10)
    drawText('Level: ' + str(gameLevel), gameFont, (0, 153, 0), 400, 10)
    drawText('Health: ' + str(fort.health) + "/" + str(fort.maxHealth), gameFont, (0, 153, 0), 500, 10)
    drawText('500', gameFont, (0, 153, 0), 715, 40)
    drawText('1000', gameFont, (0, 153, 0), 715, 120)
    drawText('2000', gameFont, (0, 153, 0), 640, 120)

# Game Classes: #

class Fort():
    def __init__(self, firstImage, secondImage, thirdImage, x, y, scale):
        self.health = 1000
        self.maxHealth = self.health
        self.fired = False
        self.money = 10000
        self.kills = 0
        width = image.get_width()
        height = image.get_height()
        self.image = firstImage
        self.firstImage = pygame.transform.scale(firstImage, (int(width * scale), int(height * scale)))
        self.secondImage = pygame.transform.scale(secondImage, (int(width * scale), int(height * scale)))
        self.thirdImage = pygame.transform.scale(thirdImage, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def fireBall(self):
        position = pygame.mouse.get_pos()
        xDistance = (position[0] - self.rect.midleft[0]+50)
        yDistance = -(position[1] - self.rect.midleft[1]+200)
        self.angle = math.degrees(math.atan2(yDistance, xDistance))
        if (pygame.mouse.get_pressed()[0] and self.fired == False and position[1] > 300 and position[0] < 280):
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
            self.image = self.firstImage
        gameWindow.blit(self.image, self.rect)

    def repairFort(self):
        if(self.money >= 500 and self.health < self.maxHealth):
            self.health += 250
            self.money -= 500
            if (self.health > self.maxHealth):
                self.health = self.maxHealth

    def upgradeArmour(self):
        if(self.money >= 1000):
            self.maxHealth += 500
            self.money -= 1000

class Tower(pygame.sprite.Sprite):
    def __init__(self, firstImage, secondImage, thirdImage, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        self.ready = False
        self.angle = 0
        self.lastShot = pygame.time.get_ticks()
        width = image.get_width()
        height = image.get_height()
        self.image = firstImage
        self.firstImage = pygame.transform.scale(firstImage, (int(width * scale), int(height * scale)))
        self.secondImage = pygame.transform.scale(secondImage, (int(width * scale), int(height * scale)))
        self.thirdImage = pygame.transform.scale(thirdImage, (int(width * scale), int(height * scale))) 
        self.rect = self.image.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def update(self, gameEnemies):
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
                ball = Ball(cannonBall, self.rect.midleft[0], self.rect.midleft[1]-125, self.angle)
                cannonBalls.add(ball)

        if(fort.health <= 250):
            self.image = self.thirdImage
        elif(fort.health <= 500):
            self.image = self.secondImage
        else:
            self.image = self.firstImage
        gameWindow.blit(self.image, self.rect)


class Ball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x+50
        self.rect.y = y-140
        self.angle = math.radians(angle)
        self.speed = 5
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
                self.health -= 0.1

            if(self.action == 0):
                self.rect.x += self.speed

            if(self.action == 1):
                if(pygame.time.get_ticks() - self.lastAttack > self.attackCooldown):
                    fort.health -= 50
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
                self.kill()
            else:
                self.frameIndex = 0

    def updateAction(self, newAction):
        if(newAction != self.action):
            self.action = newAction
            self.frameIndex = 0
            self.updateTime = pygame.time.get_ticks()

class Button():
    def __init__(self, x, y, image, scale):
        bWidth = image.get_width()
        bHeight = image.get_height()
        self.image = pygame.transform.scale(image, (int(bWidth * scale), int(bHeight * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def drawButton(self):
        action = False
        position = pygame.mouse.get_pos()

        if self.rect.collidepoint(position):
            if(pygame.mouse.get_pressed()[0] == 1 and self.clicked == False):
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        gameWindow.blit(self.image, (self.rect.x, self.rect.y))
        return action

# Game Loop: #

# Fort Creation: #
fort = Fort(fortUndamaged, fortDamaged, fortHeavilyDamaged, 500, 235, 4)

# Game Crosshair: #
crosshair = Crosshair(1.5)

# Game Buttons: #
buttonRepair = Button(700, -20, repairButton, 2)
buttonArmour = Button(700, 60, armourButton, 2)
buttonTower = Button(630, 60, towerButton, 2)

# Game Groups: #
cannonBalls = pygame.sprite.Group()
gameEnemies = pygame.sprite.Group()
gameTowers = pygame.sprite.Group()

while gameRunning: 

    handleFPS.tick(60)
    print(handleFPS)
    if(gameOver == False):
        gameWindow.blit(gameBackground, (0, 0))
        fort.drawFort()
        fort.fireBall()
        cannonBalls.update()
        cannonBalls.draw(gameWindow)
        mPositions = pygame.mouse.get_pos()
        cRect = fortCannon.get_rect()
        cRect.x = 530
        cRect.y = 320
        angle = math.degrees(math.atan2(mPositions[1], mPositions[0]+1200))
        gameCannon = pygame.transform.rotate(fortCannon, angle)
        gameWindow.blit(gameCannon, cRect)
        crosshair.drawCrosshair()
        showStats()

        if(buttonRepair.drawButton()):
            fort.repairFort()

        if(buttonArmour.drawButton()):
            fort.upgradeArmour()

        if(buttonTower.drawButton()):
            if(fort.money >= 5000 and len(gameTowers) < 4):
                tower = Tower(towerUndamaged, towerDamaged, towerHeavilyDamaged, towerPositions[len(gameTowers)][0], towerPositions[len(gameTowers)][1], 1)
                gameTowers.add(tower)
                fort.money -= 5000

        # Enemy Spawning: #

        gameEnemies.update()
        gameTowers.draw(gameWindow)
        gameTowers.update(gameEnemies)
        if(levelDifficulty < gameDifficulty):
            if(pygame.time.get_ticks() - lastEnemy > enemyTimer):
                if(gameLevel == 1):
                    randomEnemy = random.randint(0, len(enemyTypes) - 2)
                elif(gameLevel == 2):
                    randomEnemy = random.randint(0, len(enemyTypes) - 1)
                else:
                    randomEnemy = random.randint(0, len(enemyTypes) - 1)

                gameEnemy = Enemy(enemyHealth[randomEnemy], enemyAnimations[randomEnemy], -100, 499, 1)
                gameEnemies.add(gameEnemy)
                lastEnemy = pygame.time.get_ticks()
                levelDifficulty += enemyHealth[randomEnemy]

        if(levelDifficulty >= gameDifficulty):
            enemiesAlive = 0
            for enemy in gameEnemies:
                if enemy.alive == True:
                    enemiesAlive += 1
            if (enemiesAlive == 0 and nextLevel == False):
                nextLevel = True
                levelResetTime = pygame.time.get_ticks()

        if(nextLevel == True):
            drawText('LEVEL COMPLETE', secondGameFont, (204, 0, 0), 260, 200)
            if(pygame.time.get_ticks() - levelResetTime > 1500):
                nextLevel = False
                gameLevel += 1
                lastEnemy = pygame.time.get_ticks()
                gameDifficulty *= difficultyMultiplier
                levelDifficulty = 0
                gameEnemies.empty()
        if(fort.health <= 0):
            gameOver = True
    else:
        drawText('GAME OVER', secondGameFont, (204, 0, 0), 260, 200)
        drawText('PRESS "SPACE" TO RESTART', secondGameFont, (204, 0, 0), 150, 280)
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
            fort.money = 0
            pygame.mouse.set_visible(False)

    # Events handler: #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
            
    pygame.display.update()
            
pygame.quit()