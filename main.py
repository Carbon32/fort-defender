# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                    Fort Defender, defender video game                       #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

from src.engine import *

# Level: #

level = Level()

# Game: #

game = Game(level)

# Resolution: #

resolution = Resolution(game)

# Resolution: #

graphics = Graphics(game)

# Resoltuion Selection: #

while(resolution.resolution_status):
    resolution.update_background()
    if(resolution.resolution_a.render()):
        resolution.set_resolution(800, 600)
        break

    if(resolution.resolution_b.render()):
        resolution.set_resolution(1024, 768)
        break

    if(resolution.resolution_c.render()):
        resolution.set_resolution(1280, 720)
        break

    if(resolution.resolution_d.render()):
        resolution.set_resolution(1920, 1080)
        break

    resolution.update_window()

# Graphics Selection: #

while(graphics.graphics_status):
    graphics.update_background()
    if(graphics.clouds.render()):
        graphics.set_clouds()

    if(graphics.effects.render()):
        graphics.set_effects()

    if(graphics.start.render()):
        break

    graphics.update_window()

# Start Window: 

game.start_window()

# Sound: #

sounds = Sounds(game)

# Clouds: #

clouds = Clouds(game)

# Menu: #

menu = Menu(game)

# User Interface: #

ui = UserInterface(game)

# Particles: #

particles = Particles(game.display)

# Background: #

background = Background(game)

# Crosshair: #

crosshair = Crosshair(game)

# Fort: #

fort = Fort(game, game.screen_width // 3 + game.screen_width // 2, game.screen_height // 5 + game.screen_height // 2, 1000)

# Fade:

start_fade = Fade(game.display, 1, ((0, 0, 0)), 30)

# Game Icon: #

game.set_game_icon("assets/tanks/light_tank/move/0.png")

# Enemy Settings: #

enemy_animations, enemy_types, enemy_health = game.load_game_enemies(['light_tank', 'heavy_tank', 'attack_tank', 'desert_tank', 'offensive_tank', 'camo_tank'], ['move', 'attack', 'explosion'], [50, 125, 250, 350, 450, 500])

# Music: #

sounds.play_music()

# Game Loop: #

while(game.engine_running):

    # Clear Window: 

    game.clear_window()

     # Menu:

    if(menu.menu_status):
        menu.handle_menu(sounds)
        if(menu.button_start.render()):
            if(not game.started):
                menu.menu_status = False
                game.toggle_mouse_cursor_off()
                game.started = True
            else:
                menu.menu_status = False
                game.toggle_mouse_cursor_off()

        if(menu.button_quit.render()):
            game.engine_running = False

        if(menu.button_music.render()):
            if(sounds.music_status):
                sounds.music_status = False
                sounds.stop_music()
            else:
                sounds.music_status = True
                sounds.play_music()

        if(menu.button_sound.render()):
            if(sounds.sound_status):
                sounds.sound_status = False
            else:
                sounds.sound_status = True
    else:

        # Sky:

        background.update_game_background()

        # Time: 

        background.update_time()

        # Ground: 

        background.draw_level_design(0, 0)

        # Game Particles: 

        particles.update_particles(game)

        # Clouds:

        clouds.handle_clouds()

        # Fort: 

        fort.draw_fort()

        # Check for Menu:

        menu.check_menu()

        # Game Status: 

        if(game.over == False):

            # User Interface: 

            ui.show_stats(fort)

            # Button Functionality:

            if(ui.button_repair.render()):
                fort.repair_fort(sounds)

            if(ui.button_armour.render()):
                fort.upgrade_armour(sounds)

            if(ui.button_tower.render()):
                if(game.coins >= 2000 and len(game.game_towers) < 2):
                    tower = Tower(game, game.tower_positionss[len(game.game_towers)][0], game.tower_positionss[len(game.game_towers)][1])
                    game.game_towers.add(tower)
                    game.coins -= 2000
                    sounds.build.play()
                else:
                    sounds.error.play()

            if(ui.button_balls.render()):
                fort.add_balls(sounds)

            if(ui.button_ball_type.render()):
                fort.upgrade_balls(sounds)

            if(start_fade.fade(game.screen_width, game.screen_height) and game.over == False):
                fort.fire_ball(particles, sounds)

                # Sprites: 

                game.update_game_towers(fort, sounds)
                game.update_game_balls(particles, fort.ball_type)
                game.update_game_enemies(particles, fort, sounds)
                game.update_game_mechanics(fort, enemy_animations, enemy_types, enemy_health)

            if(fort.health <= 0):
                game.over = True

            # Crosshair: 

            crosshair.draw_crosshair()
        else:
            game.reset_game(fort, background)

    # Update Display: 

    game.update_display(60)

# Quit: #

game.destroy_game()
