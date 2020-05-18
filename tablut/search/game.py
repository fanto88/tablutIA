from tablut.utils.action_factory import ActionFactory
from tablut.state.state_factory import StateFactory
from tablut.utils import config


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

    def value(self, state, player):
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
        return ActionFactory.all_available_actions(state)

    def goal_test(self, state):  # TODO: implement
        return state.check_ended()

    def value(self, state, player):  # TODO: implement
        winner = state.winner
        """if player == config.WHITE:
            if not winner:
                return 0
            elif winner == player:
                return -1000000
            else:
                return 1000000
        else:
            if not winner:
                return 0
            elif winner == player:
                return 1000000
            else:
                return -1000000"""

        if not winner:
            return 0
        elif winner == player:
            #print(winner, "|", player)
            return -1000000
        else:
            return 1000000

    def process_action(self, state, action):
        return StateFactory.load_state_from_action(state, action)

    def turn_player(self, state):
        return state.turn

    def all_players(self):
        return [config.WHITE, config.BLACK]
