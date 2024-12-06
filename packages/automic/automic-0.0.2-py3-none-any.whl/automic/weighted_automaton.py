from collections import defaultdict
from typing import List, Any, Set


from automic import Automaton


class WeightedAutomaton(Automaton):
    def __init__(self, n_states, accepting: Set[int]):
        self.n_states = n_states
        self.transitions = [defaultdict(dict) for _ in range(n_states)]
        self.accepting = set(accepting)
        self.pruned_depth = 0

    def add_state(self):
        self.n_states += 1
        self.transitions.append(defaultdict(dict))
        return self.n_states-1
