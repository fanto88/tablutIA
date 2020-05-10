import tablut.utils.config as config
from tablut.client.connection_handler import ConnectionHandler
from tablut.search import parallel_search as parallel_search
from tablut.search.game import TablutProblem
from tablut.state.tablut_state import TablutState


class Client(ConnectionHandler):
    """Class that define the client logic.
    Extend ConnectionHandler that handles the connection between client and server."""

    def __init__(self, port, host, role, timeout):
        super().__init__(port, host)
        self.player_name = config.PLAYER_NAME
        self.color = role
        self.timeout = timeout
        self.state = TablutState(self.color)

    def run(self):
        """Implements the logic of the client."""
        try:
            self.connect()  # Connecting to the server
            self.send_string(self.player_name)  # Sending the name
            self.state.load_state_from_json(self.read_string())  # Read the initial state
            while True:  # Game loop
                if self.color == self.state.turn:  # check if our turn or not
                    search = parallel_search.ParallelMinMax(2, 3, self.timeout - 5)
                    action = search.make_decision(self.state, TablutProblem())
                    if action is not None:
                        self.state.move(action)  # Execute the action
                        self.send_string(action.to_server_format())  # send the action to the server
                self.state.load_state_from_json(self.read_string())  # read the new state
        except ConnectionResetError:
            pass
        finally:
            print("Game Terminated - Closing Connection")
