from multiprocessing import (Process, Manager)
from tablut.search.search import MinMaxAgent

import os
import operator


class ParallelMinMax(MinMaxAgent):

    def __init__(self, process_no, max_depth, max_time):
        super(ParallelMinMax, self).__init__(max_depth, max_time)
        self.process_no = process_no

        # Process-safe structures
        manager = Manager()
        self._result = manager.list()
        self.checked = manager.dict()

    def make_decision(self, state, problem, maximize=True):
        # Clear structs
        self._result[:] = []
        self.checked.clear()

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
        jobs = [Process(target=self._worker, args=(states, len(first_level_states), problem, not maximize, self._result))
                            for states in cut_first_level_states]

        # Start workers
        [p.start() for p in jobs]

        # Wait for workers
        [p.join() for p in jobs]

        # self._result contains couples (first_level_state, value) obtained by child processors
        # sorting the list by value means the first couple (state, value) is the best one
        self._result.sort(key=operator.itemgetter(1), reverse=maximize)

        state_action = zip(first_level_states, list_actions)
        best_state = self._result[0][0]
        best_action = ''
        for state, action in state_action:
            if state == best_state:
                best_action = action
                print("Master: risultato (stato, azione) ({state}, {action})".format(state=state, action=action))

        return best_action

    # Every process will execute this method
    def _worker(self, states, total_states, problem, maximize, out):
        # TODO: imposta in modo efficienti il timer... magari cambiando la struttura
        self.max_time = self.max_time/total_states

        # Utility value of each state inside "states" list
        values = [self.choose_action(state, problem, maximize=maximize, max_depth=self.max_depth-1) for state in states]

        # Couples (state, value)
        partial_result = list(zip(states, values))

        # Append results to the shared struct TODO: aggiungi solo il migliore tra i risultati
        out += partial_result
        #print("<PID {}> Stati saltati: {} Risultati (stato, valore): {} ".format(
            #os.getpid(), self.node_skipped, states))


# Util
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
