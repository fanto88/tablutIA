from logging import Logger


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


class AshtonTablut(Tablut):
    """
    Class that implements rules of classic tablut (9x9 chessboard)
    """

    def check_move(self, state, action):    # TODO: implement check_move
        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """
        raise NotImplementedError()

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
