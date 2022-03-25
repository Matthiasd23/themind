from mesa import Model, Agent
from mesa.time import BaseScheduler
import random
import model.round as round
import model.agents.basicAgent as bA

class Game(Model):
    """
    Model in which the game is played, coördinating the different rounds
    """
    def __init__(self):
        self.players = []
        self.schedule = BaseScheduler(self)
        self.init_players()
        self.num_lives = self.num_players
        self.init_rounds()
        self.round_num = 1
        self.present = round.Round(self)

    """
    Initializing the players, different possibilities
    For now it is a random number of players from 2-4
    """
    def init_players(self):
        self.num_players = random.choice([2,3,4])
        self.players = []
        for i in range(self.num_players):
            agent = bA.basicAgent(i, self)
            self.schedule.add(agent)
            self.players.append(agent)

    """
    Initializing the number of levels that need to be played 
    based on the number of players
    """
    def init_rounds(self):
        round_distribution = [0, 0, 12, 10, 8]
        self.num_rounds = round_distribution[self.num_players]

    def run_model(self):
        """Running all rounds of the game"""
        while (self.round_num <= self.num_rounds):
            self.present = round.Round(self)
            self.present.run_model()
            self.round_num += 1

