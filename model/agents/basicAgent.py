from mesa import Model, Agent
import numpy.random as npr
import math

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
        self.planned_interval = abs(npr.normal(self.diff*self.P, (self.diff) * 0.05))   # NOT CHANGING THE STD DEVIATION because it goes both ways
        return self.planned_interval - i

    def get_passive(self):
        return self.P

    def wrong_throw(self, played_interval):
        """
        The passive variable (P) is adjusted scaled with the number of mistakes, and the difference in card (and maybe the level should influence the scale?)
        The player should be be playing slower (higher P) because he threw too soon
        """
        goal_interval = played_interval - 1
        self.P = self.P + ((1 - (goal_interval / self.planned_interval)) * 0.5)

    def shouldve_thrown(self, played_interval):
        """
        The passive variable (P) is adjusted scaled with the number the difference in card (and maybe the level should influence the scale?)
        The player should be be playing faster (lower P) because he threw too late
        """
        goal_interval = played_interval - 1
        self.P = self.P - ((1 - (goal_interval / self.planned_interval)) * 0.5)

    def remove_card(self):
        del self.cards[0]
