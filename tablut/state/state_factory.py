from copy import deepcopy

from tablut.state.tablut_state import TablutState
from tablut.utils import config
from tablut.utils.action import Position


class StateFactory:
    """Class that has the objective of creating new States."""

    def __init__(self):
        pass

    @staticmethod
    def load_state_from_json(json_string, color):
        """Create a new State based on a json_string that represent the state of the game."""
        state = TablutState(color)
        row_index = 0
        state.turn = json_string["turn"]
        if (state.turn != config.WHITE) & (state.turn != config.BLACK):
            return
        for row in json_string["board"]:
            column_index = 8
            for column in row:
                if column == "WHITE":
                    state.white_bitboard[row_index] |= 1 << column_index
                    state.white_count += 1
                elif column == "BLACK":
                    state.black_bitboard[row_index] |= 1 << column_index
                    state.black_count += 1
                elif column == "KING":
                    state.king_bitboard[row_index] |= 1 << column_index
                    state.king_position = Position(row_index, column_index)
                column_index -= 1
            row_index += 1
        return state

    @staticmethod
    def load_state_from_action(state, action):
        """Create a new State based on the action."""
        new_state = deepcopy(state)
        new_state = new_state.move(action)
        new_state.check_ended()
        if new_state.turn == config.WHITE:
            new_state.turn = config.BLACK
        else:
            new_state.turn = config.WHITE
        return new_state
