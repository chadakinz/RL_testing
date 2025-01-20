import numpy as np
import matplotlib.pyplot as plt

class Stock:
    def __init__(self):
        pass

class Environment:
    def __init__(self, alpha, theta, n, exp_t, del_t, seed=101):
        self.max_inventory = n
        self.inventory = [0] * exp_t
        self.transit = [0] * del_t
        self.tot_inventory = 0
        self.actions = [x for x in range(n)]
        #self.actions = self.customers = [x for x in range(n)]
        self.alpha = alpha
        self.theta = theta
        self.rng = np.random.default_rng(seed)
        self.exp_t = exp_t
        self.del_t = del_t
        self.action_space = []

    def buy_inventory(self, amount):
        self.action_space.append(amount)
        self.transit[0] += amount


    def get_customer(self):

        return round(self.rng.gamma(self.alpha, self.theta, size = 1)[0])

    def order(self, num_customers):
        n = num_customers
        i = self.exp_t - 1

        while n != 0 and i > 0:

            if n > self.inventory[i]:

                n -= self.inventory[i]
                self.tot_inventory -= self.inventory[i]
                self.inventory[i] = 0
                i -= 1

            else:
                self.inventory[i] -= n
                self.tot_inventory -= n
                n = 0


        print(f"n: {n}, inventory: {self.inventory}")
        if n > 0:
            return n
        else:
            return 0



    def action_outcome(self):
        num_customers = self.get_customer()

        TS = self.order(num_customers)
        TO = self.expire_stock()
        TM = self.move_stock()

        return TO, TS, TM

    def expire_stock(self):
        p1 = self.inventory[0]

        self.inventory[0] = 0

        for i in range(self.exp_t - 1):
            p2 = self.inventory[i + 1]
            self.inventory[i + 1] = p1
            p1 = p2

        self.tot_inventory -= p1



        return p1
    def move_stock(self):
        p1 = self.transit[0]

        self.transit[0] = 0
        for i in range(self.del_t - 1):
            p2 = self.transit[i + 1]
            self.transit[i + 1] = p1
            p1 = p2


        """
        if self.tot_inventory + p1 > max_inv:
            self.inventory[0] += max_inv - self.tot_inventory
            TM = abs(max_inv - (self.tot_inventory + p1))
            return TM
        """

        self.tot_inventory += p1
        self.inventory[0] += p1
        return 0

class Model:
    def __init__(self, actions, gamma, alpha, epsilon, dec_rate):
        self.actions = actions
        self.state_actions = np.zeros((20, 5, 40))
        self.state_action_distribution = np.zeros((20, 5, 40))
        self.state_action_distribution.fill(1/len(self.actions))
        self.current_SA = None
        self.alpha = [alpha, alpha]
        self.action_log = []
        self.gamma = gamma
        self.epsilon = [epsilon, epsilon]
        self.decay_rate = dec_rate
    def get_action(self, state):
        current_action = self.choose_action(state)
        self.action_log.append(current_action)
        self.current_SA = (state[0], state[1], current_action)
        return current_action

    def policy_update(self, reward, future_state, t):



        optimal_future_action = self.get_min_value(future_state)

        self.state_actions[self.current_SA] += (self.alpha[0] *
                                                              (reward + (self.gamma *
                                                                         self.state_actions[future_state][
                                                                             optimal_future_action]) -
                                                             self.state_actions[self.current_SA]))
        self.decay(t)


    def choose_action(self, state):
        #print(f"Epsilon: {self.epsilon[0]}")
        choice = np.random.choice([0, 1], size = 1, p = [self.epsilon[0], 1 - self.epsilon[0]])[0]
        if choice == 1:
            return self.get_min_value(state)
        else:
            return np.random.choice(self.actions, size=1, p=self.state_action_distribution[state])[0]

    def get_min_value(self, state):
        #print(self.state_actions[state])
        #print(np.argmin(self.state_actions[state]))
        return np.argmin(self.state_actions[state])

    def decay(self, t):
        y = (t ** 2)/(self.decay_rate + t)
        self.alpha[0] = self.alpha[1] /(1 + y)
        self.epsilon[0] = self.epsilon[1] / (1 + y)


def env_process(env, max_inv):
    inventory = min(round((20/max_inv) * env.tot_inventory), 19)

    array = np.array(env.inventory)

    indices = np.arange(len(array))
    total_weighted_index = np.sum(indices * array)

    total_count = np.sum(array)

    average_exp = round(total_weighted_index / total_count if total_count > 0 else 0)
    return inventory, average_exp

def process_action(action, max_action):
    return action
    #return round((max_action/40) * action)

if __name__ == "__main__":
    c_o = 1
    c_s = 2

    max_inv = 100
    max_action = 40
    env1 = Environment(4, 5, max_inv, 4, 2)

    model = Model([x for x in range(40)], .97, .4, .8, 1000000000000)

    reward_l = []
    average_cost = []
    trial = 800

    state = env_process(env1, max_inv)
    for i in range(trial):
        next_action = process_action(model.get_action(state), max_action)
        env1.buy_inventory(next_action)
        TO , TS , TM = env1.action_outcome()
        reward  = ((c_o * TO) + (c_s * TS ))
        reward_l.append(reward)
        average_cost.append(np.average(reward_l))
        state = env_process(env1, max_inv)
        model.policy_update(reward, state, i)


    time = np.arange(len(reward_l))
    """
    plt.plot(time, reward_l, marker='o', linestyle='-', color='b', label='Cost over time')
    plt.title('Graph of Reward vs Time', fontsize=14)
    plt.xlabel('Time (t)', fontsize=12)
    plt.ylabel('Reward', fontsize=12)
    plt.grid(True)  # Add a grid for better readability
    plt.legend()  # Add a legend
    plt.show()
    """
    #print(f"Action list: {env1.action_space}")
    plt.plot(time, average_cost, marker='o', linestyle='-', color='b', label='Average Cost over time')
    plt.title('Average cost vs Time', fontsize=14)
    plt.xlabel('Time (t)', fontsize=12)
    plt.ylabel('Average Cost', fontsize=12)
    plt.grid(True)  # Add a grid for better readability
    plt.legend()  # Add a legend
    plt.show()


