from ale_python_interface import ALEInterface
import numpy as np
import cv2


class Environment:
    def __init__(self):
        self.ale = ALEInterface()
        self.load_game()
        (screen_width, screen_height) = self.ale.getScreenDims()
        self.screen_data = np.empty((screen_height, screen_width, 1), dtype=np.uint8)  # 210x160 screen data
        self.dims = (84, 84)  # input size for neural network
        self.actions = [0, 3, 4]  # noop,right, left

    def display_screen(self):
        self.ale.setBool("display_screen", True)

    def turn_on_sound(self):
        self.ale.setBool("sound", True)

    def restart(self):
        """reset game"""
        self.ale.reset_game()

    def act(self, action):
        """:return reward of an action"""
        return self.ale.act(self.actions[action])

    def getScreen(self):
        self.ale.getScreenGrayscale(self.screen_data)
        return cv2.resize(self.screen_data, self.dims)

    def isTerminal(self):
        """checks if game is over"""
        return self.ale.game_over()

    def load_game(self):
        """load game from file"""
        self.ale.loadROM("Breakout.bin")
