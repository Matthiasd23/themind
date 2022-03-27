from mesa import Model, Agent
from mesa.time import BaseScheduler
import random
import sys
import model.round as round
import model.agents.basicAgent as bA

class Game(Model):
    """
    Model in which the game is played, coördinating the different rounds
    """
    def __init__(self):
        self.players = []
        self.schedule = BaseScheduler(self)             # standard scheduler; do we use this?
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
        self.start_game()
        while (self.round_num <= self.num_rounds):
            self.present = round.Round(self)
            print("\nROUND " + str(self.round_num))
            self.present.run_model()
            self.round_num += 1
        self.end_game()

    def start_game(self):
        print("START GAME | Players - " + str(self.num_players) + " | Lives - "
            + str(self.num_lives) + " | Rounds - " + str(self.num_rounds))

    def end_game(self):
        round_distribution = [0, 0, 12, 10, 8]
        if self.num_lives == 0:
            print("\nEND GAME: LOST, lives left: 0")
        else:
            print("\nEND GAME: WON, lives left: " + str(self.num_lives))
        sys.exit()                                        # is this an acceptable way of ending the program?
