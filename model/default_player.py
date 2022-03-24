from mesa import Model, Agent


class boringAgent(Agent):
    """
    Most basic agent just to be able to run the basic game
    Counts down the difference between the cards
    """

    def __init__(self):

