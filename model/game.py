from mesa import Model, Agent
import random
import sys
import model.round as round
import model.agents.basicAgent as bA


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
        for i in range(self.num_players):
            agent = bA.BasicAgent(i, self)
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
        if not self.lost:
            self.end_game()

    def start_game(self):
        print("START GAME | Players - " + str(self.num_players) + " | Lives - "
              + str(self.num_lives) + " | Rounds - " + str(self.num_rounds))

    def end_game(self):
        if self.num_lives == 0:
            print("\nEND GAME: LOST | Reached: round " + str(self.round_num) + " of " + str(self.num_rounds))
        else:
            print("\nEND GAME: WON | Lives left: " + str(self.num_lives))
        self.lost = True
        #sys.exit()  # is this an acceptable way of ending the program?
