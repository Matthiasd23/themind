import random

from mesa import Model

from model.agents.basicAgent import BasicAgent
from model.agents.copyCat import CopyCat
from model.agents.statistician import Statistician
from model.agents.uncertainOne import UncertainOne
from model.agents.mathematician import Mathematician
import model.round as round


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
        self.init_rounds()
        self.round_num = 1
        self.present = round.Round(self)
        self.lost = False

    """
    Initializing the players, different possibilities
    For now it is a random number of players from 2-4
    """

    def init_players(self):
        self.num_players = random.choice([2, 3, 4])
        self.players = []
        class_list = [BasicAgent, UncertainOne, Statistician, CopyCat]
        for i in range(self.num_players):
            current_class = random.choice(class_list)
            # current_class = class_list[0]
            agent = current_class(i, self)
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
        while self.round_num <= self.num_rounds and not self.lost:
            self.present = round.Round(self)
            print("\nROUND " + str(self.round_num))
            self.present.run_model()
            self.round_num += 1
            if self.round_num == 4 or self.round_num == 7 or self.round_num == 10:
                self.num_lives = self.num_lives + 1
        if not self.lost:
            self.end_game()
            # Stars at the completion of level 2, level 5 and level 8

    def start_game(self):
        print("START GAME | Players - " + str(self.num_players) + " | Lives - "
              + str(self.num_lives) + " | Rounds - " + str(self.num_rounds))

    def end_game(self):
        if self.num_lives == 0:
            print("\nEND GAME: LOST | Reached: round " + str(self.round_num) + " of " + str(self.num_rounds))
        else:
            print("\nEND GAME: WON | Lives left: " + str(self.num_lives))
        self.lost = True
        # sys.exit()  # is this an acceptable way of ending the program? nee
