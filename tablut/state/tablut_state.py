import tablut.utils.bitboard_util as bitboard_util
from tablut.state.state import State
from tablut.utils import config
from tablut.utils.action import Action


# TODO: Pulire il codice e renderlo il più veloce ed ottimizzato possibile. Togliere tutti i for per esempio
# TODO: Dove si fa il controllo se mangia qualcosa?
# TODO: Come faccio a modificare direttamente self.__white_bitboard??? dentro move
# TODO: Migliorare il controllo se mangia il re o altre pedine strane
# TODO: Check if check_if_eat funziona, guardare anche dentro heuristica se effettivamente dice che mangia

class TablutState(State):
    def __init__(self, color):
        super().__init__(color)

    def check_ended(self):
        bitboard = self.white_bitboard | self.king_bitboard
        result = False
        if (bitboard[0] | bitboard[1] | bitboard[2] | bitboard[4] | bitboard[5] | bitboard[6] | bitboard[7] | bitboard[
            8]) == 0:
            self.winner = config.BLACK
            result = True
        elif (self.king_bitboard[0] | self.king_bitboard[1] | self.king_bitboard[2] | self.king_bitboard[4] |
              self.king_bitboard[5] | self.king_bitboard[6] | self.king_bitboard[7] | self.king_bitboard[8]) == 0:
            self.winner = config.BLACK
            result = True
        elif (self.black_bitboard[0] | self.black_bitboard[1] | self.black_bitboard[2] | self.black_bitboard[4] |
              self.black_bitboard[5] | self.black_bitboard[6] | self.black_bitboard[7] | self.black_bitboard[8]) == 0:
            self.winner = config.WHITE
            result = True

        return result

    def check_if_eat(self, bitboard, position):
        obstacle_bitboard = self.black_bitboard | self.white_bitboard | self.king_bitboard | self.throne_bitboard | self.camps_bitboard
        if position.row() - 2 >= 0:
            if bitboard_util.get_bit(obstacle_bitboard, position.row() - 2, position.column()) == 1:
                if bitboard_util.get_bit(bitboard, position.row() - 1, position.column()) == 1:
                    bitboard = bitboard_util.unset(bitboard, position.row() - 1, position.column())

        if position.column() - 2 >= 0:
            if bitboard_util.get_bit(obstacle_bitboard, position.row(), position.column() - 2) == 1:
                if bitboard_util.get_bit(bitboard, position.row(), position.column() - 1) == 1:
                    bitboard = bitboard_util.unset(bitboard, position.row(), position.column() - 1)

        if position.row() + 2 <= 8:
            if bitboard_util.get_bit(obstacle_bitboard, position.row() + 2, position.column()) == 1:
                if bitboard_util.get_bit(bitboard, position.row() + 1, position.column()) == 1:
                    bitboard = bitboard_util.unset(bitboard, position.row() + 1, position.column())

        if position.column() + 2 <= 8:
            if bitboard_util.get_bit(obstacle_bitboard, position.row(), position.column() + 2) == 1:
                if bitboard_util.get_bit(bitboard, position.row(), position.column() + 1) == 1:
                    bitboard = bitboard_util.unset(bitboard, position.row(), position.column() + 1)
        return bitboard

    def move(self, action: Action):
        if action.role() == config.WHITE:
            if bitboard_util.get_bit(self.white_bitboard, action.start().row(), action.start().column()) == 1:
                self.white_bitboard = bitboard_util.set(self.white_bitboard, action.end().row(),
                                                        action.end().column())
                self.white_bitboard = bitboard_util.unset(self.white_bitboard, action.start().row(),
                                                          action.start().column())
                self.black_bitboard = self.check_if_eat(self.black_bitboard, action.end())
            else:
                self.king_bitboard = bitboard_util.set(self.king_bitboard, action.end().row(),
                                                       action.end().column())
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, action.start().row(),
                                                         action.start().column())
                self.black_bitboard = self.check_if_eat(self.black_bitboard, action.end())
        else:
            self.black_bitboard = bitboard_util.set(self.black_bitboard, action.end().row(), action.end().column())
            self.black_bitboard = bitboard_util.unset(self.black_bitboard, action.start().row(),
                                                      action.start().column())
            self.white_bitboard = self.check_if_eat(self.white_bitboard, action.end())
            self.king_bitboard = self.check_if_eat(self.king_bitboard, action.end())
        return self

    def __hash__(self):
        return hash((
            tuple(self.white_bitboard),
            tuple(self.king_bitboard),
            tuple(self.black_bitboard),
            tuple(self.escape_bitboard),
            tuple(self.camps_bitboard),
            tuple(self.throne_bitboard),
            self.turn,
            self.winner
        ))

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

    def __repr__(self):
        return "HASH: {:d}".format(hash(self))
