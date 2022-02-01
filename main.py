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

# Game Icon:

setGameIcon("assets/Tank/Move/0.png")

# Background:
gameBackground = loadGameImage('assets/Background.png', 800, 600)
menuBackground = loadGameImage('assets/Background_2.png', 800, 600)

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
bulletButton = loadGameImage('assets/Buttons/Bullets.png', 64, 64)
startButton = loadGameImage('assets/Buttons/start.png', 168, 128)
quitButton = loadGameImage('assets/Buttons/exit.png', 168, 128)

# Crosshair: 
crosshairSprite = loadGameImage('assets/Crosshair/Crosshair.png', 32, 32)

# Enemy: 
enemyAnimations, enemyTypes = loadGameEnemies(['Tank', 'Heavy', 'Super'], ['Move', 'Attack', 'Explosion'])
enemyHealth = assignEnemyHealth([50, 125, 250])

# Music:
# playMusic("sounds/music.mp3", 0.2)

# Sounds:
shoot = loadGameSound('sounds/shoot.wav', 0.2)
explosion = loadGameSound('sounds/explosion.mp3', 0.2)
build = loadGameSound('sounds/build.mp3', 0.2)
ballLoad = loadGameSound('sounds/ball_load.mp3', 0.2)

# Game Mechanics: #

# Fort: 
fort = Fort(fortUndamaged, fortDamaged, fortHeavilyDamaged, 500, 270, 1000, 1000)

# Crosshair:
crosshair = Crosshair(crosshairSprite)

# Buttons:
buttonRepair = Button(700, 10, repairButton)
buttonArmour = Button(700, 80, armourButton)
buttonTower = Button(700, 150, towerButton)
buttonBullets = Button(550, 10, bulletButton)
buttonStart = Button(320, 100, startButton)
buttonQuit = Button(320, 250, quitButton)

# Fade:
startFade = Fade(1, ((0, 0, 0)), 5)

# Game Loop: #

while(window.engineRunning):
    # Window Setup: 
    window.setBackground(gameBackground, 0, 0)
    if(mainMenu):
        toggleMouseCursorOn()
        window.setBackground(menuBackground, 0, 0)
        if(buttonStart.drawButton(window.engineWindow)):
            mainMenu = False
            toggleMouseCursorOff()

        if(buttonQuit.drawButton(window.engineWindow)):
            window.engineRunning = False
    else:
        # Fort Particles:
        drawFortParticles(window.engineWindow, (138, 134, 142))

        # Fort Creation:
        fort.drawFort(window.engineWindow)
        showStats(window.engineWindow, fort)

        # Button Functionality:
        if(buttonRepair.drawButton(window.engineWindow)):
            fort.repairFort(build)

        if(buttonArmour.drawButton(window.engineWindow)):
            fort.upgradeArmour(build)

        if(buttonTower.drawButton(window.engineWindow)):
            if(fort.coins >= 2000 and len(gameTowers) < 2):
                tower = Tower(towerUndamaged, towerDamaged, towerHeavilyDamaged, towerPositions[len(gameTowers)][0], towerPositions[len(gameTowers)][1])
                gameTowers.add(tower)
                fort.coins -= 2000
                build.play()
        if(buttonBullets.drawButton(window.engineWindow)):
            if(fort.coins >= 250):
                fort.addBullets(ballLoad)
                fort.coins -= 250
        if(startFade.fade(window.engineWindow, 800, 600)):
            fort.fireBall(cannonBall, shoot)

        if(gameOver == False):
            # Towers:
            updateGameTowers(window.engineWindow, fort, cannonBall)
            crosshair.drawCrosshair(window.engineWindow)
            # Enemy & Damage Particles:
            drawEnemyParticles(window.engineWindow, (255, 165, 0))
            drawDamageParticles(window.engineWindow, (25, 51, 0))

            updateGameMechanics(window.engineWindow, fort, enemyAnimations, enemyTypes, enemyHealth, explosion)
            if(fort.health <= 0):
                gameOver = True
        else:
            gameOver = resetGame(window.engineWindow, fort)
          
    window.updateDisplay()
    window.limitFPS(60)

window.quit()
    
