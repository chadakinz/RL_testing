def result(history):
    if history[0] == 'K': return 1, 2
    elif history[1] == 'K': return 2, 1
    elif history[0] == 'Q': return 1, 2
    elif history[1] == 'Q': return 2, 1

def get_next_turn(history):

    if len(history) < 2:

        return 'c'
    elif len(history) == 2 or len(history) == 4:
        return 1
    else:
        return 2

def get_infoset(history, i):
    """
    :param history: History of the current subtree
    :param i: Player id
    :return: Infoset for player i
    """
    if i == 1:
        if len(history) > 2:
            infoset = (history[0],) + (history[2:])
        else:
            infoset = (history[0],)

    else:
        infoset = history[1:]

    return infoset

def update_history(history, action):
    return history + (action,)

def is_terminal(history) -> bool:

    if history is None or len(history) <= 3:
        return False
    elif len(history) == 4:
        if history[3] == 'P' or history[3] == 'C' or history[3] == 'F':
            return True
        else:
            return False
    else:
        return True

def utility(history) -> dict:
    u = dict()
    winner, looser = result(history)

    if history[3] == 'C':
        u[winner] = 2
        u[looser] = -2
    elif history[3] == 'F':
        u[1] = 1
        u[2] = -1
    elif history[3] == 'P':
        u[winner] = 1
        u[looser] = -1
    elif history[4] == 'C':
        u[winner] = 2
        u[looser] = -2
    elif history[4] == 'F':
        u[1] = -1
        u[2] = 1
    return u

def possible_actions(I) -> dict:
    """
    :param I:
    :return dictionary that maps a|I to R(I,a) set to  0 initially:
    """
    if len(I) == 1:
        return {'P': 0, 'B': 0}
    elif len(I) == 2:
        if I[1] == 'B':
            return {'F': 0, 'C': 0}

        elif I[1] == 'P':
            return {'P': 0, 'B': 0}
    elif len(I) == 3:
        return {'F': 0, 'C': 0}


