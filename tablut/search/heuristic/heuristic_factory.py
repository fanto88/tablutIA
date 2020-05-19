import tablut.search.heuristic.strategies as strategies
import tablut.search.heuristic.phase as ph
import tablut.utils.config as config
import tablut.search.heuristic.heuristic_function as hf
from tablut.search.heuristic.strategies.black_count import BlackCount
from tablut.search.heuristic.strategies.black_in_good_position import BlackInGoodPosition
from tablut.search.heuristic.strategies.black_winning_points import BlackWinningPoints
from tablut.search.heuristic.strategies.free_winning_points import FreeWinningPoints
from tablut.search.heuristic.strategies.king_in_winning_position import KingInWinningPosition
from tablut.search.heuristic.strategies.king_positioning import KingPositioning
from tablut.search.heuristic.strategies.near_king import NearKing
from tablut.search.heuristic.strategies.pawn_difference import PawnDifference
from tablut.search.heuristic.strategies.white_count import WhiteCount
from tablut.search.heuristic.strategies.white_good_position import WhiteGoodPosition
from tablut.search.heuristic.strategies.white_winning_points import WhiteWinningPoints
from tablut.utils.action import Position


def get_function(state, player, phase) -> hf.HeuristicFunction:

    def white_strategies(phase):
        """



        """
        if phase == ph.START:
            """
            return [
                    (KingPositioning(), 100),
                    (KingInWinningPosition(), 5000),
                    (WhiteGoodPosition(), 3),
                    (PawnDifference(), -5),
                    (NearKing(), -2)
                ]
          return [
                (WhiteCount(), 2),
                (BlackCount(), -2),
                (NearKing(), -10),
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 2)
            ]
            return[
                (FreeWinningPoints(), 300),
                (WhiteCount(), 30),
                (BlackCount(), -20),
                (NearKing(), -1000),
                (KingInWinningPosition(), 2000),
                (KingPositioning(), 100)
            ]

            return [
                (FreeWinningPoints(), 100),
                (WhiteWinningPoints(), 200),
                (BlackWinningPoints(), -300),
                (WhiteCount(), 200),
                (BlackCount(), -500),
                (NearKing(), -1000),
                (KingInWinningPosition(), 10000),
                (KingPositioning(), 100),
                (BlackInGoodPosition(), -300)
            ]"""

        elif phase == ph.MIDDLE:
            """return [
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]
          return [
                (WhiteCount(), 2),
                (BlackCount(), -2),
                (NearKing(), -10),
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 2)
            ]
            return[
                (FreeWinningPoints(), 300),
                (WhiteCount(), 30),
                (BlackCount(), -20),
                (NearKing(), -1000),
                (KingInWinningPosition(), 2000),
                (KingPositioning(), 100)
            ]

            return [
                (FreeWinningPoints(), 100),
                (WhiteWinningPoints(), 200),
                (BlackWinningPoints(), -300),
                (WhiteCount(), 200),
                (BlackCount(), -500),
                (NearKing(), -1000),
                (KingInWinningPosition(), 10000),
                (KingPositioning(), 100),
                (BlackInGoodPosition(), -300)
            ]"""

        elif phase == ph.LATE:
            """return [
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]
          return [
                (WhiteCount(), 2),
                (BlackCount(), -2),
                (NearKing(), -10),
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 2)
            ]
            return[
                (FreeWinningPoints(), 300),
                (WhiteCount(), 30),
                (BlackCount(), -20),
                (NearKing(), -1000),
                (KingInWinningPosition(), 2000),
                (KingPositioning(), 100)
            ]

            return [
                (FreeWinningPoints(), 100),
                (WhiteWinningPoints(), 200),
                (BlackWinningPoints(), -300),
                (WhiteCount(), 200),
                (BlackCount(), -500),
                (NearKing(), -1000),
                (KingInWinningPosition(), 10000),
                (KingPositioning(), 100),
                (BlackInGoodPosition(), -300)
            ]"""
        else:
            print("Fase non riconosciuta")

    def black_strategies(phase):
        if phase == ph.START:
            multiplier = 4
            if state.king_position == Position(4, 4):
                multiplier = 2
            if state.king_position == Position(4, 3):
                multiplier = 2
            if state.king_position == Position(4, 5):
                multiplier = 2
            if state.king_position == Position(3, 4):
                multiplier = 2
            if state.king_position == Position(5, 4):
                multiplier = 2
            return [
                (BlackInGoodPosition(), 12), (KingInWinningPosition(), -5000), (WhiteGoodPosition(), -4),
                (NearKing(), multiplier), (PawnDifference(), 4)
            ]

        elif phase == ph.MIDDLE:
            multiplier = 4
            if state.king_position == Position(4, 4):
                multiplier = 2
            if state.king_position == Position(4, 3):
                multiplier = 2
            if state.king_position == Position(4, 5):
                multiplier = 2
            if state.king_position == Position(3, 4):
                multiplier = 2
            if state.king_position == Position(5, 4):
                multiplier = 2
            return [
                (BlackInGoodPosition(), 12), (KingInWinningPosition(), -5000), (WhiteGoodPosition(), -4),
                (NearKing(), multiplier), (PawnDifference(), 4)
            ]

        elif phase == ph.LATE:
            multiplier = 4
            if state.king_position == Position(4, 4):
                multiplier = 2
            if state.king_position == Position(4, 3):
                multiplier = 2
            if state.king_position == Position(4, 5):
                multiplier = 2
            if state.king_position == Position(3, 4):
                multiplier = 2
            if state.king_position == Position(5, 4):
                multiplier = 2
            return [
                (BlackInGoodPosition(), 12), (KingInWinningPosition(), -5000), (WhiteGoodPosition(), -4),
                (NearKing(), multiplier), (PawnDifference(), 4)
            ]
        else:
            print("Fase non riconosciuta")

    # get_function() body

    strategies = white_strategies(phase) if player == config.WHITE \
        else (black_strategies(phase) if player == config.BLACK else ())
    """strategies = black_strategies(phase) if player == config.WHITE \
        else (white_strategies(phase) if player == config.BLACK else ())"""

    return hf.HeuristicFunction(strategies)
