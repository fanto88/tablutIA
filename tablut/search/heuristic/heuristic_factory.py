import tablut.search.heuristic.strategies as strategies
import tablut.search.heuristic.phase as ph
import tablut.utils.config as config
import tablut.search.heuristic.heuristic_function as hf
from tablut.search.heuristic.strategies.black_in_good_position import BlackInGoodPosition
from tablut.search.heuristic.strategies.king_in_winning_position import KingInWinningPosition
from tablut.search.heuristic.strategies.king_positioning import KingPositioning
from tablut.search.heuristic.strategies.near_king import NearKing
from tablut.search.heuristic.strategies.pawn_difference import PawnDifference
from tablut.search.heuristic.strategies.white_good_position import WhiteGoodPosition
from tablut.utils.action import Position


def get_function(state, player, phase) -> hf.HeuristicFunction:
    def white_strategies(phase):
        """
            TODO: provare a vedere che la fase funzioni correttamente


        """
        if phase == ph.START:
            return [
                (KingPositioning(), 10),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]

        elif phase == ph.MIDDLE:
            return [
                (KingPositioning(), 10),
                (KingInWinningPosition(), 5000),
                (WhiteGoodPosition(), 3),
                (PawnDifference(), -5),
                (NearKing(), -2)
            ]

        elif phase == ph.LATE:
            return [
                (KingPositioning(), 10),
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
            pawns_difference = state.black_count - state.white_count * 2
            multiplier += 0.4 * pawns_difference
            return [
                        (BlackInGoodPosition(), 6), (KingInWinningPosition(), -5000), (WhiteGoodPosition(), -4),
                        (NearKing(), multiplier),  (PawnDifference(), pawns_difference * (2 + 0.3 * pawns_difference))
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
            pawns_difference = state.black_count - state.white_count * 2
            multiplier += 0.4 * pawns_difference
            return [
                (BlackInGoodPosition(), 6), (KingInWinningPosition(), -5000), (WhiteGoodPosition(), -4),
                (NearKing(), multiplier), (PawnDifference(), pawns_difference * (2 + 0.3 * pawns_difference))
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
            pawns_difference = state.black_count - state.white_count * 2
            multiplier += 0.4 * pawns_difference
            return [
                (BlackInGoodPosition(), 6), (KingInWinningPosition(), -5000), (WhiteGoodPosition(), -4),
                (NearKing(), multiplier), (PawnDifference(), pawns_difference * (2 + 0.3 * pawns_difference))
            ]
        else:
            print("Fase non riconosciuta")

    # get_function() body

    strategies = white_strategies(phase) if player == config.WHITE \
                                        else (black_strategies(phase) if player == config.BLACK else ())
    """strategies = black_strategies(phase) if player == config.WHITE \
        else (white_strategies(phase) if player == config.BLACK else ())"""

    return hf.HeuristicFunction(strategies)
