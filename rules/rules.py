from logging import Logger

import numpy

from exceptions.custom_exceptions import *
from state.tablut_state import TablutState
from utils import config
from utils.bitboard_util import Bitboard


class Tablut:  # TODO: add other methods, such as expand, actions, ...
    """
    A simple interface that every rule-class should implement
    """

    def __init__(self, initial_state, logger=None):  # TODO: implement log_file
        self.initial_state = initial_state
        self.logger = Logger("TablutGame") if logger is None else logger
        #self.log_file

    def check_move(self, state, action):
        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """
        raise NotImplementedError()


#TODO: log delle cose???
#TODO: Mettere state: State e fare in modo che TablutState estenda State, in questo modo disaccoppio meglio
#TODO: mettere in ordine di probabilità, così finisce prima
class AshtonTablutRules(Tablut):
    """
    Class that implements rules of classic tablut (9x9 chessboard)
    """

    def check_move(self, state: TablutState, action: Action):
        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """

        # If Starting Position is equal to Ending Position than you are not moving any pawn
        if action.start() == action.end():
            raise StopException(action)

        # If you want to move a pawn to a position that is not empty
        if Bitboard.get_bit(state.obstacle_bitboard(), action.end().row(), action.end().column()) == 1:
            raise OccupitedException(action)

        # If there is an obstacle between your final position and your actual position
        if action.start().row() == action.end().row(): #TODO : Controllare che funzioni davvero
            min_col = numpy.minimum(action.start().column(), action.end().column())
            max_col = numpy.maximum(action.start().column(), action.end().column())
            while max_col != min_col:
                if Bitboard.get_bit(state.obstacle_bitboard(), action.start().row(), max_col):
                    raise ClimbingException(action)
                max_col -= 1
        else:
            min_row = numpy.minimum(action.start().row(), action.end().row())
            max_row = numpy.maximum(action.start().row(), action.end().row())
            while max_row != min_row:
                if Bitboard.get_bit(state.obstacle_bitboard(), max_row, action.start().column()):
                    raise ClimbingException(action)
                max_row -= 1

        # If i'm moving a correct pawn
        if action.role() == config.WHITE:
            bitboard = state.white_bitboard() | state.king_bitboard()
            if Bitboard.get_bit(bitboard, action.start().row(), action.start().column()) == 0:
                raise PawnException(action)

        # If i'm moving a correct pawn
        if action.role() == config.BLACK:
            if Bitboard.get_bit(state.black_bitboard(), action.start().row(), action.start().column()) == 0:
                raise PawnException(action)

        # If diagonal move
        if (action.start().row() != action.end().row()) & (action.start().column() != action.end().column()):
            raise DiagonalException(action)

        return True

    def __move_piece(self, state, action):   # TODO: implement move_piece
        """
        Move a piece from the given state using the action
        """
        raise NotImplementedError()

    def __check_capture_white(self, state, action):  # TODO: implement check capture white
        """
        Checks if performing the given action will end in capture one or more white pieces and then
        returns the new corrisponding state
        """
        raise NotImplementedError()

    def __check_capture_black(self, state, action):  # TODO: implement check capture white
        """
        Checks if performing the given action will end in capture one or more black pieces and then
        returns the new corrisponding state
        """
        raise NotImplementedError()
