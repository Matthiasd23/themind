from mesa import Model, Agent
from mesa.time import BaseScheduler
import model.game as game
import random
from itertools import islice

class Round(Model):
    """
    Model in which each round is played, retrieving and processing input from players
    """
    def __init__(self, g):
        self.g = g
        self.card_list = list(range(1, 100))
        self.cards_in_game = g.num_players * g.round_num
        self.pile = 0                                           ## card on top of the pile (last card that was played)


    def run_model(self):
        random.shuffle(self.card_list)
        card_listt = iter(self.card_list)
        for player in self.g.players:
            """
            distribute the shuffled cards from the top up until how many cards are needed
            """
            player.cards = list(islice(card_listt, self.g.round_num))
            player.order_cards()                                ## order cards in ascending order
        while (self.cards_in_game > 0):
            self.process_cards()

    def process_cards(self):
        wait_list = []
        for player in self.g.players:
            print("Cards agent " + str(player.unique_id) + ": " + str(player.cards))
            waiting_time = player.get_active()
            wait_list.append(waiting_time)
        lowest_time = wait_list.index(min(wait_list))
        playing_agent = self.g.players[lowest_time]
        self.pile = playing_agent.cards[0]
        print("---------------------------")
        print("Card played: " + str(self.pile) + " by agent " + str(playing_agent.unique_id))
        print("---------------------------\n")

        playing_agent.remove_card()
        self.cards_in_game -= 1
        if self.check_for_mistakes(self.pile):
            print("Mistakes were made")

    def check_for_mistakes(self, x):
        for player in self.g.players:
            if (any(card < x for card in player.cards)):
                return True
