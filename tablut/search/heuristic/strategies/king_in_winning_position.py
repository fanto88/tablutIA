from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class KingInWinningPosition(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
        number_of_escape_reachable = 0
        row = state.king_position.row
        column = state.king_position.column
        if state.king_position is not None:
            if row == 0 or row == 1 or row == 2 or row == 6 or row == 7 or row == 8:
                is_blocked, number_escapes_blocked = bitboard_util.is_there_obstacle_in_column(state.king_position, obstacle_bitboard)
                if not is_blocked:
                    number_of_escape_reachable += 2 - number_escapes_blocked
            if column == 0 or column == 1 or column == 2 or column == 6 or column == 7 or column == 8:
                is_blocked, number_escapes_blocked = bitboard_util.is_there_obstacle_in_row(state.king_position, obstacle_bitboard)
                if not is_blocked:
                    number_of_escape_reachable += 2 - number_escapes_blocked
        return number_of_escape_reachable
