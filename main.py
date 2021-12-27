# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                    Fort Defender, defender video game                       #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from engine import *

# Game Window: #

window = Window(800, 600, "Fort Defender")
window.init()

# Game Assets: #

# Background:
gameBackground = loadGameImage('assets/Background.png', 800, 600)

# Fort:
fortUndamaged = loadGameImage('assets/Fort/Fort.png', 300, 300)
fortDamaged = loadGameImage('assets/Fort/Fort_Damaged.png', 300, 300)
fortHeavilyDamaged = loadGameImage('assets/Fort/Fort_Heavily_Damaged.png', 300, 300)

# Tower:
towerUndamaged = loadGameImage('assets/Towers/Tower.png', 128, 128)
towerDamaged = loadGameImage('assets/Towers/Tower_Damaged.png', 128, 128)
towerHeavilyDamaged = loadGameImage('assets/Towers/Tower_Heavily_Damaged.png', 128, 128)

# Cannon Ball:
cannonBall = loadGameImage('assets/Ball/Ball.png', 16, 16)

# Buttons:
repairButton = loadGameImage('assets/Buttons/Repair.png', 64, 64)
armourButton = loadGameImage('assets/Buttons/Armour.png', 64, 64)
towerButton = loadGameImage('assets/Buttons/Tower_Button.png', 64, 64)

# Crosshair: 
crosshairSprite = loadGameImage('assets/Crosshair/Crosshair.png', 32, 32)

# Enemy: 
enemyAnimations, enemyTypes = loadGameEnemies(['Tank', 'Heavy', 'Super'], ['Move', 'Attack', 'Explosion'])
enemyHealth = assignEnemyHealth([50, 125, 250])

# Sounds:
shoot = pygame.mixer.Sound('sounds/shoot.wav')
shoot.set_volume(0.2)
explosion = pygame.mixer.Sound('sounds/explosion.mp3')
explosion.set_volume(0.2)

# Game Mechanics: #

# Fort: 
fort = Fort(fortUndamaged, fortDamaged, fortHeavilyDamaged, 500, 270, 1000, 1000)

# Crosshair:
crosshair = Crosshair(crosshairSprite)

# Buttons:
buttonRepair = Button(700, 10, repairButton)
buttonArmour = Button(700, 80, armourButton)
buttonTower = Button(700, 150, towerButton)

# Game Loop: #

while(window.engineRunning):
    # Window Setup: 
    window.limitFPS(60)
    window.setBackground(gameBackground, 0, 0)

    # Fort Creation:
    fort.drawFort(window.engineWindow)
    fort.fireBall(cannonBall, shoot)
    fort.coins = 5000

    if(gameOver == False):
        # Towers:
        updateGameTowers(window.engineWindow, fort, cannonBall)

        # Button Functionality:
        if(buttonRepair.drawButton(window.engineWindow)):
            fort.repairFort()

        if(buttonArmour.drawButton(window.engineWindow)):
            fort.upgradeArmour()

        if(buttonTower.drawButton(window.engineWindow)):
            if(fort.coins >= 2000 and len(gameTowers) < 2):
                tower = Tower(towerUndamaged, towerDamaged, towerHeavilyDamaged, towerPositions[len(gameTowers)][0], towerPositions[len(gameTowers)][1])
                gameTowers.add(tower)
                fort.coins -= 2000

        crosshair.drawCrosshair(window.engineWindow)
        updateGameMechanics(window.engineWindow, fort, enemyAnimations, enemyTypes, enemyHealth, explosion)
    else:
        resetGame()
        
    window.updateDisplay()
    
