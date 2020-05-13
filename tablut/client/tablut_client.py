import tablut.utils.config as config
from tablut.client.connection_handler import ConnectionHandler
from tablut.search import parallel_search
from tablut.search.search import MinMaxAgent
from tablut.search.game import TablutProblem
from tablut.state.state_factory import StateFactory
from tablut.utils import bitboard_util


class Client(ConnectionHandler):
    """Class that define the client logic. Extend ConnectionHandler that handles the connection
    between client and server."""

    def __init__(self, port, host, color, timeout):
        super().__init__(port, host)
        self.player_name = config.PLAYER_NAME
        self.color = color
        self.timeout = timeout

    def run(self):
        """Implements the logic of the client."""
        #try:
        self.connect()  # Connecting to the server
        self.send_string(self.player_name)  # Sending the name
        state = StateFactory().load_state_from_json(self.read_string(), self.color)  # Read the initial state
        start_as_max = True
        if self.color == config.WHITE:
            start_as_max = False
        while True:  # Game loop
            if self.color == state.turn:  # check if our turn or not
                #search = parallel_search.ParallelMinMax(1, 1, self.timeout - 5)
                #action = search.make_
                # decision(state, TablutProblem())
                minmax = MinMaxAgent(10, self.timeout - 5)
                action, value = minmax.choose_action(state, TablutProblem(), start_as_max)
                print("ESEGUO AZIONE ", action, " CON VALORE ", value)
                self.send_string(action.to_server_format())  # send the action to the server
            state = StateFactory().load_state_from_json(self.read_string(), self.color)  # Read the next state
"""        except Exception as e:
           print(e)
        finally:
           print("Game Terminated - Closing Connection")
"""