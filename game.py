from logging import Logger


class Tablut:  # TODO: add other methods, such as expand, actions, ...
    """
    A simple interface that every rule-class should implement
    """

    def __init__(self, logger=None):  # TODO: implement log_file
        self.logger = Logger("TablutGame") if logger is None else logger
        #self.log_file

    def check_move(self, state, action):
        """
        Check the correctness of the action, raising an error it is not allowed in the given state
        """
        raise NotImplementedError()

    def process_action(self, state, action):
        """
        Returns the resulting state after processing the given action in the given state
        """
        raise NotImplementedError()


class TablutProblem(Tablut):
    """
    Class which implements methods for search-tree creation
    """

    def actions(self, state):
        """
        Lists all the possibile actions which can be done in the current state
        """
        raise NotImplementedError()

    def goal_test(self, state):
        """Return True if the state is a goal"""
        raise NotImplementedError()

    def value(self, state):  # TODO: per me sarebbe l'euristica, ma non sono sicuro
        """
        Each state has a value. Some algorithms try to maximize this value
        """
        raise NotImplementedError()


class ClassicTablut(TablutProblem):
    """
    Class that implements rules of classic tablut (9x9 chessboard)
    """

    def actions(self, state):   # TODO: implement
        pass

    def goal_test(self, state):  # TODO: implement
        pass

    def value(self, state):  # TODO: implement
        pass

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

    def process_action(self, state, action):  # TODO: implement process_action
        """
        Returns the resulting state after processing the given action in the given state
        """
        raise NotImplementedError()

