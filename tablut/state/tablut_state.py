import tablut.utils.bitboard_util as bitboard_util
from tablut.state.state import State
from tablut.utils import config
from tablut.utils.action import Action


# TODO: Pulire il codice e renderlo il più veloce ed ottimizzato possibile. Togliere tutti i for per esempio
# TODO: Dove si fa il controllo se mangia qualcosa?
# TODO: Come faccio a modificare direttamente self.__white_bitboard??? dentro move
# TODO: Fare la funzione che mangia le varie pedine e il re

class TablutState(State):
    def __init__(self, color):
        super().__init__(color)

    def check_ended(self):
        bitboard = self.white_bitboard | self.king_bitboard
        if (self.king_bitboard[0] | self.king_bitboard[1] | self.king_bitboard[2] | self.king_bitboard[4] |
                self.king_bitboard[5] | self.king_bitboard[6] | self.king_bitboard[7] | self.king_bitboard[8]) == 0:
            self.winner = config.BLACK
            return True
        if (bitboard[0] | bitboard[1] | bitboard[2] | bitboard[4] | bitboard[5] | bitboard[6] | bitboard[7] |
                bitboard[8]) == 0:
            self.winner = config.BLACK
            return True
        if (self.black_bitboard[0] | self.black_bitboard[1] | self.black_bitboard[2] | self.black_bitboard[4] |
                self.black_bitboard[5] | self.black_bitboard[6] | self.black_bitboard[7] | self.black_bitboard[8]) == 0:
            self.winner = config.WHITE
            return True
        return False

    def move(self, action: Action):
        if action.role() == config.WHITE:
            if bitboard_util.get_bit(self.white_bitboard, action.start().row(), action.start().column()) == 1:
                self.white_bitboard = bitboard_util.set(self.white_bitboard, action.end().row(),
                                                        action.end().column())
                self.white_bitboard = bitboard_util.unset(self.white_bitboard, action.start().row(),
                                                          action.start().column())
            else:
                self.king_bitboard = bitboard_util.set(self.king_bitboard, action.end().row(),
                                                       action.end().column())
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, action.start().row(),
                                                         action.start().column())
        else:
            self.black_bitboard = bitboard_util.set(self.black_bitboard, action.end().row(), action.end().column())
            self.black_bitboard = bitboard_util.unset(self.black_bitboard, action.start().row(),
                                                      action.start().column())
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
