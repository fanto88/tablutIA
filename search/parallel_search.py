import importlib
from multiprocessing import (Process, Manager, set_start_method)
from search.search import (MinMaxAgent, possible_actions, resulting_state)

import os


class ParallelMinMax(MinMaxAgent):

    def __init__(self, process_no, max_depth, max_time):
        super().__init__(max_depth-1, max_time)
        self.process_no = process_no
        self.jobs = []

        # Process-safe structures
        manager = Manager()
        self.result = manager.list()
        self.checked = manager.dict()

    def make_decision(self, state, problem):
        self.node_expanded = 0

        list_actions = possible_actions(state, problem)
        first_level_states = list(map(lambda action: resulting_state(state, action, problem), list_actions))
        num_states = len(first_level_states)

        # Number of states assigned to each process
        cut = int(num_states/self.process_no) \
            if num_states > self.process_no \
            else 1
        cut_first_level_states = list(chunks(first_level_states, cut))

        # Preparing workers
        self.jobs = [Process(target=self._worker, args=(states, problem, self.result))
                            for states in cut_first_level_states]

        # Start workers
        [p.start() for p in self.jobs]

        # Wait for workers
        [p.join() for p in self.jobs]

        # TODO: Analizza risultati di self.result e restituisci l'azione più vantaggiosa
        return first_level_states

    def _worker(self, states, problem, out):
        self.max_depth -= 1  # Il primo livello è già stato espanso
        best_actions = [self.choose_action(state, problem) for state in states]
        out.append(best_actions)
        print("<PID {}> Stati: {}, Risultati: {} Stati saltati: {}".format(
            os.getpid(), states, best_actions, self.node_skipped))


# Util
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
