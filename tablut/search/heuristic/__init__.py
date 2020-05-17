import tablut.search.heuristic.heuristic_factory as heuristic_factory
import tablut.search.heuristic.heuristic_function as heuristic_function
import tablut.search.heuristic.strategies as strategies
import tablut.search.heuristic.phase as phase


def eval(state, player, phase):
    heuristic_func = heuristic_factory.get_function(state, player, phase)
    return heuristic_func.eval(state, player)
    #return strategies.random.RandomStrategy().eval(state, player)
