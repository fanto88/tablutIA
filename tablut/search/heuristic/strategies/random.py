"""from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class RandomStrategy(HeuristicStrategy):
    def eval(self, state, player):
        try:
            value = 0
            value -= (bitboard_util.count_piece(state.white_bitboard) + bitboard_util.count_piece(
                state.king_bitboard) - 1) * 2
            value += bitboard_util.count_piece(state.black_bitboard)
            print(value)
            return value
        except Exception as e:
            print(e)
"""

from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util
from tablut.utils.action import Position

BLACK_PIECE_AROUND_KING_IN_THRONE = 4
BLACK_PIECE_AROUND_KING = 5
BLACK_GOOD_POSITION = 2
KING_IN_WINNING_POSITION = 10
KING_INSIDE_ESCAPE = 10000
KING_EATED = 10000
PIECE_ATE = 2


# TODO: Verificare che king_in_winning_position funzioni correttamente
# TODO: Cercare di togliere più roba che si può e usare operazioni bit sulle bitboard
# TODO: Se il re  in una posizione vincente bloccare la sua traiettoria, ha priorità rispetto a tutto
def is_there_obstacle_in_row(state, position):
    row_index = position.row
    obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
    result = False
    blocked = 0
    for row in range(row_index - 1, -1, -1):
        if bitboard_util.get_bit(obstacle_bitboard, row, position.column) == 1:
            blocked += 1
    for row in range(row_index + 1, 9):
        if bitboard_util.get_bit(obstacle_bitboard, row, position.column) == 1:
            blocked += 1
    if blocked == 2:
        result = False
    return result


def is_there_obstacle_in_column(state, position):
    column_index = position.column
    obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
    result = False
    blocked = 0
    for col in range(column_index - 1, -1, -1):
        if bitboard_util.get_bit(obstacle_bitboard, position.row, col) == 1:
            blocked += 1
    for col in range(column_index + 1, 9):
        if bitboard_util.get_bit(obstacle_bitboard, position.row, col) == 1:
            blocked += 1
    if blocked == 2:
        result = False
    return result


def king_in_winning_position(state):
    result = 0
    if state.king_position is not None:
        if state.king_position.row == 1 or state.king_position.row == 2 or state.king_position.row == 6 or state.king_position.row == 7:
            if not is_there_obstacle_in_row(state, state.king_position):
                result += KING_IN_WINNING_POSITION
        if state.king_position.column == 1 or state.king_position.column == 2 or state.king_position.column == 6 or state.king_position.column == 7:
            if not is_there_obstacle_in_column(state, state.king_position):
                result += KING_IN_WINNING_POSITION
    return result


def black_in_good_position(state):
    value = 0
    if bitboard_util.get_bit(state.black_bitboard, 1, 6):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 1, 2):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 2, 7):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 2, 1):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 6, 7):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 6, 1):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 7, 6):
        value += BLACK_GOOD_POSITION
    if bitboard_util.get_bit(state.black_bitboard, 7, 2):
        value += BLACK_GOOD_POSITION
    return value


class RandomStrategy(HeuristicStrategy):
    def eval(self, state, player):
        try:
            value = 0
            multiplier = BLACK_PIECE_AROUND_KING
            if state.king_position == Position(4, 4):
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE

            value += bitboard_util.count_adjacent(state.king_position, state.black_bitboard) * multiplier
            value += black_in_good_position(state)
            value -= (bitboard_util.count_piece(state.white_bitboard)) * 2 * PIECE_ATE
            value += bitboard_util.count_piece(state.black_bitboard) * PIECE_ATE
            value -= king_in_winning_position(state)

            return value
        except Exception as e:
            print(e)
