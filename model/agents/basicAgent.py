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

    def get_active(self, i):
        """
        return the time the agent will wait with a little bit of deviation
        """
        self.determine_difference()
        output = abs(npr.normal(self.diff, (self.diff) * 0.05))
        # Two possible additions of the passive variable P:
        # output = abs(npr.normal(self.diff*P, (self.diff) * 0.05))
        # output = abs(npr.normal(self.diff*P, (self.diff*P) * 0.05))
        if (output - i < 1):
            print("interval " + str(i) + " diff " + str(self.diff))
        return output - i

    def get_passive(self):
        return P

    def wrong_throw(self, agent, mistakes, pile):
        """
        The passive variable (P) is adjusted scaled with the number of mistakes, and the difference in card (and maybe the level should influence the scale?)
        The player should be be playing slower (higher P) because he threw too soon
        """
        # maybe look at the cards that were lower than the card that the player threw up
        self.P = self.P + (0.05*mistakes)

    def shouldve_thrown(self, agent, pile):
        """
        The passive variable (P) is adjusted scaled with the number the difference in card (and maybe the level should influence the scale?)
        The player should be be playing faster (lower P) because he threw too late
        """
        diff = pile - self.cards[0]
        self.P = self.P - (diff/pile)

    def remove_card(self):
        del self.cards[0]
