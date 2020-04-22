from state.tablut_state import TablutState
from random import randrange, randint

from utils import config
from utils.action import Position, Action
from rules.rules import AshtonTablutRules

# TODO: Ogni tanto entra in un ciclo infinito in cui non trova una mossa da poter fare
from utils.bitboard_util import Bitboard


class Algorithm:
    def __init__(self, role):
        self.__role = role

    def get_move(self, state: TablutState):

        found_action = False
        rules = AshtonTablutRules(state)
        action = ""
        bitboard = ""
        if self.__role == config.WHITE:
            bitboard = state.white_bitboard() | state.king_bitboard()
        else:
            bitboard = state.black_bitboard()

        while not found_action:
            for row in range(9):
                if found_action:
                    break
                for column in range(9):
                    if found_action:
                        break
                    if Bitboard.get_bit(bitboard, row, column) == 1:
                        for i in range(5000):
                            if found_action:
                                break
                            row_to = randint(0, 9)
                            col_to = randint(0, 9)
                            position_start = Position(row, column)
                            position_end = Position(row_to, col_to)
                            action = Action(position_start, position_end, self.__role)
                            try:
                                rules.check_move(state, action)
                                found_action = True
                            except:
                                pass
        return action
