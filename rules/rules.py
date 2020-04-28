from logging import Logger

import numpy

from exceptions.custom_exceptions import *
from state.tablut_state import TablutState
from utils import config
import utils.bitboard_util as bitboard_util


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
#TODO: il trono può essere scavalcato, non lo gestisco
#TODO: i campi non vengono gestiti bene nel caso tu ci sia dentro oppure no
#TODO: Obstacle bitboard??
class AshtonTablutRules(Tablut):
    """
    Class that implements rules of classic tablut (9x9 chessboard)
    """

    def check_move(self, state: TablutState, action: Action):
        obstacle_bitboard = state.black_bitboard() | state.white_bitboard() | state.king_bitboard() | state.throne_bitboard() | state.camps_bitboard()
        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """
        # Check if is not moving out of the board
        # TODO: Come fare che il numero 8 non sia a mano??
        if (action.end().row() > 8) | (action.end().column() > 8):
            raise BoardException(action)

        # Check if you are actually moving a pawn
        if action.start().__eq__(action.end()):
            raise StopException(action)

        # Check if you are moving to an empty space
        # TODO: Non mi viene in mente come gestire i campi se son vuoti. Una seconda bitboard?
        if bitboard_util.get_bit(obstacle_bitboard, action.end().row(), action.end().column()) == 1:
            raise OccupitedException(action)

        # Check if it's a diagonal move
        if (action.start().row() != action.end().row()) & (action.start().column() != action.end().column()):
            raise DiagonalException(action)

        # Check If there is an obstacle between your final position and your actual position
        if action.start().row() == action.end().row():
            min_col = numpy.minimum(action.start().column(), action.end().column())
            max_col = numpy.maximum(action.start().column(), action.end().column())
            while max_col != min_col:
                if bitboard_util.get_bit(obstacle_bitboard, action.start().row(), max_col):
                    raise ClimbingException(action)
                max_col -= 1
        else:
            min_row = numpy.minimum(action.start().row(), action.end().row())
            max_row = numpy.maximum(action.start().row(), action.end().row())
            while max_row != min_row:
                if bitboard_util.get_bit(obstacle_bitboard, max_row, action.start().column()):
                    raise ClimbingException(action)
                max_row -= 1

        # If i'm moving a correct pawn
        if action.role() == config.WHITE:
            if bitboard_util.get_bit(state.white_bitboard() | state.king_bitboard(), action.start().row(), action.start().column()) == 0:
                raise PawnException(action)

        # If i'm moving a correct pawn
        if action.role() == config.BLACK:
            if bitboard_util.get_bit(state.black_bitboard(), action.start().row(), action.start().column()) == 0:
                raise PawnException(action)

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