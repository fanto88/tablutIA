import tablut.search.heuristic.heuristic_factory as heuristic_factory
import tablut.search.heuristic.heuristic_function as heuristic_function


def eval(state, player, phase):
    heuristic_func = heuristic_factory.get_function(state, player, phase)
    return heuristic_func.eval(state, player)