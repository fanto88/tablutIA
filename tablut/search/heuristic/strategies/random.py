from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config
from tablut.utils.action import Position

BLACK_PIECE_AROUND_KING_IN_THRONE = 400
BLACK_PIECE_AROUND_KING = 500
BLACK_GOOD_POSITION = 0.03
KING_IN_WINNING_POSITION = 0.1
KING_INSIDE_ESCAPE = 10000
KING_EATED = 10000


# TODO: Aggiungere un bonus per mangiare una pedina
# La differenza tra le pedine vale 1 punto
# TODO: Per controllare se, per esempio, il re è su un escape fare state.king_bitboard & state.escape_bitboard > 0 (da verificaare)
# TODO: Cercare di togliere più roba che si può e usare operazioni bit sulle bitboard

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


def king_in_escape(state):
    king_position = None
    for row in range(9):
        for column in range(9):
            if bitboard_util.get_bit(state.king_bitboard, row, column) == 1:
                king_position = Position(row, column)
                break
    if king_position is not None:
        row = king_position.row
        column = king_position.column
        if row == 0:
            if column == 1 or column == 2 or column == 6 or column == 7:
                return KING_INSIDE_ESCAPE
        if row == 1:
            if column == 0 or column == 8:
                return KING_INSIDE_ESCAPE
        if row == 2:
            if column == 0 or column == 8:
                return KING_INSIDE_ESCAPE
        if row == 6:
            if column == 0 or column == 8:
                return KING_INSIDE_ESCAPE
        if row == 7:
            if column == 0 or column == 8:
                return KING_INSIDE_ESCAPE
        if row == 8:
            if column == 1 or column == 2 or column == 6 or column == 7:
                return KING_INSIDE_ESCAPE
    return 0


def king_ate(state):
    result = False
    for row in range(9):
        for column in range(9):
            if bitboard_util.get_bit(state.king_bitboard, row, column) == 1:
                result = True
    if not result:
        return KING_EATED
    return 0


def king_in_winning_position(state):
    king_position = None
    result = 0
    for row in range(9):
        for column in range(9):
            if bitboard_util.get_bit(state.king_bitboard, row, column) == 1:
                king_position = Position(row, column)
                break
    if king_position is not None:
        if king_position.row == 1 or king_position.row == 2 or king_position.row == 6 or king_position.row == 7:
            if not is_there_obstacle_in_row(state, king_position):
                result += KING_IN_WINNING_POSITION
        if king_position.column == 1 or king_position.column == 2 or king_position.column == 6 or king_position.column == 7:
            if not is_there_obstacle_in_column(state, king_position):
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

            if player == config.WHITE:
                value -= bitboard_util.count_adjacent(state.king_position, state.black_bitboard) * multiplier
                value -= black_in_good_position(state)
                value += (bitboard_util.count_piece(state.white_bitboard | state.king_bitboard) - 1) * 2
                value -= bitboard_util.count_piece(state.black_bitboard)
                value += king_in_winning_position(state)
                value += king_in_escape(state)
                value -= king_ate(state)
            else:
                value += bitboard_util.count_adjacent(state.king_position, state.black_bitboard) * multiplier
                value += black_in_good_position(state)
                value -= (bitboard_util.count_piece(state.white_bitboard | state.king_bitboard) - 1) * 2
                value += bitboard_util.count_piece(state.black_bitboard)
                value -= king_in_winning_position(state)
                value -= king_in_escape(state)
                value += king_ate(state)

            return value
        except Exception as e:
            print(e)
