from tablut.utils import bitboard_util, config


class NearKing:
    max = 1
    min = -1

    def eval(self, state, player):
        value = bitboard_util.count_adjacent(state.king_position, state.black_bitboard)
        if player == config.WHITE:
            return -value
        return value
