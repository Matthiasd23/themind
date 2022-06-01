import numpy.random as npr

from model.agents.superAgent import SuperAgent


class BasicAgent(SuperAgent):
    """
    Most basic agent just to be able to run the basic game
    Counts down the difference between the cards
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, " (Basic agent)", 0.25)

    def get_active(self, i):
        """
        return the time the agent will wait with a little bit of deviation
        """
        if self.last_one_standing():
            return 0

        if i == 1:
            self.update_ninja()
        self.planned_interval = abs(npr.normal(self.diff * self.P, (
            self.diff) * self.std))  # NOT CHANGING THE STD DEVIATION because it goes both ways
        return (self.planned_interval * self.counting_speed - i) * self.ninja_speed # -i om de threshold te halen
