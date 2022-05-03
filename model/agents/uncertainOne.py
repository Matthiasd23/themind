import numpy.random as npr
from mesa import Agent


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
        self.adaptability = 1.0
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

    def get_active(self, i):
        """
        The uncertain one has an adjusted deviation based on the time (interval) which makes him quite unpredictable
        """
        self.determine_difference()
        # adjusted_diff = self.diff/(self.diff-i)
        adjusted_std = self.std * pow(1.01, i)
        output = abs(npr.normal(self.diff, self.diff * adjusted_std))
        return output - i

    def get_passive(self):
        return self.P

    def wrong_throw(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        The player should be be playing slower (higher P) because he threw too soon (strong adjustments)
        """
        goal_interval = played_interval - 1
        self.P = self.P + ((1 - (goal_interval / self.planned_interval)) * self.adaptability)
        print("agent (early)" + str(self.unique_id) + " | played_interval " + str(
            played_interval) + " | planned interval " + str(self.planned_interval))

    def shouldve_thrown(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        The player should be be playing faster (lower P) because he threw too late (strong adjustments)
        """
        goal_interval = played_interval - 1
        self.P = self.P - ((1 - (goal_interval / self.planned_interval)) * self.adaptability)
        print("agent (late) " + str(self.unique_id) + " | played_interval " + str(played_interval) + " | planned interval " + str(self.planned_interval))

    def remove_card(self):
        del self.cards[0]
