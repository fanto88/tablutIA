from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class WhiteGoodPosition(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        value = 0
        if bitboard_util.get_bit(state.white_bitboard, 1, 3):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 1, 5):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 3, 1):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 3, 7):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 5, 1):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 5, 7):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 7, 3):
            value += 1
        if bitboard_util.get_bit(state.white_bitboard, 7, 5):
            value += 1
        if player == config.WHITE:
            return value
        return -value
