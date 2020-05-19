from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import config


class KingPositioning(HeuristicStrategy):
    max = 1
    min = -1

    def eval(self, state, player):
        value = 0
        if state.king_position is not None:
            row = state.king_position.row
            column = state.king_position.column
            # Sul Trono
            if row == 4 and column == 4:
                value = -90

            # Riga 3, 7
            elif (row == 2 or row == 6) and (column == 1 or column == 2 or column == 3 or column == 4 or column == 5
                                             or column == 6 or column == 7):
                value = 2

            # Riga 2, 4, 5, 6, 8
            elif (row == 1 or row == 3 or row == 4 or row == 5 or row == 7) and (column == 2 or column == 6):
                value = 2

            # Riga 4
            elif row == 3 and (column == 2 or column == 6):
                value = 2

            # Riga 2, 8
            elif (row == 1 or row == 7) and (column == 1 or column == 3 or column == 5 or column == 7):
                value = 1

            # Riga 4, 6
            elif (row == 3 or row == 5) and (column == 1 or column == 7):
                value = 1

            elif (row == 0 or row == 8) and (column == 1 or column == 2 or column == 3 or column == 6 or column == 7):
                value = 100

            elif (row == 1 or row == 2 or row == 6 or row == 7) and (column == 0 or column == 8):
                value = 100

        return value
