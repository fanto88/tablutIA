import tablut.utils.bitboard_util as bitboard_util
from tablut.state.state import State
from tablut.utils import config
from tablut.utils.action import Action, Position

#TODO: Adjacent_throne fare una bitboard e poi fare l'or tra king_bitboard e bitboard e ritornare il valore,
# provanddo con time.time() quale delle due versioni è effettivamente più velcoe
#TODO: Fare la stessa cosa con king_on_throne
#TODO: eat king togliere tutti gli if fatti così e mettere le funzioni sopra
#TODO: Come controllare che l'and o l'or fra due bitboard abbia almeno 1 o più di un valore ad 1
#TODO: Guardare cosa altro si può migliorare

class TablutState(State):
    def __init__(self, color):
        super().__init__(color)

    def adjacent_throne(self):
        """Return True/False if the king is adjacent to the throne."""
        pos = self.king_position
        if pos == Position(4, 3) or pos == Position(4, 5) or pos == Position(3, 4) or pos == Position(5, 4):
            return True
        return False

    def king_on_throne(self):
        """Return True/False if the king is on the throne."""
        if self.king_position == Position(4, 4):
            return True
        return False

    def eat_king(self, action):
        """Check if the king can be eat after with the action."""
        obstacle_bitboard = self.black_bitboard | self.king_bitboard | self.throne_bitboard | self.camps_bitboard
        # Se è sul Trono
        if self.king_position == Position(4, 4):
            if bitboard_util.count_adjacent(self.king_position, obstacle_bitboard) == 4:
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, self.king_position.row,
                                                         self.king_position.column)
                self.king_position = None

        # Se è adiacente al trono
        elif (self.king_position == Position(3, 4)) or (self.king_position == Position(5, 4)) or (
                self.king_position == Position(4, 5)) or (self.king_position == Position(4, 3)):
            if bitboard_util.count_adjacent(self.king_position, obstacle_bitboard) == 4:
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, self.king_position.row,
                                                         self.king_position.column)
                self.king_position = None

        # Se è lontano dal trono
        else:
            obstacle_bitboard = self.king_bitboard | self.black_bitboard | self.throne_bitboard
            self.king_bitboard, result = bitboard_util.eat_black(self.king_bitboard, obstacle_bitboard, self.camps_bitboard, action.end)
            if result:
                self.king_position = None

    def check_ended(self):
        """Return True/False based on the game ended. In case of True change the parameter winner based on the winner
        of the game."""
        if self.king_position is None:
            self.winner = config.BLACK
            return True

        if self.black_count == 0:
            self.winner = config.WHITE
            return True

        if bitboard_util.count_piece(self.king_bitboard & self.escape_bitboard) == 1:
            self.winner = config.WHITE
            return True
        return False

    def move(self, action: Action):
        """Execute the action."""
        if action.role == config.WHITE:
            if bitboard_util.get_bit(self.white_bitboard, action.start.row, action.start.column) == 1:
                self.white_bitboard = bitboard_util.set(self.white_bitboard, action.end.row,
                                                        action.end.column)
                self.white_bitboard = bitboard_util.unset(self.white_bitboard, action.start.row,
                                                          action.start.column)
            else:
                self.king_bitboard = bitboard_util.set(self.king_bitboard, action.end.row,
                                                       action.end.column)
                self.king_bitboard = bitboard_util.unset(self.king_bitboard, action.start.row,
                                                         action.start.column)
                self.king_position = Position(action.end.row, action.end.column)
            obstacle_bitboard = self.king_bitboard | self.white_bitboard | self.throne_bitboard
            self.black_bitboard, result = bitboard_util.eat_black(self.black_bitboard, obstacle_bitboard, self.camps_bitboard, action.end)
            if result:
                self.black_count -= 1
        else:
            self.black_bitboard = bitboard_util.set(self.black_bitboard, action.end.row, action.end.column)
            self.black_bitboard = bitboard_util.unset(self.black_bitboard, action.start.row,
                                                      action.start.column)
            obstacle_bitboard = self.king_bitboard | self.black_bitboard | self.throne_bitboard | self.camps_bitboard
            self.eat_king(action)
            self.white_bitboard, result = bitboard_util.eat_white(self.white_bitboard, obstacle_bitboard, action.end)
            if result:
                self.white_count -= 1
        return self

    def __hash__(self):
        return hash((
            tuple(self.white_bitboard),
            tuple(self.king_bitboard),
            tuple(self.black_bitboard),
            tuple(self.escape_bitboard),
            tuple(self.camps_bitboard),
            tuple(self.throne_bitboard),
            self.turn,
            self.winner
        ))

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

    def __repr__(self):
        return "HASH: {:d}".format(hash(self))
