from ale_python_interface import ALEInterface
import numpy as np
import cv2
from collections import deque


class Environment:
    def __init__(self, show_screen, history_length):
        self.ale = ALEInterface()
        self.ale.setInt('frame_skip', 4)
        self.history = None
        self.history_length = history_length
        if show_screen:
            self.display_screen()
        self.load_game()
        (screen_width, screen_height) = self.ale.getScreenDims()
        self.screen_data = np.empty((screen_height, screen_width, 1), dtype=np.uint8)  # 210x160 screen data
        self.dims = (84, 84)  # input size for neural network
        self.actions = [3, 0, 1, 4]  # noop, left, right, fire,

    def display_screen(self):
        self.ale.setBool("display_screen", True)

    def turn_on_sound(self):
        self.ale.setBool("sound", True)

    def restart(self):
        """reset game"""
        self.ale.reset_game()

    def act(self, action):
        """:returns reward of an action"""
        return self.ale.act(self.actions[action])

    def __get_screen(self):
        """:returns Grayscale thresholded resized screen image """
        self.ale.getScreenGrayscale(self.screen_data)
        resized = cv2.resize(self.screen_data, self.dims)
        return resized

    def get_state(self):
        binary_screen = self.__get_screen()
        if self.history is None:
            self.history = deque(maxlen=self.history_length)
            for _ in range(self.history_length - 1):
                self.history.append(binary_screen)
        self.history.append(binary_screen)
        result = np.stack(self.history, axis=0)
        return result

    def isTerminal(self):
        """checks if game is over"""
        return self.ale.game_over()

    def load_game(self):
        """load game from file"""
        self.ale.loadROM("Breakout.bin")
