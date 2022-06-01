import random

from model.agents.superAgent import SuperAgent


class Statistician(SuperAgent):
    """
    Agent that uses statistics to decide on playing
    """

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model, " (Statistician)", 0.25)
        self.repeats = 100  # no. of simulations

    def calc_interval(self):
        """
        method to calculate the interval to play in based on a number of
        simulations
        """
        round = self.model.present
        smaller_count = 0
        total = list(range(0, 101))
        remove = list(range(0, round.pile + 1)) + self.cards  # cards not part of population
        cards_in_play = round.cards_in_game - len(self.cards)
        population = [i for i in total if i not in remove]  # removing cards
        if len(population) != 0:
            for i in range(1, self.repeats):
                X = random.sample(population, cards_in_play)
                #random.shuffle(population)
                #X = population[0:cards_in_play+1]
                for c in X:
                    if c < self.cards[0]:              # de kernvraag (Contributie door Lucas), "is er een kaart die lager is"
                        smaller_count += 1

        p = smaller_count / (self.repeats*cards_in_play)  # chance of smaller card occurring
        # Adding the passive scaling the interval
        self.planned_interval = int(p * (100 - round.pile) * self.P * self.counting_speed) + 1  # conversion to interval to wait for (+1) shou
        #print("diff: " + str(self.diff) + " | planned interval: " + str(self.planned_interval))

    def get_active(self, i):
        if self.last_one_standing():
            return 0

        round = self.model.present
        if i == 1:
            self.determine_difference()
            self.planned_interval = 200
            if len(self.cards) != 0:
                self.calc_interval()

        if i == self.planned_interval:
            certainty = 1 - self.diff * 2 / 100  # slight differentiation to avoid identical waiting times
            # print("diff: " + str(self.diff) + " | certainty: " + str(certainty))
            return round.threshold - certainty
        else:
            return 10000
