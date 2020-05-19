import tablut.utils.config as config
from tablut.client.connection_handler import ConnectionHandler
from tablut.search import parallel_search2
from tablut.search.game import TablutProblem
from tablut.state.state_factory import StateFactory
import tablut.search.heuristic.phase as ph


class Client(ConnectionHandler):
    """Class that define the client logic. Extend ConnectionHandler that handles the connection
    between client and server."""

    def __init__(self, port, host, color: str, timeout):
        super().__init__(port, host)
        self.player_name = config.PLAYER_NAME
        self.color = color
        self.timeout = timeout

    #TODO: In caso di errore eseguire una mossa random dalla lista di mosse possibili
    #TODO: Controllare il bug con profondità 1, ritorna il giocatore opposto
    def run(self):
        """Implements the logic of the client."""
        #try:
        self.connect()  # Connecting to the server
        self.send_string(self.player_name)  # Sending the name
        state = StateFactory().load_state_from_json(self.read_string(), self.color)  # Read the initial state
        turn = 1 if self.color.lower() == config.WHITE.lower() else 2
        while True:  # Game loop
            """
                from tablut.search.heuristic.strategies.free_winning_points import FreeWinningPoints
                from tablut.search.heuristic.strategies.white_count import WhiteCount
                from tablut.search.heuristic.strategies.black_count import BlackCount
                from tablut.search.heuristic.strategies.white_winning_points import WhiteWinningPoints
                from tablut.search.heuristic.strategies.black_winning_points import BlackWinningPoints
                from tablut.search.heuristic.strategies.near_king import NearKing
                from tablut.search.heuristic.strategies.king_positioning import KingPositioning
                from tablut.search.heuristic.strategies.king_in_winning_position import KingInWinningPosition
                from tablut.search.heuristic.strategies.white_good_position import WhiteGoodPosition
    
                from tablut.search.heuristic.strategies.black_in_good_position import BlackInGoodPosition
                print()         
                print("FreeWinningPoints:", (FreeWinningPoints().eval(state, self.color) * 100))
                print("WhiteWinningPoints:", (WhiteWinningPoints().eval(state, self.color) * 200))
                print("BlackWinningPoints:", (BlackWinningPoints().eval(state, self.color) * -300))
                print("WhiteCount:", (WhiteCount().eval(state, self.color) * 200))
                print("BlackCount:", (BlackCount().eval(state, self.color) * -500))
                print("NearKing:", (NearKing().eval(state, self.color) * -1000))
                print("KingInWinningPosition:", (KingInWinningPosition().eval(state, self.color) * 10000))
                print("KingPositioning:", (KingPositioning().eval(state, self.color) * 100))
                print("BlackInGoodPosition:", (BlackInGoodPosition().eval(state, self.color) * -300))
            """
            if self.color == state.turn:  # check if our turn or not
                phase = ph.get_phase(turn)
                action, value = parallel_search2.choose_action(4, state, TablutProblem(), self.timeout - 5, 5, True, given_phase=phase)
                self.send_string(action.to_server_format())  # send the action to the server
                print("Eseguita azione:", action.to_server_format(), " con valore:", value)
            turn += 1
            state = StateFactory().load_state_from_json(self.read_string(), self.color)  # Read the next state
"""        except Exception as e:
           print(e)
        finally:
           print("Game Terminated - Closing Connection")
"""