from attr import *
from Environment import *
from tqdm import tqdm
from Experiment import traverse
import numpy as np
class Play_test:
    def __init__(self):
        pass
    def sample(self):
        return np.random.choice([0,1,2], p = [0.40127352064, 0.2649362658162378, 0.33379021354376215], size = 1)[0]
def take_action(p_id, player, history, p1_turn = False, a = None):
    if p_id == 'c':
        return player.sample(history)
    else:
        return player.sample(get_infoset(history, p_id))
"""
    if p_id == 'c':
        return player.sample(history)
    elif p_id == 1:
        if not p1_turn:
            a = player.sample()

        if a == 0:
            return 'B'
        elif a == 1:
            if history[-1] == 'B':
                return 'F'
            else:
                return 'P'
        else:
            if history[-1] == 'B':
                return 'C'
            else:
                return 'P'
    else:
        return player.sample(get_infoset(history, p_id))
"""

def get_strategies():
    players = {1: Player(1), 2: Player(2), 'c': Chance()}

    for t in tqdm(range(100000)):
        for j in range(1, 3, 1):
            traverse(tuple(), j, get_next_turn(tuple()), players)
    return players[1].get_average_strategy(), players[2].get_average_strategy()

if __name__ == '__main__':
    p1, p2 = get_strategies()
    #players = {1: Play_test(), 2: Player(2, a_pol = p2, play_average_pol= True), 'c': Chance()}
    players2 = {1: Player(1, a_pol = p1, play_average_pol= True), 2: Player(2, a_pol=p2, play_average_pol=True), 'c': Chance()}
    trials = 80000
    cumulative_util = {1:0, 2:0}
    history = tuple()
    print(p1, p2)
    """
    for i in range(trials):
        history = tuple()
        ac = None
        p1_turn = False
        while not is_terminal(history):
            turn = get_next_turn(history)
            action = take_action(turn, players[turn], history, p1_turn = p1_turn, a = ac)
            if turn == 1:
                p1_turn = True
                ac = action

            history = update_history(history, action)
        cumulative_util[1] += utility(history)[1]
        cumulative_util[2] += utility(history)[2]
        """


    for i in range(trials):
        history = tuple()
        while not is_terminal(history):
            turn = get_next_turn(history)
            action = take_action(turn, players2[turn], history)
            history = update_history(history, action)
        cumulative_util[1] += utility(history)[1]
        cumulative_util[2] += utility(history)[2]

    print(f"Average return for p1 = {cumulative_util[1]/trials}, p2 = {cumulative_util[2]/trials}")





































































































