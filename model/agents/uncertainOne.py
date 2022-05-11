import numpy.random as npr
from model.agents.superAgent import SuperAgent


class UncertainOne(SuperAgent):
    """
    Most basic agent just to be able to run the basic game
    Counts down the difference between the cards
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, " (UncertainOne)", 0.5)

    def get_active(self, i):
        """
        The uncertain one has an adjusted deviation based on the time (interval) which makes him quite unpredictable
        """
        # adjusted_diff = self.diff/(self.diff-i)
        adjusted_std = self.std * pow(1.01, i)
        self.planned_interval = abs(npr.normal(self.diff * self.P, self.diff * adjusted_std))
        return (self.planned_interval - i) * self.ninja_speed