from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class WhiteCount(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        return state.white_count * 2
