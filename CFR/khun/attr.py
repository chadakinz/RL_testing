import numpy as np
from Environment import possible_actions

class Dict(dict):
    def __init__(self):
        super().__init__()

    def __setitem__(self, key, value):
        if key not in self:
            value2 = possible_actions(key)
            super().__setitem__(key, value2)
        super().__setitem__(key, value)

    def __getitem__(self, key):

        if key not in self:

            value = possible_actions(key)

            super().__setitem__(key, value)

        return super().__getitem__(key)


class Chance:
    def __init__(self):
        self.i = 'c'

    def sample(self, history):
        deck = ['J', 'Q', 'K']
        if len(history) == 0:
            return np.random.choice(['J', 'Q', 'K'], p = [1/3, 1/3, 1/3], size = 1)[0]
        else:
            deck.remove(history[0])
            return np.random.choice(deck, p = [1/2, 1/2], size = 1)[0]

class Player:
    def __init__(self, i, epsilon = .6, a_pol = None, play_average_pol = False):
        self.i = i
        self.c_Regret = Dict()  # Dictionary storing the cumulative regret for each action in every infoset.
        self.stake = 0  # How many chips we have staked in a given history
        self.I = None  # The infoset of player
        self.count = 0  # Counts how many nodes have been touched during our experiment
        self.c_Pol = Dict()  # Dictionary storing action distribution at each epoch T cumulatively.
        self.play_average_pol = play_average_pol
        self.average_pol = a_pol


    def update(self, I, a, r):
        """Accumulating regret given the action and infoset"""
        self.c_Regret[I][a] += r
        self.count += 1

    def accum_pol(self, I, a, prob):
        """Accumulate the probability of action a given infoset I. This will be used for computing the average strategy"""
        self.c_Pol[I][a] += prob

    def get_distribution(self, I):
        """Returns distribution of actions for the given infoset I, using regret matching"""
        R = sum(value for value in self.c_Regret[I].values() if value > 0)
        if R == 0:
            return self.get_random_distribution(I)
        else:
            return [action/R if action > 0 else 0 for action in self.c_Regret[I].values()]

    def get_actions(self, I):
        return [x for x in self.c_Regret[I].keys()]
    def sample(self, I):
        """Uses regret matching to sample an action at the given infoset """
        if self.play_average_pol:
            return np.random.choice(self.get_actions(I), p = list(self.average_pol[I].values()), size = 1)[0]
        else:
            return np.random.choice(self.get_actions(I), p = self.get_distribution(I), size = 1)[0]
    def get_random_distribution(self, I):
        """Used for cases when cumulative regret is below 0, or no actions have been sampled at the given infoset"""
        return [1/len(self.c_Regret[I]) for i in range(len(self.c_Regret[I]))]

    def get_action_probability(self, I, a):
        """Returns the probabilty of an action given the infoset using the regret matching method"""
        R = sum(value for value in self.c_Regret[I].values() if value > 0)
        if R == 0:
            return 1/len(self.c_Regret[I])
        elif self.c_Regret[I][a] < 0: return 0
        else:
            return self.c_Regret[I][a]/R

    def get_average_strategy(self):
        """We get our average strategy by averaging the probabilities of the actions taken during each step t"""
        a_Pol = Dict()
        for I in self.c_Pol.keys():
            n_sum = 0
            for a in self.c_Pol[I].keys():
                n_sum += self.c_Pol[I][a]

            for a in self.c_Pol[I].keys():
                if n_sum != 0:
                    a_Pol[I][a] = self.c_Pol[I][a]/n_sum
                else:
                    a_Pol[I][a] = 1/len(self.c_Pol[I])
        return a_Pol
