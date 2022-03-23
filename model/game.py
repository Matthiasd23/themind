from mesa import Model, Agent
from mesa.time import BaseScheduler
import random
import model.round as round
#import model.default_player as default_player

class Game(Model):
    """
    Model in which the game is played, coördinating the different rounds
    """
    def __init__(self):
        self.num_players = 0
        self.schedule = BaseScheduler(self)
        self.num_lives = 0
        self.num_rounds = 0
        self.current_round = 1

    def init_players(self):
        self.num_players = random.choice([2,3,4])
        ## for i in range(self.num_players):
            ## agent = Default_player(i, self)
            ## self.schedule.add(agent)

    def init_lives(self):
        self.num_lives = self.num_players

    def init_rounds(self):
        round_distribution = [0, 0, 12, 10, 8]
        self.num_rounds = round_distribution[self.num_players]

    def step(self):
        """Advancing the model by one step"""
        if (self.current_round <= self.num_rounds):
            next_round = round.Round(self)
            next_round.play()
            self.current_round += 1
