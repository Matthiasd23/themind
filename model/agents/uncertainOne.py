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
        self.P = 1
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
    method to update internal variables if needed
    """
    def update_vars(self, c, pile, time):
        pass

    def get_active(self,i):
        """
        The uncertain one has an adjusted deviation based on the time (interval) which makes him quite unpredictable
        """
        self.determine_difference()
        #adjusted_diff = self.diff/(self.diff-i)
        adjusted_std = self.std * pow(1.01, i)
        output = abs(npr.normal(self.diff, self.diff * adjusted_std))
        return output - i

    def get_passive(self):

        pass

    def remove_card(self):
        del self.cards[0]
