from logging import Logger


class Game:
    """
    Class which implements methods for search-tree creation
    """

    def actions(self, state):
        """
        Lists all the possibile actions which can be done in the current state
        """
        raise NotImplementedError()

    def turn_player(self, state):
        """
        Returns the turn player
        """
        raise NotImplementedError()

    def all_players(self):
        """
        Returns every player in the game
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

    def process_action(self, state, action):
        """
        Returns the resulting state after processing the given action in the given state
        """
        raise NotImplementedError()


class TablutProblem(Game):
    """
    Class that implements rules of classic tablut (9x9 chessboard)
    """

    def actions(self, state):   # TODO: implement
        pass

    def goal_test(self, state):  # TODO: implement
        pass

    def value(self, state):  # TODO: implement
        pass

    def process_action(self, state, action):
        pass

    def turn_player(self, state):
        pass

    def all_players(self):
        pass
