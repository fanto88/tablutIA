from multiprocessing import (Process, Manager, Value)
from tablut.search.search import MinMaxAgent

import os
import operator


class ParallelMinMax(MinMaxAgent):

    def __init__(self, process_no, max_depth, max_time):
        super(ParallelMinMax, self).__init__(max_depth, max_time)
        self.process_no = process_no

        # Process-safe structures
        manager = Manager()
        self.checked = manager.dict()


        # TODO Process-safe values

    def make_decision(self, state, problem, maximize=True, start_depth=0):
        # Clear structs
        manager = Manager()
        child_results = manager.list()

        # Obtaining all child states, starting from the given one
        list_actions = self.possible_actions(state, problem)
        first_level_states = list(map(lambda action: self.resulting_state(state, action, problem), list_actions))
        num_states = len(first_level_states)

        # Number of states assigned to each process
        cut = int(num_states/self.process_no) \
            if num_states > self.process_no \
            else 1

        # State assigned to each process
        cut_first_level_states = list(chunks(first_level_states, cut))

        # Preparing workers
        jobs = [Process(target=self._worker, args=(states, len(first_level_states), problem, not maximize, child_results, start_depth))
                            for states in cut_first_level_states]

        # Start workers
        [p.start() for p in jobs]

        # Wait for workers
        [p.join() for p in jobs]

        best_action, best_value = self._best(list(zip(list_actions, child_results)), maximize)
        print()
        print("Best action, best value: {}, {}".format(best_action, best_value))
        return best_action

    # Every process will execute this method
    def _worker(self, states, total_states, problem, maximize, out, start_depth):
        self.max_time = self.max_time/total_states

        # couples (best_action, value) of each state inside "states" list
        actions_values = [self.choose_action(state, problem, maximize=maximize, start_depth=start_depth+1)
                          for state in states]

        # values for each state in "states"
        values = [act_val[1] for act_val in actions_values]

        # Append results to the shared struct
        out += values


# Util
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
