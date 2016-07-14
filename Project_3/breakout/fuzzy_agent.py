import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzyAgent:
    def __init__(self):
        # Generate universe variables

        distance = ctrl.Antecedent(np.arange(-440, 441, 1), 'distance')  # paddle.x - ball.x
        paddle_speed = ctrl.Consequent(np.arange(-16, 17, 1), 'speed')  # paddle.x +=paddle_speed


        # Auto-membership function population is possible with .automf(3, 5, or 7)
        # distance.automf(names=['far left', 'close left', 'above', 'close right', 'far right'])
        # paddle_speed.automf(3)

        # Generate fuzzy membership functions
        distance['far right'] = fuzz.trimf(distance.universe, [-440, -440, -110])
        distance['close right'] = fuzz.trimf(distance.universe, [-220, -110, 0])
        distance['above'] = fuzz.trimf(distance.universe, [-50, 0, 50])
        distance['close left'] = fuzz.trimf(distance.universe, [0, 110, 220])
        distance['far left'] = fuzz.trimf(distance.universe, [110, 440, 440])

        paddle_speed['fast left'] = fuzz.trimf(paddle_speed.universe, [-16, -16, -4])
        paddle_speed['slow left'] = fuzz.trimf(paddle_speed.universe, [-8, -4, 0])
        paddle_speed['stay'] = fuzz.trimf(paddle_speed.universe, [-1, 0, 1])
        paddle_speed['slow right'] = fuzz.trimf(paddle_speed.universe, [0, 4, 8])
        paddle_speed['fast right'] = fuzz.trimf(paddle_speed.universe, [4, 16, 16])

        # Visualize these universes and membership functions
        # distance.view()
        # paddle_speed.view()
        # plt.show()

        rule1 = ctrl.Rule(distance['far left'], paddle_speed['fast left'])
        rule2 = ctrl.Rule(distance['close left'], paddle_speed['slow left'])
        rule3 = ctrl.Rule(distance['close right'], paddle_speed['slow right'])
        rule4 = ctrl.Rule(distance['far right'], paddle_speed['fast right'])
        rule5 = ctrl.Rule(distance['above'], paddle_speed['stay'])

        paddle_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
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
