from utils import config


class StateFactory:

    @staticmethod
    def load_state_from_action(state, action):
        state = state.move(action)
        state.winner = state.check_ended()
        if state.turn == config.WHITE:
            state.turn = config.BLACK
        else:
            state.turn = config.WHITE
        return state
