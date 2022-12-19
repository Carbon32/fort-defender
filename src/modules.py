# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#                                                                             #
#                 Defender Engine, Fort Defender's Game Engine                #
#                              Developer: Carbon                              #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Imports: #

try:
    import pygame 
    import math
    import random
    import os
    from pygame import mixer

except ImportError:
    raise ImportError("The Defender Engine couldn't import all of the necessary packages.")

# Pygame Initialization: #

pygame.init()

# Mixer Initialization: #

pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()
