import numpy.random as npr

from model.agents.superAgent import SuperAgent


class CopyCat(SuperAgent):
    """
    Copycat copies the other agents
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, " (CopyCat)", 0)
        self.coeff = 1
        self.alpha = 0.0005
        self.beta = 0.0005  # volledig gebaseerd op self.alpha

    def include_copied(self):
        # Adjusting the difference with a coefficient variable that is updated after a card is played
        self.diff *= self.coeff

    def update_vars(self, c, pile, time):
        d = c - pile
        # d = d * self.coeff
        self.coeff = self.coeff + (time + self.model.present.threshold - d) * self.beta
        # print("coeff: " + str(self.coeff))

    def get_active(self, i):
        """
        method to return the time the agent will wait with a little bit of deviation
        Also looks at the other players actions and adjusts its speed according to their actions
        """
        self.beta = self.alpha * self.model.present.cards_in_game
        # Bij welke interval wordt gespeeld? En wat is de difference?
        self.determine_difference()
        self.include_copied()
        # self.include_passive()
        output = abs(npr.normal(self.diff, (self.diff) * self.std))
        return output - i
