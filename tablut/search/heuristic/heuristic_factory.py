import tablut.search.heuristic.heuristic_function as hf
import tablut.search.heuristic.phase as ph
import tablut.utils.config as config
from tablut.search.heuristic.strategies.black_in_good_position import BlackInGoodPosition
from tablut.search.heuristic.strategies.king_in_winning_position import KingInWinningPosition
from tablut.search.heuristic.strategies.king_positioning import KingPositioning
from tablut.search.heuristic.strategies.near_king import NearKing
from tablut.search.heuristic.strategies.pawn_difference import PawnDifference
from tablut.search.heuristic.strategies.white_good_position import WhiteGoodPosition
from tablut.utils.action import Position


def get_function(state, player, phase) -> hf.HeuristicFunction:
    def white_strategies(phase):
        if phase == ph.START:
            return [
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]
        elif phase == ph.MIDDLE:
            return [
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]
        elif phase == ph.LATE:
            return [
                (KingPositioning(), 100),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]
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
    return hf.HeuristicFunction(strategies)
