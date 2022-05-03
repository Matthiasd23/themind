import numpy.random as npr
from mesa import Agent


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
        self.P = 1
        self.planned_interval = 0
        self.std = 0.05
        self.adaptability = 0.5
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
        return the time the agent will wait with a little bit of deviation
        """
        self.determine_difference()
        self.planned_interval = abs(npr.normal(self.diff * self.P, (
            self.diff) * self.std))  # NOT CHANGING THE STD DEVIATION because it goes both ways
        return self.planned_interval - i

    def get_passive(self):
        return self.P

    def wrong_throw(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        The player should be be playing slower (higher P) because he threw too soon
        """
        goal_interval = played_interval - 1
        self.P = self.P + ((1 - (goal_interval / self.planned_interval)) * self.adaptability)
        print("agent (early)" + str(self.unique_id) + " | played_interval " + str(played_interval) + " | planned interval " + str(self.planned_interval))

    def shouldve_thrown(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        The player should be be playing faster (lower P) because he threw too late
        """
        goal_interval = played_interval - 1
        self.P = self.P - ((1 - (goal_interval / self.planned_interval)) * self.adaptability)
        print("agent (late) " + str(self.unique_id) + " | played_interval " + str(played_interval) + " | planned interval " + str(self.planned))

    def remove_card(self):
        del self.cards[0]
