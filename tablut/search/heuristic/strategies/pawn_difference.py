from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import config


class PawnDifference(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        value = state.black_count - state.white_count * 2
        """if player == config.WHITE:
            return value
        return -value"""
        return value
