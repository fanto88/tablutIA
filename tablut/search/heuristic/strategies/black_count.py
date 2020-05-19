from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class BlackCount(HeuristicStrategy):
    """Count how many black pawns are actually on the board."""

    max = 1
    min = -1

    def eval(self, state, player):
        return state.black_count
