from mesa import Model, Agent

class basicAgent(Agent):
    """
    Most basic agent just to be able to run the basic game
    Counts down the difference between the cards
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.cards = []
        self.diff = 0
        ##self.playing = True

    def order_cards(self):
        self.cards.sort()

    def determine_difference(self):
        if len(self.cards) != 0:
            self.diff = self.cards[0] - self.model.present.pile
        else:
            self.diff = 1000000
            ##self.playing = False

    def get_active(self):
        self.determine_difference()
        return self.diff

    def remove_card(self):
        del self.cards[0]
