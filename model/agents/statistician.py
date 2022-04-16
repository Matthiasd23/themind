from mesa import Model, Agent
import random

class Statistician(Agent):
    """
    Agent that uses statistics to decide on playing
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cards = []
        self.diff = 0
        self.playing = True
        self.play_interval = 200
        self.type = " (Statistician)"

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
    def update_vars(self):
        pass


    def calc_interval(self):
        round = self.model.present
        list_smaller = []
        total = list(range(0, 101))
        remove = list(range(0, round.pile+1)) + self.cards # cards not part of population
        population = [i for i in total if i not in remove] # removing cards
        if len(population) != 0:
            for i in range(1,1000):
                X = random.choice(population)
                if X < self.cards[0]:
                    list_smaller.append(X)

        p = len(list_smaller)/1000 # chance of smaller card occurring
        self.play_interval = int(p * (100 - round.pile)) + 1 # conversion to interval to wait for


    def get_active(self,i):
        round = self.model.present
        if i == 1:
            self.determine_difference()
            self.play_interval = 200
            if len(self.cards) != 0:
                self.calc_interval()
                print("agent: " + str(self.unique_id) + " | interval: " + str(self.play_interval))

        if i == self.play_interval:
            certainty = 1 - self.diff / 100
            return (round.threshold - certainty)
        else:
            return 1000000


    def get_passive(self):
        pass

    def remove_card(self):
        del self.cards[0]
