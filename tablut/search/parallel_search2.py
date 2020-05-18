from multiprocessing import Process, Manager
from tablut.search.search import SearchAgent, utility, Game
from tablut.state.tablut_state import TablutState
import operator
import os
import time
import tablut.search.heuristic as heuristic


def choose_action(process_no, state: TablutState, problem, max_time, max_depth,
                  maximize=True, start_depth=0, given_phase=None, given_player=None):

    def terminal_test(state):
        return start_depth >= max_depth or problem.goal_test(state)

    # Util
    def chunks(lst, n):
        """Yield successive n-sized chunks from lst."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]



    # Body

    # Phase
    phase = heuristic.phase.START
    if given_phase:
        phase = given_phase

    # Player
    player = problem.turn_player(state)
    if given_player:
        player = given_player

    if process_no == 1:
        o = SearchAgent(max_depth, max_time)
        return o.choose_action(state, problem, maximize, given_phase=phase)

    # Check if terminal
    if terminal_test(state):
        return ('123', problem.value(state, state.turn)) if problem.goal_test(state) else ('1234', utility(state, problem))

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
                    args=(states, problem, not maximize, max_depth, max_time, phase, player, results))
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

    if not best_action:
        print("Best S, Best A", best_state, best_action)
        print("States:", first_level_states)
    return best_action, best_value


def run(states, problem:Game, maximize, max_depth, max_time, phase, player, out):
    o = SearchAgent(max_depth, max_time=max_time*0.9)
    print("<PID {}> stati {} tempo per stato {} tempo totale {}".format(os.getpid(), len(states),
                                                                        round(max_time/len(states), 3),
                                                                        round(max_time, 3)))

    start = time.time()
    child_results = [o.choose_action(st, problem, maximize, given_phase=phase, given_player=player,
                                     start_depth=1, max_time=max_time/len(states)) for st in states]
    end = time.time()

    # Only values are needed
    values = [action_value[1] for action_value in child_results]

    # Couples (state, value) for each given state
    state_values = list(zip(states, values))

    # Adding results to shared structure
    #print("<PID {}> Aggiungo a {} (stato, valore) {}".format(os.getpid(), out, state_values))
    out += state_values

    print("<PID {}> FINE. Tempo di calcolo {}".format(os.getpid(), round(end - start, 3)))

