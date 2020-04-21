from utils.action import Action


class StopException(Exception):
    def __init__(self, action: Action):
        default_message = 'Action not allowed, a pawn need to move: ' + str(action)
        super().__init__(default_message)


class DiagonalException(Exception):
    def __init__(self, action: Action):
        default_message = 'Diagonal move is not allowed: ' + str(action)
        super().__init__(default_message)


class ClimbingException(Exception):
    def __init__(self, action: Action):
        default_message = 'A pawn is trying to climb over another pawn: ' + str(action)
        super().__init__(default_message)


class ClimbingCitadelException(Exception):
    def __init__(self, action: Action):
        default_message = 'A pawn is trying to climb over a citadel: ' + str(action)
        super().__init__(default_message)


class ActionException(Exception):
    def __init__(self, action: Action):
        default_message = 'The format of the action is not correct' + str(action)
        super().__init__(default_message)


class BoardException(Exception):
    def __init__(self, action: Action):
        default_message = 'The move is out of the board: ' + str(action)
        super().__init__(default_message)


class CitadelException(Exception):
    def __init__(self, action: Action):
        default_message = 'Move into a citadel: ' + str(action)
        super().__init__(default_message)


class PawnException(Exception):
    def __init__(self, action: Action):
        default_message = 'The player is trying to move a wrong pawn: ' + str(action)
        super().__init__(default_message)


class OccupitedException(Exception):
    def __init__(self, action: Action):
        default_message = 'Move into a box occupited from another pawn: ' + str(action)
        super().__init__(default_message)


class ThroneException(Exception):
    def __init__(self, action: Action):
        default_message = 'Player is trying to go into the castle: ' + str(action)
        super().__init__(default_message)
