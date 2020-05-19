from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import config


class PawnDifference(HeuristicStrategy):
    """Return the difference between black and white pawns."""

    max = 1
    min = -1

    def eval(self, state, player):
        return state.black_count - state.white_count * 2
