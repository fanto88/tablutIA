import tablut.search.heuristic.strategies as strategies
import tablut.search.heuristic.phase as ph
import tablut.utils.config as config
import tablut.search.heuristic.heuristic_function as hf


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

    # get_function() body

    strategies = white_strategies(phase) if player == config.WHITE \
                                        else (black_strategies(phase) if player == config.BLACK else ())

    return hf.HeuristicFunction(strategies)
