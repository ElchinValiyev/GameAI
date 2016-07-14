import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


class FuzzyTrajectory:
    def __init__(self):
        # Generate universe variables

        quality = ctrl.Antecedent(np.arange(-8, 9, 1), 'quality')
        tip = ctrl.Consequent(np.arange(-2, 3, 1), 'tip')

        # Auto-membership function population is possible with .automf(3, 5, or 7)
        quality.automf(3)

        # Custom membership functions can be built interactively with a familiar,
        # Pythonic API
        tip['low'] = fuzz.trimf(tip.universe, [-2, -2, -2])
        tip['medium'] = fuzz.trimf(tip.universe, [0, 0, 2])
        tip['high'] = fuzz.trimf(tip.universe, [0, 2, 2])

        rule1 = ctrl.Rule(quality['poor'], tip['low'])
        rule2 = ctrl.Rule(quality['average'], tip['medium'])
        rule3 = ctrl.Rule(quality['good'], tip['high'])

        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
        self.agent = ctrl.ControlSystemSimulation(tipping_ctrl)

    def compute(self, distance):
        # Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
        # Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
        self.agent.input['quality'] = distance
        # Crunch the numbers
        self.agent.compute()
        return self.agent.output['tip']


if __name__ == '__main__':
    agent = FuzzyAgent()
    print agent.compute(-7)
