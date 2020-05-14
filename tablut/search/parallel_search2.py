from multiprocessing import Pool, Process, Manager
from tablut.search.search import SearchAgent, utility
from tablut.state.tablut_state import TablutState
from tablut.utils.action import Action
import operator
import os


def choose_action(process_no, state: TablutState, problem, max_time, max_depth, maximize=True, start_depth=0):

    def terminal_test(state):
        return start_depth >= max_depth or problem.goal_test(state)

    # Util
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    # Body
    if process_no == 1:
        o = SearchAgent(max_depth, max_time)
        return o.choose_action(state, problem, maximize)

    # Check if terminal
    if terminal_test(state):
        return problem.value(state, state.turn) if problem.goal_test(state) else utility(state, problem)

    # Obtaining all child states, starting from the given one
    list_actions = problem.actions(state)
    first_level_states = list(map(lambda action: problem.process_action(state, action), list_actions))
    num_states = len(first_level_states)

    # Number of states assigned to each process
    cut = int(num_states / process_no)+1 \
        if num_states > process_no \
        else 1

    # State assigned to each process
    cut_first_level_states = list(chunks(first_level_states, cut))

    # Workers
    results = Manager().list()
    jobs = [Process(target=run,
                    args=(states, problem, not maximize, max_depth, max_time/num_states, results))
            for states in cut_first_level_states]

    # Start workers
    [p.start() for p in jobs]

    # Wait for workers
    [p.join() for p in jobs]

    # Cleaning results from empty lists

    state_actions = list(zip(first_level_states, list_actions))

    results.sort(key=operator.itemgetter(1), reverse=maximize)

    best_state = results[0][0]
    best_value = results[0][1]

    best_action = ''

    for state, action in state_actions:
        if state == best_state:
            best_action = action
            break

    return best_action, best_value


def run(states, problem, maximize, max_depth, time, out):
    o = SearchAgent(max_depth, max_time=time)
    print("<PID {}> stati {} tempo per stato {} tempo totale {}".format(os.getpid(), len(states),
                                                                        round(time, 3),
                                                                        round(time*len(states), 3)))

    child_results = [o.choose_action(st, problem, maximize, start_depth=1) for st in states]

    # Only values are needed
    values = [action_value[1] for action_value in child_results]

    # Couples (state, value) for each given state
    state_values = list(zip(states, values))

    # Adding results to shared structure
    out += state_values

    print("<PID {}> FINE".format(os.getpid()))

