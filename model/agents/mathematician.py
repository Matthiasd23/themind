from mesa import Model, Agent
import random

class Mathematician(Agent):
    """
    Agent that uses probability calculation to decide on playing
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cards = []
        self.diff = 0
        self.playing = True

    def order_cards(self):
        self.cards.sort()

    def determine_difference(self):
        self.playing = True
        if len(self.cards) != 0:
            self.diff = self.cards[0] - self.model.present.pile
        else:
            self.playing = False

    """
    Use probability formula: P = (count of favourable outcomes / total count of
    outcomes) ^ number of repeats
    Probability of waiting: P = (lowest card - pile - 1) / (100 - pile - len(cards))
    """
    def calc_prob(self):
        round = self.model.present
        total_outcome = 100 - round.pile - len(self.cards) # possible cards (higher than pile, not in own
        fav_outcome = self.cards[0] - round.pile - 1 # possible cards higher than own lowest
        repeats = 1
        if round.cards_in_game - len(self.cards) > 0:
            repeats = round.cards_in_game - len(self.cards) # number of cards in other hands
        return pow((fav_outcome / total_outcome), repeats)


    def get_active(self,i):
        self.determine_difference()
        play = self.model.present.threshold
        wait = 10000

        if self.playing:
            wait_weight = self.calc_prob()
            print("agent: " + str(self.unique_id) + " wait weight: " + str(wait_weight))
            play_weight = 1 - wait_weight
            choice = random.choices([play, wait], weights=(play_weight, wait_weight))
            # certainty added to make sure the lowest card is played if two agents do decide to play at the same time
            certainty = 1 - self.diff / 100
            return choice[0] - certainty
        else:
            return 100000000

    def get_passive(self):
        pass

    def remove_card(self):
        del self.cards[0]
