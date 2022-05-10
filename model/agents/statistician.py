import random

from mesa import Agent


class Statistician(Agent):
    """
    Agent that uses statistics to decide on playing
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cards = []
        self.diff = 0
        self.playing = True
        self.planned_interval = 200
        self.type = " (Statistician)"
        self.P = 1
        self.repeats = 250
        self.adaptability = 0.25

    def order_cards(self):
        self.cards.sort()

    def determine_difference(self):
        self.playing = True
        if len(self.cards) != 0:
            self.diff = self.cards[0] - self.model.present.pile
        else:
            self.playing = False

    """
    method to update internal variables if needed
    """

    def update_vars(self, c, pile, time):
        pass

    def calc_interval(self):
        round = self.model.present
        list_smaller = []
        total = list(range(0, 101))
        remove = list(range(0, round.pile + 1)) + self.cards  # cards not part of population
        population = [i for i in total if i not in remove]  # removing cards
        if len(population) != 0:
            for i in range(1, self.repeats):
                X = random.choice(population)
                if X < self.cards[0]:
                    list_smaller.append(X)

        p = len(list_smaller) / self.repeats  # chance of smaller card occurring
        # Adding the passive scaling the interval
        self.planned_interval = int(p * (100 - round.pile) * self.P) + 1  # conversion to interval to wait for

    def get_active(self, i):
        round = self.model.present
        if i == 1:
            self.determine_difference()
            self.planned_interval = 200
            if len(self.cards) != 0:
                self.calc_interval()

        if i == self.planned_interval:
            certainty = 1 - self.diff / 100
            return round.threshold - certainty
        else:
            return 1000000

    def get_passive(self):
        return self.P

    def wrong_throw(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        The player should be be playing slower (higher P) because he threw too soon
        """
        goal_interval = played_interval - 1
        self.P = self.P + ((1 - (goal_interval / self.planned_interval)) * self.adaptability)
        print("agent (early)" + str(self.unique_id) + " | played_interval " + str(
            played_interval) + " | planned interval " + str(self.planned_interval))

    def shouldve_thrown(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        adjusting P to instead play the interval before the one that was actually played, multiplied by the adaptibility
        The player should be be playing faster (lower P) because he threw too late
        """
        goal_interval = played_interval
        self.P = self.P - ((1 - (goal_interval / self.planned_interval)) * self.adaptability)
        print("agent (late) " + str(self.unique_id) + " | played_interval " + str(played_interval) + " | planned interval " + str(self.planned_interval))

    def remove_card(self):
        del self.cards[0]
