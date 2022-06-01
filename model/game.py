import random

from mesa import Model

import model.round as round
from model.agents.basicAgent import BasicAgent
from model.agents.copyCat import CopyCat
from model.agents.statistician import Statistician
from model.agents.uncertainOne import UncertainOne
from model.agents.mathematician import Mathematician


class Game(Model):
    """
    Model in which the game is played, coordinating the different rounds
    """

    def __init__(self):
        self.num_players = None
        self.num_rounds = None
        self.players = []
        self.init_players()
        self.num_lives = self.num_players
        self.num_shuriken = 1
        self.init_rounds()
        self.round_num = 1
        self.present = round.Round(self)
        self.lost = False

    def init_players(self):
        """
        method to initialize the players, different possibilities
        For now it is a random number of players from 2-4
        """
        self.num_players = random.choice([2, 3, 4])
        self.players = []
        class_list = [BasicAgent, UncertainOne, Statistician, CopyCat]
        for i in range(self.num_players):
            current_class = random.choice(class_list)
            # current_class = class_list[2]
            agent = current_class(i, self)
            self.players.append(agent)

    def init_rounds(self):
        """
        method to initialize the number of levels that need to be played
        based on the number of players
        """
        round_distribution = [0, 0, 12, 10, 8]
        self.num_rounds = round_distribution[self.num_players]

    def run_model(self):
        """method to run all rounds of the game"""
        self.start_game()
        while self.round_num <= self.num_rounds and not self.lost:
            self.present = round.Round(self)
            #print("\nROUND " + str(self.round_num))
            self.present.run_model()
            self.round_num += 1
            if self.round_num == 4 or self.round_num == 7 or self.round_num == 10:
                self.num_lives += 1
            if self.round_num == 3 or self.round_num == 6 or self.round_num == 9:
                self.num_shuriken += 1
        self.end_game()

    def start_game(self):
        """
        method to print information when starting game
        """
        #print("START GAME | Players - " + str(self.num_players) + " | Lives - "
         #     + str(self.num_lives) + " | Rounds - " + str(self.num_rounds))

    def end_game(self):
        """
        method to print information when ending game
        """
        if not self.lost:
            if self.num_lives == 0:
                i = 0
                #print("\nEND GAME: LOST | Reached: round " + str(self.round_num) + " of " + str(self.num_rounds)
                   #   + " | Shuriken left: " + str(self.num_shuriken))
            else:
                #print("\nEND GAME: WON | Lives left: " + str(self.num_lives) + " | Shuriken left: " + str(
                    #self.num_shuriken))
                self.won = True
            self.lost = True
