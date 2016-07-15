import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzyTrajectory:
    def __init__(self):
        # Generate universe variables

        distance = ctrl.Antecedent(np.arange(-9, 9, 1), 'distance')
        trajectory = ctrl.Consequent(np.arange(-2, 3, 1), 'trajectory')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        distance.automf(3)

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        trajectory['low'] = fuzz.trimf(trajectory.universe, [-2, -2, -2])
        trajectory['medium'] = fuzz.trimf(trajectory.universe, [0, 0, 2])
        trajectory['high'] = fuzz.trimf(trajectory.universe, [0, 2, 2])

        rule1 = ctrl.Rule(distance['poor'], trajectory['low'])
        rule2 = ctrl.Rule(distance['average'], trajectory['medium'])
        rule3 = ctrl.Rule(distance['good'], trajectory['high'])

        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        trajectoryping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
        self.agent = ctrl.ControlSystemSimulation(trajectoryping_ctrl)

    def compute(self, distance):
        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        self.agent.input['distance'] = distance
        # Crunch the numbers
        self.agent.compute()
        return self.agent.output['trajectory']


if __name__ == '__main__':
    agent = FuzzyTrajectory()
    print agent.compute(-7)
