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
        self.threshold = 1
        self.ninja_active = False

    def run_model(self):
        """
        method to run the round while game has not been lost
        """
        random.shuffle(self.card_list)
        card_listt = iter(self.card_list)
        for player in self.g.players:
            player.cards = list(islice(card_listt, self.g.round_num))  # distribute the shuffled cards
            player.order_cards()  # order cards in ascending order
            player.playing = True
        while self.cards_in_game > 0 and not self.g.lost:
            self.process_cards()

    def process_cards(self):
        """
        method to retrieve all waiting time of players and store them in wait_list.
        When one of the waiting time is lower than the threshold, a card is played
        """
        wait_list = []
        time = 1
        for interval in range(1, 101):
            wait_list = []
            for player in self.g.players:
                if player.is_playing(interval):
                    waiting_time = player.get_active(interval)
                    wait_list.append((player.unique_id, waiting_time))
            wait_list.sort(key=lambda tup: tup[1])  # sort based on waiting time
            if wait_list[0][1] < self.threshold:
                # print("interval: " + str(interval))
                time = interval
                break
        """
        finding the playing agent by accessing the index of the waiting list with the lowest waiting
        """
        # print(wait_list)
        playing_agent = self.g.players[wait_list[0][0]]
        played_card = playing_agent.cards[0]
        self.update_pile(played_card, playing_agent, time)

    def update_pile(self, card, agent, time):
        """
        method to update the pile after a card is played, and update agents if necessary
        """
        # a card is played so the copycat agents are to be updated
        for player in self.g.players:
            if not player == agent:
                player.update_vars(card, self.pile, time)
        self.pile = card
        self.print_output(agent)
        agent.remove_card()

        self.process_mistake(agent, time)  # handle possible mistakes
        """ninja addition"""
        if not self.ninja_active and self.g.num_shuriken > 0:
            self.check_for_ninja()
        # print(" ")

    def process_mistake(self, agent, time):
        """
        method to remove cards that were supposed to be
        played instead of current one and adjust lives + cards left.
        Agent is the player that played the card
        """
        mistake_checker = 0
        for player in self.g.players:
            for card in player.cards[:]:  # traverse copy of list
                if card < self.pile:
                    print("MISTAKE - " + str(card) + " (agent " + str(player.unique_id)
                          + ") | " + str(self.pile) + " (pile)")
                    player.shouldve_thrown(time)  # Player that was too late
                    agent.wrong_throw(card, self.pile)  # Agent that was too fast
                    player.remove_card()
                    mistake_checker += 1

        # if mistake has been made
        if mistake_checker > 0:
            self.g.num_lives -= 1
            print("Lives left: " + str(self.g.num_lives))
            if self.g.num_lives == 0:
                self.g.end_game()

    def check_for_ninja(self):
        """
        method to check if someone would like to do a ninjastar suggestion by looping through the agents
        and finding one that is lower than a certain threshold
        """
        ninja = False
        reaction = True
        for player in self.g.players:
            if not ninja:
                ninja = player.suggest_ninja()  # check if someone wants to suggest ninja, returns boolean
            if reaction:
                reaction = player.ninja_suggestion()  # check if everyone okay with ninja, Returns a Boolean value
        if ninja and reaction:
            self.play_ninja()

    def play_ninja(self):
        """
        method to retrieve cards when ninja star is played
        and allow players to initialize their adjusted playing speeds
        based on the ninja star
        """
        self.ninja_active = True
        self.g.num_shuriken -= 1
        card_agent_list = []
        for player in self.g.players:
            card_agent_list.append((player.cards[0], player.unique_id))
            player.remove_card()
        card_agent_list.sort(key=lambda tup: tup[0], reverse=True) # sort list based on cards, descending order
        # print("NINJA STAR PLAYED: " + str(card_agent_list))
        i = 0
        for item in card_agent_list:
            agent = self.g.players[item[1]]
            agent.ninja_list = card_agent_list
            agent.set_ninja_speed(i)
            i += 1

    def print_output(self, playing_agent):
        """
        method to print some output for a clear overview of what is happening in the game
        """
        for player in self.g.players:
            print("Cards agent " + str(player.unique_id) + player.type + ": " + str(player.cards))
        print("---------------------------\n"
              + "Card played: " + str(self.pile) + " by agent " + str(playing_agent.unique_id)
              + "\n---------------------------")
