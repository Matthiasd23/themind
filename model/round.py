from mesa import Model, Agent
from mesa.time import BaseScheduler
import model.game as game
import random

class Round(Model):
    """
    Model in which each round is played, retrieving and processing input from players
    """
    def __init__(self, game):
        self.card_list = list(range(1, 100))
        self.cards_in_game = game.num_players * game.current_round

    def play(self):
        random.shuffle(self.card_list)
        print(1)
