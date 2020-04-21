from state.tablut_state import TablutState
from random import randrange
from utils.action import Position, Action
from rules.rules import AshtonTablutRules

#TODO: Ogni tanto entra in un ciclo infinito in cui non trova una mossa da poter fare
class Algorithm:
    def __init__(self, role):
        self.__role = role

    def get_move(self, state: TablutState):

        found = False
        rules = AshtonTablutRules(state)
        action = ""
        while not found:
            row_to = randrange(8)
            row_from = randrange(8)
            col_to = randrange(8)
            col_from = randrange(8)
            from_position = Position(row_from, col_from)
            to_position = Position(row_to, col_to)
            action = Action(from_position, to_position, self.__role)
            print(action.to_server_format())
            try:
                if rules.check_move(state, action):
                    found = True
            except:
                pass
        return action