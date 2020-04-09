
import networkx
import random
from enum import Enum


class Status(Enum):
    NOT_DET = 0
    LOSE = 1
    WIN = 2


N_FINGERS = 5


def _get_all_hands():
    """
    get all possible states (0 to 2 hands) for a player"
    """
    states = []
    # no hands:
    states.append(())
    # one hand:
    for i in range(1, N_FINGERS):
        states.append((i,))
    # two hands:
    for i in range(1, N_FINGERS):
        for j in range(1, i + 1):
            states.append((i, j))
    return states


ALL_HANDS = _get_all_hands()


def rep_hand(hand):
    """
    convert to standard form: sort descending, and remove empty hands
    """
    assert isinstance(hand, tuple) and 0 <= len(hand) <= 2
    return tuple(sorted(filter(lambda x: x != 0, hand), reverse=True))


def _get_states_after_hit(h2, h1, x):
    """
    return list of possible states when hitting h2 with x, (x chosen from h1)"
    """
    res = []
    if len(h2) == 1:
        res.append((rep_hand(((h2[0] + x) % N_FINGERS,)), h1))
    else:
        res.append((rep_hand(((h2[0] + x) % N_FINGERS, h2[1])), h1))
        res.append((rep_hand(((h2[1] + x) % N_FINGERS, h2[0])), h1))
    return res


def _get_next_possible_states(h1, h2):
    """
    return a list of possible next state"
    """
    assert len(h1) > 0, len(h2) > 0
    res = []
    res.extend(_get_states_after_hit(h2, h1, h1[0]))
    if len(h1) == 1:
        # splitting
        if h1[0] % 2 == 0:
            res.append((h2, (h1[0] // 2, h1[0] // 2)))
    else:
        res.extend(_get_states_after_hit(h2, h1, h1[1]))
        # hit yourself
        res.append((h2, rep_hand(((h1[0] + h1[1]) % N_FINGERS, h1[0]))))
        res.append((h2, rep_hand(((h1[0] + h1[1]) % N_FINGERS, h1[1]))))
    return list(set(res))
    
 
class Game:
    def __init__(self):
        self._graph = networkx.DiGraph()
        self._labels = dict()
        self._init_graph()
    
    def _init_graph(self):
        for h1 in ALL_HANDS:
            for h2 in ALL_HANDS:
                self._graph.add_node((h1, h2))
                # add label
                if len(h1) == 0:
                    self._labels[(h1, h2)] = Status.LOSE
                elif len(h2) == 0:  # player2 just made himself/herself lose?
                    self._labels[(h1, h2)] = Status.WIN
                else:
                    self._labels[(h1, h2)] = Status.NOT_DET
                    # if game isn't over, add edges
                    for state in _get_next_possible_states(h1, h2):
                        self._graph.add_edge((h1, h2), state)
                
    def _process_state(self, state):
        if self._labels[state] != Status.NOT_DET:
            return  # this is labeled already
        all_neighbors_labels = [self._labels[x] for x in self._graph.neighbors(state)]
        if all(x == Status.WIN for x in all_neighbors_labels):
            self._labels[state] = Status.LOSE
        elif any(x == Status.LOSE for x in all_neighbors_labels):
            self._labels[state] = Status.WIN
            
    def calculate_labels(self):
        for i in range(len(self._graph.nodes())):
            # move over all vertices, repeat |V| times
            for state in self._graph.nodes():
                self._process_state(state)
        
    def get_label(self, state):
        return self._labels[state]
        
    def get_best_move(self, state, dumb=False):
        # TODO : shortest win, we might get stuck forever
        neighbors = list(self._graph.neighbors(state))
        if dumb or self._labels[state] == Status.LOSE:
            return random.choice(neighbors)  # any move
        elif self._labels[state] == Status.WIN:
            # if there's immediate win, do it
            immediate_wins = list(filter(lambda s: s[0] == (), neighbors))
            if immediate_wins:
                return random.choice(immediate_wins)
            else:
                return random.choice(list(filter(lambda s: self._labels[s] == Status.LOSE,
                                          neighbors)))
        else:  # not determined, pick any not losing move
            return random.choice(list(filter(lambda s: self._labels[s] != Status.WIN,
                                             neighbors)))
