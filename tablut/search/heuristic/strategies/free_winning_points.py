from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util, config


class FreeWinningPoints(HeuristicStrategy):
    """Count how many free escape points are on the board."""

    max = 1
    min = -1

    def eval(self, state, player):
        count_free_winning_points = 0
        obstacle_bitboard = state.white_bitboard | state.black_bitboard | state.king_bitboard
        if not bitboard_util.get_bit(obstacle_bitboard, 0, 2):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 0, 3):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 0, 6):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 0, 7):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 1, 0):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 1, 8):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 2, 0):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 2, 8):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 6, 0):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 6, 8):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 7, 0):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 7, 8):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 8, 1):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 8, 2):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 8, 6):
            count_free_winning_points += 1
        if not bitboard_util.get_bit(obstacle_bitboard, 8, 7):
            count_free_winning_points += 1
        return count_free_winning_points
