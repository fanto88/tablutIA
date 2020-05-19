from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class WhiteCount(HeuristicStrategy):
    """Return the number of white pawns on the board."""
    max = 1
    min = -1

    def eval(self, state, player):
        return state.white_count * 2
