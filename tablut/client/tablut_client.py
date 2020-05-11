import tablut.utils.config as config
from tablut.client.connection_handler import ConnectionHandler
from tablut.search import parallel_search as parallel_search
from tablut.search.game import TablutProblem
from tablut.state.state_factory import StateFactory


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
        try:
            self.connect()  # Connecting to the server
            self.send_string(self.player_name)  # Sending the name
            state = StateFactory().load_state_from_json(self.read_string(), self.color)  # Read the initial state
            while True:  # Game loop
                if self.color == state.turn:  # check if our turn or not
                    search = parallel_search.ParallelMinMax(2, 2, self.timeout - 5)
                    action = search.make_decision(state, TablutProblem())
                    if action is not None:
                        state.move(action)  # Execute the action
                        self.send_string(action.to_server_format())  # send the action to the server
                state = StateFactory().load_state_from_json(self.read_string(), self.color)  # Read the next state
        except Exception as ex:
            print(ex)
        finally:
            print("Game Terminated - Closing Connection")
