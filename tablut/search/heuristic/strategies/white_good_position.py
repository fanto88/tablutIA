from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class WhiteGoodPosition(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        count_pawns = 0
        if bitboard_util.get_bit(state.white_bitboard, 1, 3):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 1, 5):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 3, 1):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 3, 7):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 5, 1):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 5, 7):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 7, 3):
            count_pawns += 1
        if bitboard_util.get_bit(state.white_bitboard, 7, 5):
            count_pawns += 1
        return count_pawns
