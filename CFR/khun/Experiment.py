from copy import deepcopy
from attr import *
from Environment import *
from tqdm import tqdm
def traverse(a, env, i, players):
    env = deepcopy(env)
    r = dict()
    g = 0
    if a is not None: env.process_action(i, a)
    if env.is_terminal(): return env.utility()[i]

    infoset = env.N[i].I

    t = env.get_next_turn()
    while t != i:
        if env.is_terminal(): return env.utility()[i]
        if t != 'c':
            a = players[t].sample(infoset)
            prob = players[t].get_action_probability(infoset, a)
            players[t].accum_pol(infoset, a, prob)
        else: a = env.N['c'].sample()

        env.process_action(t, a)
        if env.is_terminal(): return env.utility()[i]
        t = env.get_next_turn()

    for a in players[i].c_Regret[env.N[i].I].keys():
        r[a] = traverse(a, env, i, players)
        g += r[a] * (players[i].get_action_probability(infoset, a))

    for a in players[i].c_Regret[infoset].keys():
        reg = r[a] - g
        players[i].update(infoset, a, reg)

    return g



if __name__ == '__main__':
    players = {1: Player(1), 2: Player(2), 'c': Chance()}
    env = KhunEnv(players)
    for t in tqdm(range(100000)):
        for j in range(1, 3, 1):
            traverse(None, env, j, players)
    print(players[1].get_average_strategy())
    print(players[1].count)
    print(players[2].get_average_strategy())
    print(players[2].count)



