from multiprocessing import (Process, Manager)
from tablut.search.search import MinMaxAgent

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
        self.jobs = [Process(target=self._worker, args=(states, len(first_level_states), problem, not maximize, self._result))
                            for states in cut_first_level_states]

        # Start workers
        [p.start() for p in self.jobs]

        # Wait for workers
        [p.join() for p in self.jobs]

        # Visto che questa classe ottiene gli stati di profondità 1 e ai sottoprocessi viene passata
        # profondità massima ridotta di 1
        self.max_depth += 1

        # self._result contains couples (first_level_state, value) obtained by child processors
        # sorting the list by value means the first couple (state, value) is the best one
        self._result.sort(key=operator.itemgetter(1), reverse=maximize)
        #print("----------------------------------")
        #print(self._result)
        #print(list(zip(first_level_states, list_actions)))

        # list(zip(first_level_states, list_actions)) is list of couples (first_level_state, action_to_reach_that_state)
        # filter is used to obtain the best action, using the best state (first element of self._result) as key
        # the final result is a list with a single element [(best_state, best_action)]
        #best_action = list(filter(lambda x: x[0] == self._result[0][0],
                                  #list(zip(first_level_states, list_actions))))[0][1]
        state_action = zip(first_level_states, list_actions)
        best_state = self._result[0][0]
        best_action = ''
        for state, action in state_action:
            print(best_state, "|", state)
            if state == best_state:
                best_action = action
                break
                #print("Master: risultato (stato, azione) ({state}, {action})".format(state=state, action=action))
        print("AZIONE:" ,best_action, "TIPO:", type(best_action))
        print("\n\n")
        print("-------------")

        return best_action

    # Every process will execute this method
    def _worker(self, states, total_states, problem, maximize, out):
        # TODO: imposta in modo efficienti il timer... magari cambiando la struttura
        self.max_time = self.max_time/total_states

        # Utility value of each state inside "states" list
        values = [self.choose_action(state, problem, maximize=maximize) for state in states]

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
