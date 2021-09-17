# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Fort Kruz, defender video game                              #
#                                   based in World War II                     #
#                                             Developer: Carbon               #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

import pygame

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

# Game Classes: #

class Fort():
    def __init__(self, sprite, x, y, scale):
        self.health = 1000
        self.maxHealth = self.health
        width = sprite.get_width()
        height = sprite.get_height()
        self.sprite = pygame.transform.scale(sprite, (int(width * scale), int(height * scale)))
        self.rect = self.sprite.get_rect()
        self.rect.x = x 
        self.rect.y = y

    def fireBall(self):
        position = pygame.mouse.get_pos()
        pygame.draw.line(gameWindow, (255, 255, 255), (self.rect.midleft[0], self.rect.midleft[1]), (position))

    def drawFort(self):
        self.image = self.sprite
        gameWindow.blit(self.image, self.rect)

        
# Game Loop: #

fort = Fort(fortUndamaged, 500, 235, 3) # Fort Creation

while gameRunning: 

    handleFPS.tick(60)
    gameWindow.blit(gameBackground, (0, 0))
    fort.drawFort()
    fort.fireBall()

    # Events handler: #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameRunning = False
            
    pygame.display.update()
            
pygame.quit()