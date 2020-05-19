from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class BlackInGoodPosition(HeuristicStrategy):
    """Count how many black pawns are in a good position and give them a weight based on the King location."""

    max = 1
    min = -1

    def eval(self, state, player):
        count_pawns = 0
        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        very_good = 1
        good = 1 / 2
        not_bad = 1 / 4
        good_position_value = [good, good, good, good]

        # Il re è sotto al trono a destra
        if state.king_position.row > 4:
            if state.king_position.column < 4:
                good_position_value = [not_bad, very_good, good, very_good]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re è sotto al trono a sinistra
        if state.king_position.row > 4:
            if state.king_position.column > 4:
                good_position_value = [very_good, not_bad, very_good, good]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re è sotto al trono in centro
        if state.king_position.row > 4:
            if state.king_position.column == 4:
                good_position_value = [not_bad, not_bad, very_good, very_good]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re si trova a destra del trono
        if state.king_position.row == 4:
            if state.king_position.column < 4:
                good_position_value = [not_bad, very_good, not_bad, very_good]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re si trova a sinistra del trono
        if state.king_position.row == 4:
            if state.king_position.column > 4:
                good_position_value = [very_good, not_bad, very_good, not_bad]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re è sopra al trono a destra
        if state.king_position.row < 4:
            if state.king_position.column < 4:
                good_position_value = [good, very_good, not_bad, very_good]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re è sopra al trono a sinistra
        if state.king_position.row < 4:
            if state.king_position.column > 4:
                good_position_value = [very_good, good, very_good, not_bad]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        # Il re è sopra al trono in centro
        if state.king_position.row < 4:
            if state.king_position.column == 4:
                good_position_value = [very_good, very_good, not_bad, not_bad]

        # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
        if bitboard_util.get_bit(state.black_bitboard, 1, 6):
            count_pawns += good_position_value[0]
        if bitboard_util.get_bit(state.black_bitboard, 2, 7):
            count_pawns += good_position_value[0]
        if bitboard_util.get_bit(state.black_bitboard, 1, 2):
            count_pawns += good_position_value[1]
        if bitboard_util.get_bit(state.black_bitboard, 2, 1):
            count_pawns += good_position_value[1]
        if bitboard_util.get_bit(state.black_bitboard, 6, 7):
            count_pawns += good_position_value[2]
        if bitboard_util.get_bit(state.black_bitboard, 7, 6):
            count_pawns += good_position_value[2]
        if bitboard_util.get_bit(state.black_bitboard, 6, 1):
            count_pawns += good_position_value[3]
        if bitboard_util.get_bit(state.black_bitboard, 7, 2):
            count_pawns += good_position_value[3]
        return count_pawns
