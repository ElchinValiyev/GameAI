import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzyAgent:
    def __init__(self):
        # Generate universe variables

        distance = ctrl.Antecedent(np.arange(-440, 441, 1), 'distance')  # paddle.x - ball.x
        paddle_speed = ctrl.Consequent(np.arange(-12,13,4), 'speed')  # paddle.x +=paddle_speed


        # Auto-membership function population is possible with .automf(3, 5, or 7)
        # Generate fuzzy membership functions
        distance['far right'] = fuzz.trimf(distance.universe, [-440, -250, -110])
        distance['close right'] = fuzz.trimf(distance.universe, [-200, -10, 0])
        distance['close left'] = fuzz.trimf(distance.universe, [0, 10, 200])
        distance['far left'] = fuzz.trimf(distance.universe, [200, 440, 440])

        paddle_speed.automf(7)
        rule1 = ctrl.Rule(distance['far left'], paddle_speed['dismal'])
        rule2 = ctrl.Rule(distance['close left'], paddle_speed['dismal'])
        rule3 = ctrl.Rule(distance['close right'], paddle_speed['excellent'])
        rule4 = ctrl.Rule(distance['far right'], paddle_speed['excellent'])
        # rule5 = ctrl.Rule(distance['above'], paddle_speed['average'])

        paddle_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4])
        self.agent = ctrl.ControlSystemSimulation(paddle_ctrl)

    def compute(self, distance):
        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        self.agent.input['distance'] = distance
        # Crunch the numbers
        self.agent.compute()
        return self.agent.output['speed']


if __name__ == '__main__':
    agent = FuzzyAgent()
    print agent.compute(0)
