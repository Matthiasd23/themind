from mesa import Model, Agent
from mesa.time import BaseScheduler
import model.game as game
import random

class Round(Model):
    """
    Model in which each round is played, retrieving and processing input from players
    """
    def __init__(self, g):
        self.g = g
        self.card_list = list(range(1, 100))
        self.cards_in_game = g.num_players * g.current_round


    def play(self):
        random.shuffle(self.card_list)
        print(1)

    def distribute_cards(self):
        card_listt = iter(self.card_list)
        for player in self.g.players:
            """
            distribute the shuffled cards from the top up until how many cards are needed
            """
            player.cards = list(islice(card_listt, self.g.current_round))
            print(player.cards)
        """
        Have the player order the cards to have the lowest card in the lowest index
        """
        player.order_cards()

    def process_cards(self):
        pass
