import numpy

import tablut.utils.bitboard_util as bitboard_util
from tablut.state.state import State
from tablut.state.state_factory import StateFactory
from tablut.utils import config
from tablut.utils.action import Action


# TODO: Pulire il codice e renderlo il più veloce ed ottimizzato possibile. Togliere tutti i for per esempio
# TODO: Dove si fa il controllo se mangia qualcosa?
# TODO: Come faccio a modificare direttamente self.__white_bitboard??? dentro move
# TODO: Capire perchè ogni volta bisogna instanziare di nuovo le bitboard a vuoto dentro move.
#           Per il semplice motivo che altrimenti fa l'or con quella vecchia


class TablutState(State):
    def __init__(self, color):
        super().__init__(color)

    def load_state_from_json(self, json_string):
        row_index = 0
        self.turn = json_string["turn"]
        if (self.turn != config.WHITE) & (self.turn != config.BLACK):
            return
        self.white_bitboard = numpy.zeros(shape=9, dtype=int)
        self.king_bitboard = numpy.zeros(shape=9, dtype=int)
        self.black_bitboard = numpy.zeros(shape=9, dtype=int)
        for row in json_string["board"]:
            column_index = 8
            for column in row:
                if column == "WHITE":
                    self.white_bitboard[row_index] |= 1 << column_index
                elif column == "BLACK":
                    self.black_bitboard[row_index] |= 1 << column_index
                elif column == "KING":
                    self.king_bitboard[row_index] |= 1 << column_index
                column_index -= 1
            row_index += 1
        return self

    def load_state_from_action(self, state, action):
        return StateFactory.load_state_from_action(state, action)

    def check_ended(self):
        bitboard = self.white_bitboard | self.king_bitboard
        result = False
        if (bitboard[0] | bitboard[1] | bitboard[2] | bitboard[4] | bitboard[5] | bitboard[6] | bitboard[7] | bitboard[
            8]) == 0:
            self.winner = config.BLACK
            result = True
        elif (self.black_bitboard[0] | self.black_bitboard[1] | self.black_bitboard[2] | self.black_bitboard[4] |
              self.black_bitboard[5] | self.black_bitboard[6] | self.black_bitboard[7] | self.black_bitboard[8]) == 0:
            self.winner = config.WHITE
            result = True
        return result

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
