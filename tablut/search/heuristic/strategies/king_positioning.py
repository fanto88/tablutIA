from tablut.utils import config


class KingPositioning:
    max = 1
    min = -1

    def eval(self, state, player):
        result = 0
        if state.king_position is not None:
            row = state.king_position.row
            column = state.king_position.column
            # Sul Trono
            if row == 4 and column == 4:
                result -= 10

            # Riga 3, 7
            elif (row == 2 or row == 6) and (column == 1 or column == 2 or column == 3 or column == 4 or column == 5
                                             or column == 6 or column == 7):
                result += 2

            # Riga 2, 4, 5, 6, 8
            elif (row == 1 or row == 3 or row == 4 or row == 5 or row == 7) and (column == 2 or column == 6):
                result += 2

            # Riga 4
            elif row == 3 and (column == 2 or column == 6):
                result += 2

            # Riga 2, 8
            elif (row == 1 or row == 7) and (column == 1 or column == 3 or column == 5 or column == 7):
                result += 1

            # Riga 4, 6
            elif (row == 3 or row == 5) and (column == 1 or column == 7):
                result += 1

        if player == config.WHITE:
            return result
        return -result
