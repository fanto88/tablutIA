import numpy

import utils.bitboard_util as bitboard_util
from state.state import State
from utils import config
from utils.action import Action, Position


# TODO: Pulire il codice e renderlo il più veloce ed ottimizzato possibile. Togliere tutti i for per esempio
# TODO: Dove si fa il controllo se mangia qualcosa?
# TODO: Check della vittoria, sconfitta o pareggio
# TODO: Come faccio a modificare direttamente self.__white_bitboard??? dentro move
# TODO: Capire perchè ogni volta bisogna instanziare di nuovo le bitboard a vuoto dentro move.
#           Per il semplice motivo che altrimenti fa l'or con quella vecchia
# TODO: Funzione che hasha lo stato

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

    def get_available_moves_for_pawn(self, position, obstacle_bitboard, color):
        row_index = position.row()
        column_index = position.column()
        all_available_moves_for_pawn = []
        for row in range(row_index - 1, -1, -1):
            if bitboard_util.get_bit(obstacle_bitboard, row, column_index) != 1:
                action = Action(Position(row_index, column_index), Position(row, column_index), color)
                all_available_moves_for_pawn.append(action)
            else:
                break
        for col in range(column_index - 1, -1, -1):
            if bitboard_util.get_bit(obstacle_bitboard, row_index, col) != 1:
                action = Action(Position(row_index, column_index), Position(row_index, col), color)
                all_available_moves_for_pawn.append(action)
            else:
                break
        for row in range(row_index + 1, 9):
            if bitboard_util.get_bit(obstacle_bitboard, row, column_index) != 1:
                action = Action(Position(row_index, column_index), Position(row, column_index), color)
                all_available_moves_for_pawn.append(action)
            else:
                break
        for col in range(column_index + 1, 9):
            if bitboard_util.get_bit(obstacle_bitboard, row_index, col) != 1:
                action = Action(Position(row_index, column_index), Position(row_index, col), color)
                all_available_moves_for_pawn.append(action)
            else:
                break
        return all_available_moves_for_pawn

    def all_available_moves(self, state, color):
        all_available_moves = []
        if color == config.WHITE:
            obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
            for row_index in range(0, 9):
                for column_index in range(0, 9):
                    if bitboard_util.get_bit((state.white_bitboard | state.king_bitboard), row_index,
                                             column_index) == 1:
                        all_available_moves += self.get_available_moves_for_pawn(Position(row_index, column_index),
                                                                                 obstacle_bitboard, config.WHITE)
        else:
            obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard
            for row_index in range(0, 9):
                for column_index in range(0, 9):
                    if bitboard_util.get_bit(state.black_bitboard, row_index, column_index):
                        new_obstacle_bitboard = obstacle_bitboard.copy()
                        if (row_index == 8 or row_index == 0) & (column_index == 3 or column_index == 5):
                            row = 8 - row_index
                            new_obstacle_bitboard = bitboard_util.set(new_obstacle_bitboard, row, column_index)

                        elif (row_index == 3 or row_index == 5) & (column_index == 3 or column_index == 8):
                            column = 8 - column_index
                            new_obstacle_bitboard = bitboard_util.set(new_obstacle_bitboard, row_index, column)

                        else:
                            new_obstacle_bitboard |= state.camps_bitboard
                        all_available_moves += self.get_available_moves_for_pawn(Position(row_index, column_index),
                                                                                 new_obstacle_bitboard, config.BLACK)

        return all_available_moves

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
