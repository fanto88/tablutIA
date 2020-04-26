import numpy

from state.pawn import Pawn
from utils import config
import utils.bitboard_util as bitboard_util
from utils.action import Action


# TODO: Pulire il codice e renderlo il più veloce ed ottimizzato possibile
# TODO: Migliorare il print_bitboard dentro bitboard_util.py
# TODO: La board serve davvero?
# TODO: Dove si fa il controllo se mangia qualcosa?
# TODO: Check della vittoria, sconfitta o pareggio
# TODO : come faccio a modificare direttamente self.__white_bitboard??? dentro move
# TODO: Ogni tanto non trova una mossa da fare, problema dello stato oppure del random?
# TODO: Capire perchè ogni volta bisogna instanziare di nuovo le bitboard a vuoto dentro move
# TODO: Obstacle bitboard inutile?

class TablutState:
    def __init__(self):
        self.__board = numpy.full((9, 9), Pawn.Empty.value)
        self.__white_bitboard = numpy.zeros(shape=9, dtype=int)
        self.__king_bitboard = numpy.zeros(shape=9, dtype=int)
        self.__black_bitboard = numpy.zeros(shape=9, dtype=int)
        self.__obstacle_bitboard = numpy.zeros(shape=9, dtype=int)
        self.__escape_bitboard = numpy.empty(shape=9, dtype=int)
        self.__camps_bitboard = numpy.empty(shape=9, dtype=int)
        self.__throne_bitboard = numpy.empty(shape=9, dtype=int)
        self.__turn = config.WHITE

        # Initialize Board Escape Point
        self.__board[0][1] = self.__board[0][2] = self.__board[0][6] = self.__board[0][7] = Pawn.Escapes.value
        self.__board[1][0] = self.__board[1][8] = Pawn.Escapes.value
        self.__board[2][0] = self.__board[2][8] = Pawn.Escapes.value
        self.__board[6][0] = self.__board[6][8] = Pawn.Escapes.value
        self.__board[7][0] = self.__board[7][8] = Pawn.Escapes.value
        self.__board[8][1] = self.__board[8][2] = self.__board[8][6] = self.__board[8][7] = Pawn.Escapes.value

        # Initialize Escape Bitboard
        self.__escape_bitboard[0] = 0b011000110
        self.__escape_bitboard[1] = 0b100000001
        self.__escape_bitboard[2] = 0b100000001
        self.__escape_bitboard[3] = 0b000000000
        self.__escape_bitboard[4] = 0b000000000
        self.__escape_bitboard[5] = 0b000000000
        self.__escape_bitboard[6] = 0b100000001
        self.__escape_bitboard[7] = 0b100000001
        self.__escape_bitboard[8] = 0b011000110

        # Initialize Camps Bitboard
        self.__camps_bitboard[0] = 0b000111000
        self.__camps_bitboard[1] = 0b000010000
        self.__camps_bitboard[2] = 0b000000000
        self.__camps_bitboard[3] = 0b100000001
        self.__camps_bitboard[4] = 0b110000011
        self.__camps_bitboard[5] = 0b100000001
        self.__camps_bitboard[6] = 0b000000000
        self.__camps_bitboard[7] = 0b000010000
        self.__camps_bitboard[8] = 0b000111000

        # Initialize Throne Bitboard
        self.__throne_bitboard[0] = 0b000000000
        self.__throne_bitboard[1] = 0b000000000
        self.__throne_bitboard[2] = 0b000000000
        self.__throne_bitboard[3] = 0b000000000
        self.__throne_bitboard[4] = 0b000010000
        self.__throne_bitboard[5] = 0b000000000
        self.__throne_bitboard[6] = 0b000000000
        self.__throne_bitboard[7] = 0b000000000
        self.__throne_bitboard[8] = 0b000000000

    def turn(self, turn=None):
        if turn is None:
            return self.__turn
        self.__turn = turn
        return self

    def white_bitboard(self, white_bitboard=None):
        if white_bitboard is None:
            return self.__white_bitboard
        self.__white_bitboard = white_bitboard
        return self

    def black_bitboard(self, black_bitboard=None):
        if black_bitboard is None:
            return self.__black_bitboard
        self.__black_bitboard = black_bitboard
        return self

    def obstacle_bitboard(self, obstacle_bitboard=None):
        if obstacle_bitboard is None:
            return self.__obstacle_bitboard
        self.__obstacle_bitboard = obstacle_bitboard
        return self

    def king_bitboard(self, king_bitboard=None):
        if king_bitboard is None:
            return self.__king_bitboard
        self.__king_bitboard = king_bitboard
        return self

    def throne_bitboard(self, throne_bitboard=None):
        if throne_bitboard is None:
            return self.__throne_bitboard
        self.__throne_bitboard = throne_bitboard
        return self

    def camps_bitboard(self, camps_bitboard=None):
        if camps_bitboard is None:
            return self.__camps_bitboard
        self.__camps_bitboard = camps_bitboard
        return self

    def board(self, board=None):
        if board is None:
            return self.__board
        self.__board = board
        return self

    def load_state_from_json(self, json_string):
        row_index = 0
        self.__turn = json_string["turn"]
        if (self.__turn != config.WHITE) & (self.__turn != config.BLACK):
            return
        self.__white_bitboard = numpy.zeros(shape=9, dtype=int)
        self.__king_bitboard = numpy.zeros(shape=9, dtype=int)
        self.__black_bitboard = numpy.zeros(shape=9, dtype=int)
        for row in json_string["board"]:
            column_index = 8
            for column in row:
                if column == "WHITE":
                    self.__board[row_index][column_index] = Pawn.White.value
                    self.__white_bitboard[row_index] |= 1 << column_index
                elif column == "BLACK":
                    self.__board[row_index][column_index] = Pawn.Black.value
                    self.__black_bitboard[row_index] |= 1 << column_index
                elif column == "KING":
                    self.__board[row_index][column_index] = Pawn.King.value
                    self.__king_bitboard[row_index] |= 1 << column_index
                column_index -= 1
            row_index += 1

    def move(self, action: Action):
        if action.role() == config.WHITE:
            if bitboard_util.get_bit(self.__white_bitboard, action.start().row(), action.start().column()) == 1:
                self.__white_bitboard = bitboard_util.set(self.__white_bitboard, action.end().row(), action.end().column())
                self.__white_bitboard = bitboard_util.unset(self.__white_bitboard, action.start().row(), action.start().column())
            else:
                self.__king_bitboard = bitboard_util.set(self.__king_bitboard, action.end().row(), action.end().column())
                self.__king_bitboard = bitboard_util.unset(self.__king_bitboard, action.start().row(), action.start().column())
        else:
            self.__black_bitboard = bitboard_util.set(self.__black_bitboard, action.end().row(), action.end().column())
            self.__black_bitboard= bitboard_util.unset(self.__black_bitboard, action.start().row(), action.start().column())
