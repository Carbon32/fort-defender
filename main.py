# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                    Fort Defender, defender video game                       #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Imports: #

from engine import *

# Level: #

level = Level()

# Game: #

game = Game(level)

# Resolution: #

resolution = Resolution(game)

# Resoltuion Selection: #

while(resolution.resolutionStatus):
    resolution.updateBackground()

    if(resolution.resolutionA.render()):
        resolution.setResolution(800, 600)
        break

    if(resolution.resolutionB.render()):
        resolution.setResolution(1024, 768)
        break

    if(resolution.resolutionC.render()):
        resolution.setResolution(1280, 720)
        break

    if(resolution.resolutionD.render()):
        resolution.setResolution(1920, 1080)
        break

    resolution.updateWindow()

# Start Window: 

game.startWindow()

# Sound: #

sounds = Sounds()

# Menu: #

menu = Menu(game.display)

# User Interface: #

ui = UserInterface(game)

# Particles: #

particles = Particles(game.display)

# Background: #

background = Background(game.display)

# Crosshair: #

crosshair = Crosshair(game.display)

# Fort: #

fort = Fort(game, game.screenWidth // 3 + game.screenWidth // 2, game.screenHeight // 5 + game.screenHeight // 2, 1000)

# Fade:

startFade = Fade(game.display, 1, ((0, 0, 0)), 18)

# Game Icon: #

game.setGameIcon("assets/Tank/Move/0.png")

# Enemy Settings: #

enemyAnimations, enemyTypes, enemyHealth = loadGameEnemies(game.display, ['Tank', 'Heavy', 'Super'], ['Move', 'Attack', 'Explosion'], [50, 125, 250])

# Music: #

sounds.playMusic()

# Game Loop: #

while(game.engineRunning):

    # Clear Window: 
    print(game.fpsHandler)
    game.clearWindow()

     # Menu:

    if(menu.menuStatus):

        menu.handleMenu(sounds.musicStatus, sounds.soundStatus)

        if(menu.buttonStart.render()):

            menu.menuStatus = False
            toggleMouseCursorOff()

        if(menu.buttonQuit.render()):

            game.engineRunning = False

        if(menu.buttonMusic.render()):

            if(sounds.musicStatus):

                sounds.musicStatus = False
                stopMusic()

            else:

                sounds.musicStatus = True
                sounds.playMusic()

        if(menu.buttonSound.render()):

            if(sounds.soundStatus):

                sounds.soundStatus = False

            else:

                sounds.soundStatus = True

    else:

        # Sky:

        background.setGameBackground()

        # Time: 

        background.updateTime()

        # Ground: 

        background.setLevelDesign(loadGameImage('assets/Background.png', game.screenWidth, game.screenHeight), 0, 0)

        # Game Particles: 

        particles.updateParticles()

        # Fort: 

        fort.drawFort()

        # Check for Menu:

        menu.checkMenu()

        # Game Status: 

        if(game.over == False):

            # User Interface: 

            ui.showStats(fort, level.currentLevel)

            # Button Functionality:

            if(ui.buttonRepair.render()):

                fort.repairFort(sounds.soundStatus, sounds.build,  sounds.error)

            if(ui.buttonArmour.render()):

                fort.upgradeArmour(sounds.soundStatus, sounds.build,  sounds.error)

            if(ui.buttonTower.render()):

                if(game.coins >= 2000 and len(game.gameTowers) < 2):

                    tower = Tower(game, game.towerPositions[len(game.gameTowers)][0], game.towerPositions[len(game.gameTowers)][1])
                    game.gameTowers.add(tower)
                    game.coins -= 2000

            if(ui.buttonBullets.render()):

                fort.addBullets(sounds.soundStatus, sounds.ballLoad, sounds.error)

            if(startFade.fade(game.screenWidth, game.screenHeight) and game.over == False):

                fort.fireBall(particles, sounds.soundStatus, sounds.shoot)

            if(fort.health <= 0):

                game.over = True

            # Update Sprites: 

            game.updateGameTowers(fort)
            game.updateGameBalls(particles)
            game.updateGameEnemies(particles, fort, sounds.soundStatus, sounds.explosion)
            game.updateGameMechanics(fort, enemyAnimations, enemyTypes, enemyHealth)

            # Crosshair: 

            crosshair.drawCrosshair()

        else:

            game.resetGame(fort)



    # Update Display: 

    game.updateDisplay(60)

# Quit: #

destroyGame()
