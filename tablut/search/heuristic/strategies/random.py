from tablut.search.heuristic.strategies.strategy import HeuristicStrategy
from tablut.utils import bitboard_util
from tablut.utils.action import Position

BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT = 2
BLACK_PIECE_AROUND_KING = 4
BLACK_GOOD_POSITION = 6
KING_IN_WINNING_POSITION = 5000
PIECE_ATE = 2
WHITE_IN_STRATEGIC_PLACE = 4
USELESS_BLACK_POSITION = 0.5


def white_in_good_position(state):
    value = 0
    if bitboard_util.get_bit(state.white_bitboard, 1, 3):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 1, 5):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 3, 1):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 3, 7):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 5, 1):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 5, 7):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 7, 3):
        value += WHITE_IN_STRATEGIC_PLACE
    if bitboard_util.get_bit(state.white_bitboard, 7, 5):
        value += WHITE_IN_STRATEGIC_PLACE
    return value


def king_in_winning_position(state):
    result = 0
    row = state.king_position.row
    column = state.king_position.column
    obstacle_bitboard = state.black_bitboard | state.white_bitboard | state.king_bitboard | state.throne_bitboard | state.camps_bitboard
    if state.king_position is not None:
        if row == 0 or row == 1 or row == 2 or row == 6 or row == 7 or row == 8:
            is_blocked, number_escapes_blocked = bitboard_util.is_there_obstacle_in_column(state.king_position, obstacle_bitboard)
            if not is_blocked:
                result += KING_IN_WINNING_POSITION * (2 - number_escapes_blocked)
        if column == 0 or column == 1 or column == 2 or column == 6 or column == 7 or column == 8:
            is_blocked, number_escapes_blocked = bitboard_util.is_there_obstacle_in_row(state.king_position, obstacle_bitboard)
            if not is_blocked:
                result += KING_IN_WINNING_POSITION * (2 - number_escapes_blocked)
    return result


def black_in_good_position(state):
    value = 0
    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    very_good = BLACK_GOOD_POSITION
    good = BLACK_GOOD_POSITION / 2
    not_bad = BLACK_GOOD_POSITION / 4
    good_position_value = [good, good, good, good]
    # Il re è sotto al trono a destra
    if state.king_position.row > 4:
        if state.king_position.column < 4:
            good_position_value = [not_bad, very_good, good, very_good]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re è sotto al trono a sinistra
    if state.king_position.row > 4:
        if state.king_position.column > 4:
            good_position_value = [very_good, not_bad, very_good, good]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re è sotto al trono in centro
    if state.king_position.row > 4:
        if state.king_position.column == 4:
            good_position_value = [not_bad, not_bad, very_good, very_good]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re si trova a destra del trono
    if state.king_position.row == 4:
        if state.king_position.column < 4:
            good_position_value = [not_bad, very_good, not_bad, very_good]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re si trova a sinistra del trono
    if state.king_position.row == 4:
        if state.king_position.column > 4:
            good_position_value = [very_good, not_bad, very_good, not_bad]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re è sopra al trono a destra
    if state.king_position.row < 4:
        if state.king_position.column < 4:
            good_position_value = [good, very_good, not_bad, very_good]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re è sopra al trono a sinistra
    if state.king_position.row < 4:
        if state.king_position.column > 4:
            good_position_value = [very_good, good, very_good, not_bad]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    # Il re è sopra al trono in centro
    if state.king_position.row < 4:
        if state.king_position.column == 4:
            good_position_value = [very_good, very_good, not_bad, not_bad]

    # BLACK_GOOD_POSITION = [X, X, X, X]  # Top left, Top right, Bottom Left, Bottom Right
    if bitboard_util.get_bit(state.black_bitboard, 1, 6):
        value += good_position_value[0]
    if bitboard_util.get_bit(state.black_bitboard, 2, 7):
        value += good_position_value[0]
    if bitboard_util.get_bit(state.black_bitboard, 1, 2):
        value += good_position_value[1]
    if bitboard_util.get_bit(state.black_bitboard, 2, 1):
        value += good_position_value[1]
    if bitboard_util.get_bit(state.black_bitboard, 6, 7):
        value += good_position_value[2]
    if bitboard_util.get_bit(state.black_bitboard, 7, 6):
        value += good_position_value[2]
    if bitboard_util.get_bit(state.black_bitboard, 6, 1):
        value += good_position_value[3]
    if bitboard_util.get_bit(state.black_bitboard, 7, 2):
        value += good_position_value[3]
    return value


class RandomStrategy(HeuristicStrategy):
    def eval(self, state, player):
        try:
            value = 0
            multiplier = BLACK_PIECE_AROUND_KING
            if state.king_position == Position(4, 4):
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT
            if state.king_position == Position(4, 3):
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT
            if state.king_position == Position(4, 5):
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT
            if state.king_position == Position(3, 4):
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT
            if state.king_position == Position(5, 4):
                multiplier = BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT

            """                      
            Team imbattuti:




            BALANCED PROFILE:
                Ha vinto contro:
                Fede -  ./osarracino white
                AiTeamTablut 2019 - python3 AITeam.py Colore 
                TablutAI - ant failureState -Darg0=WHITE -Darg1=1 -Darg2=localhost
                Existential_Tablut - ./runmyplayer White 60 'localhost'
                NorsemanTablut - java -jar Tablut/Executables/TablutAIClient.jar White 60 localhost - Vittoria per Timeout
                TablutPlayer_Capitano - python3.7 Client.py White 60 'localhost' - Vittoria per Timeout

                Ha perso contro: 
                Pelle - java -jar bin/pelle -p w
                Tablut - java -jar dist/StudentPlayer.jar white
                Tablut_client - python3 src/client.py White 60 'localhost'

                Ha pareggiato contro:


                PARAMETRI:  
                    BLACK_PIECE_AROUND_KING_IN_THRONE_OR_ADJACENT = 2
                    BLACK_PIECE_AROUND_KING = 4
                    BLACK_GOOD_POSITION = 6
                    KING_IN_WINNING_POSITION = 5000
                    PIECE_ATE = 2
                    WHITE_IN_STRATEGIC_PLACE = 4
                    USELESS_BLACK_POSITION = 0.5

                VALUE FUNCTION:
                    pawns_difference = state.black_count - state.white_count * 2
                    multiplier += 0.4 * pawns_difference
                    value += bitboard_util.count_adjacent(state.king_position, state.black_bitboard) * multiplier
                    value += black_in_good_position(state)
                    value += pawns_difference * (PIECE_ATE + 0.3 * pawns_difference)
                    value -= king_in_winning_position(state)
                    value -= white_in_good_position(state)
            """

            pawns_difference = state.black_count - state.white_count * 2
            multiplier += 0.4 * pawns_difference
            value += bitboard_util.count_adjacent(state.king_position, state.black_bitboard) * multiplier
            value += black_in_good_position(state)
            value += pawns_difference * (PIECE_ATE + 0.3 * pawns_difference)
            value -= king_in_winning_position(state)
            value -= white_in_good_position(state)

            return value
        except Exception as e:
            print(e)
