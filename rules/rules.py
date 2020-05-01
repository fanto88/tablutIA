from logging import Logger

import numpy

import utils.bitboard_util as bitboard_util
from exceptions.custom_exceptions import *
from state.tablut_state import TablutState
from utils import config


class Tablut:  # TODO: add other methods, such as expand, actions, ...
    """
    A simple interface that every rule-class should implement
    """

    def __init__(self, initial_state, logger=None):  # TODO: implement log_file
        self.initial_state = initial_state
        self.logger = Logger("TablutGame") if logger is None else logger
        # self.log_file

    def check_move(self, state, action):
        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """
        raise NotImplementedError()


# TODO: log delle cose???
# TODO: Mettere state: State e fare in modo che TablutState estenda State, in questo modo disaccoppio meglio
# TODO: mettere in ordine di probabilità, così finisce prima
# TODO: i campi non vengono gestiti bene nel caso tu ci sia dentro oppure no. Bisognare controllare, ora dovrebbe funzionare correttamente
# TODO: Obstacle bitboard??
class AshtonTablutRules(Tablut):
    """
    Class that implements rules of classic tablut (9x9 chessboard)
    """

    def check_move(self, state: TablutState, action: Action):
        obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard

        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """

        # Check if is not moving out of the board
        # Just checking if the row and column are over the size board
        if (action.end().row() > 8) | (action.end().column() > 8):
            raise BoardException(action)

        # Check if you are actually moving a pawn
        # Just checking if you the 2 actions are not the same, so you are not moving a pawn at his initial position
        if action.start() == action.end():
            raise StopException(action)

        # Check if you can move the black inside the camps
        # How does that work:
        # 1) We see if we are moving a pawn from the camps
        # 2) We see if the destination is a camps
        # 3) 
        if bitboard_util.get_bit(state.camps_bitboard, action.start().row(), action.start().column()):
            if bitboard_util.get_bit(state.camps_bitboard, action.end().row(), action.end().column()):
                if (numpy.absolute(action.start().row() - action.end().row() > 2)) | (
                numpy.absolute(action.start().column() - action.end().column() > 2)):
                    raise CitadelException(action)
        else:
            obstacle_bitboard = obstacle_bitboard | state.camps_bitboard

        # Check if you are moving to an empty space
        if bitboard_util.get_bit(obstacle_bitboard, action.end().row(), action.end().column()) == 1:
            raise OccupitedException(action)

        # Check if it's a diagonal move
        if (action.start().row() != action.end().row()) & (action.start().column() != action.end().column()):
            raise DiagonalException(action)

        # Check If there is an obstacle between your final position and your actual position
        if action.start().row() == action.end().row():
            par = 1
            if action.start().column() < action.end().column():
                par = -1
            for index in range(action.end().column(), action.start().column(), par):
                if bitboard_util.get_bit(obstacle_bitboard, action.start().row(), index) == 1:
                    raise ClimbingException(action)
        else:
            par = 1
            if action.start().row() < action.end().row():
                par = -1
            for index in range(action.end().row(), action.start().row(), par):
                if bitboard_util.get_bit(obstacle_bitboard, index, action.start().column()) == 1:
                    raise ClimbingException(action)

        # If i'm moving a correct pawn
        if action.role() == config.WHITE:
            if bitboard_util.get_bit(state.white_bitboard | state.king_bitboard, action.start().row(),
                                     action.start().column()) == 0:
                raise PawnException(action)

        # If i'm moving a correct pawn
        if action.role() == config.BLACK:
            if bitboard_util.get_bit(state.black_bitboard, action.start().row(), action.start().column()) == 0:
                raise PawnException(action)
        return True

    def __move_piece(self, state, action):  # TODO: implement move_piece
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
