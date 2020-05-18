from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class WhiteWinningPoints(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        occupied_by_white = 0
        if bitboard_util.get_bit(state.white_bitboard, 0, 1):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 0, 2):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 0, 6):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 0, 7):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 1, 0):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 1, 8):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 2, 0):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 2, 8):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 6, 0):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 6, 8):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 7, 0):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 7, 8):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 8, 1):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 8, 2):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 8, 6):
            occupied_by_white += 1
        if bitboard_util.get_bit(state.white_bitboard, 8, 7):
            occupied_by_white += 1
        return occupied_by_white
