from state.tablut_state import TablutState
from random import randrange, randint
from utils import config
from utils.action import Position, Action
from rules.rules import AshtonTablutRules
import utils.bitboard_util as bitboard_util

# TODO: Ogni tanto entra in un ciclo infinito in cui non trova una mossa da poter fare


class Algorithm:
    def __init__(self, role):
        self.__role = role

    def get_move(self, state: TablutState):

        found_action = False
        rules = AshtonTablutRules(state)
        action = ""
        bitboard = state.black_bitboard()
        if self.__role == config.WHITE:
            bitboard = state.white_bitboard() | state.king_bitboard()

        while not found_action:
            row_from = randint(0, 8)
            col_from = randint(0, 8)
            if bitboard_util.get_bit(bitboard, row_from, col_from) == 1:
                row_to = randint(0, 8)
                col_to = randint(0, 8)
                position_start = Position(row_from, col_from)
                position_end = Position(row_to, col_to)
                action = Action(position_start, position_end, self.__role)
                try:
                    if rules.check_move(state, action):
                        found_action = True
                except:
                    pass
        return action
