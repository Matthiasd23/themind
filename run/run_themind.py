import sys
import os

# current directory
current = os.path.dirname(os.path.realpath(__file__))
# parent directory
parent = os.path.dirname(current)
# adding parent directory to sys.path
sys.path.append(parent)
# import game.py
import model.game as game

current_game = game.Game()
current_game.init_players()
current_game.init_lives()
current_game.init_rounds()
for i in range(current_game.num_rounds):
    current_game.step()
