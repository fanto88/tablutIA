from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class BlackCount(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        return state.black_count
