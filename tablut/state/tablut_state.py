from copy import deepcopy

import tablut.utils.bitboard_util as bitboard_util
from tablut.state.state import State
from tablut.utils import config
from tablut.utils.action import Action, Position


# TODO: Pulire il codice e renderlo il più veloce ed ottimizzato possibile. Togliere tutti i for per esempio
# TODO: Dove si fa il controllo se mangia qualcosa?
# TODO: Come faccio a modificare direttamente self.__white_bitboard??? dentro move
# TODO: Fare la funzione che mangia le varie pedine e il re
# TODO: Forse muore quando cambio la bitboard del re perchè fa il check della vittoria
# TODO: Funzione per contare quante pedine una pedina ha intorno
# TODO: Capire come controllare se hai una pedina da un lato e una dall'altro
# TODO: If any al posto di tutte le righe in OR nella funzione check_ended
# TODO: Ma se quando muore il re mettessi None? Mi basta fare il controllo dopo, se è none allora è morto
class TablutState(State):
    def __init__(self, color):
        super().__init__(color)

    def eat_king(self, action):
        obstacle_bitboard = self.black_bitboard | self.king_bitboard | self.throne_bitboard | self.camps_bitboard
        # Se è sul Trono
        if self.king_position == Position(4, 4):
            if bitboard_util.count_adjacent(self.king_position, obstacle_bitboard) == 4:
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, self.king_position.row(),
                                                         self.king_position.column())
                self.king_position = None
        # Se è adiacente al trono
        elif (self.king_position == Position(3, 4)) or (self.king_position == Position(5, 4)) or (
                self.king_position == Position(4, 5)) or (self.king_position == Position(4, 3)):
            if bitboard_util.count_adjacent(self.king_position, obstacle_bitboard) == 4:
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, self.king_position.row(),
                                                         self.king_position.column())
                self.king_position = None
        # Se è lontano dal trono
        else:
            obstacle_bitboard = self.king_bitboard | self.black_bitboard | self.throne_bitboard | self.camps_bitboard
            self.king_bitboard = bitboard_util.eat(self.king_bitboard, obstacle_bitboard, action.end())
            self.king_position = None

    def check_ended(self):
        if bitboard_util.count_piece(self.king_bitboard) == 0:
            self.winner = config.BLACK
            return True

        if bitboard_util.count_piece(self.black_bitboard) == 0:
            self.winner = config.WHITE
            return True

        # TODO: Da verificare che funzioni
        if bitboard_util.count_piece(self.king_bitboard & self.escape_bitboard) == 1:
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
                self.king_position = Position(action.end().row(), action.end().column())
            obstacle_bitboard = self.king_bitboard | self.white_bitboard | self.throne_bitboard | self.camps_bitboard
            self.black_bitboard = bitboard_util.eat(self.black_bitboard, obstacle_bitboard, action.end())
        else:
            self.black_bitboard = bitboard_util.set(self.black_bitboard, action.end().row(), action.end().column())
            self.black_bitboard = bitboard_util.unset(self.black_bitboard, action.start().row(),
                                                      action.start().column())
            obstacle_bitboard = self.king_bitboard | self.black_bitboard | self.throne_bitboard | self.camps_bitboard
            self.eat_king(action)

            self.white_bitboard = bitboard_util.eat(self.white_bitboard, obstacle_bitboard, action.end())
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
