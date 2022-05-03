import random
from itertools import islice
from mesa import Model


class Round(Model):
    """
    Model in which each round is played, retrieving and processing input from players
    """

    def __init__(self, g):
        self.g = g
        self.card_list = list(range(1, 101))
        self.cards_in_game = g.num_players * g.round_num
        self.pile = 0  # card on top of the pile (last card that was played)
        self.max_interval = 101
        self.threshold = 1

    def run_model(self):
        random.shuffle(self.card_list)
        card_listt = iter(self.card_list)
        for player in self.g.players:
            """
            distribute the shuffled cards from the top up until how many cards are needed
            """
            player.cards = list(islice(card_listt, self.g.round_num))
            player.order_cards()  # order cards in ascending order
        while self.cards_in_game > 0 and not self.g.lost:
            self.process_cards()

    def process_cards(self):
        """
        Retrieve all waiting time of players and storing them in wait_list, find lowest and thus also the card that is played
        When one of the waiting time is lower than the threshold, a card is played
        """
        wait_list = []
        time = 1
        for interval in range(1, self.max_interval):
            wait_list = []
            for player in self.g.players:
                waiting_time = player.get_active(interval)
                wait_list.append(waiting_time)
            if min(wait_list) < self.threshold:
                # print("interval: " + str(interval))
                time = interval
                break
        """
        finding the playing agent by accessing the index of the waiting list with the lowest waiting
        """
        print(wait_list)
        var = wait_list.index(min(wait_list))
        playing_agent = self.g.players[var]
        played_card = playing_agent.cards[0]
        self.update_pile(played_card,playing_agent, time)

    def update_pile(self, card, agent, time):
        """
        Updating the pile after a card is played, and updating agents if necessary
        """
        # a card is played so the copycat agents are to be updated
        for player in self.g.players:
            if not player == agent:
                player.update_vars(card,self.pile,time)
        self.pile = card
        self.print_output(agent)
        agent.remove_card()
        self.cards_in_game -= 1

        self.process_mistake(agent)  # handle possible mistakes
        print(" ")

    def process_mistake(self, agent):
        """
        If mistake has been made, remove cards that were supposed to be
        played instead of current one and adjust lives + cards left
        agent is the player that played the card
        """
        mistake_checker = 0
        for player in self.g.players:
            for card in player.cards[:]:  # traverse copy of list to avoid skipping
                # player die op had moeten gooien
                if card < self.pile:
                    # player onthouden en eventueel in een lijst > meteen passive aanpassen
                    print("MISTAKE - " + str(card) + " (agent " + str(player.unique_id)
                          + ") | " + str(self.pile) + " (pile)")
                    player.shouldve_thrown(time)       # Player that was too late
                    agent.wrong_throw(time)            # Agent that was too fast
                    player.cards.remove(card)
                    mistake_checker += 1
                    P = player.get_passive()
                    print(P)

        # if mistake checker is 1
        if mistake_checker > 0:
            self.cards_in_game -= mistake_checker  # adjust the number of cards left in game
            self.g.num_lives -= 1
            print("Lives left: " + str(self.g.num_lives))
            if self.g.num_lives == 0:
                self.g.end_game()

    def print_output(self, playing_agent):
        """
        Print some output for a clear overview of what is happening in the game
        """
        for player in self.g.players:
            print("Cards agent " + str(player.unique_id) + player.type + ": " + str(player.cards))
        print("---------------------------\n"
              + "Card played: " + str(self.pile) + " by agent " + str(playing_agent.unique_id)
              + "\n---------------------------")
