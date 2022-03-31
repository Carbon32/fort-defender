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

game = Game(window, level)

# Sound: #

sounds = Sounds()

# Menu: #

menu = Menu(window)

# User Interface: #

ui = UserInterface(window, game)

# Particles: #

particles = Particles(window)

# Background: #

background = Background(window)

# Crosshair: #

crosshair = Crosshair(window)

# Fort: #

fort = Fort(game, 500, 270, 1000)

# Fade:

startFade = Fade(window, 1, ((0, 0, 0)), 12)

# Game Icon: #

game.setGameIcon("assets/Tank/Move/0.png")

# Enemy Settings: #

enemyAnimations, enemyTypes, enemyHealth = loadGameEnemies(['Tank', 'Heavy', 'Super'], ['Move', 'Attack', 'Explosion'], [50, 125, 250])

# Music: #

sounds.playMusic()

# Game Loop: #

while(game.engineRunning):

    # Clear Window: 

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

        background.setLevelDesign(loadGameImage('assets/Background.png', screenWidth, screenHeight), 0, 0)

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

                    tower = Tower(game.towerPositions[len(game.gameTowers)][0], game.towerPositions[len(game.gameTowers)][1])
                    game.gameTowers.add(tower)
                    game.coins -= 2000

            if(ui.buttonBullets.render()):

                fort.addBullets(sounds.soundStatus, sounds.ballLoad, sounds.error)

            if(startFade.fade(800, 600) and game.over == False):

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
