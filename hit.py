
import networkx
import random

NOT_DET = 0
LOSE    = 1
WIN     = 2

N_FINGERS = 5

def get_all_hands():
    "get all possible hands (0 to 2 hands) for a player"
    ah = []
    # no hands:
    ah.append(())
    # one hand:
    for i in range(1, N_FINGERS):
        ah.append((i,))
    # two hands:
    for i in range(1, N_FINGERS):
        for j in range(1, i + 1):
            ah.append((i,j))
    return ah
ALL_HANDS = get_all_hands()

def rep_hand(h):
    "order tuple, top down, and remove if 0 fingers"
    assert isinstance(h, tuple) and 0 <= len(h) <= 2
    return tuple(sorted(list(filter(lambda x : x != 0, h)), reverse=True))

def get_next_possible_states(h1, h2):
    "return a list of possible next state"
    assert len(h1) > 0, len(h2) > 0
    res = []
    def hit_h_with_x_states(h2, h1, x):
        "possible states when hitting h2 with x, (x chosen from h1)"
        res = []
        if len(h2) == 1:
            res.append((rep_hand(((h2[0] + x) % N_FINGERS,)), h1))
        else:
            res.append((rep_hand(((h2[0] + x) % N_FINGERS, h2[1])), h1))
            res.append((rep_hand(((h2[1] + x) % N_FINGERS, h2[0])), h1))
        return res
        
    res.extend(hit_h_with_x_states(h2, h1, h1[0]))
    if len(h1) == 1:
        # splitting
        if h1[0] % 2 == 0:
            res.append((h2, (h1[0] // 2, h1[0] // 2)))
    else:
        res.extend(hit_h_with_x_states(h2, h1, h1[1]))
        # hit yourself
        res.append((h2, rep_hand(((h1[0] + h1[1]) % N_FINGERS, h1[0]))))
        res.append((h2, rep_hand(((h1[0] + h1[1]) % N_FINGERS, h1[1]))))
    return list(set(res))
    
 
class Game(object):
    def __init__(self):
        self.graph = networkx.DiGraph()
        self.labels = dict()
        self.init_graph()
    
    def init_graph(self):
        for h1 in ALL_HANDS:
            for h2 in ALL_HANDS:
                self.graph.add_node((h1,h2))
                # add label
                if len(h1) == 0:
                    self.labels[(h1, h2)] = LOSE
                elif len(h2) == 0:  # player2 just made himself/herself lose?
                    self.labels[(h1, h2)] = WIN
                else:
                    self.labels[(h1, h2)] = NOT_DET
                    # if game isn't over, add edges
                    for state in get_next_possible_states(h1, h2):
                        self.graph.add_edge((h1, h2), state)
                
    def process_state(self, state):
        if self.labels[state] != NOT_DET:
            return  # this is labeled already
        all_neighbors_labels = [self.labels[x] for x in self.graph.neighbors(state)]
        if all(x == WIN for x in all_neighbors_labels):
            self.labels[state] = LOSE
        elif any(x == LOSE for x in all_neighbors_labels):
            self.labels[state] = WIN
            
    def calculate_labels(self):
        for i in range(len(self.graph.nodes())):
            # move over all vertices, repeat |V| times
            for state in self.graph.nodes():
                self.process_state(state)
        
    def get_label(self, state):
        return self.labels[state]
        
    def get_best_move(self, state, dumb=False):
        # TODO : shortest win, we might get stuck forever
        neighbors = list(self.graph.neighbors(state))
        if dumb or self.labels[state] == LOSE:
            return random.choice(neighbors) # any move
        elif self.labels[state] == WIN:
            # if there's immediate win, do it
            immediate_wins = list(filter(lambda s:s[0] == (), neighbors))
            if immediate_wins != []:
                return random.choice(immediate_wins)
            else:
                return random.choice(list(filter(lambda s:self.labels[s] == LOSE,
                                          neighbors)))
        else:  # not determined, pick any not losing move
            return random.choice(list(filter(lambda s:self.labels[s] != WIN,
                                             neighbors)))
            
if __name__ == "__main__":
    pass
    
