from model.game import Game
from model.agents.mathematician import Mathematician
import pandas as pd
win = 0
lose = 0
upper = 15

list1 = list(range(1, 26))
list2 = []
list3 = []
list4 = []
repeats = 100

for lower in range(1, 26):
    total = 0
    for i in range(1, repeats):
        current_game = Game(lower, upper)
        current_game.run_model()
        if current_game.won:
            total += 1
    list2.append((total/repeats)*100)

lower = 7
for up in range(1, 26):
    total = 0
    for i in range(1, repeats):
        current_game = Game(lower, up)
        current_game.run_model()
        if current_game.won:
            total += 1
    list3.append((total/repeats)*100)

for up in range(1, 26):
    total = 0
    for i in range(1, repeats):
        current_game = Game(100, 100)
        current_game.run_model()
        if current_game.won:
            total += 1
    list4.append((total/repeats)*100)

col1 = "Value"
col2 = "Win-% Lower"
col3 = "Win-% Upper"
col4 = "Win-% No ninja"
data = pd.DataFrame({col1:list1,col2:list2,col3:list3,col4:list4})
data.to_excel('sample_data.xlsx', sheet_name='sheet1', index=False)