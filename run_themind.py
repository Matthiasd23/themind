from model.game import Game
from model.agents.mathematician import Mathematician

win = 0
lose = 0
round_reached = []
for i in range(1, 101):
    current_game = Game()
    current_game.run_model()
    if current_game.won:
        win += 1
    else:
        lose += 1

print("Win %: " + str(win/(win+lose) * 100) + "%")