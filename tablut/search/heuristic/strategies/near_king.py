from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util


class NearKing(HeuristicStrategy):
    """Return how many black pawns are adjacent to the king. """

    max = 1
    min = -1

    def eval(self, state, player):
        return bitboard_util.count_adjacent(state.king_position, state.black_bitboard)
