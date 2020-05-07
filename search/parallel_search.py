import importlib
from multiprocessing import (Process, Manager)
from search.search import MinMaxAgent

import os
import operator


class ParallelMinMax(MinMaxAgent):

    def __init__(self, process_no, max_depth, max_time):
        super(ParallelMinMax, self).__init__(max_depth-1, max_time)
        self.process_no = process_no
        self.jobs = []

        # Process-safe structures
        manager = Manager()
        self._result = manager.list()
        self.checked = manager.dict()

    def make_decision(self, state, problem):
        self.node_expanded = 0

        list_actions = self.possible_actions(state, problem)
        first_level_states = list(map(lambda action: self.resulting_state(state, action, problem), list_actions))
        num_states = len(first_level_states)

        # couples

        # Number of states assigned to each process
        cut = int(num_states/self.process_no) \
            if num_states > self.process_no \
            else 1
        cut_first_level_states = list(chunks(first_level_states, cut))

        # Preparing workers
        self.jobs = [Process(target=self._worker, args=(states, problem, self._result))
                            for states in cut_first_level_states]

        # Start workers
        [p.start() for p in self.jobs]

        # Wait for workers
        [p.join() for p in self.jobs]

        self._result.sort(key=operator.itemgetter(1))
        print("----------------------------------")
        print(list(filter(lambda x: x[0] == self._result[0][0],
                                  list(zip(first_level_states, list_actions)))))
        print(len(first_level_states))
        print(len(list_actions))
        best_action = list(filter(lambda x: x[0] == self._result[0][0],
                                  list(zip(first_level_states, list_actions))))[0][1]
        return best_action

    # Every process will execute this method
    def _worker(self, states, problem, out):
        best_actions = [self.choose_action(state, problem) for state in states]

        # Visto che il primo livello è stato diviso
        self.max_depth += 1

        values = [a[1] for a in best_actions]
        partial_result = list(zip(states, values))
        out += partial_result
        print("<PID {}> Stati: {}, Risultati (stato, valore): {} Stati saltati: {}".format(
            os.getpid(), states, partial_result, self.node_skipped))


# Util
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
