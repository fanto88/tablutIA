from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config
from tablut.utils.action import Position

BLACK_PIECE_AROUND_KING_IN_THRONE = 1
BLACK_PIECE_AROUND_KING = 5
BLACK_GOOD_POSITION = 3
KING_IN_WINNING_POSITION = 10
KING_INSIDE_ESCAPE = 10000
KING_EATED = 10000

# La differenza tra le pedine vale 1 punto

class RandomStrategy(HeuristicStrategy):
    """min = 0
    max = 10

    def eval(self, state, player):
        return secrets.randbelow(self.max+1)"""

    def eval(self, state, player):
        value = 0
        if player == config.WHITE:
            value += - self.black_pieces_around_king(state) - self.black_in_good_position(state) + (
                    self.count_piece(state.white_bitboard | state.king_bitboard) - 1) * 2 - self.count_piece(
                state.black_bitboard) + self.king_in_winning_position(state) + self.king_in_escape(state) - self.king_eated(state)
        else:
            value += self.black_pieces_around_king(state) + self.black_in_good_position(state) - (
                    self.count_piece(state.white_bitboard | state.king_bitboard) - 1) * 2 + self.count_piece(
                state.black_bitboard) - self.king_in_winning_position(state) - self.king_in_escape(state) + self.king_eated(state)
        return value

    def black_pieces_around_king(self, state):
        king_position = None
        for row in range(9):
            for column in range(9):
                if bitboard_util.get_bit(state.king_bitboard, row, column) == 1:
                    king_position = Position(row, column)
                    break
        count = 0
        if king_position is not None:
            if king_position.row() == 4 and king_position.column() == 4:
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE
            else:
                multiplier = BLACK_PIECE_AROUND_KING
            if king_position.column() - 1 >= 0:
                if bitboard_util.get_bit(state.black_bitboard, king_position.row(), king_position.column() - 1) == 1:
                    count += 1
            if king_position.column() + 1 <= 8:
                if bitboard_util.get_bit(state.black_bitboard, king_position.row(), king_position.column() + 1) == 1:
                    count += 1
            if king_position.row() - 1 >= 0:
                if bitboard_util.get_bit(state.black_bitboard, king_position.row() - 1, king_position.column()) == 1:
                    count += 1
            if king_position.row() + 1 <= 8:
                if bitboard_util.get_bit(state.black_bitboard, king_position.row() + 1, king_position.column()) == 1:
                    count += 1
            return count * multiplier
        return 0

    def black_in_good_position(self, state):
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

    def count_piece(self, bitboard):
        count = 0
        for row in range(9):
            for column in range(9):
                if bitboard_util.get_bit(bitboard, row, column) == 1:
                    count += 1
        return count

    def king_in_winning_position(self, state):
        king_position = None
        result = 0
        for row in range(9):
            for column in range(9):
                if bitboard_util.get_bit(state.king_bitboard, row, column) == 1:
                    king_position = Position(row, column)
                    break
        if king_position is not None:
            if king_position.row() == 1 or king_position.row() == 2 or king_position.row() == 6 or king_position.row() == 7:
                if not self.is_there_obstacle_in_row(state, king_position):
                    result += KING_IN_WINNING_POSITION
            if king_position.column() == 1 or king_position.column() == 2 or king_position.column() == 6 or king_position.column() == 7:
                if not self.is_there_obstacle_in_column(state, king_position):
                    result += KING_IN_WINNING_POSITION
        return result

    def is_there_obstacle_in_row(self, state, position):
        row_index = position.row()
        obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
        result = False
        blocked = 0
        for row in range(row_index - 1, -1, -1):
            if bitboard_util.get_bit(obstacle_bitboard, row, position.column()) == 1:
                blocked += 1
        for row in range(row_index + 1, 9):
            if bitboard_util.get_bit(obstacle_bitboard, row, position.column()) == 1:
                blocked += 1
        if blocked == 2:
            result = False
        return result

    def is_there_obstacle_in_column(self, state, position):
        column_index = position.column()
        obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
        result = False
        blocked = 0
        for col in range(column_index - 1, -1, -1):
            if bitboard_util.get_bit(obstacle_bitboard, position.row(), col) == 1:
                blocked += 1
        for col in range(column_index + 1, 9):
            if bitboard_util.get_bit(obstacle_bitboard, position.row(), col) == 1:
                blocked += 1
        if blocked == 2:
            result = False
        return result

    def king_in_escape(self, state):
        king_position = None
        for row in range(9):
            for column in range(9):
                if bitboard_util.get_bit(state.king_bitboard, row, column) == 1:
                    king_position = Position(row, column)
                    break
        if king_position is not None:
            row = king_position.row()
            column = king_position.column()
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

    def king_eated(self, state):
        if (state.king_bitboard[0] | state.king_bitboard[1] | state.king_bitboard[2] | state.king_bitboard[4] |
                state.king_bitboard[5] | state.king_bitboard[6] | state.king_bitboard[7] | state.king_bitboard[8]) == 0:
            return KING_EATED
        return 0
