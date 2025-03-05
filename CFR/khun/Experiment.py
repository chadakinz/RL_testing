from copy import deepcopy
from attr import *
from Environment import *
from tqdm import tqdm
def traverse(history, i, curr_player, players):
    if is_terminal(history): return utility(history)[i]

    infoset = get_infoset(history, curr_player)

    if curr_player == i:
        action_utilities = dict()
        counterfactual_value = 0
        for a in players[i].c_Regret[infoset].keys():
            next_history = update_history(history, a)
            action_utilities[a] = traverse(next_history, i, get_next_turn(next_history), players)
            counterfactual_value += action_utilities[a] * (players[i].get_action_probability(infoset, a))

        for a in players[i].c_Regret[infoset].keys():
            regret = action_utilities[a] - counterfactual_value
            players[i].update(infoset, a, regret)

        return counterfactual_value

    else:
        if curr_player != 'c':
            a = players[curr_player].sample(infoset)
            prob = players[curr_player].get_action_probability(infoset, a)
            players[curr_player].accum_pol(infoset, a, prob)

        else:  a = players['c'].sample(history)

        next_history = update_history(history, a)
        next_player = get_next_turn(next_history)

        return traverse(next_history, i, next_player, players)


if __name__ == '__main__':
    players = {1: Player(1), 2: Player(2), 'c': Chance()}

    for t in tqdm(range(100000)):
        for j in range(1, 3, 1):
            traverse(tuple(), j, get_next_turn(tuple()), players)
    print(players[1].get_average_strategy())
    print(players[1].count)
    print(players[2].get_average_strategy())
    print(players[2].count)



