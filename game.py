from mesa import Model
from mesa import Agent

class Game(Model):
    """
    Model in which the game is played, coördinating the different rounds
    """
    def __init__(self):
        self.Agents
