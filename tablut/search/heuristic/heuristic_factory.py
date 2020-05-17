import tablut.search.heuristic.strategies as strategies
import tablut.search.heuristic.phase as ph
import tablut.utils.config as config
import tablut.search.heuristic.heuristic_function as hf
from tablut.search.heuristic.strategies.black_in_good_position import BlackInGoodPosition
from tablut.search.heuristic.strategies.king_in_winning_position import KingInWinningPosition
from tablut.search.heuristic.strategies.near_king import NearKing
from tablut.search.heuristic.strategies.pawn_difference import PawnDifference
from tablut.search.heuristic.strategies.white_good_position import WhiteGoodPosition


def get_function(state, player, phase) -> hf.HeuristicFunction:

    def white_strategies(phase):
        if phase == ph.START:
            # Aggiungi
            pass

        elif phase == ph.MIDDLE:
            # TODO: aggiungi
            pass

        elif phase == ph.LATE:
            # TODO: aggiungi
            pass
        else:
            print("Fase non riconosciuta")

    def black_strategies(phase):
        if phase == ph.START:
            multiplier = 4
            if state.king_on_throne() or state.adjacent_throne:
                multiplier = 2

            multiplier += 0.4 * (state.black_count - state.white_count * 2)
            return [
                        (BlackInGoodPosition(), 6), (KingInWinningPosition(), 5000), (WhiteGoodPosition(), 4),
                        (NearKing(), multiplier), (PawnDifference(), (2 + 0.3 * (state.black_count - state.white_bitboard * 2)))
                    ]
            pass

        elif phase == ph.MIDDLE:
            # TODO: aggiungi
            pass

        elif phase == ph.LATE:
            # TODO: aggiungi
            pass
        else:
            print("Fase non riconosciuta")

    # get_function() body

    strategies = white_strategies(phase) if player == config.WHITE \
                                        else (black_strategies(phase) if player == config.BLACK else ())

    return hf.HeuristicFunction(strategies)
