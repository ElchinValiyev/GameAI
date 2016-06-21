#!/usr/bin/env python
# python_example.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from
# ALE provided in doc/examples/sharedLibraryInterfaceExample.cpp
import sys
import numpy as np
from random import randrange
from ale_python_interface import ALEInterface

ale = ALEInterface()

# Get & Set the desired settings
ale.setInt('random_seed', 123)

# Shows screen of the game to see what is going on
ale.setBool("display_screen", True)
ale.setBool("sound", True)

# Set USE_SDL to true to display the screen. ALE must be compilied
# with SDL enabled for this to work. On OSX, pygame init is used to
# proxy-call SDL_main.
# USE_SDL = False
# if USE_SDL:
#     if sys.platform == 'darwin':
#         import pygame
#
#         pygame.init()
#         ale.setBool('sound', False)  # Sound doesn't work on OSX
#     elif sys.platform.startswith('linux'):
#         ale.setBool('sound', True)
#     ale.setBool('display_screen', True)

# Load the ROM file
ale.loadROM('Breakout.bin')

# Get the list of legal actions
# legal_actions = ale.getLegalActionSet()
legal_actions = ale.getMinimalActionSet()
print legal_actions

# (screen_width,screen_height) = ale.getScreenDims()
# screen_data = np.zeros(screen_width*screen_height,dtype=np.uint32)
# ale.getScreenRGB(screen_data)

(screen_width, screen_height) = ale.getScreenDims()
screen_data = np.zeros(screen_width * screen_height, dtype=np.uint8)
print type(ale.getScreen(screen_data))

# Play 10 episodes
for episode in xrange(10):

    total_reward = 0
    while not ale.game_over():
        a = legal_actions[randrange(len(legal_actions))]
        # Apply an action and get the resulting reward
        reward = ale.act(a)
        print  reward
        total_reward += reward
    print 'Episode', episode, 'ended with score:', total_reward
    ale.reset_game()
