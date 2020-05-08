from copy import copy
from utils import config


class StateFactory:

    @staticmethod
    def load_state_from_action(state, action):
        new_state = copy(state)
        new_state = new_state.move(action)
        new_state.winner = new_state.check_ended()
        if new_state.turn == config.WHITE:
            new_state.turn = config.BLACK
        else:
            new_state.turn = config.WHITE
        return new_state
