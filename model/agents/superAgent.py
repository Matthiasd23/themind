from mesa import Agent
import numpy as np

class SuperAgent(Agent):
    """
    Possible superclass for all agents
    """

    def __init__(self, unique_id, model, Type, adaptability):
        super().__init__(unique_id, model)
        # general variables
        self.cards = []
        self.diff = 0
        self.std = 0.05
        self.P = 1
        self.planned_interval = 0
        # self.playing = True

        # ninja-star variables
        self.ninja_list = []
        self.ninja_index = -1
        self.ninja_speed = 1
        self.ninja_lower_threshold = 10
        self.ninja_upper_threshold = 20
        self.ninja_speed_interval = 0.1

        # variable variables
        self.type = Type
        self.adaptability = adaptability

    def order_cards(self):
        self.cards.sort()

    def remove_card(self):
        del self.cards[0]
        self.model.present.cards_in_game -= 1

    def determine_difference(self):
        if len(self.cards) != 0:
            self.diff = self.cards[0] - self.model.present.pile
        else:
            self. diff = 1000000

    def update_vars(self, c, pile, time):
        """
        method to update internal variables if needed
        """
        pass

    def find_avg_diff_cards(self):
        """
        method to find the average difference between the cards in the list
        """
        if len(self.cards) > 1:
            arr = np.array(self.cards)
            diff_list = np.diff(arr)
            return sum(diff_list)/len(diff_list)
        else:
            return 100

    def suggest_ninja(self):
        """
        method to either suggest a ninja star or not, the average difference in cards should be lower than the threshold
        """
        return (self.find_avg_diff_cards() < self.ninja_lower_threshold) and len(self.cards) > 2

    def ninja_suggestion(self):
        """
        method to react to ninja suggestion by other player (agree if under upper threshold)
        """
        return self.find_avg_diff_cards() < self.ninja_upper_threshold

    def set_ninja_speed(self, index):
        self.ninja_index = index-1
        x = self.ninja_speed_interval
        speed_list = [1, 1-x, 1-2*x, 1-3*x]
        self.ninja_speed = speed_list[index]

    def stop_ninja(self):
        self.ninja_list = []
        self.ninja_index = -1
        self.ninja_speed = 1

    def update_ninja(self):
        if len(self.ninja_list) != 0 and len(self.cards) != 0 and self.ninja_index > -1 and self.cards[0] > \
                self.ninja_list[self.ninja_index][0]:
            print("lowest card: " + str(self.cards[0]) + " goal card: " + str(self.ninja_list[self.ninja_index][0]))
            self.ninja_speed += self.ninja_speed_interval
            print("agent: " + str(self.unique_id) + " speed: " + str(self.ninja_speed))
            self.ninja_index -= 1
            self.update_ninja()
            if self.ninja_index == -1:
                print("STOP")
                self.stop_ninja()

    def get_passive(self):
        return self.P

    def wrong_throw(self, card, pile):
        """
        The passive variable (P) is adjusted based on card that shouldve been played and the card that was (wrongfully) played
        Multiplied by adaptability (0.5 / 50%)
        The player should be be playing slower (higher P) because he threw too soon
        """
        self.P = self.P + ((1 - (card / pile)) * self.adaptability)

    def shouldve_thrown(self, played_interval):
        """
        The passive variable (P) is adjusted based on the interval that was played and the interval the agent planned to play
        adjusting P to instead play the interval before the one that was actually played, multiplied by the adaptibility
        The player should be be playing faster (lower P) because he threw too late
        """
        goal_interval = played_interval
        self.P = self.P - ((1 - (goal_interval / self.planned_interval)) * self.adaptability)