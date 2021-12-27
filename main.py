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
gameGrass = loadGameImage('assets/Grass.png', 800, 600)

# Fort:
fortCannon = loadGameImage('assets/Cannon.png', 64, 64)
fortUndamaged = loadGameImage('assets/Fort.png', 64, 64)
fortDamaged = loadGameImage('assets/Fort_Damaged.png', 64, 64)
fortHeavilyDamaged = loadGameImage('assets/Fort_Heavily_Damaged.png', 64, 64)

# Tower:
towerUndamaged = loadGameImage('assets/Tower.png', 64, 64)
towerDamaged = loadGameImage('assets/Tower_Damaged.png', 64, 64)
towerHeavilyDamaged = loadGameImage('assets/Tower_Heavily_Damaged.png', 64, 64)

# Cannon Ball:
cannonBall = loadGameImage('assets/Ball.png', 64, 64)

# Buttons:
repairButton = loadGameImage('assets/Repair.png', 64, 64)
armourButton = loadGameImage('assets/Armour.png', 64, 64)
towerButton = loadGameImage('assets/Tower_Button.png', 64, 64)

# Game Loop: #

while(window.engineRunning):
    window.limitFPS(60)
    window.setBackground(gameBackground, 0, 0)
    window.updateDisplay()
    
