import importlib
from multiprocessing import (Process, Manager)
from search.search import MinMaxAgent

import os
import operator


class ParallelMinMax(MinMaxAgent):

    def __init__(self, process_no, max_depth, max_time):
        # TODO: guarda max_depth -1 qua sotto e max_depth += 1 nella funzione workers e vedi come risolvere
        super(ParallelMinMax, self).__init__(max_depth-1, max_time)
        self.process_no = process_no
        self.jobs = []

        # Process-safe structures
        manager = Manager()
        self._result = manager.list()
        self.checked = manager.dict()

    def make_decision(self, state, problem, maximize=True):
        self.node_expanded = 0

        # Obtaining all child states, starting from the given one
        list_actions = self.possible_actions(state, problem)
        first_level_states = list(map(lambda action: self.resulting_state(state, action, problem), list_actions))
        num_states = len(first_level_states)

        # Number of states assigned to each process
        cut = int(num_states/self.process_no) \
            if num_states > self.process_no \
            else 1
        cut_first_level_states = list(chunks(first_level_states, cut))

        # Preparing workers
        self.jobs = [Process(target=self._worker, args=(states, problem, not maximize, self._result))
                            for states in cut_first_level_states]

        # Start workers
        [p.start() for p in self.jobs]

        # Wait for workers
        [p.join() for p in self.jobs]

        # self._result contains couples (first_level_state, value) obtained by child processors
        # sorting the list by value means the first couple (state, value) is the best one
        self._result.sort(key=operator.itemgetter(1), reverse=maximize)
        print("----------------------------------")
        print(self._result)
        print(list(zip(first_level_states, list_actions)))

        # list(zip(first_level_states, list_actions)) is list of couples (first_level_state, action_to_reach_that_state)
        # filter is used to obtain the best action, using the best state (first element of self._result) as key
        # the final result is a list with a single element [(best_state, best_action)]
        #best_action = list(filter(lambda x: x[0] == self._result[0][0],
                                  #list(zip(first_level_states, list_actions))))[0][1]
        state_action = zip(first_level_states, list_actions)
        best_state = self._result[0][0]
        best_action = ''
        for state, action in state_action:
            if state == best_state:
                best_action = action
        return best_action

    # Every process will execute this method
    def _worker(self, states, problem, maximize, out):

        # Couples (action, value)
        best_actions = [self.choose_action(state, problem, maximize=maximize) for state in states]

        # Visto che il primo livello è stato diviso
        self.max_depth += 1  # TODO: cambia qualcosa toglierlo?

        # List of values of best_actions
        values = [a[1] for a in best_actions]

        # Couples (state, value)
        partial_result = list(zip(states, values))

        # Append results to the shared struct TODO: aggiungi solo il migliore tra i risultati
        out += partial_result
        print("<PID {} best_actions({}) {} partial_result({}) {}".format(os.getpid(), len(best_actions), best_actions, len(partial_result), partial_result))
        print("<PID {}> Stati: {}, Risultati (stato, valore): {} Stati saltati: {}".format(
            os.getpid(), states, partial_result, self.node_skipped))


# Util
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
