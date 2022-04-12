from mesa import Model, Agent
import numpy.random as npr

class UncertainOne(Agent):
    """
    Most basic agent just to be able to run the basic game
    Counts down the difference between the cards
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cards = []
        self.diff = 0
        self.std = 0.05
        self.type = " (UncertainOne)"
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
    The uncertain one counts a bit 'faster' which decreases the time variable more over time
    """
    def get_active(self,i):
        self.determine_difference()
        #adjusted_diff = self.diff/(self.diff-i)
        adjusted_std = self.std * pow(1.01, i)
        return abs(npr.normal(self.diff, self.diff * adjusted_std))

    def get_passive(self):
        pass

    def remove_card(self):
        del self.cards[0]