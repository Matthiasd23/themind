import numpy.random as npr

from model.agents.superAgent import SuperAgent


class CopyCat(SuperAgent):
    """
    Copycat copies the other agents
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, " (CopyCat)", 0)
        self.coeff = 1
        self.avg_counter = 0

    def include_copied(self):
        # Adjusting the difference with a coefficient variable that is updated after a card is played
        self.diff *= self.coeff

    def update_vars(self, c, pile, time):
        if c > pile:
            self.avg_counter += 1
            d = time / (c-pile)
            self.coeff = (self.coeff * self.avg_counter + d) / (self.avg_counter + 1)

    def get_active(self, i):
        """
        method to return the time the agent will wait with a little bit of deviation
        Also looks at the other players actions and adjusts its speed according to their actions
        """
        if self.last_one_standing():
            return 0

        # Bij welke interval wordt gespeeld? En wat is de difference?
        self.determine_difference()
        self.include_copied()
        # self.include_passive()
        output = abs(npr.normal(self.diff, (self.diff) * self.std))
        return output - i
