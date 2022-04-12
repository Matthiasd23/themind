from mesa import Model, Agent
import numpy.random as npr

class BasicAgent(Agent):
    """
    Most basic agent just to be able to run the basic game
    Counts down the difference between the cards
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cards = []
        self.diff = 0
        self.type = " (Basic agent)"
        # self.playing = True

    def order_cards(self):
        self.cards.sort()

    def determine_difference(self):
        if len(self.cards) != 0:
            self.diff = self.cards[0] - self.model.present.pile
            # self.diff = -(self.cards[0] - self.model.present.pile) -> check processing mistakes
        else:
            self.diff = 1000000
            # self.playing = False

    """
    return the time the agent will wait with a little bit of deviation
    """
    def get_active(self, i):
        self.determine_difference()
        return abs(npr.normal(self.diff, (self.diff) * 0.05))
        #return abs(npr.normal(self.diff / i, (self.diff / i) * 0.10))

    def get_passive(self):
        pass

    def remove_card(self):
        del self.cards[0]
