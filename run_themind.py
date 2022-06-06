from model.game import Game
from model.agents.mathematician import Mathematician
import pandas as pd
win = 0
lose = 0

list1 = []
list2 = []
repeats = 100

for lower in range(1, 26):
    for upper in range(1, 26):
        total = 0
        for i in range(1, repeats):
            current_game = Game(lower, upper)
            current_game.run_model()
            if current_game.won:
                total += 1
        xrange = str(lower) + str(upper)
        list1.append(xrange)
        list2.append((total/repeats)*100)

col1 = "Thresholds"
col2 = "Win-%"
# col3 = "Win-% Upper"
# col4 = "Win-% No ninja"
data = pd.DataFrame({col1:list1,col2:list2})
data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)